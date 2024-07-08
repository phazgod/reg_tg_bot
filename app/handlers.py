import re
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import ADMIN_CHAT_ID

import app.keyboards as kb

router = Router()


class Register(StatesGroup):
    name = State()
    phone = State()
    comment = State()
    answer = State()

user_states = {}

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_states[user_id] = 'start_used'
    await message.answer(f"{message.from_user.first_name}, Добро пожаловать в компанию DamnIT")
    await state.set_state(Register.name)
    await message.answer('Напишите свое ФИО')


# Обработка ввода ФИО
@router.message(Register.name, lambda message: not re.fullmatch(r'[A-Za-zА-Яа-яёЁ]+', message.text))
async def invalid_phio(message: Message):
    await message.reply("ФИО может содержать только буквы. Попробуйте снова:")


@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.phone)
    await message.answer('Укажите Ваш номер телефона\nНомер телефона должен быть в формате 7 999 999 99 99', reply_markup=kb.get_number)


# Обработка Номера
if Register.phone == Message.text:
    @router.message(Register.phone, lambda message: not re.fullmatch(r'7 \d{3} \d{3} \d{2} \d{2}', message.text))
    async def invalid_phone(message: Message):
        await message.reply("Номер телефона должен быть в формате 7 999 999 99 99. Попробуйте снова:")


@router.message(Register.phone, F.contact)
async def register_phone(message: Message, state: FSMContext):
    # if Register.phone == message.text:
    #     await state.update_data(phone=message.text)
    # elif Register.phone == message.contact:
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(Register.comment)
    await message.answer('Напишите любой комментарий')



@router.message(Register.comment)
async def register_comment(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    data = await state.get_data()
    await message.answer(f"Ваше имя: {data['name']}\nВаш номер: {data['phone']}\nВаш комментарий: {data['comment']}")
    await message.answer('Последний шаг! Ознакомься с вводными положениями')
    await message.answer_document(document='BQACAgIAAxkBAAPjZovEtgwCQFk7wbxcsxzJJxBmZrkAAndLAAKtI2BIpsSvPCOUhKY1BA')
    await state.set_state(Register.answer)
    await message.answer('Ознакомился?', reply_markup=kb.yes_pdf)


# Обработка ДА
@router.message(Register.answer, lambda message: not re.fullmatch('Да', message.text))
async def invalid_yes(message: Message):
    await message.reply("Ознакомься с вводными положениями.")


@router.message(lambda message: message.text != "/start")
async def last_message(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    if user_states.get(user_id) == 'start_used':
        await message.answer("Спасибо за успешную регистрацию")
        await message.answer_photo(photo='AgACAgIAAxkBAAPTZovCiqUAAUKvX_WkC2eu7cVVa3U1AAI02jEbrSNgSNh2q9HFrniTAQADAgADeQADNQQ')
        user_states[user_id] = 'no'
    else:
        await message.reply("Сначала ознакомьтесь с правилами, используя команду /start.")
    





@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID фото: {message.photo[-1].file_id}')

@router.message(F.document)
async def get_pdf(message: Message):
    await message.answer(f'ID pdf: {message.document.file_id}')