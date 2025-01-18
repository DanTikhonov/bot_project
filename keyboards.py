from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lessons import days

def gen_markup(texts, prefix):
    """Генератор кнопок, с различными колбэками"""
    markup = []
    ls = list(texts.keys())
    for les in ls:
        markup.append([InlineKeyboardButton(text=f"{les}", callback_data=f"{prefix}{les}")])
    print(markup)
    return markup


'''
Кнопки функции "strat"
'''
btn_fill_less = InlineKeyboardButton(
    text='Заполнить расписание.',
    callback_data='fill_lessons'
)
btn_fill_hw = InlineKeyboardButton(
    text='Записать домашнее задание.',
    callback_data='fill_hw'
)
btn_check_les = InlineKeyboardButton(
    text='Посмотреть домашнее задание.',
    callback_data='check_hw'
)
btn_edit_les = InlineKeyboardButton(
    text='Изменить домашнее задание.',
    callback_data='edit_les_hw'
)
keyboard_start = InlineKeyboardMarkup(
    inline_keyboard=[[btn_fill_less],
                     [btn_fill_hw],
                     [btn_check_les],
                     [btn_edit_les]]
)

'''
Функция генератора кнопок по дням
'''

def gen_markup_by_days(prefix):
    markup = []
    for day in days:
        markup.append([InlineKeyboardButton(text=f"{days[day]}", callback_data=f"{prefix}_{day}")])
    print(markup)
    return InlineKeyboardMarkup(inline_keyboard=markup)
