import re
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

from dotenv import load_dotenv
import os
load_dotenv()


router = Router()
user_states = {}
id_photo = 'AgACAgIAAxkBAAMFZpBOStL6uIBAlI6046Bey5QjSWEAAmvjMRvR54FI7k3R6gUEsuABAAMCAAN5AAM1BA'
id_pdf = 'BQACAgIAAxkBAAPjZovEtgwCQFk7wbxcsxzJJxBmZrkAAndLAAKtI2BIpsSvPCOUhKY1BA'

class Register(StatesGroup):
    name = State()
    phone = State()
    comment = State()
    answer = State()



@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_states[user_id] = 'enabled'
    await message.answer(f"@{message.from_user.username}, Добро пожаловать в компанию 'Название компании'")
    await state.set_state(Register.name)
    await message.answer('Напишите свое ФИО')


# Обработка ввода ФИО
@router.message(Register.name, lambda message: not re.fullmatch(r'[A-Za-zА-Яа-яёЁ ]+', message.text))
async def invalid_name(message: Message):
    await message.reply("ФИО может содержать только буквы. Попробуйте снова:")

@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.phone)
    await message.answer('Укажите Ваш номер телефона\nНомер телефона должен быть в формате +7 999 999 99 99', reply_markup=kb.get_number)


# Обработка некорректного номера телефона
@router.message(Register.phone, lambda message: message.text and not re.fullmatch(r'\+7 \d{3} \d{3} \d{2} \d{2}', message.text))
async def invalid_phone(message: Message):
    await message.reply("Номер телефона должен быть в формате +7 999 999 99 99. Попробуйте снова:")

@router.message(Register.phone, lambda message:  message.text)
async def register_phone_text(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(Register.comment)
    await message.answer('Напишите любой комментарий')

@router.message(Register.phone, lambda message: message.contact)
async def register_phone_contact(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(Register.comment)
    await message.answer('Напишите любой комментарий')


@router.message(Register.comment)
async def register_comment(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await message.answer('Последний шаг! Ознакомься с вводными положениями')
    await message.answer_document(document=id_pdf)
    await state.set_state(Register.answer)
    await message.answer('Ознакомился?', reply_markup=kb.yes_pdf)


# Обработка Кнопки
@router.message(Register.answer, lambda message: not re.fullmatch('да', message.text, re.IGNORECASE))
async def invalid_yes(message: Message):
    await message.reply("Ознакомься с вводными положениями.")


@router.message(lambda message: message.text != "/start")
async def last_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_states.get(user_id) == 'enabled':
        await message.answer("Спасибо за успешную регистрацию")
        await message.answer_photo(photo=id_photo)
        
        data = await state.get_data()
        admin_message = (f"Пользователь оставил комментарий:\nИмя: {data['name']}\nНомер: {data['phone']}\nКомментарий: {data['comment']}")
        await message.bot.send_message(chat_id=os.getenv('ADMIN_CHAT_ID'), text=admin_message)
        await state.clear()

        user_states[user_id] = 'disabled'
    else:
        await message.reply("Чтобы воспользоваться ботом, используйте команду /start.")