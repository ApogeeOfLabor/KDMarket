from time import sleep
from src import *
import os


def main():
    root_dir = f'{os.path.dirname(__file__)}'
    catalog_dir_addr = maker.make_dir(config.START_URL.split('/')[-1], addr=root_dir)

    driver = config.set_up()
    getter.get_url(driver, config.START_URL)

    # blocks_with_values = getter.get_elements(source=driver, cls='[class="catalog_section_title"]', finds=True)
    # header_values = [getter.get_text(pattern=config.CATALOG_CATEGORY_PATTERN, row=value.text) for value in blocks_with_values]
    #
    # blocks_with_links = getter.get_elements(source=driver, cls='[class="catalog_section_title"]', finds=True)
    # header_links = [getter.get_elements(source=value, attr='href') for value in blocks_with_links if value.strip('/').split('/')[-1] != 'undefined']
    #
    # catalog_name = f'start_{config.START_URL.split("/")[-1]}'
    # catalog_data = [['КАТЕГОРИЯ', 'ССЫЛКА'], [header_values, header_links]]
    # file_name = maker.make_csv(name=catalog_name, data=catalog_data, addr=catalog_dir_addr)

    content = getter.get_file_content(f'{catalog_dir_addr}/start_{config.START_URL.split("/")[-1]}.csv')
    """ f'{catalog_dir_addr}/start_{const.START_URL.split("/")[-1]}.csv' ----- file_name"""

    for row in content.split('\n')[1:]:  # итерируем данные из CSV со второй строки

        """ ПРИМЕРНО ЗДЕСЬ НУЖНО ЗАПУСКАТЬ НОВУЮ ФУНКЦИЮ ГЛАВНОГО МЕНЕДЖЕРА """
        router.router(driver=driver, row=row, addr=catalog_dir_addr)

        break


if __name__ == '__main__':
    main()






    """ TODO: парсим асинхронно блок с карточками собирая только ссылки на каждый блок отдельно """
    """ TODO: создаём дирректорию для каждой подкатегории к примеру СМАРТФОН Apple """
    """ TODO: заходим в эту дирректорию """
    """ TODO: тут кладём csv_min с сылками именно по этому превью блоку к примеру СМАРТФОН или ПЛАНШЕТ """
    """ TODO: дальше уже заходим в каждую карточку, парсим ссылки по возможным цветам  """
    """ TODO: тут кладём csv_full с сылками уже на каждый дивайс """
    """ TODO: далее на примере одной - двух карточках с каждой категории строим итоговый шаблон списков с данными """
    """ TODO: в итоге разные блоки-категории парсим в несколько ядер(браузеров) через proxy асинхронно """
    """ TODO: структура каталогов в YAML.config """
    """ TODO: structure_tree.yaml
    catalog   - ТЕХНИКА APPLE         - СМАРТФОН      - file.csv
                        - file.csv                              - /image/*.jpg
                                                - ПЛАНШЕТ
                                                - НАУШНИКИ
                                                - НОУТБУК
                                                - МОНОБЛОК
                                                - и т.д.
                        - МОБИЛЬНЫЕ ТЕЛЕФОНЫ
                        - file.csv

                        - ПЛАНШЕТЫ
                        - file.csv

                        - ИГРОВЫЕ ПРИСТАВКИ
                        - file.csv

                        - ГАДЖЕТЫ
                        - file.csv

                        - ТЕХНИКА XIAOMI
                        - file.csv

                        - ТЕХНИКА DYSON
                        - file.csv

                        - АУДИО
                        - file.csv

                        - ДЛЯ ДОМА
                        - file.csv

                        - КРАСОТА И ЗДОРОВЬЕ
                        - file.csv

                        - ДЛЯ КУХНИ
                        - file.csv

    """
    """ TODO: подумать возможно ли реализовать движение мышкой - аналог реального человека """



    # driver = config.set_up()
    # try:
    #     getter.get_url(driver, link='https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html')
    #     # getter.get_url(driver, link='')
    #     sleep(10)
    # except Exception as ex:
    #     print(ex)
    # finally:
    #     driver.close()
    #     driver.quit()



