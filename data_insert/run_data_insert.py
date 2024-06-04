"""
Модуль, который вызывает функцию из data_inserter_from_json, благодаря чему
информация из json записывается в таблицу в базе данных.
"""
from data_inserter_from_json import insert_data_from_json
from main.models import Beer, Discounts, Shop, Goods


def main() -> None:
    """
    При запуске функции, json файлы вставляются в таблицы в базе данных.
    :return: Ничего не возвращает.
    """
    print('Начало вставки данных...')
    insert_data_from_json("../jsons/main_beer.json", Beer)
    insert_data_from_json("../jsons/main_discounts.json", Discounts)
    insert_data_from_json("../jsons/main_shop.json", Shop)
    insert_data_from_json("../jsons/main_goods.json", Goods)
    print('Успешно выполнено!')

if __name__ == "__main__":
    main()
