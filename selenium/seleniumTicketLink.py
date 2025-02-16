from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


options=Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

#url = "https://www.ticketlink.co.kr/home"
url = "https://www.ticketlink.co.kr/sports/1191/574"   # handball
driver.get(url)
time.sleep(1)

# # sports page
# sports = driver.find_element(By.XPATH, "/html/body/div/div[1]/header/div[2]/nav/ul/li[2]/a")
# sports.click()
# print("sports page loaded")
# time.sleep(1)

#login page
login = driver.find_element(By.XPATH,"/html/body/div/div[1]/header/div[1]/div/div[2]/ul/li[1]/a")
login.click()
print("login")
time.sleep(1)
driver.switch_to.window(driver.window_handles[1])
ID = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[1]/form/div[1]/div/div[1]/input")
ID.send_keys("Put your ID here")
time.sleep(0.5)
password = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[1]/form/div[2]/div[1]/input")
password.send_keys("Put your password here")
time.sleep(0.3)
login_btn = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/button[1]")
login_btn.click()
time.sleep(0.5)

# birthday page
birthday = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/form/div/div[1]/input")
birthday.send_keys("Put your birthday here")
birthday_btn = driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/button")
birthday_btn.click()
print("login completed")
time.sleep(2)


#switch back to booking site window
driver.switch_to.window(driver.window_handles[0])

# book tickets
book_btn = driver.find_element(By.XPATH,"/html/body/div/div/main/article/section[3]/div[2]/div[2]/ul/li[1]/div[3]/a")
book_btn.click()

time.sleep(1)
confirm_btn = driver.find_element(By.XPATH,"/html/body/div/div[2]/div[2]/div[3]/button")
confirm_btn.click()
time.sleep(1)


#select seats




