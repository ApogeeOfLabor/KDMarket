import re
from selenium import webdriver
import undetected_chromedriver as uc

# option = webdriver.FirefoxOptions()
# option.set_preference('dom.webdriver.enabled', False)
# option.set_preference('dom.webnotifications.enabled', False)
# option.set_preference('media.volume_scale', '0.0')
#
# options = webdriver.ChromeOptions()
# options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0")
# options.add_argument("--disable-blink-features=AutomationControlled")
#
# service = Service(executable_path='/home/vksource/KDMarket/chromedriver/chromedriver')
#

def set_up() -> uc.Chrome:
    return uc.Chrome()

# os.environ()
URL = 'https://kdmarket.ru'
START_URL = 'https://kdmarket.ru/catalog'

CATALOG_CATEGORY_PATTERN = re.compile(r'([A-ZА-Я-]+\s?)+')
# CATEGORY_NAME = re.compile(r'>([A-ZА-Я-]+\s?)+<')
