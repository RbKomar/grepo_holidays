# -*- coding: utf-8 -*-
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
import logging
from selenium.webdriver.common.action_chains import ActionChains

CITY_NAME_XPATH = '/html/body/div[1]/div[17]/div[3]/div[1]/div'

logging.basicConfig(level=logging.INFO, format='%(asctime)s::%(levelname)s::%(name)s - %(message)s')
logger = logging.getLogger('GrepoBot')


def define_idle_time(multiplier=1.):
    def long_idle():
        time.sleep(1 * multiplier)

    def short_idle():
        time.sleep(.5 * multiplier)

    return short_idle, long_idle


class City:
    def __init__(self, driver, short_idle, long_idle, building_bot=False):
        self.wood = 0
        self.stone = 0
        self.silver_coins = 0
        self.driver = driver
        self.short_idle = short_idle
        self.long_idle = long_idle

        self.name = self.get_city_name()
        if building_bot:
            self.building_names_map = self.load_building_names()
            self.building_list = self.load_building_list()
            self.building_levels = self.get_building_levels()
        else:
            self.building_names_map = None
            self.building_list = None
            self.building_levels = None

    @staticmethod
    def load_building_names():
        with open("resources/buildings_naming.json", "r") as fp:
            building_name_map = json.load(fp)
        return building_name_map

    def load_building_list(self):
        to_building_list_path = os.path.join("resources", "building_lists", f"{self.name}.csv")
        full_path = os.path.join(os.getcwd(), to_building_list_path)
        with open(full_path, "r") as fp:
            reader = csv.reader(fp)
            building_list = list(reader)
            if len(building_list) != 0:
                return building_list[0]
            else:
                return []

    def update_building_list(self, building_list):
        to_building_list_path = os.path.join("resources", "building_lists", f"{self.name}.csv")
        full_path = os.path.join(os.getcwd(), to_building_list_path)
        with open(full_path, "w") as fp:
            writer = csv.writer(fp)
            writer.writerow(building_list)

    def get_city_name(self):
        self.long_idle()
        city_name = self.driver.find_element(By.XPATH, CITY_NAME_XPATH).text
        logger.info(f"Welcome in {city_name}")
        return city_name

    def get_resources(self):
        self.wood = int(self.driver.find_element(By.XPATH, '//*[@id="ui_box"]/div[6]/div[1]/div[1]/div[2]').text)
        self.stone = int(self.driver.find_element(By.XPATH, '//*[@id="ui_box"]/div[6]/div[2]/div[1]/div[2]').text)
        self.silver_coins = int(
            self.driver.find_element(By.XPATH, '//*[@id="ui_box"]/div[6]/div[3]/div[1]/div[2]').text)
        logger.info(f"Currently in {self.name}: {self.wood} wood, {self.stone} stone, {self.silver_coins} silver coins")

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
            logger.error(f"Problem occured while reading the building levels in city {self.name}")
        return b

    def check_if_enough_free_residents(self, ):
        self.long_idle()
        ppl = int(self.driver.find_element(By.XPATH, '/html/body/div[1]/div[6]/div[4]/div[1]/div[2]').text)
        if ppl < 100 and len(self.building_list) != 0:
            if "Gospodarstwo wiejskie" != self.building_list[0]:
                self.building_list.insert(0, "Gospodarstwo wiejskie")
                self.update_building_list(self.building_list)
                logger.info("Not enough free residents, adding a farm to building list.")

    def is_building_possible(self, building: str):
        try:
            self.long_idle()
            self.driver.refresh()
            time.sleep(4)
            self.driver.find_element(By.CSS_SELECTOR,
                                     '#building_main_area_main').click()
            self.long_idle()
            try:
                msg = self.driver.find_element(By.XPATH,
                                               f'//*[@id="building_main_not_possible_button_{self.building_names_map[building]}"]').text
                logger.debug(msg)
                return False
            except Exception:
                if building != "" and building is not None:
                    logger.debug(f"Building {building} is possible.")
                return True
        except Exception as e:
            logger.error(f"Problem while checking if building {building} is possible.")

    def build(self, building: str):
        try:
            if self.is_building_possible(building):
                building_mapped_name = self.building_names_map[building]
                self.long_idle()
                self.long_idle()
                self.driver.find_element(By.XPATH,
                                         f'//*[@id="building_main_{building_mapped_name}"]/div[2]/a[1]').click()
                logger.info(f"Start building of {building_mapped_name}")
                return True
            else:
                return False
        except Exception as e:
            logger.error("Problem while building.")
            return False

    def building_bot(self):
        building_list = self.load_building_list()
        self.check_if_enough_free_residents()
        for building in building_list:
            building_stripped = building.strip()
            if self.build(building_stripped):
                building_list.remove(building)
                self.update_building_list(building_list)
            else:
                break



    def farming_villages(self, farm_cities):
        try:
            city_list = get_cities_list(self.driver, self.long_idle)
            for city in city_list.find_elements(By.TAG_NAME, "li"):
                try:
                    city_name = city.find_element(By.CLASS_NAME, "gp_town_link").text
                    if city_name in farm_cities:
                        city.find_element(By.CLASS_NAME, "town_checkbox").click()
                except Exception:
                    continue
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
                logger.info("Resources from the villages were collected.")
                return True
            except Exception as e:
                logger.error("Can't handle with popup screen in village farming.")
                logger.error(str(e))
        except Exception as e:
            logger.error("Exception occured while farming villages.")
            logger.error(str(e))


