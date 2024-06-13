"""
Модуль в котором хранятся модели (catalog).
"""

from django.db import models


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

    class Meta:
        db_table = "Beers"


class Goods(models.Model):
    """
    :param Shop_id: id магазина
    :param Beer_id: id пива
    """

    Shop_id = models.IntegerField(default=0)
    Beer_id = models.IntegerField(default=0)

    class Meta:
        db_table = "Goods"


class Shop(models.Model):
    """
    Модель магазина, в ней хранится информация:
    :param id: id магазина
    :param Job: нужен ли работник магазину,
    :param Discounts_id: id на талицу со скидками,
    :param Beer_id: id на таблицу с пивом.
    """

    id = models.IntegerField(primary_key=True, default=1)
    Job = models.IntegerField(default=0)
    Address = models.CharField(default="Бульвар", max_length=256)

    class Meta:
        db_table = "Shops"


class Discounts(models.Model):
    """
    Модель скидок, в ней хранится:
    :param Shop_id: id магазина
    :param Amount: сама скидка
    """

    Shop_id = models.IntegerField(default=0)
    Amount = models.IntegerField(default=0)
    Beer_id = models.IntegerField(default=0)

    class Meta:
        db_table = "Discounts"
