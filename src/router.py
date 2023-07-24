from src import getter, maker, config, parser


def router(driver, row, addr):
    print("вход в router")

    category_link = row.split(',')[-1]

    driver = config.set_up()
    getter.get_url(driver, category_link)
    # открытие ссылки apple при первой итерации

    category_dir_name = f'{row.split(",")[-1].strip("/").split("/")[-1]}'
    category_dir_addr = maker.make_dir(name=category_dir_name, addr=addr)
    # создание директории apple

    list_blocks = getter.get_elements(source=driver, cls='[class*="catalog_section "]', finds=True)
    # получаем все блоки из apple типа СМАРТФОН, ПЛАНШЕТ, ЧАСЫ и т.д.

    for block in list_blocks:

        _SUBCATEGORY_HEADERS = ['CATEGORY', 'SUBCATEGORY', 'TITLE', 'PRICE', 'CARD-LINK', 'ONLINE-IMG-LINKS', 'OFFLINE-IMG-LINKS', 'DESCRIPTION']
        _SUBCATEGORY_VALUES = [[] for _ in range(len(_SUBCATEGORY_HEADERS))]

        raw_title_row = getter.get_elements(source=block, cls='[class="catalog_section_title"]', text=True)
        subcategory_name = getter.get_text(pattern=config.CATALOG_CATEGORY_PATTERN, row=raw_title_row)
        # на каждой итерации получаем имя подкатегории тпиа СМАРТФОН

        subcategory_addr = maker.make_dir(subcategory_name, addr=category_dir_addr)
        # создаём директорию по имени подкатергории к примеру СМАРТФОН

        preview_dir_name = f'{subcategory_name}_preview'
        preview_address = maker.make_dir(name=preview_dir_name, addr=subcategory_addr)
        # создаём preview директорию в подкатергории к примеру в СМАРТФОН_preview

        preview_links = [getter.get_elements(source=elem, attr="href") for elem in getter.get_elements(source=block, cls='[class="offer_link"]', finds=True)]
        # maker.Downloader(source=preview_links, flag="wb", addr=preview_address, name='preview')
        # СКАЧИВАЕМ ВСЕ PREVIEW

        image_address = maker.make_dir('image', addr=subcategory_addr)
        # создаём директорию для основных фото

        card_list = getter.get_elements(source=driver, cls='[class="offer offer_shadow"]', finds=True)
        # далее получаем все карточки этого раздела

        for card in card_list:

            card.click()
            print('кликнул по карточке')
            # кликаем на каждую карточку

            colors = getter.get_elements(source=driver, cls='[class*="offer_color_item "]', finds=True)
            # получили все карточки по доступным цветам

            for color in colors:
                # начинаем парсить цвет

                temp_list = [category_dir_name.capitalize(), subcategory_name.capitalize()]
                color.click()

                data_list = parser.pars_color(driver=driver)

                if isinstance(data_list[-1], list):
                    for item in data_list[-1][0]:
                        if item not in _SUBCATEGORY_HEADERS:
                            _SUBCATEGORY_HEADERS.append(item.upper())

                    num = len(_SUBCATEGORY_HEADERS) - len(_SUBCATEGORY_VALUES)
                    if num:
                        _SUBCATEGORY_VALUES.extend([[] for _ in range(num)])
                    temp_list.extend(data_list[:-1])
                    temp_list.extend(data_list[-1][1])
                    if len(_SUBCATEGORY_VALUES) == len(temp_list):
                        for index, value in enumerate(temp_list):
                            _SUBCATEGORY_VALUES[index].append(value)

                else:
                    temp_list.extend(data_list)
                    if len(_SUBCATEGORY_VALUES) == len(temp_list):
                        for index, value in enumerate(temp_list):
                            _SUBCATEGORY_VALUES[index].append(value)

        if len(_SUBCATEGORY_HEADERS) == len(_SUBCATEGORY_VALUES):
            maker.make_csv(name=subcategory_name, data=[_SUBCATEGORY_HEADERS, _SUBCATEGORY_VALUES], addr=subcategory_addr)
        # тут на каждой итерации должен создаваться csv файл в соответствующей директории

        _SUBCATEGORY_HEADERS.clear()
        _SUBCATEGORY_VALUES.clear()

        break

    driver.close()
    driver.quit()
