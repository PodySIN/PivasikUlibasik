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

from main.Utility import change_beers_mark
from main.configure import configure_logging
from main.forms import RegistrationForm, LoginForm, Feedback_Form
from main.models import Users, Feedback
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


def feedback_save(request: WSGIRequest, beer_id: int, current_beer) -> HttpResponse:
    """
    Функция, которая сохраняет отзыв пользователя.
    :param request: Запрос к странице.
    :param beer_id: Id пива, к которому пользователь оставил отзыв.
    :param current_beer: Пиво.
    :return: Сохраненную форму с отзывом.
    """
    logger.info("Получаем запрос с методом POST.")
    form: Feedback_Form = Feedback_Form(request.POST)
    logger.info("Получаем форму отзывов и проверяем её правильность заполнения.")
    if form.is_valid():
        logger.info("Форма заполнена правильно")
        logger.info("Получаем данные из формы...")
        text: str = form.data.get("Text")
        mark: int = form.data.get("Mark")
        logger.info("Данные получены!")
        if int(mark) >= 1 and int(mark) <= 5:
            logger.info("Проверяем на правильность выставленной оценки.")
            feedback = Feedback(
                Beer_id=beer_id,
                Text=text,
                Mark=mark,
                Username=request.user.username,
            )
            feedback.save()
            logger.info("Все хорошо, сохраняем отзыв!")
            change_beers_mark(current_beer)
        else:
            logger.warning("Оценка поставлена некорректно!")
            messages.add_message(request, messages.INFO, "Введите оценку от 1 до 5")
