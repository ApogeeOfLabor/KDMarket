from checking import detection
import requests
import multiprocessing


def get_url(driver, link):
    driver.get(link)
    return driver.page_source


def get_img(file, links_list):
    headers = {
        'Accept': '*/*',
        # "user-agent": UserAgent().random
    }

    for link in links_list:
        if not detection(f'{file}'):
            responce = requests.get(link, headers=headers)

            with open(f'{file}', 'flag') as file:
                file.write(responce.content)


def download_html(source, dir_name='catalog', file_name='catalog'):
    print('НАЧИНАЮ СКАЧИВАНИЕ HTML')
    """ source = self.driver.page_source """

    if dir_name == 'catalog' and file_name == 'catalog':
        if not os.path.exists(f'{os.path.dirname(__file__)}/catalog/catalog.html'):
            with open(f'{os.path.dirname(__file__)}/catalog/catalog.html', 'w', encoding='utf-8') as file:
                file.write(source)
            print('СКАЧАН CATALOG.HTML')
        return True

    # print(f'{os.path.dirname(__file__)}/catalog/{dir_name}/{file_name}.html', '--- ПРОВЕРКА КОРРЕКТНОСТИ НАЗВАНИЯ ФАЙЛА')
    if not detection(f'{file_path}.html'):
        try:
            with open(f'{os.path.dirname(__file__)}/catalog/{dir_name}/{file_name}.html', 'w', encoding='utf-8') as file:
                file.write(source)
            print(f'СКАЧАН  НОВЫЙ {file_name}.html в {dir_name}')
        except Exception:
            print('ПОХОДУ НЕ СИСТЕМНАЯ ОШИБКА')
    return True
