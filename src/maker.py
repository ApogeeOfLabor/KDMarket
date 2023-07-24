from src.checking import check_object
import pandas as pd
import asyncio
import aiohttp
import aiofiles
import os


def make_request_headers(*args):
    headers = {
        ''
    }
    return headers


def make_headers():
    main_headers = []


def make_rows(*args, **kwargs):
    ...


def make_csv(name: str, data: list, addr: str = f'{os.path.dirname(__file__)}') -> str:
    res_dict = {}
    for key, value in zip(data[0], data[1]):
        res_dict[key] = value
    res_df = pd.DataFrame(res_dict)

    if not check_object(f'{addr}/{name}.csv'):
        res_df.to_csv(f'{addr}/{name}.csv', index=False)
    return f'{addr}/{name}.csv'


def make_dir(name, addr=f'{os.path.dirname(__file__)}'):
    if not check_object(f'{addr}/{name}'):
        os.mkdir(f'{addr}/{name}')
    return f'{addr}/{name}'


def make_file(file_name, data='', flag='w'):
    with open(file_name, flag) as file:
        file.write(data)


class Downloader:
    def __init__(self, source: list, flag: str, addr: str = None, name: str = None):
        self.source = source
        self.addr = addr
        self.name = name
        self.flag = flag
        self.__download_files()

    @staticmethod
    async def __downloader(self, session, link=None):
        print('вход в __downloader')
        if self.name:
            self.name = f'{self.name}_{link.strip("/").split("/")[-1]}'
        else:
            self.name = f'{link.strip("/").split("/")[-1]}'
        async with session.get(link) as res:
            print('сессия  в __downloader открыта')

            if not check_object(f'{self.addr}/{self.name}'):
                async with aiofiles.open(f'{self.addr}/{self.name}', self.flag) as file:
                    await file.write(await res.read())

    async def __download_files(self):
        print('вход в __download_files')
        tasks = []
        async with aiohttp.ClientSession() as session:
            print('сессия открыта ---- ')
            for link in self.source:
                print('- цикл запущен -')
                task = await asyncio.create_task(self.__downloader(self, session, link))
                tasks.append(task)
                print('задания добавлены')
            print('начинаю исполнять задания в asyncio.gather')
            await asyncio.gather(*tasks)



