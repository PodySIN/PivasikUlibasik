"""
Модуль отвечающий за отображение страниц
"""

from django.contrib.auth import (
    logout as django_logout,
)
from django.contrib.auth.decorators import login_required

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from main.Utility import (
    get_base_context,
    get_shops_of_the_current_beer,
    get_discounts_of_beer,
    get_Beers_array,
    get_object_from_db,
    get_all_objects_from_db,
)
from main.form_saver import user_registration, user_login, feedback_save
from main.forms import RegistrationForm, LoginForm, Feedback_Form
from main.models import Beer, Feedback, Shop
from main.configure import configure_logging

logger = configure_logging()


def index_page(request: WSGIRequest) -> HttpResponse:
    """
    Главная страница сайта
    :param request: запрос к странице
    :return: главную страницу
    """
    logger.info("Вход на главную страницу.")
    context: dict = get_base_context("ПивасикУлыбасик")
    logger.info("Данные получены, рендерим главную страницу.")
    return render(request, "pages/index.html", context)


def registration_page(request: WSGIRequest) -> HttpResponse:
    """
    Страница регистрации пользователя в систему.
    :param request: запрос к странице.
    :return: страницу регистрации пользователя.
    """
    logger.info("Вход на страницу регистрации.")
    context: dict = get_base_context("ПивасикУлыбасик")
    context["RegistrationForm"]: dict = RegistrationForm()
    logger.info("Собрали данные из контекста.")
    if request.method == "POST":
        user_registration(request)
    logger.info("По запросу с методом GET рендерим страницу.")
    return render(request, "pages/registration.html", context)


def login(request: WSGIRequest) -> HttpResponse:
    """
    Страница входа пользователя в систему.
    :param request: запрос к странице.
    :return: страницу входа пользователя в систему.
    """
    logger.info("Переходим на страницу входа в систему.")
    context: dict = get_base_context("ПивасикУлыбасик")
    context["form"]: dict = LoginForm()
    logger.info("Получаем данные из context.")
    if request.method == "POST":
        user_login(request)
    logger.info("По запросу с методом GET рендерим страниц.")
    return render(request, "pages/login.html", context)


def logout(request: WSGIRequest) -> HttpResponse:
    """
    Выход пользователя из системы.
    :param request: запрос к странице.
    :return: на главную страницу.
    """
    logger.warning(f"Пользователь с ником: {request.user.username} выходит из системы!")
    django_logout(request)
    messages.add_message(request, messages.INFO, "Вы успешно вышли из аккаунта")
    return redirect("/")


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
    return render(request, "pages/catalog.html", context)


@login_required
def profile_page(request: WSGIRequest) -> HttpResponse:
    """
    Страница отображения профиля пользователя.
    :param request: запрос к странице.
    :return: страницу профиля пользователя.
    """
    logger.info("Переходим на страницу профиля.")
    context: dict = get_base_context("ПивасикУлыбасик")
    context["username"]: dict = request.user.username
    context["bonuses"]: dict = request.user.Bonuses
    logger.info("Получаем количество отзывов, которые написал пользователь.")
    context["feedback"]: dict = int(
        str(len(Feedback.objects.filter(Username=request.user.username)))[-1]
    )
    logger.info("Рендерим страницу профиля страницу каталога.")
    return render(request, "pages/profile.html", context)


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
    context["feedbacks"]: dict = Feedback.objects.filter(Beer_id=beer_id)
    logger.info("Получаем все данные.")
    if request.method == "POST":
        feedback_save(request, beer_id, current_beer)
    logger.info(f"По запросу с методом GET возвращаем страницу пива с id: {beer_id}.")
    return render(request, "pages/particular_beer.html", context)


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
    return render(request, "pages/particular_shop.html", context)


def vacancy_page(request: WSGIRequest) -> HttpResponse:
    """
    Страница отображения всех магазинов, в которых нужен работник.
    :param request: Запрос к странице.
    :return: Страницу со всеми вакансиями из магазинов.
    """
    logger.info("Переходим на страницу со всеми вакансиями.")
    context: dict = get_base_context("ПивасикУлыбасик")
    logger.info("Получаем все вакансии в магазинах.")
    context["shops"]: dict = Shop.objects.filter(Job__gte=1, Job__lte=2)
    logger.info("Рендерим страницу со всеми вакансиями.")
    return render(request, "pages/vacancy.html", context)


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
    return render(request, "pages/particular_vacancy.html", context)


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
    return render(request, "pages/shops_catalog.html", context)


def about_us_page(request: WSGIRequest) -> HttpResponse:
    """
    Страница отображения страницы 'о нас'.
    :param request: Запрос к странице.
    :return: Страницу 'о нас'.
    """
    logger.info("Переходим на страницу о нас.")
    context: dict = get_base_context("ПивасикУлыбасик")
    logger.info("Рендерим страницу о нас.")
    return render(request, "pages/about_us.html", context)


def privacy_policy_page(request: WSGIRequest) -> HttpResponse:
    """
    Страница отображения страницы с политикой конфиденциальности.
    :param request: Запрос к странице.
    :return: Страницу политики конфиденциальности.
    """
    logger.info("Переходим на страниц с политикой конфиденциальности.")
    context: dict = get_base_context("ПивасикУлыбасик")
    logger.info("Рендерим страницу с политикой конфиденциальности.")
    return render(request, "pages/privacy_policy.html", context)
