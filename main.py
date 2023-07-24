import os
from src import maker, config, getter, router


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

    driver.close()
    driver.quit()

    content = getter.get_file_content(f'{catalog_dir_addr}/start_{config.START_URL.split("/")[-1]}.csv')
    """ f'{catalog_dir_addr}/start_{const.START_URL.split("/")[-1]}.csv' ----- file_name"""

    for row in content.split('\n')[1:]:  # итерируем данные из CSV со второй строки

        """ ПРИМЕРНО ЗДЕСЬ НУЖНО ЗАПУСКАТЬ НОВУЮ ФУНКЦИЮ ГЛАВНОГО МЕНЕДЖЕРА """
        router.router(driver=driver, row=row, addr=catalog_dir_addr)

        break


if __name__ == '__main__':
    main()

    """ TODO: далее на примере одной - двух карточках с каждой категории строим итоговый шаблон списков с данными """
    """ TODO: в итоге разные блоки-категории парсим в несколько ядер(браузеров) через proxy асинхронно """
    """ TODO: структура каталогов в YAML.config """
    """ TODO: structure_tree.yaml
    catalog   - ТЕХНИКА APPLE                   - СМАРТФОН      - file.csv
                                                                - /image/*.jpg
                                                                - /SUBCATEGORY-NAME_preview/*.jpg
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
                        и т.д.
    """
    """ TODO: подумать возможно ли реализовать движение мышкой - аналог реального человека """
