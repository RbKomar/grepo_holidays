from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time

url = "https://pl106.grepolis.com/"
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.maximize_window()
driver.get(url)

attack_counter = 0

# INFO VARS
############################################################################################
login = "l"
password = "p"
MAXIMUM_STORAGE = 14315

building_name_map = {
    "Senat": "main",
    "Obóz drwali": "lumber",
    "Gospodarstwo wiejskie": "farm",
    "Kamieniołom": "stoner",
    "Magazyn": "storage",
    "Kopalnia srebra": "ironer",
    "Koszary": "barracks",
    "Świątynia": "temple",
    "Targowisko": "market",
    "Port": "docks",
    "Akademia": "academy",
    "Mur miejski": "wall",
    "Jaskinia": "hide"}

building_list = [
]


# FUNCTIONS
############################################################################################
def collect_building_levels():
    b = {}
    time.sleep(4)
    driver.find_element(By.XPATH,
                        '//*[@id="quickbar_dropdown0"]/div').click()
    time.sleep(2)
    b["Senat"] = int(driver.find_element(By.XPATH, '//*[@id="building_main_main"]/div[2]/div[1]/span[2]').text)
    b["Obóz drwali"] = int(driver.find_element(By.XPATH, '//*[@id="building_main_lumber"]/div[2]/div[1]/span[2]').text)
    b["Gospodarstwo wiejskie"] = int(
        driver.find_element(By.XPATH, '//*[@id="building_main_farm"]/div[2]/div[1]/span[1]').text)
    b["Kamieniołom"] = int(driver.find_element(By.XPATH, '//*[@id="building_main_stoner"]/div[2]/div[1]/span[1]').text)
    b["Magazyn"] = int(driver.find_element(By.XPATH, '//*[@id="building_main_storage"]/div[2]/div[1]/span[1]').text)
    b["Kopalnia srebra"] = int(
        driver.find_element(By.XPATH, '//*[@id="building_main_ironer"]/div[2]/div[1]/span[1]').text)
    b["Koszary"] = int(driver.find_element(By.XPATH, '//*[@id="building_main_barracks"]/div[2]/div[1]/span[1]').text)
    b["Świątynia"] = int(driver.find_element(By.XPATH, '//*[@id="building_main_temple"]/div[2]/div[1]/span[1]').text)
    b["Targowisko"] = int(driver.find_element(By.XPATH, '//*[@id="building_main_market"]/div[2]/div[1]/span[1]').text)
    b["Port"] = int(driver.find_element(By.XPATH, '//*[@id="building_main_docks"]/div[2]/div[1]/span[1]').text)
    b["Akademia"] = int(driver.find_element(By.XPATH, '//*[@id="building_main_academy"]/div[2]/div[1]/span[1]').text)
    b["Mur miejski"] = int(driver.find_element(By.XPATH, '//*[@id="building_main_wall"]/div[2]/div[1]/span[1]').text)
    b["Jaskinia"] = int(driver.find_element(By.XPATH, '//*[@id="building_main_hide"]/div[2]/div[1]/span[1]').text)
    return b


def is_building_possible(building: str):
    try:
        time.sleep(4)
        driver.find_element(By.XPATH,
                            '//*[@id="quickbar_dropdown0"]/div').click()
        time.sleep(2)
        msg = driver.find_element(By.XPATH, '// *[ @ id = "building_main_not_possible_button_' + building_name_map[
            building] + '"]').text
        print(msg)
        return False
    except:
        return True


def build(building: str):
    try:
        time.sleep(4)
        driver.find_element(By.XPATH,
                            '//*[@id="quickbar_dropdown0"]/div').click()
        time.sleep(2)
        if is_building_possible(building):
            driver.find_element(By.XPATH,
                                '//*[@id="building_main_' + building_name_map[building] + '"]/div[2]/a[1]').click()
            return True
        else:
            print("something is not ok in build()")
            return False
    except:
        print("Can't build yet")
        return False


def building_bot(building_l: []):
    check_farm()
    for building in building_l[:]:
        if build(building):
            building_l.remove(building)
        else:
            break


def farming_villages():
    if check_storage():
        print("Full storage")
        return False
    time.sleep(3)
    try:
        time.sleep(5)
        driver.find_element(By.XPATH,
                            '/html/body/div[1]/div[14]/div[3]/div'
                            ).click()
        time.sleep(3)
        driver.find_element(By.XPATH,
                            '/html/body/div[7]/div[2]/div/div/ul/li[2]/ul/li[2]'
                            ).click()
        time.sleep(3)
        driver.find_element(By.XPATH,
                            '//*[@id="fto_town_wrapper"]/div/div[9]/span/a'
                            ).click()
        time.sleep(3)
        driver.find_element(By.XPATH,
                            '//*[@id="fto_claim_button"]'
                            ).click()
        try:
            time.sleep(2)
            driver.find_element(By.XPATH,
                                '/html/body/div[14]/div/div[11]/div/div[2]/div[1]/div[3]'
                                ).click()
            time.sleep(2)
        except:
            print("Can't handle with popup screen in village farming")
        return True
    except:
        return False


