from selenium.webdriver.common.by import By
import os


def no_break(): ...


def check_object(file_name) -> bool:
    return os.path.exists(file_name)


def check_class_name(source, cls: str) -> bool:
    """
    format cls: '[class="some-name-class"]'
    if the class name is included in some css selector: '[class*="some-name-class "]'
    """
    try:
        if source.find_element(By.CSS_SELECTOR, cls):
            return True
    except Exception as ex:
        print(ex)


def check_tag_name(source, tag: str) -> str:
    try:
        if source.find_element(By.TAG_NAME, tag):
            return tag
    except Exception as ex:
        print(ex)
