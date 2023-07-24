from src import getter, maker, config, parser


def router(driver, row, addr):
    print("вход в router")

    category_link = row.split(',')[-1]
    getter.get_url(driver, category_link)
    # открытие ссылки apple при первой итерации

    category_dir_name = f'{row.split(",")[-1].strip("/").split("/")[-1]}'
    category_dir_addr = maker.make_dir(name=category_dir_name, addr=addr)
    # создание директории apple

    """ получаем все блоки -
    и итерируем -
    на каждой итерации получаем имя категории -
    создаём директорию -
    далее получаем все карточки этого раздела и итерируем -
    кликаем на каждую карточку -
    заходим и определяем цифру сколько цветов доступно и собираем это колличество ссылок -
    в цикле кликаем на каждую ссылку и заходим -
    снимаем данные (название, ссылка, описание, заголовки спецификации, значения спецификации) --- все данные должны быть строковыми
    --- стуктуру снятия ПРОДУМАТЬ ---
    """

    list_blocks = getter.get_elements(source=driver, cls='[class*="catalog_section "]', finds=True)
    # получаем все блоки из apple типа СМАРТФОН, ПЛАНШЕТ, ЧАСЫ и т.д.

    for block in list_blocks:

        raw_title_row = getter.get_elements(source=block, cls='[class="catalog_section_title"]', text=True)
        subcategory_name = getter.get_text(pattern=config.CATALOG_CATEGORY_PATTERN, row=raw_title_row)
        # на каждой итерации получаем имя категории тпиа СМАРТФОН

        subcategory_addr = maker.make_dir(subcategory_name, addr=category_dir_addr)
        # создаём директорию по имени подкатергории к примеру СМАРТФОН

        preview_dir_name = f'{subcategory_name}_preview'
        preview_address = maker.make_dir(name=preview_dir_name, addr=subcategory_addr)
        # создаём preview директорию в подкатергории к примеру в СМАРТФОН_preview

        # preview_links = [getter.get_elements(source=elem, attr="href") for elem in getter.get_elements(source=block, cls='[class="offer_link"]', finds=True)]
        # maker.Downloader(source=preview_links, flag="wb", addr=preview_address, name='preview')
        # # СКАЧИВАЕМ ВСЕ PREVIEW

        image_address = maker.make_dir('image', addr=subcategory_addr)
        # создаём директорию для основных фото

        card_list = getter.get_elements(source=driver, cls='[class="offer offer_shadow"]', finds=True)
        # далее получаем все карточки этого раздела

        subcategory_data = []
        subcategory_headers = []
        subcategory_values = []

        for card in card_list:

            card.click()
            print('кликнул по карточке')
            # кликаем на каждую карточку

            colors = getter.get_elements(source=driver, cls='[class*="offer_color_item "]', finds=True)
            # получили все элементы по доступным цветам

            # начинаем парсить карточку
            for color in colors:
                color.click()
                data = parser.pars_color(driver=driver)

                break
            break

        # тут как проходим весь блок к примеру СМАРТФОН создаём файл CSV по этому блоку в соответствующей директории
        maker.make_csv(name=subcategory_name, data=data, addr=subcategory_addr)

        break