def attack_bandits():
    time.sleep(4)
    driver.find_element(By.XPATH,
                        '// *[ @ id = "ui_box"] / div[8] / div[1] / div[1] / div[1] / div'
                        ).click()
    try:
        try:
            time.sleep(3)
            driver.find_element(By.XPATH,
                                '/html/body/div[1]/div[22]/div/div[1]/div[1]/div[2]/div[5]/div'
                                ).click()
        except:
            print("Couldn't find the bandits")
        time.sleep(1.5)
        # KLIKANIE JEDNOSTEK XD
        driver.find_element(By.XPATH,
                            '/html/body/div[12]/div/div[11]/div/div[3]/div/div[11]/div/div[1]/div[2]/div[1]'
                            ).click()
        time.sleep(.5)
        driver.find_element(By.XPATH,
                            '/html/body/div[12]/div/div[11]/div/div[3]/div/div[11]/div/div[1]/div[4]/div[1]'
                            ).click()
        time.sleep(.5)
        driver.find_element(By.XPATH,
                            '/html/body/div[12]/div/div[11]/div/div[3]/div/div[11]/div/div[1]/div[5]/div[1]'
                            ).click()
        time.sleep(.5)
        driver.find_element(By.XPATH,
                            '/html/body/div[12]/div/div[11]/div/div[3]/div/div[11]/div/div[1]/div[9]/div[1]'
                            ).click()
        time.sleep(.5)
        print("wybral wojska")
        # kliknij w atak
        driver.find_element(By.XPATH,
                            '/html/body/div[12]/div/div[11]/div/div[5]/div[3]'
                            ).click()
        time.sleep(2)
    except:
        collect_reward()
        print("Something happened during preparing the attack on bandits")


def collect_reward():
    try:
        time.sleep(2)
        driver.find_element(By.XPATH,
                            '/html/body/div[1]/div[8]/div[1]/div[1]/div[1]/div'
                            ).click()
        time.sleep(2)
        driver.find_element(By.XPATH,
                            '/html/body/div[1]/div[22]/div/div[1]/div[1]/div[2]/div[5]/div'
                            ).click()
        time.sleep(2)
        driver.find_element(By.XPATH,
                            '/html/body/div[12]/div/div[11]/div/div/div[3]/a'
                            ).click()
        time.sleep(2)
        try:
            driver.find_element(By.XPATH,
                                '/html/body/div[13]/div[2]'
                                ).click()
        except:
            driver.find_element(By.XPATH,
                                '/html/body/div[13]/div[1]'
                                ).click()
        time.sleep(1)
    except:
        print("Couldn't collect the fight reward.")


def check_storage():
    wood = int(driver.find_element(By.XPATH, '//*[@id="ui_box"]/div[6]/div[1]/div[1]/div[2]').text)
    stone = int(driver.find_element(By.XPATH, '//*[@id="ui_box"]/div[6]/div[2]/div[1]/div[2]').text)
    cash = int(driver.find_element(By.XPATH, '//*[@id="ui_box"]/div[6]/div[3]/div[1]/div[2]').text)
    print(f"Wood: {wood} | Stone: {stone}| Silver coins: {cash}")
    if wood >= MAXIMUM_STORAGE and stone >= MAXIMUM_STORAGE and cash >= MAXIMUM_STORAGE:
        return True
    else:
        return False


def check_farm():
    ppl = int(driver.find_element(By.XPATH, '/html/body/div[1]/div[6]/div[4]/div[1]/div[2]').text)
    if ppl < 10:
        if "Gospodarstwo wiejskie" != building_list[0]:
            building_list.insert(0, "Gospodarstwo wiejskie")


# MAIN BODY
############################################################################################
while True:
    # LOGIN
    try:
        driver.find_element(By.XPATH,
                            '//*[@id="login_userid"]').send_keys(login)
        driver.find_element(By.XPATH,
                            '//*[@id="login_password"]').send_keys(password)
        driver.find_element(By.XPATH,
                            '/html/body/div[3]/div/div[1]/div[1]/div[1]/div/form/button/span'
                            ).click()
        time.sleep(2)
    except:
        pass
    # select server
    try:
        driver.find_element(By.XPATH,
                            '/html/body/div[2]/div/div/div[1]/div[2]/div[5]/form/div[2]/div/ul/li[1]/div'
                            ).click()
        time.sleep(1)
    except:
        pass
    # AFTER LOGIN
    time.sleep(5)
    if attack_counter % 2 == 0:
        building_bot(building_list)
        driver.refresh()
        time.sleep(4)
    # ATTACKING BANDITS ES
    # if attack_counter % 2 == 0:
    #     collect_reward()
    #     attack_bandits()
    #     driver.refresh()
    #     time.sleep(3)
    #     if attack_counter == 2:
    #         attack_counter = 0
    # if attack_counter == 1:
    #     collect_reward()
    #     driver.refresh()
    #     time.sleep(3)
    ##############################
    if farming_villages():
        waiting_time = 310
        attack_counter += 1
    else:
        waiting_time = 5
    time.sleep(waiting_time)
    driver.refresh()
    time.sleep(20)
# driver.quit()
