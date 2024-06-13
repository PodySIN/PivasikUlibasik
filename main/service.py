"""
Модуль, который хранит вспомогательные функции
"""

from main.configure import configure_logging

logger = configure_logging()


def get_object_from_db(model, id: int):
    """
    Функция, которая возвращает объект модели по id.
    :param model: Модель из которой мы хотим получить данные.
    :param id: Id объекта этой модели.
    :return: Возвращаем объект модели по id.
    """
    logger.info(f"Получаем объект из {model} с id: {id}.")
    return model.objects.get(id=id)


def get_all_objects_from_db(model):
    """
    Функция, которая возвращает все объекты модели.
    :param model: Модель из которой мы хотим получить данные.
    :return: Возвращаем все объекты модели.
    """
    logger.info(f"Получаем все объекты из {model}.")
    return model.objects.all()


def filter_objects_from_db(objects, **kwargs):
    """
    Функция, которая фильтрует все объекты модели.
    :param objects: Объекты, которые нужно отфильтровать.
    :param kwargs: Фильтры.
    :return: Возвращаем все отфильтрованные объекты модели.
    """
    logger.info("Фильтруем объекты из модели.")
    return objects.filter(**kwargs)


def get_base_context(Title: str) -> dict:
    """
    Возвращает словарь с названием страницы
    :param Title: Название страницы
    :return: словарь с названием страницы
    """
    logger.info("Получаем context.")
    context: dict = {
        "Title": Title,
    }
    return context
