from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


options=Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

url = "https://www.naver.com/"

driver.get(url)

# 1sec delay
time.sleep(1)

# searching input
query = driver.find_element(By.ID,"query")

# input
query.send_keys("...")

search_btn = driver.find_element(By.ID,"search-btn")
time.sleep(3)
search_btn.click()

driver.save_screenshot("1.png")
driver.quit()


