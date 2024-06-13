"""
Модуль отвечающий за отображение страниц (main).
"""

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from main.service import get_base_context
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


def about_us_page(request: WSGIRequest) -> HttpResponse:
    """
    Страница отображения страницы 'о нас'.
    :param request: Запрос к странице.
    :return: Страницу 'о нас'.
    """
    logger.info("Переходим на страницу о нас.")
    context: dict = get_base_context("ПивасикУлыбасик")
    logger.info("Рендерим страницу о нас.")
    return render(request, "main/templates/pages/about_us.html", context)


def privacy_policy_page(request: WSGIRequest) -> HttpResponse:
    """
    Страница отображения страницы с политикой конфиденциальности.
    :param request: Запрос к странице.
    :return: Страницу политики конфиденциальности.
    """
    logger.info("Переходим на страниц с политикой конфиденциальности.")
    context: dict = get_base_context("ПивасикУлыбасик")
    logger.info("Рендерим страницу с политикой конфиденциальности.")
    return render(request, "main/templates/pages/privacy_policy.html", context)
