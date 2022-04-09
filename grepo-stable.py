# coding: utf-8
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import csv
import time
import configparser
import os


def define_idle_time(multiplier=1.):
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
        self.driver = driver
        self.short_idle = short_idle
        self.long_idle = long_idle

        self.storage = self.get_storage_capacity()
        self.name = self.get_city_name()

        self.building_names_map = self.load_building_names()
        self.building_list = self.load_building_list()

        #self.building_levels = self.get_building_levels()

    @staticmethod
    def load_building_names():
        with open("resources/buildings_naming.json", "r") as fp:
            building_name_map = json.load(fp)
        return building_name_map

    def load_building_list(self):
        to_building_list_path = os.path.join(os.path.join("resources", "building_lists"), f"{self.name}.csv")
        full_path = os.path.join(os.getcwd(), to_building_list_path)
        with open(full_path, "r") as fp:
            reader = csv.reader(fp)
            building_list = list(reader)
            return building_list[0]

    def update_building_list(self, building_list):
        to_building_list_path = os.path.join(os.path.join("resources", "building_lists"), f"{self.name}.csv")
        full_path = os.path.join(os.getcwd(), to_building_list_path)
        with open(full_path, "w") as fp:
            writer = csv.writer(fp)
            writer.writerow(building_list)

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
            window_id = self.driver.find_element(By.CSS_SELECTOR,
                                                 'body > div.window_curtain.ui-front > div').get_attribute("id")
            storage_cap_string = self.driver.find_element(By.XPATH,
                                                          f'//*[@id="{window_id}"]/div[11]/div/div[2]/div[1]/div[3]'
                                                          ).text
            storage_cap_possible = [int(s) for s in storage_cap_string.split() if s.isdigit()]
            storage_cap = storage_cap_possible[-1]
            return storage_cap
        except Exception as e:
            print(str(e))
            return 0

    def get_building_levels(self):
        b = {}
        try:
            self.driver.refresh()
            self.long_idle()
            self.long_idle()

            self.driver.find_element(By.ID,
                                     'building_main_area_main').click()
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
            print(str(e))
        return b

    def check_if_enough_free_residents(self, ):
        ppl = int(self.driver.find_element(By.XPATH, '/html/body/div[1]/div[6]/div[4]/div[1]/div[2]').text)
        if ppl < 20 and "Gospodarstwo wiejskie" != self.building_list[0]:
            self.building_list.insert(0, "Gospodarstwo wiejskie")

    def is_building_possible(self, building: str):
        try:
            self.long_idle()
            self.long_idle()
            self.long_idle()
            self.driver.refresh()
            self.long_idle()
            self.driver.find_element(By.CSS_SELECTOR,
                                     '#building_main_area_main').click()
            self.long_idle()
            try:
                msg = self.driver.find_element(By.XPATH,
                                               f'//*[@id="building_main_not_possible_button_{self.building_names_map[building]}"]').text
                print(msg)
                return False
            except Exception as e:
                if building != "" and building is not None:
                    print("Budowa jest możliwa.")
                print(e)
                return True
        except Exception as e:
            print(str(e))

    def build(self, building: str):
        try:
            if self.is_building_possible(building):
                building_mapped_name = self.building_names_map[building]
                self.driver.find_element(By.XPATH,
                                         f'//*[@id="building_main_{building_mapped_name}"]/div[2]/a[1]').click()
                #self.building_levels[building] += 1
                print(f"Start building of {building_mapped_name}")
                return True
            else:
                return False
        except Exception as e:
            print(str(e))
            return False

    def building_bot(self):
        building_list = self.load_building_list()
        self.check_if_enough_free_residents()
        for building in building_list:
            if self.build(building):
                building_list.remove(building)
                self.update_building_list(building_list)
            else:
                break

    def check_storage(self):
        if self.wood >= self.storage - 500 and self.stone >= self.storage - 500 and self.silver_coins >= self.storage - 500:
            return True
        else:
            return False

    def farming_villages(self):
        try:
            self.long_idle()
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[1]/div[14]/div[3]/div'
                                     ).click()
            self.long_idle()
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[7]/div[2]/div/div/ul/li[2]/ul/li[2]'
                                     ).click()
            self.long_idle()
            self.driver.find_element(By.XPATH,
                                     '//*[@id="fto_town_wrapper"]/div/div[9]/span/a'
                                     ).click()
            self.long_idle()
            self.driver.find_element(By.XPATH,
                                     '//*[@id="fto_claim_button"]'
                                     ).click()
            try:
                self.long_idle()
                selector_path = 'body > div.window_curtain.ui-front.show_curtain.is_modal_window > div'
                window_id = self.driver.find_element(By.CSS_SELECTOR,
                                                     selector_path).get_attribute("id")

                self.driver.find_element(By.XPATH,
                                         f'//*[@id="{window_id}"]/div[11]/div/div[2]/div[1]/div[3]'
                                         ).click()
                self.long_idle()
                return True
            except Exception as e:
                print("Can't handle with popup screen in village farming")
                print(str(e))
        except Exception as e:
            print(str(e))


