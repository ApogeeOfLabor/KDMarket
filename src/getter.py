from selenium.webdriver.common.by import By
import src
import re


def get_text(pattern, row) -> str:
    try:
        return re.search(pattern, row).group(0)
    except Exception:
        return 'ОШИБКА ВХОДНЫХ ДАННЫХ'


def get_url(driver, link):
    driver.get(link)


def get_file_content(file_name: str, flag: str = 'r'):
    if src.checking.check_object(file_name=file_name):
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


def get_description(source, cls) -> str:
    description_block = src.getter.get_elements(source=source, cls='[class="offer_desc_wrap"]')
    return ''.join([f'{row}\n' for row in src.getter.get_elements(source=description_block, tag='span', finds=True, text=True) if row])


def get_props(source) -> list:
    if src.checking.check_class_name(source=source, cls='[class="scrollbot-inner-parent"]'):
        general_props_block = src.getter.get_elements(source=source, cls='[class="scrollbot-inner-parent"]')
        if src.checking.check_class_name(source=general_props_block, cls='[class="offer_prop_row"]'):
            props_blocks = src.getter.get_elements(source=general_props_block, cls='[class="offer_prop_row"]', finds=True)
            headers = []
            values = []
            for props_item in props_blocks:
                if src.checking.check_class_name(source=props_item, cls='[class="offer_prop_name"]'):
                    props_header = src.getter.get_elements(source=props_item, cls='[class="offer_prop_name"]', text=True)
                    if props_header not in headers:
                        headers.extend(props_header)
                if src.checking.check_class_name(source=props_item, cls='[class*="offer_prop_value"]'):
                    props_value_blocks = src.getter.get_elements(source=props_item, cls='[class*="offer_prop_value"]', finds=True)
                    result_value = ''
                    if len(props_value_blocks) != 1:
                        for values_block in props_value_blocks:
                            props_value = ': '.join(src.getter.get_elements(source=values_block, tag='p', finds=True, text=True))
                            result_value += f'{props_value}\n'
                    else:
                        for values_block in props_value_blocks:
                            result_value = values_block.text
                    values.extend(result_value)

            return [headers, values] if len(headers) == len(values) else 'ДЛИНА СПИСКОВ НА ВЫХОДЕ ИЗ get_props НЕ ОДИНАКОВАЯ'
