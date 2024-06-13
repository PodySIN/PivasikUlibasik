"""
Модуль отвечающий за сохранение форм.
"""

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse

from catalog.service import change_beers_mark
from main.configure import configure_logging
from catalog.forms import Feedback_Form
from users.models import Feedback
from django.contrib import messages

logger = configure_logging()


def feedback_save(request: WSGIRequest, beer_id: int, current_beer) -> HttpResponse:
    """
    Функция, которая сохраняет отзыв пользователя.
    :param request: Запрос к странице.
    :param beer_id: Id пива, к которому пользователь оставил отзыв.
    :param current_beer: Пиво.
    :return: Сохраненную форму с отзывом.
    """
    logger.info("Получаем запрос с методом POST.")
    form: Feedback_Form = Feedback_Form(request.POST)
    logger.info("Получаем форму отзывов и проверяем её правильность заполнения.")
    if form.is_valid():
        logger.info("Форма заполнена правильно")
        logger.info("Получаем данные из формы...")
        text: str = form.data.get("Text")
        mark: int = form.data.get("Mark")
        logger.info("Данные получены!")
        if int(mark) >= 1 and int(mark) <= 5:
            logger.info("Проверяем на правильность выставленной оценки.")
            feedback = Feedback(
                Beer_id=beer_id,
                Text=text,
                Mark=mark,
                Username=request.user.username,
            )
            feedback.save()
            logger.info("Все хорошо, сохраняем отзыв!")
            change_beers_mark(current_beer)
        else:
            logger.warning("Оценка поставлена некорректно!")
            messages.add_message(request, messages.INFO, "Введите оценку от 1 до 5")