class Account:
    def __init__(self, username: str, password: str, server_url: str, multiplier: float):
        self.current_city_obj = None
        self.username = username
        self.password = password
        self.server_url = server_url
        self.is_init = True
        self.cities_names = []
        self.driver = None

        self.short_idle, self.long_idle = define_idle_time(multiplier)

    def run(self):
        try:
            self.login()
            self.long_idle()
            self.load_cities()
            self.long_idle()
            while True:
                self.build_in_every_city()
                self.long_idle()
                self.collect_farms()
                time.sleep(random.randint(300, 310))
        except Exception as e:
            print(str(e))

    def load_cities(self):
        self.driver.find_element(By.XPATH,
                                 '/html/body/div[1]/div[17]/div[3]/div[2]'
                                 ).click()
        city_counter = 1
        self.long_idle()
        while True:
            try:
                city_name = self.driver.find_element(By.XPATH,
                                                     f'//*[@id="town_groups_list"]/div[1]/div/div[2]/div/div[{city_counter}]/span').text
                self.cities_names.append(city_name)
                open(os.path.join(os.path.join("resources", "building_lists"), f"{city_name}.csv"), 'a', encoding='UTF8').close()
                city_counter += 1
            except Exception:
                break

    def login(self):
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s)

        self.driver.maximize_window()
        self.driver.get(self.server_url)
        try:
            self.driver.find_element(By.XPATH,
                                     '//*[@id="login_userid"]').send_keys(self.username)
            self.driver.find_element(By.XPATH,
                                     '//*[@id="login_password"]').send_keys(self.password)
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[3]/div/div[1]/div[1]/div[1]/div/form/button/span'
                                     ).click()
            self.long_idle()
        except Exception as e:
            print("Problem with login.")
            print(str(e))
        try:
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[2]/div/div/div[1]/div[2]/div[5]/form/div[2]/div/ul/li[1]/div'
                                     ).click()
            self.long_idle()
        except Exception as e:
            print("Problem with choosing the server.")
            print(str(e))

    def check_storage_in_every_city(self):
        first_city = self.driver.find_element(By.XPATH,
                                              '/html/body/div[1]/div[17]/div[3]/div[1]/div').text
        actual_city = ""
        is_storage_not_full = True
        while actual_city != first_city:
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[1]/div[17]/div[2]').click()
            self.long_idle()
            actual_city = self.driver.find_element(By.XPATH,
                                                   '/html/body/div[1]/div[17]/div[3]/div[1]/div').text
            city = self.create_city_object()
            is_storage_not_full = is_storage_not_full and city.check_storage()
        return is_storage_not_full

    def iterate_until_city(self, city_name: str):
        actual_city = self.driver.find_element(By.XPATH,
                                               '/html/body/div[1]/div[17]/div[3]/div[1]/div').text
        while actual_city != city_name:
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[1]/div[17]/div[2]').click()
            self.long_idle()
            actual_city = self.driver.find_element(By.XPATH,
                                                   '/html/body/div[1]/div[17]/div[3]/div[1]/div').text

    def create_city_object(self):
        city = City(self.driver, self.short_idle, self.long_idle)
        return city

    def build_in_every_city(self):
        for city in self.cities_names:
            self.iterate_until_city(city)
            self.current_city_obj = self.create_city_object()
            self.current_city_obj.building_bot()

    def collect_farms(self):
        if self.check_storage_in_every_city():
            self.current_city_obj.farming_villages()
        else:
            print("Storage is full!")


def main():
    config = configparser.ConfigParser()
    config.read(r'config.txt')
    username = config.get('Account', 'username')
    password = config.get('Account', 'password')
    server_url = config.get('Account', 'server_url')
    multiplier = float(config.get('Account', 'multiplier'))

    acc = Account(username, password, server_url, multiplier)
    acc.run()
    return 0


if __name__ == '__main__':
    main()
