import telebot
import applications
from telebot import types
import re

bot = telebot.TeleBot('6636078377:AAHY_bT6ebzOacyg7o4fFjbaPed8vVMbTKY')
user_state = {}
#eqw
@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button_start = types.InlineKeyboardButton(text='Начать', callback_data='start')
    markup.add(button_start)

    bot.send_message(message.chat.id, "Нажмите кнопку, чтобы начать", reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def response(function_call):
    if function_call.message:
        chat_id = function_call.message.chat.id
        if function_call.data == "start":
            text = f"Здравствуйте!\n\nВыберите что вам нужно"
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            button_info = telebot.types.InlineKeyboardButton(text='Информация', callback_data='info')
            button_register = telebot.types.InlineKeyboardButton(text='Регистрация', callback_data='register')
            button_service = telebot.types.InlineKeyboardButton(text='Запись на обслуживание', callback_data='service')
            markup.add(button_info, button_register, button_service)

            bot.send_message(function_call.message.chat.id, text, parse_mode='html', reply_markup=markup)

        elif function_call.data == "info":
            text = "Мы компания. Более детально можешь ознакомиться с нами на нашем сайте!"
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text="Перейти на сайт", url="https://www.twitch.tv/"))
            bot.send_message(function_call.message.chat.id, text, reply_markup=markup)
            bot.answer_callback_query(function_call.id)

        elif function_call.data == "register":
            text = "Напишите свое имя:"
            user_state[chat_id] = 'waiting_for_fio'
            bot.send_message(function_call.message.chat.id, text)

        elif user_state.get(chat_id) == "waiting_for_phone_number":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
            markup.add(button_phone)
            bot.send_message(function_call.message.chat.id, reply_markup=markup)
            bot.answer_callback_query(function_call.id)

        elif function_call.data[:5] == 'date_':
            selected_date = function_call.data.split('_')[1]
            phone_number = function_call.data.split('_')[2]
            times = read_times_from_file(selected_date)
            text = f"Свободное время для {selected_date}:"

            markup = telebot.types.InlineKeyboardMarkup(row_width=7)
            for time in times:
                markup.add(telebot.types.InlineKeyboardButton(text=time, callback_data=f"time_{time}_date_{selected_date}_{phone_number}"))
            bot.send_message(function_call.message.chat.id, text, reply_markup=markup)

        elif function_call.data[:5] == 'time_':
            time = function_call.data.split('_')[1]
            date = function_call.data.split('_')[3]
            phone_number = function_call.data.split('_')[4]
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Подтвердить', callback_data=f"confirm_{date}_{time}_{phone_number}"))
            bot.send_message(function_call.message.chat.id, f"Вы выбрали {time} на {date} для записи", reply_markup=markup)

        elif function_call.data.split('_')[0] == 'confirm':
            date = function_call.data.split('_')[1]
            time = function_call.data.split('_')[2]
            phone_number = function_call.data.split('_')[3]
            str = '\n' + phone_number + ' ' + date + ' ' + time
            appendClient(str)
            text = 'Вы записаны успешно'
            bot.send_message(function_call.message.chat.id, text)

        #Просмотр всех клиентов
        elif function_call.data == 'client_table':
            rows = applications.get_all_client_table()
            text = '      Имя      | Номер телефона | Машина \n'
            for row in rows:
                text += row[1] + ' | ' + row[2] + ' | ' + row[3] + '\n'
            bot.send_message(function_call.message.chat.id, text)
        #Просмотр всех записей
        elif function_call.data == 'register_table':

            text = 'date  | time   | Имя клиента | Номер телефона | info \n'
            rows = applications.dates_to_watch()
            for i in range(0, len(rows)):
                print(rows[i])
                print(rows[i][2], type(rows[i][2]))
                text += rows[i][0] + ' | ' + rows[i][1] + ' | ' + rows[i][2] + ' | ' + rows[i][3] + ' | ' + rows[i][4]  + '\n'
            bot.send_message(function_call.message.chat.id, text)

        elif function_call.data.split('_')[:2] == ['send','date']:
            date = function_call.data.split('_')[2]
            date = applications.transform_date_to_add(date)
            text = ''
            if not(date): func = date
            else:
                if applications.check_date_in_table(date): func = applications.add_rows('register_days', date)
                else:
                    func = False
                    text = 'Запись уже была добавлена'
            if func and text == '':
                text = 'Запись добавлена успешно'
                user_state[chat_id] = ''
            elif not(func) and text == '': text = 'Запись введена некорректно'
            bot.send_message(function_call.message.chat.id, text)

        elif function_call.data == 'add_date':
            user_state[chat_id] = "waiting_for_fill_dates"
            text = 'Напишите дату и свободное время через пробел (пример: 01.01 12:00 13:30): '
            bot.send_message(function_call.message.chat.id, text)

        elif function_call.data == 'delete_date':
            user_state[chat_id] = "waiting_for_delete_dates"
            text = 'Напишите запись через пробел, которую надо удалить или нажмите на кнопку: '
            dates = applications.get_all_dates()
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            for date in dates:
                markup.add(telebot.types.InlineKeyboardButton(text=date, callback_data=f"delete_button_date_{date}"))
            bot.send_message(function_call.message.chat.id, text, reply_markup=markup)

        elif function_call.data.split('_')[:2] == ['delete', 'button']:
            date = function_call.data.split('_')[3]
            date = applications.transform_date_to_delete(date)
            func = applications.delete_by_date_time('register_days', date)
            if func:
                text = 'Запись удалена успешно'
                user_state[chat_id] = ''
            else:
                text = 'Запись не найдена'
            bot.send_message(function_call.message.chat.id, text)

        elif function_call.data.split('_')[:4] == ['delete','date', 'confirm', 'button']:
            date = function_call.data.split('_')[4]
            date = applications.transform_date_to_delete(date)
            func = applications.delete_by_date_time('register_days', date)
            if func:
                text = 'Запись удалена успешно'
                user_state[chat_id] = ''
            else: text = 'Запись не найдена'
            bot.send_message(function_call.message.chat.id, text)



