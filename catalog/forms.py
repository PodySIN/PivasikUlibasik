"""
Модуль отвечающий за сохранение форм.
"""

from django import forms


class Feedback_Form(forms.Form):
    """
    Форма отзывов пользователя о конкретном пивке
    :param Text: Текст, который ввел пользователь для отзыва
    :param Mark: Оценка, которую поставил пользователь
    """

    Text = forms.CharField(
        max_length=1024,
        required=True,
        label="Напишите свой царский отзыв:",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Пожалуйста, напишите своё мнение о товаре",
                "style": "width:1250px; height: 250px",
            }
        ),
    )
    Mark = forms.IntegerField(
        required=True,
        label="Поставьте свою мощную оценку:",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "от 1 до 5",
                "style": "width:100px; height: 40px",
            }
        ),
    )
