"""
Модуль отвечающий за отображение страниц
"""

from django.contrib.auth import (
    login as django_login,
    authenticate,
    logout as django_logout,
)

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from main.Utility import (
    get_base_context,
    change_beers_mark,
    get_shops_of_the_current_beer,
    get_discounts_of_beer,
)
from main.forms import RegistrationForm, LoginForm, Feedback_Form
from main.models import Users, Beer, Feedback, Shop


def index_page(request: WSGIRequest) -> HttpResponse:
    """
    Главная страница сайта
    :param request: запрос к странице
    :return: главную страницу
    """
    context: dict = get_base_context("ПивасикУлыбасик")

    return render(request, "pages/index.html", context)


def registration_page(request: WSGIRequest) -> HttpResponse:
    """
    Страница регистрации пользователя в систему
    :param request: запрос к странице
    :return: страницу регистрации пользователя
    """
    context: dict = get_base_context("Регистрация")
    context["RegistrationForm"] = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            password = form.data.get("Password")
            password_repeat = form.data.get("RepeatPassword")
            if password == password_repeat:
                username = form.data.get("Username")
                if Users.objects.filter(username=username).exists():
                    messages.info(request, "Пользователь с вашим именем уже существует!!!!")
                    return redirect("/")
                user = Users(username=username, password=password)
                user.set_password(user.password)
                user.save()
                auth_user = authenticate(request, username=username, password=password)
                if auth_user is not None:
                    django_login(request, user)
                    messages.success(
                        request, f"Привет, {username}, вы успешно зарегистрировались!!"
                    )
                    return redirect("registration")
    return render(request, "pages/registration.html", context)


def login(request: WSGIRequest) -> HttpResponse:
    """
    Страница входа пользователя в систему
    :param request: запрос к странице
    :return: страницу входа пользователя в систему
    """
    context: dict = get_base_context("Login")
    context["form"] = LoginForm()
    if request.method == "POST":
        form: LoginForm = LoginForm(request.POST)
        if form.is_valid():
            username: str = form.cleaned_data["username"]
            password: str = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                django_login(request, user)
                messages.success(request, f"Привет, {username.title()}, с возвращением!!")
                return redirect("/")
            messages.info(request, "Некорректные данные в форме авторизации!")
            return redirect("login")
    return render(request, "pages/login.html", context)


def logout(request: WSGIRequest) -> HttpResponse:
    """
    Выход пользователя из системы
    :param request: запрос к странице
    :return: на главную страницу
    """
    django_logout(request)
    messages.add_message(request, messages.INFO, "Вы успешно вышли из аккаунта")
    return redirect("/")


def catalog_page(request: WSGIRequest) -> HttpResponse:
    """
    Страница всего пива в магазинах
    :param request: запрос к странице
    :return: каталог пива
    """
    context: dict = get_base_context("Каталог")
    context["beers"] = Beer.objects.all()
    return render(request, "pages/catalog.html", context)


def profile_page(request: WSGIRequest) -> HttpResponse:
    """
    Страница отображения профиля пользователя
    :param request: запрос к странице
    :return: страницу профиля пользователя
    """
    context: dict = get_base_context("Профиль")
    context["username"] = request.user.username
    context["bonuses"] = request.user.Bonuses

    return render(request, "pages/profile.html", context)


def particular_beer(request: WSGIRequest, beer_id: int) -> HttpResponse:
    """
    Страница отображения конкретного пива из каталога
    :param request: запрос к странице
    :param beer_id: id конкретного пива, которое мы смотрим
    :return: страницу конкретного пива
    """
    current_beer = Beer.objects.get(id=beer_id)
    context = get_base_context(f"{current_beer.Name}")
    context["beer"] = current_beer
    context["form"] = Feedback_Form()
    context["discounts"] = get_discounts_of_beer(beer_id)
    context["shops"] = get_shops_of_the_current_beer(beer_id)
    context["feedbacks"] = Feedback.objects.filter(Beer_id=beer_id)
    if request.method == "POST":
        form: Feedback_Form = Feedback_Form(request.POST)
        if form.is_valid():
            text: str = form.data.get("Text")
            mark: int = form.data.get("Mark")
            if int(mark) >= 1 and int(mark) <= 5:
                feedback = Feedback(
                    Beer_id=beer_id,
                    Text=text,
                    Mark=mark,
                    Username=request.user.username,
                )
                feedback.save()
                change_beers_mark(current_beer)
            else:
                messages.add_message(request, messages.INFO, "Введите оценку от 1 до 5")
    return render(request, "pages/particular_beer.html", context)


def particular_shop(request: WSGIRequest, shop_id) -> HttpResponse:
    context = get_base_context("Магазины")
    context["shop"] = Shop.objects.get(Shop_id=shop_id)
    return render(request, "pages/particular_shop.html", context)
