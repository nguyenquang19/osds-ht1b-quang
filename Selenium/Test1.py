from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Edge()
driver.get("https://www.myinstants.com/en/instant/snoop-dogg-meme-88682/")
time.sleep(12)  
try:
    driver.find_element(By.ID, "instant-page-button-element").click()
    time.sleep(3)
except:
    driver.quit()