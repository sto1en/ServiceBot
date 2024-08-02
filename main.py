import telebot
import applications
from telebot import types
import re

bot = telebot.TeleBot('6636078377:AAHY_bT6ebzOacyg7o4fFjbaPed8vVMbTKY')
client = applications.Client

@bot.message_handler(commands = ['start'])
def start(message):
    client.state[message.chat.id] = 'menu'
    text = f"Здравствуйте!\n\nВыберите что вам нужно"
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    button_info = telebot.types.InlineKeyboardButton(text='Информация', callback_data='info')
    button_register = telebot.types.InlineKeyboardButton(text='Личный кабинет', callback_data='account')
    button_service = telebot.types.InlineKeyboardButton(text='Запись на обслуживание', callback_data='service')
    markup.add(button_info, button_register, button_service)
    bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def response(function_call):
    if function_call.message:

        if function_call.data == "menu":
            client.state[function_call.message.chat.id] = 'menu'
            text = f"Здравствуйте!\n\nВыберите что вам нужно"
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            button_info = telebot.types.InlineKeyboardButton(text='Информация', callback_data='info')
            button_register = telebot.types.InlineKeyboardButton(text='Личный кабинет', callback_data='account')
            button_service = telebot.types.InlineKeyboardButton(text='Запись на обслуживание', callback_data='service')
            markup.add(button_info, button_register, button_service)
            bot.send_message(function_call.message.chat.id, text, parse_mode='html', reply_markup=markup)

        elif function_call.data == "info":
            client.state[function_call.message.chat.id] = 'info'
            text = "Мы компания. Более детально можешь ознакомиться с нами на нашем сайте!"
            markup = telebot.types.InlineKeyboardMarkup()
            button_url = telebot.types.InlineKeyboardButton(text="Перейти на сайт", url="https://www.twitch.tv/")
            button_back = telebot.types.InlineKeyboardButton(text="Назад", callback_data='menu')
            markup.add(button_url)
            markup.add(button_back)
            bot.send_message(function_call.message.chat.id, text, reply_markup=markup)
            bot.answer_callback_query(function_call.id)

        elif function_call.data == "account":
            client.state[function_call.message.chat.id] = 'account'
            text = "Личный кабинет"
            markup = telebot.types.InlineKeyboardMarkup()
            button_register = telebot.types.InlineKeyboardButton(text = "Регистрация", callback_data="client_register")
            button_correct = telebot.types.InlineKeyboardButton(text = "Изменить информацию", callback_data="client_correct")
            button_back = telebot.types.InlineKeyboardButton(text="Назад", callback_data='menu')
            markup.add(button_register, button_correct)
            markup.add(button_back)
            bot.send_message(function_call.message.chat.id, text, reply_markup=markup)

        elif function_call.data == "client_register":
            client.chat_id = function_call.message.from_user.id
            f = 0
            rows = applications.get_all_client_table()
            for row in rows:
                if row[4] == client.chat_id:
                    text = "Вы уже зарегистрированы"
                    markup = telebot.types.InlineKeyboardMarkup()
                    button_back = telebot.types.InlineKeyboardButton(text="Назад", callback_data='account')
                    markup.add(button_back)
                    bot.send_message(function_call.message.chat.id, text, reply_markup=markup)
                    f = 1
                    break
            if f == 0:
                client.state[function_call.message.chat.id] = 'writing_name'
                text = "Напишите ваше имя"
                bot.send_message(function_call.message.chat.id, text)

        elif function_call.data == "client_correct":
            client.state[function_call.message.chat.id] = 'correct_menu'
            text = "Выберите, что нужно изменить"
            markup = telebot.types.InlineKeyboardMarkup()
            button_name = types.InlineKeyboardButton(text = "Имя", callback_data="correct_name")
            button_phone_number = types.InlineKeyboardButton(text = "Номер телефона", callback_data="correct_phone_number")
            button_car_info = types.InlineKeyboardButton(text = "Марку и модель машины", callback_data="correct_car_info")
            markup.add(button_name)
            markup.add(button_phone_number)
            markup.add(button_car_info)
            bot.send_message(function_call.message.chat.id, text, reply_markup=markup)

        elif function_call.data == "correct_name":
            client.state[function_call.message.chat.id] = 'correct_name'
            client.chat_id = function_call.message.from_user.id
            text = "Напишите ваше имя"
            bot.send_message(function_call.message.chat.id, text)

        elif function_call.data == "correct_phone_number":
            client.state[function_call.message.chat.id] = 'correct_phone_number'
            client.chat_id = function_call.message.from_user.id
            text = "Напишите ваш номер телефона"
            bot.send_message(function_call.message.chat.id, text)

        elif function_call.data == "correct_car_info":
            client.state[function_call.message.chat.id] = 'correct_car_info'
            client.chat_id = function_call.message.from_user.id
            text = "Напишите марку и модель вашей машины"
            bot.send_message(function_call.message.chat.id, text)

