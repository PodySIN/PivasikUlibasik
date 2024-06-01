"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path

from main import views

urlpatterns = [
    path("", views.index_page, name="index"),
    path("registration/", views.registration_page, name="registration"),
    path("login/", views.login, name="login"),
    path("profile/", views.profile_page, name="profile"),
    path("logout/", views.logout, name="logout"),
    path("catalog/", views.catalog_page, name="catalog"),
    path("particular_beer/<beer_id>", views.particular_beer, name="particular_beer/<beer_id>"),
    path("particular_shop/<shop_id>", views.particular_shop, name="particular_shop/<shop_id>"),
    path("vacancy/", views.vacancy_page, name="vacancy"),
    path(
        "vacancy/particular_shop_vacancy/<shop_id>",
        views.particular_vacancy_need_shop,
        name="vacancy/particular_shop_vacancy/<shop_id>",
    ),
]
