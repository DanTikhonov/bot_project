from pack import TOKEN, YANDEX_API, CATAL_IDEN  # файл с приватными токенами и ключами
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards import keyboard_fill, keyboard_start, gen_markup, keyboard_hw, keyboard_ch, keyboard_edit
from aiogram.types import InlineKeyboardMarkup
from lessons import Dairy
from YAPI import YGPT

dairy = Dairy()
ygpt = YGPT(CATAL_IDEN, YANDEX_API)


class LES(StatesGroup):
    day = State()
    lessons = State()
    hw = State()
    edit_hw = State()
    gpt = State()


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command(commands='gpt_help'))
async def gpt_help(message: Message, state: FSMContext):
    """28-43 - обработка запроса пользователя, ответ от YandexGPT"""
    await state.clear()
    await state.set_state(LES.gpt)
    await message.answer(text='Введите ваш запрос:')


@dp.message(LES.gpt)
async def set_gpt(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    text = data['text']
    ans = ygpt.message_YGPT(text)
    await message.answer(ans)
    await state.clear()


@dp.message(Command(commands='drop'))
async def drop(message: Message):
    """функция, очищающая бд."""
    dairy.clearAll()
    await message.answer(text='Всё очищено.')


@dp.message(Command(commands='start'))
async def start(message: Message):
    await message.answer(
        text='Привет!\nНиже представлен весь мой функционал на данный момент\n/drop - если надо всё '
             'сбрость.\nДЕМО:\n/gpt_help - YandexGPT',
        reply_markup=keyboard_start
    )


''' 
59 - 181 обработка колбэков, выполнение последующего функционала, заполнение бд
'''


@dp.callback_query(F.data.in_(['check_hw']))
async def show_ch_menu(call: CallbackQuery):
    await call.message.answer(
        text='Выберите день для просмотра домашнего задания',
        reply_markup=keyboard_ch
    )


@dp.callback_query(F.data.in_(['edit_les_hw']))
async def show_edit_hw_menu(call: CallbackQuery):
    await call.message.answer(
        text='Выберете день недели.',
        reply_markup=keyboard_edit
    )


@dp.callback_query(F.data.in_(['fill_lessons']))
async def start_fill_les(callback: CallbackQuery):
    await callback.message.answer(
        text='Выберите день недели:',
        reply_markup=keyboard_fill
    )


@dp.callback_query(F.data.in_(['fill_hw']))
async def start_fill_hw(callback: CallbackQuery):
    await callback.message.answer(
        text='Выберите день недели:',
        reply_markup=keyboard_hw
    )


@dp.callback_query(F.data.startswith('edit_'))
async def show_e_m(call: CallbackQuery):
    day = call.data.split('_')[1]
    les = dairy.getLesHWasDict(call.from_user.id, day)
    markup = gen_markup(les, f'editd_{day}_')
    await call.message.answer(
        text='Выберите урок',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=markup)
    )


@dp.callback_query(F.data.startswith("editd_"))
async def edit(call: CallbackQuery, state: FSMContext):
    day = call.data.split('_')[1]
    les = call.data.split('_')[2]
    await state.update_data(day=day)
    await state.update_data(lesson=les)
    await state.set_state(LES.edit_hw)
    await call.message.answer('Введите новый урок')


@dp.message(LES.edit_hw)
async def edit_homework(message: Message, state: FSMContext):
    await state.update_data(homework=message.text)
    data = await state.get_data()
    day = data['day']
    les = data['lesson']
    homework = data['homework']
    dairy.updateHW(message.from_user.id, day, les, homework)
    await state.clear()


@dp.callback_query(F.data.startswith('ch_'))
async def check_hw(call: CallbackQuery):
    day = call.data.split('_')[1]

    lessons = dairy.getLesHWasDict(call.from_user.id, day)
    for key in lessons:
        await call.message.answer(f'{key}:{lessons[key]}')


@dp.callback_query(F.data.in_(['hw_mon', 'hw_tue', 'hw_wed', 'hw_thu', 'hw_fri']))
async def start_hw_les(call: CallbackQuery):
    day = call.data.split('_')[1]
    les = dairy.getLesHWasDict(call.from_user.id, day)
    markup = gen_markup(les, f'les_{day}_')
    await call.message.answer(
        text='Выберите урок:',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=markup)
    )


@dp.callback_query(F.data.startswith("les_"))
async def les_fill(call: CallbackQuery, state: FSMContext):
    day = call.data.split('_')[1]
    les = call.data.split('_')[2]
    await state.update_data(day=day)
    await state.update_data(lesson=les)
    await state.set_state(LES.hw)
    await call.message.answer('Введите задание')


@dp.message(LES.hw)
async def f_hw(message: Message, state: FSMContext):
    print(1)
    await state.update_data(hom=message.text)
    data = await state.get_data()
    hw_day = data['day']
    les = data['lesson']
    homework = data['hom']
    dairy.updateHW(message.from_user.id, hw_day, les, homework)
    await state.clear()


@dp.callback_query(F.data.in_(['fill_mon', 'fill_tue', 'fill_wed', 'fill_thu', 'fill_fri']))
async def les_d(call: CallbackQuery, state: FSMContext):
    action = call.data.split("_")[1]
    await state.update_data(day=action)
    await state.set_state(LES.lessons)
    await call.message.answer(f"Введите уроки")


@dp.message(LES.lessons)
async def input_lessons(message: Message, state: FSMContext):
    await state.update_data(lessons=message.text.split(' '))
    data = await state.get_data()
    lesson = data['lessons']
    day = data['day']
    dairy.addRecord(message.from_user.id, day, lesson)
    await state.clear()


'''
184 - 205 простейшие функции
'''


@dp.message(Command(commands='fill_lessons'))
async def fill_lessons(message: Message):
    await message.answer(
        text='Выберите день недели:',
        reply_markup=keyboard_fill
    )


@dp.message(Command(commands='fill_homework'))
async def fill_hw(message: Message):
    await message.answer(
        text='На кокой день заполнить д/з.',
        reply_markup=keyboard_hw
    )


@dp.message(Command(commands='check_homework'))
async def c_h(message: Message):
    await message.answer(
        text='В кокой день посмотреть д/з.',
        reply_markup=keyboard_ch
    )


'''
208 - 247 работа с различными медиафайлами (эхо функции)
'''


@dp.message(F.photo)
async def photo(message):
    print(message)
    await message.reply_photo(message.photo[0].file_id)


@dp.message(F.sticker)
async def sticker(message):
    print(message)
    await message.answer_sticker(message.sticker.file_id)


@dp.message(F.audio)
async def audio(message):
    print(message)
    await message.answer_audio(message.audio.file_id)


@dp.message(F.video)
async def video(message):
    print(message)
    await message.answer_video(message.video.file_id)


@dp.message(F.voice)
async def voice(message):
    print(message)
    await message.answer_voice(message.voice.file_id)


@dp.message(F.animation)
async def animation(message):
    print(message)
    await message.answer_animation(message.animation.file_id)


@dp.message(F.document)
async def document(message):
    print(message)
    await message.answer_document(message.document.file_id)


if __name__ == '__main__':
    dp.run_polling(bot)
