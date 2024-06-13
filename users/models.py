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

    class Meta:
        db_table = "Users"


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

    class Meta:
        db_table = "Feedbacks"
