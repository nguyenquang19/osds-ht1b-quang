import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import os

######################################################
## I. Cấu hình và Chuẩn bị
######################################################

DB_FILE = 'Painters_Data.db'
TABLE_NAME = 'painters_info'
all_links = []

# Nếu muốn bắt đầu với DB trống, có thể xóa file cũ (Tùy chọn)
if os.path.exists(DB_FILE):
    try:
        os.remove(DB_FILE)
        print(f"Đã xóa file DB cũ: {DB_FILE}")
    except PermissionError:
        print("Không thể xóa DB vì đang mở ở chương trình khác. Đóng hết chương trình dùng DB rồi chạy lại.")
        # Nếu muốn dừng hẳn:
        # raise

# Mở kết nối SQLite và tạo bảng nếu chưa tồn tại
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    name TEXT PRIMARY KEY,
    birth TEXT,
    death TEXT,
    nationality TEXT
);
"""
cursor.execute(create_table_sql)
conn.commit()
print(f"Đã kết nối và chuẩn bị bảng '{TABLE_NAME}' trong '{DB_FILE}'.")

######################################################
## II. Lấy Đường dẫn (URLs) với 1 driver Edge
######################################################

print("\n--- Bắt đầu Lấy Đường dẫn ---")

driver = webdriver.Edge()

# Lấy List F
url = 'https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22F%22'
driver.get(url)
time.sleep(3)

ul_tags = driver.find_elements(By.TAG_NAME, "ul")
ul_painters = None

# Tìm đúng <ul> chứa painter (dựa vào từ 'Fragonard' như code 1)
for ul in ul_tags:
    if "Fragonard" in ul.text:
        ul_painters = ul
        break

if ul_painters is None:
    print("Không tìm thấy danh sách painters (không có 'Fragonard').")
    driver.quit()
    conn.close()
    raise SystemExit()

li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

for li in li_tags:
    links_in_li = li.find_elements(By.TAG_NAME, "a")
    if not links_in_li:
        continue
    href = links_in_li[0].get_attribute("href")
    if href:
        all_links.append(href)

print(f"Hoàn tất lấy đường dẫn. Tổng cộng {len(all_links)} links đã tìm thấy.")

######################################################
## III. Lấy thông tin & LƯU TRỮ TỨC THỜI
######################################################

print("\n--- Bắt đầu Cào và Lưu Trữ Tức thời ---")

count = 0
for link in all_links:
    if count >= 10:   # giới hạn 10 painter để test
        break
    count += 1

    try:
        driver.get(link)
        time.sleep(2)

        # 1. Tên
        try:
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = ""

        # 2. Ngày sinh (Born)
        try:
            birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
            birth_text = birth_element.text
            birth_match = re.findall(
                r'(\d{1,2}\s[A-Za-z]+\s\d{4}|\d{4}|c\.\s?\d{4}|[0-9]{1,2}th century)',
                birth_text
            )
            birth = birth_match[0] if birth_match else ""
        except:
            birth = ""

        # 3. Ngày mất (Died)
        try:
            death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
            death_text = death_element.text
            death_match = re.findall(
                r'(\d{1,2}\s[A-Za-z]+\s\d{4}|\d{4}|c\.\s?\d{4}|[0-9]{1,2}th century)',
                death_text
            )
            death = death_match[0] if death_match else ""
        except:
            death = ""

        # 4. Quốc tịch (Nationality hoặc Citizenship)
        try:
            nationality_element = driver.find_element(
                By.XPATH,
                "//th[text()='Nationality' or text()='Citizenship']/following-sibling::td"
            )
            nationality = nationality_element.text.split('\n')[0]
        except:
            nationality = ""

        # 5. LƯU VÀO SQLITE
        insert_sql = f"""
        INSERT OR IGNORE INTO {TABLE_NAME} (name, birth, death, nationality)
        VALUES (?, ?, ?, ?);
        """
        cursor.execute(insert_sql, (name, birth, death, nationality))
        conn.commit()
        print(f"  --> Đã lưu thành công: {name}")

    except Exception as e:
        print(f"Lỗi khi xử lý hoặc lưu họa sĩ {link}: {e}")

print("\nHoàn tất quá trình cào và lưu dữ liệu tức thời.")


######################################################
## IV. Truy vấn SQLite
######################################################

print("\n=== A. Thống Kê và Toàn Cục ===")

# 1. Đếm tổng số họa sĩ
cursor.execute("SELECT COUNT(*) FROM painters_info")
print("1. Tổng số họa sĩ:", cursor.fetchone()[0])

# 2. Hiển thị 5 dòng dữ liệu đầu tiên
print("\n2. 5 dòng dữ liệu đầu tiên:")
cursor.execute("SELECT * FROM painters_info LIMIT 5")
for row in cursor.fetchall():
    print(row)

# 3. Liệt kê danh sách quốc tịch duy nhất
print("\n3. Danh sách quốc tịch duy nhất:")
cursor.execute("SELECT DISTINCT nationality FROM painters_info")
for row in cursor.fetchall():
    print(row[0])

print("\n=== B. Lọc và Tìm Kiếm ===")

# 4. Họa sĩ có tên bắt đầu bằng 'F'
print("\n4. Họa sĩ có tên bắt đầu bằng 'F':")
cursor.execute("SELECT name FROM painters_info WHERE name LIKE 'F%'")
for row in cursor.fetchall():
    print(row[0])

# 5. Họa sĩ có quốc tịch chứa 'French'
print("\n5. Họa sĩ có quốc tịch chứa 'French':")
cursor.execute("SELECT name, nationality FROM painters_info WHERE nationality LIKE '%French%'")
for row in cursor.fetchall():
    print(row)

# 6. Họa sĩ không có thông tin quốc tịch
print("\n6. Họa sĩ không có thông tin quốc tịch:")
cursor.execute("SELECT name FROM painters_info WHERE nationality IS NULL OR nationality = ''")
for row in cursor.fetchall():
    print(row[0])

# 7. Họa sĩ có cả ngày sinh và ngày mất
print("\n7. Họa sĩ có cả ngày sinh và ngày mất:")
cursor.execute("""
SELECT name FROM painters_info
WHERE birth IS NOT NULL AND birth <> ''
  AND death IS NOT NULL AND death <> ''
""")
for row in cursor.fetchall():
    print(row[0])

# 8. Họa sĩ có tên chứa 'Fales'
print("\n8. Họa sĩ có tên chứa 'Fales':")
cursor.execute("SELECT * FROM painters_info WHERE name LIKE '%Fales%'")
for row in cursor.fetchall():
    print(row)

print("\n=== C. Nhóm và Sắp Xếp ===")

# 9. Sắp xếp tên họa sĩ theo thứ tự A-Z
print("\n9. Danh sách họa sĩ theo thứ tự A-Z:")
cursor.execute("SELECT name FROM painters_info ORDER BY name ASC")
for row in cursor.fetchall():
    print(row[0])

# 10. Nhóm và đếm số lượng họa sĩ theo từng quốc tịch
print("\n10. Số lượng họa sĩ theo từng quốc tịch:")
cursor.execute("""
SELECT nationality, COUNT(*) AS count_painters
FROM painters_info
GROUP BY nationality
ORDER BY count_painters DESC
""")
for row in cursor.fetchall():
    print(row)


######################################################
## V. Đóng kết nối
######################################################

driver.quit()
conn.close()
print("\nĐã đóng driver và kết nối cơ sở dữ liệu.")
