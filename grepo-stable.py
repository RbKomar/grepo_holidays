from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time


def define_idle_time(multiplier=1):
    def long_idle():
        time.sleep(1 * multiplier)

    def short_idle():
        time.sleep(.5 * multiplier)

    return short_idle, long_idle


class City:
    def __init__(self, driver, short_idle, long_idle):
        self.wood = 0
        self.stone = 0
        self.silver_coins = 0
        self.storage = self.get_storage_capacity()
        self.name = self.get_city_name()

        self.building_names_map = self.load_building_names()
        self.building_list = self.load_building_list()

        self.driver = driver
        self.short_idle = short_idle
        self.long_idle = long_idle

        self.building_levels = self.get_building_levels()

    @staticmethod
    def load_building_names():
        with open("mapping/buildings_naming.json", "r") as fp:
            building_name_map = json.load(fp)
        return building_name_map

    @staticmethod
    def load_building_list(path=""):
        if path != "":
            with open(path, "r") as fp:
                data = fp.read()
                building_list = data.split(r"\n")
                return building_list
        return []

    def get_city_name(self):
        city_name = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[17]/div[3]/div[1]/div').text
        return city_name

    def get_resources(self):
        self.wood = int(self.driver.find_element(By.XPATH, '//*[@id="ui_box"]/div[6]/div[1]/div[1]/div[2]').text)
        self.stone = int(self.driver.find_element(By.XPATH, '//*[@id="ui_box"]/div[6]/div[2]/div[1]/div[2]').text)
        self.silver_coins = int(
            self.driver.find_element(By.XPATH, '//*[@id="ui_box"]/div[6]/div[3]/div[1]/div[2]').text)

    def get_storage_capacity(self):
        try:
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[1]/div[6]/div[1]'
                                     ).click()
            self.long_idle()
            storage_cap_string = self.driver.find_element(By.XPATH,
                                                          '/html/body/div[13]/div/div[11]/div/div[2]/div[1]/div[3]/text()[2]'
                                                          ).text()
            storage_cap_possible = [int(s) for s in storage_cap_string.split() if s.isdigit()]
            storage_cap = storage_cap_possible[-1]
            return storage_cap
        except Exception as e:
            print(e)
            return 0

    def get_building_levels(self):
        b = {}
        try:
            self.long_idle()
            self.driver.find_element(By.XPATH,
                                     '//*[@id="quickbar_dropdown0"]/div').click()
            self.short_idle()
            b["Senat"] = int(
                self.driver.find_element(By.XPATH, '//*[@id="building_main_main"]/div[2]/div[1]/span[2]').text)
            b["Obóz drwali"] = int(
                self.driver.find_element(By.XPATH, '//*[@id="building_main_lumber"]/div[2]/div[1]/span[2]').text)
            b["Gospodarstwo wiejskie"] = int(
                self.driver.find_element(By.XPATH, '//*[@id="building_main_farm"]/div[2]/div[1]/span[1]').text)
            b["Kamieniołom"] = int(
                self.driver.find_element(By.XPATH, '//*[@id="building_main_stoner"]/div[2]/div[1]/span[1]').text)
            b["Magazyn"] = int(
                self.driver.find_element(By.XPATH, '//*[@id="building_main_storage"]/div[2]/div[1]/span[1]').text)
            b["Kopalnia srebra"] = int(
                self.driver.find_element(By.XPATH, '//*[@id="building_main_ironer"]/div[2]/div[1]/span[1]').text)
            b["Koszary"] = int(
                self.driver.find_element(By.XPATH, '//*[@id="building_main_barracks"]/div[2]/div[1]/span[1]').text)
            b["Świątynia"] = int(
                self.driver.find_element(By.XPATH, '//*[@id="building_main_temple"]/div[2]/div[1]/span[1]').text)
            b["Targowisko"] = int(
                self.driver.find_element(By.XPATH, '//*[@id="building_main_market"]/div[2]/div[1]/span[1]').text)
            b["Port"] = int(
                self.driver.find_element(By.XPATH, '//*[@id="building_main_docks"]/div[2]/div[1]/span[1]').text)
            b["Akademia"] = int(
                self.driver.find_element(By.XPATH, '//*[@id="building_main_academy"]/div[2]/div[1]/span[1]').text)
            b["Mur miejski"] = int(
                self.driver.find_element(By.XPATH, '//*[@id="building_main_wall"]/div[2]/div[1]/span[1]').text)
            b["Jaskinia"] = int(
                self.driver.find_element(By.XPATH, '//*[@id="building_main_hide"]/div[2]/div[1]/span[1]').text)
        except Exception as e:
            print(f"Problem occured while reading the building levels in city {self.name}")
            print(e)
        return b

    def check_if_enough_free_residents(self, ):
        ppl = int(self.driver.find_element(By.XPATH, '/html/body/div[1]/div[6]/div[4]/div[1]/div[2]').text)
        if ppl < 20 and "Gospodarstwo wiejskie" != self.building_list[0]:
            self.building_list.insert(0, "Gospodarstwo wiejskie")

    def is_building_possible(self, building: str):
        try:
            self.long_idle()
            self.driver.find_element(By.XPATH,
                                     '//*[@id="quickbar_dropdown0"]/div').click()
            self.long_idle()
            msg = self.driver.find_element(By.XPATH,
                                           '// *[ @ id = "building_main_not_possible_button_' + self.building_names_map[
                                               building] + '"]').text
            print(msg)
            return False
        except:
            print("Budowa jest możliwa.")
            return True

    def build(self, building: str):
        try:
            if self.is_building_possible(building):
                building_mapped_name = self.building_names_map[building]
                self.driver.find_element(By.XPATH,
                                         f'//*[@id="building_main_{building_mapped_name}"]/div[2]/a[1]').click()
                self.building_levels[building] += 1
                print(f"Start building of {building_mapped_name} on level {self.building_levels[building]}")
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def building_bot(self, building_l: []):
        self.check_if_enough_free_residents()
        for building in building_l[:]:
            if self.build(building):
                building_l.remove(building)
            else:
                break


class Account:
    def __init__(self, multiplier):
        self.username = ""
        self.password = ""
        self.server_url = ""
        self.cities = []
        self.driver = None

        self.short_idle, self.long_idle = define_idle_time(multiplier)
        self.login()

    def load_cities(self):
        self.driver.find_element(By.XPATH,
                            '/html/body/div[3]/div/div[1]/div[1]/div[1]/div/form/button/span'
                            ).click()

    def login(self):
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s)

        self.driver.maximize_window()
        self.driver.get(self.server_url)

        try:
            self.driver.find_element(By.XPATH,
                                '//*[@id="login_userid"]').send_keys(self.login)
            self.driver.find_element(By.XPATH,
                                '//*[@id="login_password"]').send_keys(self.password)
            self.driver.find_element(By.XPATH,
                                '/html/body/div[3]/div/div[1]/div[1]/div[1]/div/form/button/span'
                                ).click()
            self.long_idle()
        except Exception as e:
            print("Problem with login.")
            print(e)
        try:
            self.driver.find_element(By.XPATH,
                                '/html/body/div[2]/div/div/div[1]/div[2]/div[5]/form/div[2]/div/ul/li[1]/div'
                                ).click()
            self.long_idle()
        except Exception as e:
            print("Problem with choosing the server.")
            print(e)

def main():
    return 0

if __name__ == '__main__':
    main()
