from src import checking, getter


def pars_color(driver):

    print("вход в parser")
    device_title: str = getter.get_elements(source=driver, cls='[class="offer_title"]', text=True)
    price: str = getter.get_elements(source=driver, cls='[class="offer_price"]', text=True)
    card_link: str = getter.get_elements(source=getter.get_elements(source=driver, cls='[class="offer_color_item"]'), attr='href')

    list_gallery_blocks = getter.get_elements(source=driver, cls='[class="gallery_preview_wrap lightgallery_item"]', finds=True)
    list_image_blocks = [getter.get_elements(source=block, tag='img') for block in list_gallery_blocks]
    online_image_links: str = ', '.join([getter.get_elements(source=item, attr='src') for item in list_image_blocks])

    # СКАЧИВАНИЕ ФОТО ---
    # ПОЛУЧАЕМ СТРОКОЙ - СПИСОК ОФФЛАЙН ССЫЛОК НА КАРТИНКИ
    # offline_image_links

    print(' начинаю проверку наличия кнопок меню ')
    if checking.check_class_name(source=driver, cls='[class="offer_menu"]'):
        print(' проверка пройдена, получаю елементы кнопок ')

        submenu = getter.get_elements(source=driver, cls='[class="offer_menu"]')
        submenu_buttons = getter.get_elements(source=submenu, tag='p', finds=True)
        title_buttons: list = [getter.get_elements(source=button, tag='span', text=True) for button in submenu_buttons]
        # получаем кнопки, если они есть

        if len(submenu_buttons) == 2:
            submenu_buttons[0].click()
            description = getter.get_description(source=driver, cls='[class="offer_desc_wrap"]')
            # ОПИСАНИЕ ДОЛЖНО ВЕРНУТСЯ СРОКОЙ

            submenu_buttons[1].click()
            props = getter.get_props(source=driver)
            # PROPS ДОЛЖЕН ВЕРНУТСЯ СПИСКОМ С ДВУМЯ СПИСКАМИ ['СТРОКИ ЗАГОЛОВКОВ', 'СТРОКИ ЗНАЧЕНИЙ']

            return [device_title, price, card_link, online_image_links, offline_image_links, description, props]


        else:
            if title_buttons[0] == 'Описание':
                description = getter.get_description(source=driver, cls='[class="offer_desc_wrap"]')
                return [device_title, price, card_link, online_image_links, offline_image_links, description]
            if title_buttons[0] == 'Характеристики':
                props = getter.get_props(source=driver)
                return [device_title, price, card_link, online_image_links, offline_image_links, ' ', props]
