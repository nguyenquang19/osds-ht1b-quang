import sqlite3
    
db = r"D:/BAITAP/longchau_db.db"
conn = sqlite3.connect(db)
cursor = conn.cursor()
#Nhóm 1
# Kiểm tra trùng lặp theo product_url hoặc product_name
print("1) Kiểm tra trùng lặp (URL hoặc Name):")

cursor.execute("""
SELECT product_url, product_name, COUNT(*)
FROM sanpham
GROUP BY product_url, product_name
HAVING COUNT(*) > 1
""")
dupes = cursor.fetchall()

if dupes:
    for d in dupes:
        print(" -", d)
else:
    print("Không có trùng lặp.",dupes)

# Kiểm tra dữ liệu thiếu giá bán
cursor.execute("""
SELECT COUNT(*)
FROM sanpham
WHERE price IS NULL 
   OR price = '' 
   OR price = '0'
   OR price = 'Không có giá'
""")
missing = cursor.fetchone()[0]

print("Số sản phẩm thiếu giá:", missing)

# Giá bán > Giá gốc
cursor.execute("""
SELECT product_name, price, original_price
FROM sanpham
WHERE 
    price != '' AND original_price != '' AND
    CAST(REPLACE(price, '.', '') AS INTEGER) >
    CAST(REPLACE(original_price, '.', '') AS INTEGER)
""")
wrong_prices = cursor.fetchall()

if wrong_prices:
    for p in wrong_prices:
        print(" -", p)
else:
    print("Không có bất thường.",wrong_prices)

# Liệt kê tất cả unit duy nhất
cursor.execute("SELECT DISTINCT unit FROM sanpham")
units = cursor.fetchall()
for u in units:
    print(" -", u[0])



#Nhóm2
#Sản phẩm có giảm giá: Hiển thị 10 sản phẩm có mức giá giảm (chênh lệch giữa original_price và price) lớn nhất.
print("\n2.1) Top 10 sản phẩm giảm giá nhiều nhất:")

cursor.execute("""
SELECT product_name, price, original_price,
       CAST(REPLACE(original_price, '.', '') AS INTEGER) -
       CAST(REPLACE(price, '.', '') AS INTEGER) AS discount
FROM sanpham
WHERE price != '' AND original_price != ''
ORDER BY discount DESC
LIMIT 10
""")

biggest_discounts = cursor.fetchall()

for p in biggest_discounts:
    print(" -", p)

#Sản phẩm đắt nhất: Tìm và hiển thị sản phẩm có giá bán cao nhất.
print("\n2.2) Sản phẩm có giá bán cao nhất:")

cursor.execute("""
SELECT product_name, price
FROM sanpham
WHERE price != ''
ORDER BY CAST(REPLACE(price, '.', '') AS INTEGER) DESC
LIMIT 1
""")

max_price = cursor.fetchone()
print(" ->", max_price)

#Thống kê theo đơn vị: Đếm số lượng sản phẩm theo từng Đơn vị tính (unit).
print("\n2.3) Thống kê theo đơn vị tính (unit):")

cursor.execute("""
SELECT unit, COUNT(*)
FROM sanpham
GROUP BY unit
ORDER BY COUNT(*) DESC
""")

unit_stats = cursor.fetchall()

for u in unit_stats:
    print(f" - {u[0]}: {u[1]} sản phẩm")

#Sản phẩm cụ thể: Tìm kiếm và hiển thị tất cả thông tin của các sản phẩm có tên chứa từ khóa "Vitamin C".
print("\n2.4) Sản phẩm chứa từ khóa 'Vitamin C':")

cursor.execute("""
SELECT *
FROM sanpham
WHERE product_name LIKE '%Vitamin C%'
""")

vitamin_products = cursor.fetchall()

for v in vitamin_products:
    print(" -", v)

#Lọc theo giá: Liệt kê các sản phẩm có giá bán nằm trong khoảng từ 100.000 VNĐ đến 200.000 VNĐ.
print("\n2.5) Sản phẩm giá từ 100.000 đến 200.000 VNĐ:")

cursor.execute("""
SELECT product_name, price
FROM sanpham
WHERE price != ''
  AND CAST(REPLACE(price, '.', '') AS INTEGER) BETWEEN 100000 AND 200000
""")

midrange_products = cursor.fetchall()

for m in midrange_products:
    print(" -", m)

# Tổng số bản ghi
cursor.execute("SELECT COUNT(*) FROM sanpham")
total = cursor.fetchone()[0]
print("Tổng số sản phẩm:", total)

conn.close()