@bot.message_handler(content_types = ['text'])
def get_text_messages(message):

    #Начало регистрации
    if client.state.get(message.chat.id) == "writing_name":
        client.state[message.chat.id] = 'writing_phone_number'
        client.client_name = message.text
        text = "Спасибо. Напишите ваш номер телефона для обратной связи"
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button_send_phone = types.KeyboardButton('Отправить номер телефона', request_contact=True)
        markup.add(button_send_phone)
        bot.send_message(message.chat.id, text, reply_markup=markup)

    elif client.state.get(message.chat.id) == "writing_phone_number":
        phone_pattern = re.compile(r'^\+?\d{10,15}$')
        if not (phone_pattern.match(message.text)):
            text = "Пожалуйста, отправьте верный номер телефона: "
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            button_send_phone = types.KeyboardButton('Отправить номер телефона', request_contact=True)
            markup.add(button_send_phone)
            bot.send_message(message.chat.id, text, reply_markup=markup)
        else:
            text = "Спасибо. Отправьте марку вашей машины:"
            client.state[message.chat.id] = 'writing_car_info'
            client.phone_number = message.text
            text = 'Спасибо. Напишите марку и модель вашей машины'
            bot.send_message(message.chat.id, text)

    elif client.state.get(message.chat.id) == "writing_car_info":
        client.state[message.chat.id] = 'registration_finished'
        client.car_info = message.text
        data = applications.transform_client_data(client)
        applications.add_row("client_info", data)
        text = "Регистрация закончена"
        markup = telebot.types.InlineKeyboardMarkup()
        button_back = telebot.types.InlineKeyboardButton(text="Назад", callback_data='account')
        markup.add(button_back)
        bot.send_message(message.chat.id, text, reply_markup=markup)
    #Конец регистрации

    #Изменения одного поля
    elif client.state.get(message.chat.id) == "correct_name":
        client.state[message.chat.id] = 'name_corrected'
        client.client_name = message.text
        applications.update_client_row(client, "client_name")
        text = "Имя изменено"
        markup = telebot.types.InlineKeyboardMarkup()
        button_back = telebot.types.InlineKeyboardButton(text='Назад', callback_data='client_correct')
        markup.add(button_back)
        bot.send_message(message.chat.id, text, reply_markup=markup)

    elif client.state.get(message.chat.id) == "correct_phone_number":
        phone_pattern = re.compile(r'^\+?\d{10,15}$')
        if not (phone_pattern.match(message.text)):
            text = "Пожалуйста, отправьте верный номер телефона: "
            bot.send_message(message.chat.id, text)
        else:
            client.state[message.chat.id] = 'phone_number_corrected'
            client.phone_number = message.text
            applications.update_client_row(client, "phone_number")
            text = "Номер телефона изменен"
            markup = telebot.types.InlineKeyboardMarkup()
            button_back = telebot.types.InlineKeyboardButton(text='Назад', callback_data='client_correct')
            markup.add(button_back)
            bot.send_message(message.chat.id, text, reply_markup=markup)

    elif client.state.get(message.chat.id) == "correct_car_info":
        client.state[message.chat.id] = 'car_info_corrected'
        client.car_info = message.text
        applications.update_client_row(client, "car_info")
        text = "Информация о машине изменена"
        markup = telebot.types.InlineKeyboardMarkup()
        button_back = telebot.types.InlineKeyboardButton(text='Назад', callback_data='client_correct')
        markup.add(button_back)
        bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    text = "Спасибо. Напишите марку и модель вашей машины:"
    if message.contact is not None:
        client.state[message.chat.id] = 'writing_car_info'
        client.phone_number = message.contact.phone_number
    else: text = 'Напишите /start'
    bot.send_message(message.chat.id, text)

bot.polling(none_stop=True, interval=0)