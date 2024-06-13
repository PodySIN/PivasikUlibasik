"""
Модуль отвечающий за сохранение форм.
"""

from django.contrib.auth import (
    login as django_login,
    authenticate,
)
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect

from main.configure import configure_logging
from users.forms import RegistrationForm, LoginForm
from users.models import Users
from django.contrib import messages

logger = configure_logging()


def user_registration(request: WSGIRequest) -> HttpResponse:
    """
    Функция, которая регистрирует нашего пользователя.
    :param request: Запрос к странице от пользователя.
    :return: Зарегистрированного пользователя с сохраненными данными.
    """
    logger.info("Отправлен метод POST")
    form: RegistrationForm = RegistrationForm(request.POST)
    logger.info("Обрабатываем форму.")
    if form.is_valid():
        logger.info("Форма заполнена правильно.")
        password = form.data.get("Password")
        password_repeat = form.data.get("RepeatPassword")
        logger.info("Получаем пароли.")
        if password == password_repeat:
            logger.info("Пароли совпали.")
            username = form.data.get("Username")
            logger.info("Получаем имя пользователя.")
            if Users.objects.filter(username=username).exists():
                logger.error("Пользователь ввел имя уже существующего человека!")
                messages.info(
                    request,
                    "Пользователь с вашим именем уже существует!!!!",
                )
                return redirect("/")
            logger.info("Пользователь ввел корректное имя.")
            user = Users(username=username, password=password)
            logger.info("заполняем данные пользователя.")
            user.set_password(user.password)
            user.save()
            logger.info("Сохраняем пароль и имя.")
            auth_user = authenticate(request, username=username, password=password)
            logger.info("Аутефицируем пользователя...")
            if auth_user is not None:
                logger.info(
                    f"Все хорошо! Производится вход в систему: пользователем {username}."
                )
                django_login(request, user)
                logger.info("Пользователь успешно вошел в систему!")
                messages.success(
                    request,
                    f"Привет, {username}, вы успешно зарегистрировались!!",
                )
                return redirect("registration")


def user_login(request: WSGIRequest) -> HttpResponse:
    """
    Функция, которая производит вход нашего пользователя в систему.
    :param request: Запрос к странице от пользователя.
    :return: Вход пользователя в систему или отказ.
    """
    logger.info("Получили запрос с методом POST.")
    form: LoginForm = LoginForm(request.POST)
    logger.info("Получаем форму и проверяем её на валидность.")
    if form.is_valid():
        logger.info("Форма заполнена правильно.")
        username: str = form.cleaned_data["username"]
        password: str = form.cleaned_data["password"]
        user = authenticate(request, username=username, password=password)
        logger.info("Аутефицируем пользователя.")
        if user is not None:
            logger.info("Пользователь есть в бд.")
            django_login(request, user)
            logger.info(f"Вход прошел успешно для {username}!")
            messages.success(request, f"Привет, {username.title()}, с возвращением!!")
            return redirect("/")
        logger.error(
            f"Пользователь ввел некорректные данные: возможное имя пользователя {username}!"
        )
        messages.info(request, "Некорректные данные в форме авторизации!")
        return redirect("login")