class Account:
    def __init__(self, username: str, password: str, server_url: str, multiplier: float, use_building_bot: bool,
                 check_storage: bool):
        self.current_city_obj = None
        self.username = username
        self.password = password
        self.server_url = server_url
        self.use_building_bot = use_building_bot
        self.check_storage = check_storage
        self.is_init = True
        self.cities_names = []
        self.driver = None
        self.multiplier = multiplier
        self.short_idle, self.long_idle = time.sleep(.5), time.sleep(1)
        self.define_idle_time()

    def run(self):
        farm_collector_counter = 0
        while True:
            try:
                self.login()
                self.long_idle()
                self.load_cities()
                self.long_idle()
                while True:
                    if self.use_building_bot:
                        self.build_in_every_city()
                        self.long_idle()
                    self.collect_farms()
                    farm_collector_counter += 1
                    print(f"Villages collected already {farm_collector_counter} times during this session.")
                    time.sleep(random.randint(300, 310))
            except Exception as e:
                logger.error(str(e))
                self.define_idle_time(.2)

    def load_cities(self):
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div[17]/div[3]/div[2]').click()
        city_counter = 1
        self.long_idle()
        while True:
            try:
                city_name = self.driver.find_element(By.XPATH,
                                                     f'//*[@id="town_groups_list"]/div[1]/div/div[2]/div/div[{city_counter}]/span').text
                self.cities_names.append(city_name)
                open(os.path.join(os.path.join("resources", "building_lists"), f"{city_name}.csv"), 'a',
                     encoding='UTF8').close()
                city_counter += 1
            except Exception:
                break

    def login(self):
        if self.is_init:
            s = Service(ChromeDriverManager().install())
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--mute-audio")
            self.driver = webdriver.Chrome(service=s, options=chrome_options)
            self.driver.maximize_window()
            self.driver.get(self.server_url)
            self.is_init = False
        try:
            self.driver.find_element(By.XPATH,
                                     '//*[@id="login_userid"]').send_keys(self.username)
            self.driver.find_element(By.XPATH,
                                     '//*[@id="login_password"]').send_keys(self.password)
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[3]/div/div[1]/div[1]/div[1]/div/form/button/span'
                                     ).click()
            self.long_idle()
        except Exception:
            print("Problem with login.")
        try:
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[2]/div/div/div[1]/div[2]/div[5]/form/div[2]/div/ul/li[1]/div'
                                     ).click()
            self.long_idle()
        except Exception:
            pass

    @staticmethod
    def is_overflowing(city_name, wood, stone, iron, storage_capacity):
        wood, stone, iron, storage_capacity = int(wood), int(stone), int(iron), int(storage_capacity)- 100
        is_wood_overflowing = wood >= storage_capacity
        is_stone_overflowing = stone >= storage_capacity
        is_iron_overflowing = iron >= storage_capacity
        logger.info(
            f"Are resources overflowing in {city_name}: Wood: {is_wood_overflowing} | Stone: {is_stone_overflowing} | Iron: {is_iron_overflowing} | Storage capacity: {storage_capacity}")
        return is_wood_overflowing and is_stone_overflowing and is_iron_overflowing

    def deal_exception(self, tries):
        self.define_idle_time(.2)
        tries += 1
        logger.debug(f"Try number: {tries}")
        return tries

    def get_cities_by_island(self):
        tries = 0
        while True:
            try:
                city_list = get_cities_list(self.driver, self.long_idle)
                islands = {}
                island_name = None
                for elem in city_list.find_elements(By.TAG_NAME, "li"):
                    try:
                        current_island_name = elem.find_element(By.CLASS_NAME, "gp_island_link").text
                        if current_island_name:
                            island_name = current_island_name
                    except Exception:
                        pass
                    if island_name and island_name not in islands:
                        islands[island_name] = []
                    try:
                        city_name = elem.find_element(By.CLASS_NAME, "gp_town_link").text
                        islands[island_name].append(city_name)
                    except Exception:
                        pass
                for island, cities in islands.items():
                    logger.info(f"{island}: {cities}")
                return islands
            except Exception as e:
                logger.error(str(e))
                tries = self.deal_exception(tries)
                if tries > 4:
                    break

    def check_storage_in_every_city(self):
        tries = 0
        while True:
            try:
                cities_with_full_storage = []
                self.driver.refresh()
                self.long_idle()
                self.driver.find_element(By.XPATH,
                                         '//*[@id="ui_box"]/div[14]/div[3]/div'
                                         ).click()
                self.short_idle()
                city_list = self.driver.find_element(By.ID, 'trade_overview_towns')
                for city in city_list.find_elements(By.TAG_NAME, "li"):
                    city_name = city.find_element(By.CLASS_NAME, "gp_town_link").text
                    wood = city.find_element(By.CLASS_NAME, "resource_wood_icon").text
                    stone = city.find_element(By.CLASS_NAME, "resource_stone_icon").text
                    iron = city.find_element(By.CLASS_NAME, "resource_iron_icon").text
                    storage_capacity = city.find_element(By.CLASS_NAME, "storage_icon").text
                    if self.is_overflowing(city_name, wood, stone, iron, storage_capacity):
                        cities_with_full_storage.append(city_name)
                if cities_with_full_storage:
                    logger.info(f'Cities with full storage are {", ".join(cities_with_full_storage)}')
                else:
                    logger.info("No city has full storage.")
                return cities_with_full_storage
            except Exception:
                logger.error("Exception occured while checking storage in every city.")
                tries = self.deal_exception(tries)
                if tries > 4:
                    break

    def iterate_until_city(self, city_name: str):
        counter = 0
        while True:
            try:
                if counter > 30:
                    logger.error(f"Can't find the city with name: {city_name}.")
                    break
                self.long_idle()
                city_at_the_moment = self.driver.find_element(By.XPATH, CITY_NAME_XPATH).text
                if city_at_the_moment == city_name:
                    return
                else:
                    self.driver.find_element(By.XPATH,
                                             '/html/body/div[1]/div[17]/div[2]').click()
                self.long_idle()
                counter += 1
            except Exception as e:
                logger.error("Exception occured while iterating until city.")
                self.define_idle_time(.2)

    def create_city_object(self):
        city = City(self.driver, self.short_idle, self.long_idle)
        return city

    def build_in_every_city(self):
        for city in self.cities_names:
            self.driver.refresh()
            self.long_idle()
            self.iterate_until_city(city)
            self.current_city_obj = self.create_city_object()
            self.driver.refresh()
            self.long_idle()
            self.current_city_obj.building_bot()

    @staticmethod
    def cities_to_farm(cities_with_full_storage: list, cities_by_island: dict):
        cities_to_use = []
        for island, cities in cities_by_island.items():
            for city in cities:
                if city not in cities_with_full_storage:
                    cities_to_use.append(city)
                    break
                else:
                    found = False
                    for city_on_island in cities:
                        if city_on_island not in cities_to_use and city_on_island not in cities_with_full_storage:
                            cities_to_use.append(city_on_island)
                            found = True
                            break
                    if found:
                        break
        return cities_to_use

    def collect_farms(self):
        self.driver.refresh()
        self.long_idle()
        self.current_city_obj = self.create_city_object()
        self.long_idle()
        if self.check_storage:
            cities_with_full_storage = self.check_storage_in_every_city()
            cities_by_island = self.get_cities_by_island()
            farm_cities = self.cities_to_farm(cities_with_full_storage, cities_by_island)
            self.driver.refresh()
            self.long_idle()
            self.current_city_obj.farming_villages(farm_cities)
        else:
            self.driver.refresh()
            self.long_idle()
            self.current_city_obj.farming_villages([])

    def define_idle_time(self, redefine: float = .0):
        self.multiplier += redefine

        def long_idle():
            time.sleep(1 * self.multiplier)

        def short_idle():
            time.sleep(.5 * self.multiplier)

        if self.multiplier >= 3.5:
            self.multiplier = 2
        self.short_idle = short_idle
        self.long_idle = long_idle


def get_cities_list(driver, long_idle):
    driver.refresh()
    long_idle()
    button_to_hover = driver.find_element(By.XPATH,
                                               '/html/body/div[1]/div[14]/div[3]/div'
                                               )
    ActionChains(driver).move_to_element(button_to_hover).perform()
    driver.find_element(By.XPATH,
                             '//*[@id="overviews_link_hover_menu"]/div[2]/div/div/ul/li[2]/ul/li[2]/a'
                             ).click()
    long_idle()
    city_list = driver.find_element(By.ID, 'fto_town_list')
    return city_list


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def main():
    config = configparser.ConfigParser()
    config.read(r'config.txt')
    username = config.get('Account', 'username')
    password = config.get('Account', 'password')
    server_url = config.get('Account', 'server_url')
    multiplier = float(config.get('Account', 'multiplier'))
    building_bot = str2bool(config.get('Account', 'building_bot'))
    check_storage = str2bool(config.get('Account', 'storage_check'))

    acc = Account(username, password, server_url, multiplier, building_bot, check_storage)
    acc.run()
    return 0


if __name__ == '__main__':
    main()
