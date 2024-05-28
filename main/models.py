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
    """

    Beer_id = models.IntegerField(default=0)
    Text = models.CharField(default="", max_length=512)
    Mark = models.IntegerField(default=5)


class Beer(models.Model):
    """
    Модель пива, в ней хранится вся информация, а также ключ
    на модель отзывов.
    :param Name: Название пива
    :param Origin: Место производства
    :param Price: Цена пива
    :param Description: Состав пива
    :param Id_of_feedback: id на таблицу с отзывами
    :param Mark: Оценка пива
    """

    Name = models.CharField(default="Балтика", max_length=128)
    Amount = models.IntegerField(default=500)
    Strength = models.FloatField(default=9.9)
    Origin = models.CharField(default="Россия", max_length=128)
    Price = models.IntegerField(default=100)
    Description = models.CharField(default="", max_length=512)
    Feedback_id = models.ForeignKey(Feedback, on_delete=models.CASCADE, default=0)
    Mark = models.IntegerField(default=5)


class Goods(models.Model):
    """
    :param Shop_id: id магазина
    :param Beer_id: id пива
    """

    Shop_id = models.IntegerField(primary_key=True, default=1)
    Beer_id = models.ForeignKey(Beer, on_delete=models.CASCADE, default=0)


class Discounts(models.Model):
    """
    Модель скидок, в ней хранится:
    :param Shop_id: id магазина
    :param Discount: id конкретного пива
    :param Amount: сама скидка
    """

    Shop_id = models.IntegerField(primary_key=True, default=1)
    Discount = models.ForeignKey(Beer, on_delete=models.CASCADE, default=1)
    Amount = models.IntegerField(default=0)


class Shop(models.Model):
    """
    Модель магазина, в ней хранится информация:
    :param Shop_id: id магазина
    :param Job: нужен ли работник магазину,
    :param Discounts_id: id на талицу со скидками,
    :param Beer_id: id на таблицу с пивом.
    """

    Shop_id = models.IntegerField(primary_key=True, default=1)
    Job = models.BinaryField(default=1)
    Address = models.CharField(default="Бульвар", max_length=256)
    Discounts_id = models.ForeignKey(Discounts, on_delete=models.CASCADE, default=1)
    Beer_id = models.ForeignKey(Goods, on_delete=models.CASCADE, default=1)
