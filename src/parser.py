from src import checking, getter


def pars_color(driver):
    print("вход в parser")
    device_title: str = getter.get_elements(source=driver, cls='[class="offer_title"]', text=True)
    price: str = getter.get_elements(source=driver, cls='[class="offer_price"]', text=True)
    card_link: str = getter.get_elements(source=getter.get_elements(source=driver, cls='[class="offer_color_item"]'), attr='href')

    list_gallery_blocks = getter.get_elements(source=driver, cls='[class="gallery_preview_wrap lightgallery_item"]', finds=True)
    list_image_blocks = [getter.get_elements(source=block, tag='img') for block in list_gallery_blocks]
    list_image_links = ', '.join([getter.get_elements(source=item, attr='src') for item in list_image_blocks])

    # СКАЧИВАНИЕ ФОТО ---

    print(' начинаю проверку наличия кнопок меню ')
    if checking.check_class_name(source=driver, cls='[class="offer_menu"]'):
        print(' проверка пройдена, получаю елементы кнопок ')

        submenu = getter.get_elements(source=driver, cls='[class="offer_menu"]')
        submenu_buttons = getter.get_elements(source=submenu, tag='p', finds=True)
        title_buttons = [getter.get_elements(source=button, tag='span', text=True) for button in submenu_buttons]
        # получаем кнопки, если они есть

        # надо как-то реализовать проверку какая именно кнопка есть если одна или определить каким именам кнопок соответствуют индексы
        # и возможно по индексам перенаправлять ветки description и props

        if len(submenu_buttons) == 2:
            submenu_buttons[0].click()
            description = [title_buttons[0], getter.get_description(source=driver, cls='[class="offer_desc_wrap"]')]
            submenu_buttons[1].click()
            props = getter.get_props(source=driver)
            return description, props


        else:
            if title_buttons[0] == 'Описание':
                description = [title_buttons[0], getter.get_description(source=driver, cls='[class="offer_desc_wrap"]')]
                return description
            if title_buttons[0] == 'Характеристики':
                props = getter.get_props(source=driver)
                return props
