from django.urls import path

from users import views

urlpatterns = [
    path("registration/", views.registration_page, name="registration"),
    path("login/", views.login, name="login"),
    path("profile/", views.profile_page, name="profile"),
    path("logout/", views.logout, name="logout"),
]
