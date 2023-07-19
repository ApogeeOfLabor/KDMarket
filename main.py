import csv
import os
import re
from time import sleep
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import requests
from fake_useragent import UserAgent


class DynamicParser:
    def __init__(self, url: str, items: list = None, count: int = None, version_chrome=None):
        self.url = url
        self.items = items
        self.count = count
        self.browser = version_chrome

    # @staticmethod
    # def __download_img(links_list, addr):
    #     headers = {
    #         'Accept': '*/*',
    #         "user-agent": UserAgent().random
    #     }
    #     for link in links_list:
    #         if not os.path.exists(f'{addr}/{link.split("/")[-1]}'):
    #             try:
    #                 responce = requests.get(link, headers=headers)
    #
    #                 with open(f'{addr}/{link.split("/")[-1]}', 'wb') as file:
    #                     file.write(responce.content)
    #                 print(f'скачано -- {link}')
    #             except Exception as ex:
    #                 print('UPPS!!!')
    #
    #             sleep(1)

    # @staticmethod
    # def __make_csv(file_name, addr, data_list=None, flag='w'):
    #     res_dict = {}
    #     print('СТАРТ СОЗДАНИЯ CSV')
    #     if data_list:
    #         for key, value in zip(data_list[0], data_list[1]):
    #             res_dict[key] = value
    #         res_df = pd.DataFrame(res_dict)
    #         # print(res_df)
    #         if not os.path.exists(f'{addr}/{file_name}.csv'):
    #             res_df.to_csv(f'{addr}/{file_name}.csv')  # , index=False, mode=f'{flag}'
    #             print(f'{file_name}.CSV СОЗДАН')
    #     else:
    #         if not os.path.exists(f'{addr}/{file_name}.csv'):
    #             with open(f'{addr}/{file_name}.csv', 'w', encoding='utf-8') as file:
    #                 file.write('')

    # @staticmethod
    # def __make_dirs(dir_name, addr=f'{os.path.dirname(__file__)}'):
    #     print('СТАРТ СОЗДАНИЯ ДИРЕКТОРИЙ')
    #     if not os.path.exists(f'{addr}/{dir_name}'):
    #         os.mkdir(f'{addr}/{dir_name}')
    #         print(f'СОЗДАНА ДИРЕКТОРИЯ {dir_name}')
    #         return True

    # @staticmethod
    # def __download_html(source, dir_name='catalog', file_name='catalog'):
    #     print('НАЧИНАЮ СКАЧИВАНИЕ HTML')
    #     """ source = self.driver.page_source """
    #
    #     if dir_name == 'catalog' and file_name == 'catalog':
    #         if not os.path.exists(f'{os.path.dirname(__file__)}/catalog/catalog.html'):
    #             with open(f'{os.path.dirname(__file__)}/catalog/catalog.html', 'w', encoding='utf-8') as file:
    #                 file.write(source)
    #             print('СКАЧАН CATALOG.HTML')
    #         return True
    #
    #     # print(f'{os.path.dirname(__file__)}/catalog/{dir_name}/{file_name}.html', '--- ПРОВЕРКА КОРРЕКТНОСТИ НАЗВАНИЯ ФАЙЛА')
    #     if not os.path.exists(f'{os.path.dirname(__file__)}/catalog/{dir_name}/{file_name}.html'):
    #         try:
    #             with open(f'{os.path.dirname(__file__)}/catalog/{dir_name}/{file_name}.html', 'w', encoding='utf-8') as file:
    #                 file.write(source)
    #             print(f'СКАЧАН  НОВЫЙ {file_name}.html в {dir_name}')
    #         except Exception:
    #             print('ПОХОДУ НЕ СИСТЕМНАЯ ОШИБКА')
    #     return True

    def __set_up(self):
        print('ЗАШЛИ В SETUP')
        self.driver = uc.Chrome(version_main=self.browser)


    def __get_target_list_online(self, source):
        with open(source, 'r') as file:
            page = file.read()

        soup = BeautifulSoup(page, 'lxml')

        category_name = [elem for elem in soup.find_all(itemprop="item")][-1].text
        device_full_name = soup.find(class_ ="offer_title").text
        price = soup.find(class_="offer_price").text
        online_big_img_links = []

        gallery_preview_rows = soup.find_all(class_="gallery_preview_wrap lightgallery_item")
        for elem in gallery_preview_rows:
            online_big_img_links.append(f'https://kdmarket.ru{elem.find("img").get("src")}')
        online_big_img_links.append(f'https://kdmarket.ru{soup.find(class_="gallery_main").find("img").get("src")}')
        desc = ''
        try:
            for elem in soup.find(class_="offer_desc_wrap").find_all('span'):
                if elem.text:
                    desc += f'{elem.text}'
        except Exception:
            print('Нет описания или ошибка в коде')

        props = [[], []]
        # props_block = self.driver.find_element(By.CSS_SELECTOR, '[class="offer_info offer_specs"]')
        try:
            props_row_blocks = soup.find_all(class_="offer_prop_row")

            for block in props_row_blocks:
                header_name = block.find(class_="offer_prop_name").text.upper()

                try:
                    value_list_blocks = block.find_all(class_="offer_prop_value_row")
                    for values_row in value_list_blocks:
                        try:
                            rvalue = values_row.find(class_="offer_prop_value").text
                            lvalue = values_row.find(class_="offer_prop_desc").text

                            if header_name in props[0]:
                                header_index = props[0].index(header_name)
                                props[1][header_index].append(f'{lvalue}: {rvalue}')
                            else:
                                props[0].append(header_name)
                                props[1].append([f'{lvalue}: {rvalue}'])

                        except Exception:
                            lvalue = values_row.find(class_="offer_prop_desc").text

                            if header_name in props[0]:
                                header_index = props[0].index(header_name)
                                props[1][header_index].append(f'{lvalue}')
                            else:
                                props[0].append(header_name)
                                props[1].append([f'{lvalue}'])

                except Exception:
                    value_ = soup.find_all(class_="offer_prop_value").text

                    if header_name in props[0]:
                        header_index = props[0].index(header_name)
                        props[1][header_index].append(f'{value_}')
                    else:
                        props[0].append(header_name)
                        props[1].append([f'{value_}'])


        except Exception:
            print('НЕТ СПЕЦИФИКАЦИИ')

        print('ВЫХОД - ИЗ  __get_target_list_online')

        return category_name, device_full_name, price, online_big_img_links, desc, props




    @staticmethod
    def __get_target_offline(file_link, tag_value='', dir_preview=''):
        # print(dir_preview)
        # print('НАЧИНАЕМ ПАРСИТЬ ОФЛАЙН')
        """ input tuple with link to offline page and tag element for find """
        url = 'https://kdmarket.ru'

        with open(file_link, 'r') as file:
            page = file.read()

        soup = BeautifulSoup(page, 'lxml')
        items_list = soup.find_all(class_=tag_value)

        section_data = []

        category_name = []
        category_link = []
        subcategory_name = []
        item_title = []
        item_page_link = []
        preview_img_link = []
        preview_local_link = []
        price = []
        temp_link = None
        for item in items_list:
            try:
                temp_link = item.find(class_="catalog_section_title").get('href')

                text = re.search(re.compile(r">([A-ZА-Я-]+\s?)+<"), str(item))[0].strip('><')
            except Exception:
                continue

            if temp_link and temp_link.strip('/').split('/')[1] != 'undefined':     # работа с global_category
                category_name.append(text)
                category_link.append(f'{os.path.dirname(__file__)}{temp_link}')
            else:                                                                   # работа с subcategory
                inner_item_list = item.find_all(class_="offer offer_shadow active")
                for inner_item in inner_item_list:

                    subcategory_name.append(text)
                    item_title.append(inner_item.find(class_="offer_name").text)
                    item_page_link.append(f"{url}{inner_item.find(class_='offer_link').get('href')}")
                    preview_img_link.append(f"{url}{inner_item.find(class_='offer_img').get('src')}")
                    price.append(inner_item.find(class_="offer_price").text)
                    preview_local_link.append(f'.{dir_preview}/{inner_item.find(class_="offer_img").get("src").split("/")[-1]}')

        if temp_link and temp_link.strip('/').split('/')[1] != 'undefined':
            section_data.append(category_name)
            section_data.append(category_link)
        else:
            section_data.append(['subcategory_name', 'item_title', 'item_page_link', 'preview_img_link', 'price', 'preview_local_link'])
            section_data.append([subcategory_name, item_title, item_page_link, preview_img_link, price, preview_local_link])
        return section_data

    # def __pars_card(self, link):
    #     print('ВХОД В __PARS_CARD')
    #     # print(link)
    #
    #     self.driver.get(link)
    #     return [elem.get_attribute('href') for elem in self.driver.find_elements(By.CSS_SELECTOR, '[class*="offer_color_item"]')]

    def main(self):
        category_name = []
        category_link = []
        sub_category_name = []
        # self.__set_up()
        # self.__make_dirs(self.url.strip('/').split('/')[-1])
        # page_source = self.__get_url(self.url)
        # self.__download_html(self.driver.page_source, dir_name=f'{os.path.dirname(__file__)}/catalog/', file_name='catalog.html')
        # print('ЗАКРЫВАЮ БРАУЗЕР')
        # target_dict = self.__get_target_offline(f'{os.path.dirname(__file__)}/catalog/catalog.html', tag_value="catalog_section")
        # for item in target_dict.items():
        #     print(item, 'ПРОХОД FOR')
        #     category_name.append(item[0])
        #     print(f'category_name.append: {item[0]}')
        #     category_link.append(item[1][0])
        #     print(f'category_link.append: {item[1][0]}')
        #     sub_category_name.append(item[1][1].strip('/').split('/')[1])
        #     print(f"ub_category_name.append: {item[1][1].strip('/').split('/')[1]}")
        #     self.__get_url(file_name=f'{item[1][1].strip("/").split("/")[1]}', dir_name=f'{item[1][1].strip("/").split("/")[1]}', link=f'{item[1][0]}')
        #
        # self.__make_csv('global_categories', [['Название категории', 'Ссылка на категорию'], [category_name, category_link]])
        # print(sub_category_name)
        # count = 0
        for index, (address, dirs, files) in enumerate(os.walk(os.path.dirname(__file__)+'/catalog')):
            print(address, dirs, files)
            if not dirs: ...
                # self.__make_dirs(f'{files[0].split(".")[0]}_img_preview', address)
                # data_list = self.__get_target_offline(f'{address}/{files[0]}', tag_value="catalog_section", dir_preview=f'{files[0].split(".")[0]}_img_preview')
                # self.__download_img(data_list[1][3], f'{address}/{files[0].split(".")[0]}_img_preview')
                # self.__make_csv(files[0].split('.')[0], address, data_list)

            if index:
                # self.__make_dirs(f'{files[0].split(".")[0]}_img_full', f'{address}')

                with open(f'{address}/{files[0].split(".")[0]}.csv', 'r') as file:
                    content_list = file.read().split('\n')[1:]
                    self.__set_up()
                    section_data = []
                    headers_list = ['CATEGORY', 'FULL TITLE', 'PRICE', 'DEVICE CARD LINK', 'ONLINE IMAGE LINKS', 'OFFLINE IMAGE LINKS', 'DESCRIPTIONS']
                    # headers_list расширяемый список заголовками пришедшими из PROPS

                    category_names, device_full_name, price, device_card_link, online_big_img_links, offline_big_img_links, descriptions = [], [], [], [], [], [], []
                    flag = True
                    for row in content_list:
                        self.make_dirs(f'{row.split(",")[0]}', f'{address}')
                        self.make_csv(f'result_{row.split(",")[0]}', f'{address}/{row.split(",")[0]}')
                        self.make_dirs(f'{row.split(",")[0]}_IMAGE', f'{address}/{row.split(",")[0]}')

                        color_links = self.pars_card(row.split(',')[2])
                        for link in color_links:
                            device_card_link.append(link)
                            self.download_html(self.get_url(link), f'{files[0].split(".")[0]}/{row.split(",")[0]}', f'{link.split("/")[-1]}')
                            data_tuple = self.__get_target_list_online(f'{address}/{row.split(",")[0]}/{link.split("/")[-1]}.html')
                            category_names.append(data_tuple[0])
                            device_full_name.append(data_tuple[1])
                            price.append(data_tuple[2])
                            online_big_img_links.extend(data_tuple[3])
                            self.download_img(data_tuple[3], f'{address}/{row.split(",")[0]}/{row.split(",")[0]}_IMAGE')
                            offline_big_img_links.extend([f".{row.split(',')[0]}_IMAGE/{link.split('/')[-1]}" for link in data_tuple[3]])
                            descriptions.append(data_tuple[4])
                            if flag:
                                headers_list.extend(data_tuple[5][0])
                            section_data.extend([category_names, device_full_name, price, device_card_link, online_big_img_links, offline_big_img_links, descriptions])
                            section_data.extend(data_tuple[5][1])
                            # print(len(headers_list) == len(section_data), len(headers_list), len(section_data))
                            # self.__make_csv(f'result_{row.split(",")[0]}', f'{address}/{row.split(",")[0]}', section_data)  #  , flag='w+'
                            with open(f'{address}/{row.split(",")[0]}/result_{row.split(",")[0]}.csv', 'a') as f:
                                writer = csv.writer(f, delimiter=',')
                                print('пишем')
                                if flag:
                                    writer.writerow(headers_list)
                                    flag = False
                                writer.writerow(section_data)
                                print('записали')
                            category_names, device_full_name, price, device_card_link = [], [], [], []
                            online_big_img_links, offline_big_img_links, descriptions = [], [], []
                            section_data = []
                            headers_list = ['CATEGORY', 'FULL TITLE', 'PRICE', 'DEVICE CARD LINK', 'ONLINE IMAGE LINKS', 'OFFLINE IMAGE LINKS', 'DESCRIPTIONS']

                break


if __name__ == '__main__':

    kd = DynamicParser('https://kdmarket.ru/catalog/')
    kd.main()
