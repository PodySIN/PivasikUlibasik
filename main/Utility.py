"""
Модуль, который хранит вспомогательные функции
"""
from main.models import Feedback


def get_base_context(Title: str) -> dict:
    """
    Возвращает словарь с названием страницы
    :param Title: Название страницы
    :return: словарь с названием страницы
    """
    context: dict = {
        "Title": Title,
    }
    return context


def change_beers_mark(particular_beer):
    """
    Функция, которая изменяет в бд оценку пива по отзывам пользователя.
    :param particular_beer: Конкретное пиво, на которое перешел пользователь
    :return: Ничего не возвращает, а сохраняет изменения в бд
    """
    all_feedbacks = Feedback.objects.all()
    middle_mark: int = 0
    for i in range(len(all_feedbacks)):
        middle_mark += all_feedbacks[i].Mark
    middle_mark: int = round(middle_mark / len(all_feedbacks))
    particular_beer.Mark = middle_mark
    particular_beer.save()
