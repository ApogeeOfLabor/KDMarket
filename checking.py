import os
from selenium.webdriver.common.by import By


def try_except(driver, find='', finds=''):
    try:
        if find:
            return driver.find_element(By.CLASS_NAME, 'find')
        if finds:
            return driver.find_elements(By.CLASS_NAME, 'finds')

    except Exception:
        return None


def detection(file_name):
    if os.path.exists(file_name):
        return True
    return False
