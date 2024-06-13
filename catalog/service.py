"""
Сервис, который обрабатывает информацию из базы данных.
"""

from math import ceil
from catalog.models import Goods, Shop, Beer, Discounts
from main.service import get_all_objects_from_db, get_object_from_db
from users.models import Feedback
from main.configure import configure_logging

logger = configure_logging()


def change_beers_mark(particular_beer):
    """
    Функция, которая изменяет в бд оценку пива по отзывам пользователя.
    :param particular_beer: Конкретное пиво, на которое перешел пользователь
    :return: Ничего не возвращает, а сохраняет изменения в бд
    """
    logger.info("Изменяем оценку пива.")
    all_feedbacks = get_all_objects_from_db(Feedback)
    middle_mark: int = 0
    for i in range(len(all_feedbacks)):
        middle_mark += all_feedbacks[i].Mark
    middle_mark: int = round(middle_mark / len(all_feedbacks))
    logger.info(f"Получили оценку пива: {particular_beer.id} = {middle_mark}.")
    particular_beer.Mark = middle_mark
    particular_beer.save()
    logger.info(f"Сохранили изменения в пиве: {particular_beer.id}.")


def get_shops_of_the_current_beer(beer_id: int) -> list:
    """
    Функция, которая возвращает список с магазинами, в которых есть конкретное пиво.
    :param beer_id: id конкретного пива
    :return: возвращает список с магазинами, в которых есть конкретное пиво
    """
    logger.info("Получаем все магазины, в которых есть наше пиво.")
    goods = Goods.objects.filter(Beer_id=beer_id)
    logger.info("Фильтруем все товары по id пива.")
    shops_arr: list = []
    for i in range(len(goods)):
        shops_arr.append(get_object_from_db(Shop, goods[i].Shop_id))
    logger.info("Возвращаем список магазинов, в которых есть наше пиво.")
    return shops_arr


def get_discounts_of_beer(beer_id: int) -> list:
    """
    Функция, которая возвращает словарь с магазинами,
    в которых есть скидка на конкретное пиво
    :param beer_id: id конкретного пива
    :return: возвращает словарь с магазинами,
             в которых есть скидка на конкретное пиво
    """
    shops: list = get_shops_of_the_current_beer(beer_id)
    beer_cost = get_object_from_db(Beer, beer_id).Price
    information_array: list = []
    for i in range(len(shops)):
        filter_discount = Discounts.objects.filter(Shop_id=shops[i].id, Beer_id=beer_id)
        logger.info(f"Получаем все скидки на наше пиво с id: {beer_id}.")
        if filter_discount.exists():
            id_of_shop = filter_discount.values("Shop_id")[0]["Shop_id"]
            address_of_shop = get_object_from_db(Shop, id_of_shop).Address
            Amount = filter_discount.values("Amount")[0]["Amount"] / 100
            Cost = ceil(beer_cost - (beer_cost * Amount))
            information_array.append(
                {"id": id_of_shop, "address": address_of_shop, "cost": Cost}
            )
    logger.info(
        f"Возвращаем словарь с магазинами, в которых есть скидка на конкретное пиво({beer_id})."
    )
    return information_array


def get_Beers_array(shop_id: int) -> list:
    """
    Функция, которая возвращает весь список пива, который есть в магазине.
    :param shop_id: Id магазина, в который мы перешли.
    :return: Весь список пива, который есть в магазине.
    """
    Beers_id_array = Goods.objects.filter(id=shop_id)
    logger.info(f"Фильтруем все товары в магазине: {shop_id}.")
    Beers_array: list = []
    for i in range(len(Beers_id_array)):
        Beers_array.append(
            {
                "id": Beers_id_array[i].Beer_id,
                "Name": get_object_from_db(Beer, Beers_id_array[i].Beer_id).Name,
            }
        )
    logger.info(f"Возвращаем словари с пивом из магазина: {shop_id}.")
    return Beers_array
