from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

# Tạo DataFrame rỗng
df = pd.DataFrame({"name": [], "birth": [], "death": [], "nationality": []})

# Khởi tạo WebDriver
driver = webdriver.Edge()

# Mở trang
url = "https://en.wikipedia.org/wiki/Edvard_Munch"
driver.get(url)

# Đợi 2 giây cho trang tải
time.sleep(2)

# Lấy tên họa sĩ
try:
    name = driver.find_element(By.TAG_NAME, "h1").text
except Exception:
    name = ""

# Lấy ngày sinh
try:
    birth_element = driver.find_element(
        By.XPATH, "//th[text()='Born']/following-sibling::td"
    )
    birth_text = birth_element.text
    birth_match = re.findall(r"[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}", birth_text)  # regex
    birth = birth_match[0] if birth_match else ""
except Exception:
    birth = ""

# Lấy ngày mất
try:
    death_element = driver.find_element(
        By.XPATH, "//th[text()='Died']/following-sibling::td"
    )
    death_text = death_element.text
    death_match = re.findall(r"[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}", death_text)
    death = death_match[0] if death_match else ""
except Exception:
    death = ""

# Lấy quốc tịch
try:
    nationality_element = driver.find_element(
        By.XPATH, "//th[text()='Nationality']/following-sibling::td"
    )
    nationality = nationality_element.text
except Exception:
    nationality = ""

# Tạo dictionary thông tin của họa sĩ
painter = {
    "name": name,
    "birth": birth,
    "death": death,
    "nationality": nationality,
}

# Chuyển đổi dictionary thành DataFrame
painter_df = pd.DataFrame([painter])

# Thêm thông tin vào DataFrame chính
df = pd.concat([df, painter_df], ignore_index=True)

# In ra DataFrame
print(df)

# Đóng WebDriver
driver.quit()
