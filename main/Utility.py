"""
Модуль, который хранит вспомогательные функции
"""

from math import floor, ceil

from main.models import Feedback, Goods, Shop, Beer, Discounts


def get_base_context(Title: str) -> dict:
    """
    Возвращает словарь с названием страницы
    :param Title: Название страницы
    :return: словарь с названием страницы
    """
    context: dict = {
        "Title": Title,
    }
    return context


def change_beers_mark(particular_beer):
    """
    Функция, которая изменяет в бд оценку пива по отзывам пользователя.
    :param particular_beer: Конкретное пиво, на которое перешел пользователь
    :return: Ничего не возвращает, а сохраняет изменения в бд
    """
    all_feedbacks = Feedback.objects.all()
    middle_mark: int = 0
    for i in range(len(all_feedbacks)):
        middle_mark += all_feedbacks[i].Mark
    middle_mark: int = round(middle_mark / len(all_feedbacks))
    particular_beer.Mark = middle_mark
    particular_beer.save()


def get_shops_of_the_current_beer(beer_id: int) -> list:
    """
    Функция, которая возвращает список с магазинами, в которых есть конкретное пиво.
    :param beer_id: id конкретного пива
    :return: возвращает список с магазинами, в которых есть конкретное пиво
    """
    goods = Goods.objects.filter(Beer_id=beer_id)
    shops_arr: list = []
    for i in range(len(goods)):
        shops_arr.append(Shop.objects.get(Shop_id=goods[i].Shop_id))
    return shops_arr


def get_discounts_of_beer(beer_id: int) -> list[dict]:
    """
    Функция, которая возвращает словарь с магазинами,
    в которых есть скидка на конкретное пиво
    :param beer_id: id конкретного пива
    :return: возвращает словарь с магазинами,
             в которых есть скидка на конкретное пиво
    """
    shops: list = get_shops_of_the_current_beer(beer_id)
    beer_cost = Beer.objects.get(id=beer_id).Price
    information_array: list[dict] = []
    for i in range(len(shops)):
        filter_discount = Discounts.objects.filter(
            Shop_id=shops[i].Shop_id, Beer_id=beer_id
        )
        if filter_discount.exists():
            id_of_shop = filter_discount.values("Shop_id")[0]["Shop_id"]
            address_of_shop = Shop.objects.get(Shop_id=id_of_shop).Address
            Amount = filter_discount.values("Amount")[0]["Amount"] / 100
            Cost = ceil(beer_cost - (beer_cost * Amount))
            information_array.append(
                {"id": id_of_shop, "address": address_of_shop, "cost": Cost}
            )
    return information_array


def get_Beers_array(shop_id: int) -> list[dict]:
    """
    Функция, которая возвращает весь список пива, который есть в магазине.
    :param shop_id: Id магазина, в который мы перешли.
    :return: Весь список пива, который есть в магазине.
    """
    Beers_id_array = Goods.objects.filter(Shop_id=shop_id)
    Beers_array: list[dict] = []
    for i in range(len(Beers_id_array)):
        Beers_array.append(
            {
                "id": Beers_id_array[i].Beer_id,
                "Name": Beer.objects.get(id=Beers_id_array[i].Beer_id).Name,
            }
        )
    return Beers_array
