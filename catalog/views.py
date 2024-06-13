"""
Модуль отвечающий за отображение страниц (catalog).
"""

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from catalog.service import (
    get_shops_of_the_current_beer,
    get_discounts_of_beer,
    get_Beers_array,
    get_object_from_db,
    get_all_objects_from_db,
)
from main.service import (
    filter_objects_from_db,
    get_base_context,
)
from catalog.form_saver import feedback_save
from catalog.forms import Feedback_Form
from catalog.models import Beer, Shop
from users.models import Feedback
from main.configure import configure_logging

logger = configure_logging()


def catalog_page(request: WSGIRequest) -> HttpResponse:
    """
    Страница всего пива в магазинах.
    :param request: запрос к странице.
    :return: каталог пива.
    """
    logger.info("Переходим на страницу каталога.")
    context: dict = get_base_context("ПивасикУлыбасик")
    context["beers"]: dict = get_all_objects_from_db(Beer)
    logger.info("Рендерим страницу каталога.")
    return render(request, "catalog/templates/pages/catalog.html", context)


def particular_beer(request: WSGIRequest, beer_id: int) -> HttpResponse:
    """
    Страница отображения конкретного пива из каталога.
    :param request: запрос к странице.
    :param beer_id: id конкретного пива, которое мы смотрим.
    :return: страницу конкретного пива.
    """
    logger.info(f"Переходим на страницу пива с id: {beer_id}.")
    current_beer = get_object_from_db(Beer, beer_id)
    context: dict = get_base_context("ПивасикУлыбасик")
    context["beer"]: dict = current_beer
    context["form"]: dict = Feedback_Form()
    context["discounts"]: dict = get_discounts_of_beer(beer_id)
    context["shops"]: dict = get_shops_of_the_current_beer(beer_id)
    logger.info(f"Получаем все отзывы для пива с id: {beer_id}.")
    context["feedbacks"]: dict = filter_objects_from_db(Feedback.objects, Beer_id=beer_id)
    if request.method == "POST":
        feedback_save(request, beer_id, current_beer)
    logger.info(f"По запросу с методом GET возвращаем страницу пива с id: {beer_id}.")
    return render(request, "catalog/templates/pages/particular_beer.html", context)


def particular_shop(request: WSGIRequest, shop_id: int) -> HttpResponse:
    """
    Страница отображения конкретного магазина, в котором продается пиво пользователя.
    :param request: Запрос к странице.
    :param shop_id: Id конкретного магазина, который мы смотрим.
    :return: страницу конкретного магазина.
    """
    logger.info(f"Переходим на станицу магазина с id: {shop_id}.")
    context: dict = get_base_context("ПивасикУлыбасик")
    context["shop"]: dict = get_object_from_db(Shop, shop_id)
    context["beers"]: dict = get_Beers_array(shop_id)
    context["shop_id"]: dict = shop_id
    logger.info(f"Рендерим страницу магазина с id: {shop_id}.")
    return render(request, "catalog/templates/pages/particular_shop.html", context)


def vacancy_page(request: WSGIRequest) -> HttpResponse:
    """
    Страница отображения всех магазинов, в которых нужен работник.
    :param request: Запрос к странице.
    :return: Страницу со всеми вакансиями из магазинов.
    """
    logger.info("Переходим на страницу со всеми вакансиями.")
    context: dict = get_base_context("ПивасикУлыбасик")
    context["shops"]: dict = filter_objects_from_db(Shop.objects, Job__gte=1, Job__lte=2)
    logger.info("Рендерим страницу со всеми вакансиями.")
    return render(request, "catalog/templates/pages/vacancy.html", context)


def particular_vacancy_need_shop(request: WSGIRequest, shop_id: int) -> HttpResponse:
    """
    Страница отображения вакансии, которая приглянулась пользователю.
    :param request: Запрос к странице.
    :param shop_id: Id конкретного магазина, который мы смотрим.
    :return: Страницу вакансии.
    """
    logger.info(f"Страница магазина с id: {shop_id}, в котором нужны работники.")
    context: dict = get_base_context("ПивасикУлыбасик")
    context["vacancy"]: dict = get_object_from_db(Shop, shop_id).Job
    context["shop"]: dict = get_object_from_db(Shop, shop_id)
    context["shop_id"]: dict = shop_id
    logger.info(f"Рендерим страницу с вакансией в магазин с id: {shop_id}.")
    return render(request, "catalog/templates/pages/particular_vacancy.html", context)


def shop_catalog_page(request: WSGIRequest) -> HttpResponse:
    """
    Страница отображения все магазины.
    :param request: Запрос к странице.
    :return: Страницу всех магазинов.
    """
    logger.info("Переходим на страницу со всеми магазинами.")
    context: dict = get_base_context("ПивасикУлыбасик")
    context["shops"]: dict = get_all_objects_from_db(Shop)
    logger.info("Рендерим страницу со всеми магазинами.")
    return render(request, "catalog/templates/pages/shops_catalog.html", context)
