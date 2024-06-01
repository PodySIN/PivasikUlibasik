"""
Модуль содержащий модель базы данных.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    """
    Модель пользователя основанная на AbstractUser,
    а значит в ней есть все поля стандартной модели User
    (Имя, пароль, дата регистрации, последний вход и т.д).
    :param Bonuses: Бонус пользователя
    """

    Bonuses = models.IntegerField(default=0)


class Feedback(models.Model):
    """
    Модель отзывов пользователя о продукте.
    :param Beer_id: id пива
    :param Text: Текст отзыва
    :param Mark: Оценка пива
    :param Username: Ник пользователя, написавшего отзыв
    """

    Beer_id = models.IntegerField(default=0)
    Text = models.CharField(default="", max_length=512)
    Mark = models.IntegerField(default=5)
    Username = models.CharField(default=0, max_length=128)


class Beer(models.Model):
    """
    Модель пива, в ней хранится вся информация, а также ключ
    на модель отзывов.
    :param Name: Название пива
    :param Origin: Место производства
    :param Price: Цена пива
    :param Description: Состав пива
    :param Mark: Оценка пива
    :param Amount: Объём
    :param Strength: Градусы
    :param Image: Изображение
    """

    Name = models.CharField(default="Балтика", max_length=128)
    Image = models.CharField(max_length=128, default="images/beers/baltika_7.jpg")
    Amount = models.FloatField(default=500)
    Strength = models.FloatField(default=9.9)
    Origin = models.CharField(default="Россия", max_length=128)
    Price = models.IntegerField(default=100)
    Description = models.CharField(default="", max_length=512)
    Mark = models.IntegerField(default=5)


class Goods(models.Model):
    """
    :param Shop_id: id магазина
    :param Beer_id: id пива
    """

    Shop_id = models.IntegerField(default=0)
    Beer_id = models.IntegerField(default=0)


class Discounts(models.Model):
    """
    Модель скидок, в ней хранится:
    :param Shop_id: id магазина
    :param Discount: id конкретного пива
    :param Amount: сама скидка
    """

    Shop_id = models.IntegerField(default=0)
    Amount = models.IntegerField(default=0)
    Beer_id = models.IntegerField(default=0)


class Shop(models.Model):
    """
    Модель магазина, в ней хранится информация:
    :param Shop_id: id магазина
    :param Job: нужен ли работник магазину,
    :param Discounts_id: id на талицу со скидками,
    :param Beer_id: id на таблицу с пивом.
    """

    Shop_id = models.IntegerField(primary_key=True, default=1)
    Job = models.IntegerField(default=0)
    Address = models.CharField(default="Бульвар", max_length=256)
