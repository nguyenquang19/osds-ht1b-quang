from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#Khởi tạo Webdriver
driver = webdriver.Edge()

#Mở trang
url = "https://en.wikipedia.org/wiki/List_of_painters_by_name beginning with %22P%22"
driver.get(url)

#Đợi để tải trang 
time.sleep(2)

# Lấy ra tất cả các thẻ ul
ul_tags = driver.find_elements(By.TAG_NAME, "ul")
print(len(ul_tags))

# Chọn các thẻ ul thứ 21
ul_painter = ul_tags[20]

# Lấy tất cả các thẻ <li> thuộc ul_painter
li_tags = ul_painter.find_elements(By.TAG_NAME, "li")

# Chọn thẻ ul thứ 20
ul_painter = ul_tags[20]

# Lấy ra tát cả cac thẻ <li> thuộc ul_painter
li_tags = ul_painter.find_elements(By.TAG_NAME, "li")

# Tạo danh sách các url
links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]

# Tạo danh sách các url
titles = [tag.find_element(By.TAG_NAME, "a").get_attribute("title") for tag in li_tags]

# In ra url
for link in links:
    print(link)
    
# In ra title
for title in titles:
    print(title)
    
#Đóng webdriver
driver.quit()