@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    chat_id = message.chat.id
    text = "Марка вашей машины:"
    if message.contact is not None and user_state.get(chat_id) == 'waiting_for_phone_number':
        user_state[chat_id] = 'waiting_for_car_mark'
        print(message.contact.phone_number)
    else: text = 'Напишите /start'
    bot.send_message(message.chat.id, text)



@bot.message_handler(commands = ['admin'])
def AdminBot(message):
    chat_id = message.chat.id
    user_state[chat_id] = "waiting_for_fill_dates"
    text = "Меню"
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    button_client = telebot.types.InlineKeyboardButton(text='Посмотреть всех клиентов', callback_data='client_table')
    button_date = telebot.types.InlineKeyboardButton(text='Посмотреть все записи', callback_data='register_table')
    button_info = telebot.types.InlineKeyboardButton(text='Добавить дату', callback_data='add_date')
    button_register = telebot.types.InlineKeyboardButton(text='Удалить дату', callback_data='delete_date')
    markup.add(button_client, button_date, button_info, button_register)
    bot.send_message(message.chat.id, text, reply_markup=markup)



@bot.message_handler(content_types = ['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    text = message.text
    if user_state.get(chat_id) == 'waiting_for_fio':
        fio_pattern = re.compile(r'^[А-ЯЁ][а-яё]+$')
        if fio_pattern.match(text):
            response = "Спасибо. Отправьте ваш номер телефона: "
            user_state[chat_id] = "waiting_for_phone_number"
        else:
            response = "Пожалуйста, отправьте свое настоящее имя: "
        bot.send_message(chat_id, response)

    elif user_state.get(chat_id) == 'waiting_for_phone_number':
        phone_pattern = re.compile(r'^\+?\d{10,15}$')
        if not(phone_pattern.match(message.text)):
            text = "Пожалуйста, отправьте верный номер телефона: "
        text = "Спасибо. Отправьте марку вашей машины:"
        user_state[chat_id] = 'waiting_for_car_mark'
        bot.send_message(chat_id, text)
        print(message.text)

    elif user_state.get(chat_id) == 'waiting_for_car_mark':
        if len(message.text) <= 2:
            text = "Пожалуйста, отправьте верную марку машины: "
        text = "Спасибо. Отправьте модель вашей машины:"
        user_state[chat_id] = 'waiting_for_car_model'
        bot.send_message(chat_id, text)
        print(message.text)

    elif user_state.get(chat_id) == 'waiting_for_fill_dates':
        text = "Нажмите на кнопку, чтобы занести в базу данных"
        date = message.text
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Подтвердить', callback_data=f"send_date_{date}"))
        bot.send_message(chat_id, text, reply_markup=markup)

    elif user_state.get(chat_id) == 'waiting_for_delete_dates':
        text = "Нажмите на кнопку, чтобы удалить из базы данных"
        date = message.text
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Подтвердить', callback_data=f"delete_date_confirm_button_{date}"))
        bot.send_message(chat_id, text, reply_markup=markup)

    else: bot.send_message(message.from_user.id, "Напишите /start")




bot.polling(none_stop=True, interval=0)