from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер',
                                                           request_contact=True)]],
                                                           resize_keyboard=True,
                                                           input_field_placeholder='При использовании кнопки вы укажите номер telegram',
                                                           one_time_keyboard=True)

yes_pdf = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Да')]],
                                                        resize_keyboard=True,
                                                        input_field_placeholder="Нажмите 'Да', если ознакомились",
                                                        one_time_keyboard=True)