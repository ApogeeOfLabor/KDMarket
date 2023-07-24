from selenium.webdriver.common.by import By
from src import getter, checking
import re


def get_text(pattern, row):
    try:
        return re.search(pattern, row).group(0)
    except Exception:
        return 'ОШИБКА ВХОДНЫХ ДАННЫХ'


def get_url(driver, link):
    driver.get(link)


def get_file_content(file_name: str, flag: str = 'r'):
    if checking.check_object(file_name=file_name):
        with open(file_name, flag) as file:
            return file.read()


def get_elements(source, tag: str = None, cls: str = None, attr: str = None, finds: int = 0, text: int = None):
    if tag:
        if not finds:
            if text:
                return source.find_element(By.TAG_NAME, f'{tag}').text
            return source.find_element(By.TAG_NAME, f'{tag}')
        if text:
            return source.find_elements(By.TAG_NAME, f'{tag}').text
        return source.find_elements(By.TAG_NAME, f'{tag}')
    if cls:
        if not finds:
            if text:
                return source.find_element(By.CSS_SELECTOR, cls).text
            return source.find_element(By.CSS_SELECTOR, cls)
        if text:
            return source.find_elements(By.CSS_SELECTOR, cls).text
        return source.find_elements(By.CSS_SELECTOR, cls)
    if attr:
        return source.get_attribute(attr)


def get_description(source, cls):
    description_block = getter.get_elements(source=source, cls='[class="offer_desc_wrap"]')
    description = ''.join([f'{row}\n' for row in getter.get_elements(source=description_block, tag='span', finds=True, text=True) if row])
    print(description)
    return description


def get_props(source):
    if checking.check_class_name(source=source, cls='[class="scrollbot-inner-parent"]'):
        general_props_block = getter.get_elements(source=source, cls='[class="scrollbot-inner-parent"]')
        if checking.check_class_name(source=general_props_block, cls='[class="offer_prop_row"]'):
            props_blocks = getter.get_elements(source=general_props_block, cls='[class="offer_prop_row"]', finds=True)
            headers = []
            values = []
            for props_item in props_blocks:
                if checking.check_class_name(source=props_item, cls='[class="offer_prop_name"]'):
                    props_header = getter.get_elements(source=props_item, cls='[class="offer_prop_name"]', text=True)
                    if props_header not in headers:
                        headers.extend(props_header)
                if checking.check_class_name(source=props_item, cls='[class*="offer_prop_value"]'):
                    props_value_blocks = getter.get_elements(source=props_item, cls='[class*="offer_prop_value"]', finds=True)
                    result_value = ''
                    if len(props_value_blocks) != 1:
                        for values_block in props_value_blocks:
                            props_value = ': '.join(getter.get_elements(source=values_block, tag='p', finds=True, text=True))
                            result_value += f'{props_value}\n'
                    else:
                        for values_block in props_value_blocks:
                            result_value = values_block.text
                    values.extend(result_value)

            return headers, values if len(headers) == len(values) else 'ДЛИНА СПИСКОВ НА ВЫХОДЕ ИЗ get_props НЕ ОДИНАКОВАЯ'
        return ''
    return ''
