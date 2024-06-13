"""
Модуль отвечающий за отображение страниц (users).
"""

from django.contrib.auth import (
    logout as django_logout,
)
from django.contrib.auth.decorators import login_required

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from main.service import (
    get_base_context,
    filter_objects_from_db,
)
from users.form_saver import user_registration, user_login
from users.forms import RegistrationForm, LoginForm
from users.models import Feedback
from main.configure import configure_logging

logger = configure_logging()


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
    return render(request, "users/templates/pages/registration.html", context)


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
    return render(request, "users/templates/pages/login.html", context)


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
    context["feedback"]: dict = int(
        str(
            len(filter_objects_from_db(Feedback.objects, Username=request.user.username))
        )[-1]
    )
    logger.info("Рендерим страницу профиля страницу каталога.")
    return render(request, "users/templates/pages/profile.html", context)
