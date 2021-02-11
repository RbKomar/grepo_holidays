from selenium import webdriver
import time

url = "https://pl96.grepolis.com/"
driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)

# potem napisze bo tera mi sie nie chce XD
def building_bot(building_list: []):
    driver.find_element_by_xpath(
        '/html/body/div[3]/div/div[1]/div[1]/div[1]/div/form/button/span'
    ).click()


login = "kanapke"
password = "robcio98"
collected_flag = False
while True:
    try:
        driver.find_element_by_xpath(
            '//*[@id="login_userid"]').send_keys(login)
        driver.find_element_by_xpath(
            '//*[@id="login_password"]').send_keys(password)
        driver.find_element_by_xpath(
            '/html/body/div[3]/div/div[1]/div[1]/div[1]/div/form/button/span'
        ).click()
        time.sleep(2)
    except:
        pass

    try:
        driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[1]/div[2]/div[4]/form/div[2]/div/ul/li[1]/div'
        ).click()
        time.sleep(1)
    except:
        pass

    try:
        driver.find_element_by_xpath(
            '/html/body/div[13]/div/div[8]/div[3]/div'
        ).click()
        time.sleep(1)
    except:
        pass

    try:
        time.sleep(5)
        driver.find_element_by_xpath(
            '/html/body/div[1]/div[14]/div[3]/div'
        ).click()
        time.sleep(3)
        driver.find_element_by_xpath(
            '/html/body/div[7]/div[2]/div/div/ul/li[2]/ul/li[2]'
        ).click()
        time.sleep(3)
        driver.find_element_by_xpath(
            '/html/body/div[14]/div[2]/div[5]/div[2]/div[2]/div/ul/li[2]/div[3]/div[3]'
        ).click()
        collected_flag = True
    except:
        collected_flag = False
    if collected_flag:
        waiting_time = 300
    else:
        waiting_time = 1
    time.sleep(waiting_time)
    driver.refresh()
    time.sleep(2)
#driver.quit()


