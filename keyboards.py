from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
Кнопки для заполнения уроков по дням
'''
btd_fill_monday = InlineKeyboardButton(
    text='Понедельник',
    callback_data='fill_mon',
)
btd_fill_tuesday = InlineKeyboardButton(
    text='Вторник',
    callback_data='fill_tue',
)
btd_fill_wednesday = InlineKeyboardButton(
    text='Среда',
    callback_data='fill_wed',
)
btd_fill_thursday = InlineKeyboardButton(
    text='Четверг',
    callback_data='fill_thu',
)
btd_fill_friday = InlineKeyboardButton(
    text='Пятница',
    callback_data='fill_fri',
)
keyboard_fill = InlineKeyboardMarkup(
    inline_keyboard=[
        [btd_fill_monday],
        [btd_fill_tuesday],
        [btd_fill_wednesday],
        [btd_fill_thursday],
        [btd_fill_friday]
    ]
)
'''
Кнопки для заполнения дз по дням
'''
btd_fill_monday = InlineKeyboardButton(
    text='Понедельник',
    callback_data='hw_mon',
)
btd_fill_tuesday = InlineKeyboardButton(
    text='Вторник',
    callback_data='hw_tue',
)
btd_fill_wednesday = InlineKeyboardButton(
    text='Среда',
    callback_data='hw_wed',
)
btd_fill_thursday = InlineKeyboardButton(
    text='Четверг',
    callback_data='hw_thu',
)
btd_fill_friday = InlineKeyboardButton(
    text='Пятница',
    callback_data='hw_fri',
)
keyboard_hw = InlineKeyboardMarkup(
    inline_keyboard=[
        [btd_fill_monday],
        [btd_fill_tuesday],
        [btd_fill_wednesday],
        [btd_fill_thursday],
        [btd_fill_friday]
    ]
)
'''
кнопки для изменения дз
'''
btd_edit_monday = InlineKeyboardButton(
    text='Понедельник',
    callback_data='edit_mon',
)
btd_edit_tuesday = InlineKeyboardButton(
    text='Вторник',
    callback_data='edit_tue',
)
btd_edit_wednesday = InlineKeyboardButton(
    text='Среда',
    callback_data='edit_wed',
)
btd_edit_thursday = InlineKeyboardButton(
    text='Четверг',
    callback_data='edit_thu',
)
btd_edit_friday = InlineKeyboardButton(
    text='Пятница',
    callback_data='edit_fri',
)

keyboard_edit = InlineKeyboardMarkup(
    inline_keyboard=[
        [btd_edit_monday],
        [btd_edit_tuesday],
        [btd_edit_wednesday],
        [btd_edit_thursday],
        [btd_edit_friday],
    ]
)
'''
кнопки для просмотра дз
'''
btd_ch_monday = InlineKeyboardButton(
    text='Понедельник',
    callback_data='ch_mon',
)
btd_ch_tuesday = InlineKeyboardButton(
    text='Вторник',
    callback_data='ch_tue',
)
btd_ch_wednesday = InlineKeyboardButton(
    text='Среда',
    callback_data='ch_wed',
)
btd_ch_thursday = InlineKeyboardButton(
    text='Четверг',
    callback_data='ch_thu',
)
btd_ch_friday = InlineKeyboardButton(
    text='Пятница',
    callback_data='ch_fri',
)

keyboard_ch = InlineKeyboardMarkup(
    inline_keyboard=[
        [btd_ch_monday],
        [btd_ch_tuesday],
        [btd_ch_wednesday],
        [btd_ch_thursday],
        [btd_ch_friday],
    ]
)
