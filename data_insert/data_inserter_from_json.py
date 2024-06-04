"""
Модуль, который вставляет данные из json файла в таблицу в бд.
"""

import json


def insert_data_from_json(json_file, model):
    """
    Функция, которая вставляет данные из json файла в таблицу в бд.
    :param json_file: Принимает json file, который надо вставить в таблицу.
    :param model: Принимает модель, в которую надо вставить файл.
    :return: Таблицу, в которую вставили json.
    """
    with open(json_file) as file:
        data = json.load(file)
        for obj in data:
            model.objects.create(**obj)
