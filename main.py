from pack import TOKEN
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards import keyboard_fill, keyboard_start, gen_markup, keyboard_hw, keyboard_ch, keyboard_edit
from aiogram.types import InlineKeyboardMarkup





monday = {}
#monday = {'русский': '345 347', 'английский': 'сб стр 78', 'испанский': 'читать цуши'}
tuesday = {'алгебра': '456', 'геомнтрия': '234', 'физика': 'теоремы'}
wednesday = {'изо': 'чертить', 'технология': 'рисовать', 'черчение': 'пилить'}
thursday = {'химия': 'митоз', 'биология': 'мейоз', 'история': 'п8', 'обществознание': 'учить'}
friday = {'литература': 'читать', 'английская_литература': 'читать'}

days_lessons = [monday, tuesday, wednesday, thursday, friday]
# [{'русский': '345 347', 'английский': 'сб стр 78', 'испанский': 'читать цуши'}, {'алгебра': '456', 'геомнтрия':
# '234', 'физика': 'теоремы'}, {'изо': 'чертить', 'технология': 'рисовать', 'черчение': 'пилить'}, {'химия': 'митоз',
# 'биология': 'мейоз', 'история': 'п8', 'обществознание': 'учить'}, {'литература': 'читать', 'английская_литература':
# 'читать'}]
lessons = {}



class LES(StatesGroup):
    day = State()
    lessons = State()
    hw = State()
    edit_hw = State()

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command(commands='start'))
async def start(message: Message):
    await message.answer(
        text='Привет!\nНиже представлен весь мой функционал на данный момент',
        reply_markup=keyboard_start
    )


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

    # TODO: Считать список уроков

    markup = gen_markup(monday, f'editd_{day}_')
    await call.message.answer(
        text='Выберите урок',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=markup)
    )



@dp.callback_query(F.data.startswith("editd_"))
async def edit(call: CallbackQuery, state: FSMContext):
    day = call.data.split('_')[1]
    ind = call.data.split('_')[2]
    await state.update_data(day=day)
    await state.update_data(index=ind)
    await state.set_state(LES.edit_hw)
    await call.message.answer('Введите новый урок')


@dp.message(LES.edit_hw)
async def edit_homework(message: Message, state: FSMContext):
    await state.update_data(homework=message.text)
    data = await state.get_data()
    day = data['day']
    index = int(data['index'])
    homework = data['homework']
    # TODO: Request data from database
    if day == 'mon':
        k = list(monday.keys())[index]
        monday[k] = homework
    if day == 'tue':
        k = list(tuesday.keys())[index]
        tuesday[k] = homework
    if day == 'wed':
        k = list(wednesday.keys())[index]
        wednesday[k] = homework
    if day == 'thu':
        k = list(thursday.keys())[index]
        thursday[k] = homework
    if day == 'fri':
        k = list(friday.keys())[index]
        friday[k] = homework
    await state.clear()


@dp.callback_query(F.data.startswith('ch_'))
async def check_hw(call: CallbackQuery):
    day = call.data.split('_')[1]

    # TODO: read homework from database

    if day == 'mon':
        await call.message.answer('Понедельник')
        for key in monday:
            if monday[key] != '':
                await call.message.answer(f'{key}:{monday[key]}')
    if day == 'tue':
        await call.message.answer("Вторник")
        for key in tuesday:
            if tuesday[key] != '':
                await call.message.answer(f'{key}:{tuesday[key]}')
    if day == 'wed':
        await call.message.answer("Среда")
        for key in wednesday:
            if wednesday[key] != '':
                await call.message.answer(f'{key}:{wednesday[key]}')
    if day == 'thu':
        await call.message.answer('Четверг')
        for key in thursday:
            if thursday[key] != '':
                await call.message.answer(f'{key}:{thursday[key]}')
    if day == 'fri':
        await call.message.answer("Пятница")
        for key in friday:
            if friday[key] != '':
                await call.message.answer(f'{key}:{friday[key]}')
    if day == 'all':
        for i in days_lessons:
            if i == monday:
                await call.message.answer('Понедельник')
            if i == tuesday:
                await call.message.answer('Вторник')
            if i == wednesday:
                await call.message.answer('Среда')
            if i == thursday:
                await call.message.answer('Четверг')
            if i == friday:
                await call.message.answer('Пятница')
            for key, value in i:
                if value != '':
                    await call.message.answer(f'{key}:{value}')


@dp.callback_query(F.data.in_(['hw_mon', 'hw_tue', 'hw_wed', 'hw_thu', 'hw_fri']))
async def start_hw_les(call: CallbackQuery):
    day = call.data.split('_')[1]
    markup = gen_markup(tuesday, f'les_{day}_')
    await call.message.answer(
        text='Выберите урок:',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=markup)
    )



@dp.callback_query(F.data.startswith("les_"))
async def les_fill(call: CallbackQuery, state: FSMContext):
    day = call.data.split('_')[1]
    index = call.data.split('_')[2]
    await state.update_data(day=day)
    await state.update_data(index=index)
    await state.set_state(LES.hw)
    print(day, index)
    await call.message.answer('Введите задание')


@dp.message(LES.hw)
async def f_hw(message: Message, state: FSMContext):
    print(1)
    await state.update_data(hom=message.text)
    data = await state.get_data()
    hw_day = data['day']
    les_in = int(data['index'])
    homework = data['hom']
    print(data)
    if hw_day == 'mon':
        k = list(monday.keys())[les_in]
        monday[k] = homework
    if hw_day == 'tue':
        k = list(tuesday.keys())[les_in]
        tuesday[k] = homework
    if hw_day == 'wed':
        k = list(wednesday.keys())[les_in]
        wednesday[k] = homework
    if hw_day == 'thu':
        k = list(thursday.keys())[les_in]
        thursday[k] = homework
    if hw_day == 'fri':
        k = list(friday.keys())[les_in]
        friday[k] = homework
    await state.clear()
    print(days_lessons)


@dp.callback_query(F.data.in_(['fill_monday', 'fill_tuesday', 'fill_wednesday', 'fill_thursday', 'fill_friday']))
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
    if day == 'monday':
        for i in range(len(lesson)):
            monday[lesson[i]] = ''
    if day == 'tuesday':
        for i in range(len(lesson)):
            tuesday[lesson[i]] = ''
    if day == 'wednesday':
        for i in range(len(lesson)):
            wednesday[lesson[i]] = ''
    if day == 'thursday':
        for i in range(len(lesson)):
            thursday[lesson[i]] = ''
    if day == 'friday':
        for i in range(len(lesson)):
            friday[lesson[i]] = ''
    await state.clear()
    print(days_lessons)


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


@dp.message(Command(commands='lessons'))
async def show_lessons(message: Message):
    await message.answer('Смотри в компиляторе.')
    print(days_lessons)


if __name__ == '__main__':
    dp.run_polling(bot)
