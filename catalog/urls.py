"""
юрлки (catalog).
"""

from django.urls import path

from catalog import views

urlpatterns = [
    path("catalog/", views.catalog_page, name="catalog"),
    path(
        "catalog/particular_beer/<beer_id>",
        views.particular_beer,
        name="catalog/particular_beer/<beer_id>",
    ),
    path("vacancy/", views.vacancy_page, name="vacancy"),
    path(
        "vacancy/particular_shop_vacancy/<shop_id>",
        views.particular_vacancy_need_shop,
        name="vacancy/particular_shop_vacancy/<shop_id>",
    ),
    path("shop_catalog/", views.shop_catalog_page, name="shop_catalog"),
    path(
        "shop_catalog/particular_shop/<shop_id>",
        views.particular_shop,
        name="shop_catalog/particular_shop/<shop_id>",
    ),
]
