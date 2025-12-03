from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Khởi tạo WebDriver
driver = webdriver.Edge()

for i in range(65, 91):
    # URL danh sách họa sĩ theo chữ cái đầu
    url = (
        "https://en.wikipedia.org/wiki/"
        "List_of_painters_by_name_beginning_with_%22" + chr(i) + "%22"
    )

    try:
        # Mở trang
        driver.get(url)

        # Đợi một chút để trang tải
        time.sleep(3)

        # Lấy ra tất cả các thẻ <ul>
        ul_tags = driver.find_elements(By.TAG_NAME, "ul")
        print(len(ul_tags))

        # Chọn thẻ <ul> thứ 21 (list bắt đầu từ index = 0)
        ul_painters = ul_tags[20]

        # Lấy ra tất cả các thẻ <li> thuộc ul_painters
        li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

        # Tạo danh sách các title (tên họa sĩ) từ thẻ <a> bên trong mỗi <li>
        titles = [
            tag.find_element(By.TAG_NAME, "a").get_attribute("title")
            for tag in li_tags
        ]

        # In ra các title
        for title in titles:
            print(title)

    except Exception as e:
        print("Error!", e)

# Đóng WebDriver
driver.quit()

print("Finished!")