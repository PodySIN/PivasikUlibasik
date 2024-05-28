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
from main.Utility import get_base_context
from main.forms import RegistrationForm, LoginForm
from main.models import Users


def index_page(request: WSGIRequest) -> HttpResponse:
    """
    Главная страница сайта
    """
    context: dict = get_base_context("ПивасикУлыбасик")

    return render(request, "pages/index.html", context)


def registration_page(request: WSGIRequest) -> HttpResponse:
    """
    Страница регистрации на сайте
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
    Страница входа пользователя
    """
    context = get_base_context("Login")
    context["form"] = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
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
    Выход пользователя
    """
    django_logout(request)
    messages.add_message(request, messages.INFO, "Вы успешно вышли из аккаунта")
    return redirect("/")


def catalog_page(request:WSGIRequest) -> HttpResponse:
    context: dict = get_base_context("Каталог")
    return render(request,"pages/catalog.html",context)

def profile(request: WSGIRequest) -> HttpResponse:
    """
    Страница профиля пользователя
    """
    context = get_base_context("Профиль")

    return render(request, "pages/profile.html", context)
