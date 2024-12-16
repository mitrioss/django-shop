# your_app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def to(value, arg):  # Добавляем второй аргумент
    return range(int(value), int(arg))  # Например, создаем диапазон от value до arg

@register.filter
def float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0  # Возвращаем значение по умолчанию, если преобразование не удалось
