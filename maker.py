import os
import pandas as pd
from checking import detection


def make_headers(*args):
    ...


def make_rows(*args, **kwargs):
    ...


def make_csv(name: str, data: list, addr: str = f'{os.path.dirname(__file__)}', flag: str = 'w'):
    """ data - список с двумя списками равной длины, в первом заголовки, во втором значения строками """
    print('СТАРТ СОЗДАНИЯ CSV')

    res_dict = {}
    for key, value in zip(data[0], data[1]):
        res_dict[key] = value
    res_df = pd.DataFrame(res_dict)

    if not detection(f'{addr}/{name}.csv'):
        res_df.to_csv(f'{addr}/{name}.csv')

        print(f"{name}.CSV СОЗДАН")


def make_dir(name, addr=f'{os.path.dirname(__file__)}'):
    if not detection(f'{addr}/{name}'):
        os.mkdir(f'{addr}/{name}')


def file_read(file_name):
    with open(file_name, 'r') as file:
        return file.read()


def file_write(file_name, data, flag='w'):
    with open(file_name, flag) as file:
        file.write(data)
