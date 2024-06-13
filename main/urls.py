from django.urls import path

from main import views

urlpatterns = [
    path("", views.index_page, name="index"),
    path("about_us/", views.about_us_page, name="about_us"),
    path("privacy_policy/", views.privacy_policy_page, name="privacy_policy"),
]
