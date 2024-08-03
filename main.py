import telebot
import applications
from telebot import types
import re

bot = telebot.TeleBot('6636078377:AAHY_bT6ebzOacyg7o4fFjbaPed8vVMbTKY')
client = applications.Client
record = applications.Record
admin_state = {}


@bot.message_handler(commands = ['start'])
def start(message):
    client.state[message.chat.id] = 'menu'
    client.chat_id = message.from_user.id
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

        #Личный кабинет
        elif function_call.data == "account":
            client.chat_id = function_call.from_user.id
            client.state[function_call.message.chat.id] = 'account'
            text = "Личный кабинет \n"
            rows = applications.get_all_client_table()
            for row in rows:
                if row[4] == client.chat_id:
                    text += 'Имя: ' + row[1] + '\n'
                    text += 'Номер телефона: ' + row[2] + '\n'
                    text += 'Машина: ' + row[3] + '\n'
                    f = 1
                    break
                else:
                    f = 0
            if f == 0:
                text = 'Вы не зарегистрированы!'
                client.state[function_call.message.chat.id] = 'log_in'
            markup = telebot.types.InlineKeyboardMarkup(row_width = 2)
            button_register = telebot.types.InlineKeyboardButton(text = "Регистрация", callback_data="client_register")
            button_correct = telebot.types.InlineKeyboardButton(text = "Изменить информацию", callback_data="client_correct")
            button_record = telebot.types.InlineKeyboardButton(text = "Записи на обслуживание", callback_data="see_records")
            button_delete = telebot.types.InlineKeyboardButton(text = "Удалить данные", callback_data="client_delete")
            button_back = telebot.types.InlineKeyboardButton(text="Назад", callback_data='menu')
            markup.add(button_register, button_correct, button_record)
            markup.add(button_delete)
            markup.add(button_back)
            bot.send_message(function_call.message.chat.id, text, reply_markup=markup)

        elif function_call.data == "client_register":
            client.chat_id = function_call.from_user.id
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
            client.chat_id = function_call.from_user.id
            if client.state.get(function_call.message.chat.id) == 'log_in':
                text = 'Вы не зарегистрированы!'
                markup = telebot.types.InlineKeyboardMarkup()
                button_back = telebot.types.InlineKeyboardButton(text = 'Назад', callback_data = 'account')
                markup.add(button_back)
            else:
                client.state[function_call.message.chat.id] = 'correct_menu'
                text = "Выберите, что нужно изменить"
                markup = telebot.types.InlineKeyboardMarkup()
                button_name = types.InlineKeyboardButton(text = "Имя", callback_data="correct_name")
                button_phone_number = types.InlineKeyboardButton(text = "Номер телефона", callback_data="correct_phone_number")
                button_car_info = types.InlineKeyboardButton(text = "Марку и модель машины", callback_data="correct_car_info")
                button_back = telebot.types.InlineKeyboardButton(text="Назад", callback_data='account')
                markup.add(button_name)
                markup.add(button_phone_number)
                markup.add(button_car_info)
                markup.add(button_back)
            bot.send_message(function_call.message.chat.id, text, reply_markup=markup)

        elif function_call.data == "correct_name":
            client.state[function_call.message.chat.id] = 'correct_name'
            text = "Напишите ваше имя"
            bot.send_message(function_call.message.chat.id, text)

        elif function_call.data == "correct_phone_number":
            client.state[function_call.message.chat.id] = 'correct_phone_number'
            text = "Напишите ваш номер телефона"
            bot.send_message(function_call.message.chat.id, text)

        elif function_call.data == "correct_car_info":
            client.state[function_call.message.chat.id] = 'correct_car_info'
            text = "Напишите марку и модель вашей машины"
            bot.send_message(function_call.message.chat.id, text)

        elif function_call.data == "client_delete":
            client.chat_id = function_call.from_user.id
            client.state[function_call.message.chat.id] = 'delete_data'
            text = "Вы уверены, что хотите удалить свои данные?"
            markup = telebot.types.InlineKeyboardMarkup()
            button_confirm = telebot.types.InlineKeyboardButton(text = 'Подтвердить', callback_data = 'data_deleted')
            markup.add(button_confirm)
            bot.send_message(function_call.message.chat.id, text, reply_markup = markup)

        elif function_call.data == "data_deleted":
            client.state[function_call.message.chat.id] = 'data_deleted'
            applications.delete_client(client)
            text = 'Данные удалены'
            markup = telebot.types.InlineKeyboardMarkup()
            button_back = telebot.types.InlineKeyboardButton(text='Назад', callback_data='account')
            markup.add(button_back)
            bot.send_message(function_call.message.chat.id, text, reply_markup=markup)

        #Записи в личном кабинете
        elif function_call.data == "see_records":
            client.state[function_call.message.chat.id] = 'see_my_records'
            client.chat_id = function_call.from_user.id
            text = 'Ваши записи. Нажмите, чтобы посмотреть полную информацию'
            markup = telebot.types.InlineKeyboardMarkup(row_width = 4)
            buttons = []
            for row in applications.get_client_records(client):
                rec = row[0] + ' ' + row[1]
                button = telebot.types.InlineKeyboardButton(text = rec, callback_data = f'see_record_{rec}_{row[2]}')
                buttons.append(button)

            for i in range(0, len(buttons), 4):
                markup.row(*buttons[i:i + 4])

            button_back = telebot.types.InlineKeyboardButton(text="Назад", callback_data='account')
            markup.add(button_back)
            bot.send_message(function_call.message.chat.id, text, reply_markup = markup)

        elif function_call.data.split('_')[:2] == ["see", "record"]:
            client.state[function_call.message.chat.id] = 'see_my_record'
            client.chat_id = function_call.from_user.id
            rec = function_call.data.split('_')[2]
            info = function_call.data.split('_')[3]
            record.date = rec.split(' ')[0]
            record.time = rec.split(' ')[1]
            text = f'Запись на {rec}, {info}'
            markup = telebot.types.InlineKeyboardMarkup(row_width = 2)
            button_change = telebot.types.InlineKeyboardButton(text="Изменить доп информацию", callback_data = f'change_record')
            button_delete = telebot.types.InlineKeyboardButton(text="Удалить запись", callback_data = f'remove_record')
            markup.add(button_change)
            markup.add(button_delete)
            bot.send_message(function_call.message.chat.id, text, reply_markup = markup)

        elif function_call.data == "remove_record":
            client.state[function_call.message.chat.id] = 'remove_my_record'
            text = "Вы хотите отменить запись?"
            markup = telebot.types.InlineKeyboardMarkup()
            button_confirm = telebot.types.InlineKeyboardButton(text = "Подтвердить", callback_data = "remove_confirm")
            button_back = telebot.types.InlineKeyboardButton(text="Назад", callback_data='see_records')
            markup.add(button_confirm)
            markup.add(button_back)
            bot.send_message(function_call.message.chat.id, text, reply_markup = markup)

        elif function_call.data == "remove_confirm":
            client.state[function_call.message.chat.id] = 'removed_my_record'
            client.chat_id = function_call.from_user.id
            applications.update_record(record, "client_id", 0)
            applications.update_record(record, "info", "Свободно")
            text = "Запись отменена"
            markup = telebot.types.InlineKeyboardMarkup()
            button_back = telebot.types.InlineKeyboardButton(text="Назад", callback_data='see_records')
            markup.add(button_back)
            bot.send_message(function_call.message.chat.id, text, reply_markup=markup)

        elif function_call.data == "change_record":
            client.state[function_call.message.chat.id] = 'change_my_record'
            text = "Напишите дополнительную информацию о необходимом обслуживании"
            bot.send_message(function_call.message.chat.id, text)

        #Запись на обслуживание
        elif function_call.data == "service":
            client.state[function_call.message.chat.id] = 'service'
            text = 'Выберите дату для записи'
            markup = telebot.types.InlineKeyboardMarkup(row_width=7)
            dates = []
            rows = applications.get_all_date_table()
            for row in rows:
                if row[3] == 0:
                    dates.append(row[1])
            dates = applications.quick_sort_dates(dates)
            buttons = []
            button_date = telebot.types.InlineKeyboardButton(text=dates[0], callback_data='service_date_' + dates[0])
            buttons.append(button_date)
            for i in range(1, len(dates)):
                date = dates[i]
                if date != dates[i - 1]:
                    button_date = telebot.types.InlineKeyboardButton(text=date, callback_data='service_date_' + date)
                    buttons.append(button_date)

            for i in range(0, len(buttons), 7):
                markup.row(*buttons[i:i + 7])
            button_back = telebot.types.InlineKeyboardButton(text = "Назад", callback_data = 'menu')
            markup.add(button_back)
            bot.send_message(function_call.message.chat.id, text, reply_markup=markup)

        elif function_call.data.split('_')[:2] == ['service', 'date']:
            date = function_call.data.split('_')[2]
            markup = telebot.types.InlineKeyboardMarkup(row_width=7)
            if applications.is_busy_date(date):
                text = f'Выберите время записи на {date}'
                rows = applications.get_all_date_table()
                buttons = []
                for i in range(1, len(rows)):
                    date_i = rows[i][1]
                    time = rows[i][2]
                    if date_i == date and rows[i][3] == 0:
                        button_time = telebot.types.InlineKeyboardButton(text=time,
                                                                   callback_data='service_time_' + time + '_' + date)
                        buttons.append(button_time)

                for i in range(0, len(buttons), 7):
                    markup.row(*buttons[i:i + 7])
            else:
                text = 'Эта дата уже занята'
                button = telebot.types.InlineKeyboardButton(text='Назад', callback_data=f'service')
                markup.add(button)
            bot.send_message(function_call.message.chat.id, text, reply_markup=markup)

        elif function_call.data.split('_')[:2] == ['service', 'time']:
            client.state[function_call.message.chat.id] = 'writing_info'
            date = function_call.data.split('_')[3]
            time = function_call.data.split('_')[2]
            record.date = date
            record.time = time
            text = f'Напишите дополнительную информацию о необходимом обслуживании'
            bot.send_message(function_call.message.chat.id, text)

        elif function_call.data == 'service_record':
            client.chat_id = function_call.from_user.id
            if applications.check_record_in_table(record.date, record.time):
                applications.date_sign(record.date, record.time, client.chat_id, record.info)
                text = 'Вы записаны успешно'
            else:
                text = 'Запись уже занята'
            markup = telebot.types.InlineKeyboardMarkup()
            button_back = telebot.types.InlineKeyboardButton(text='Назад', callback_data='menu')
            markup.add(button_back)
            bot.send_message(function_call.message.chat.id, text, reply_markup=markup)


        #Меню администратора
        elif function_call.data == "admin_menu":
            admin_state[function_call.message.chat.id] = "menu"
            text = "Меню"
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            button_client = telebot.types.InlineKeyboardButton(text='Посмотреть всех клиентов',
                                                               callback_data='client_table')
            button_date = telebot.types.InlineKeyboardButton(text='Посмотреть все записи',
                                                             callback_data='register_table')
            button_info = telebot.types.InlineKeyboardButton(text='Добавить дату', callback_data='add_date')
            button_register = telebot.types.InlineKeyboardButton(text='Удалить дату', callback_data='delete_date')
            markup.add(button_client, button_date, button_info, button_register)
            bot.send_message(function_call.message.chat.id, text, reply_markup=markup)

        # Просмотр всех клиентов для администратора
        elif function_call.data == 'client_table':
            admin_state[function_call.message.chat.id] = "watch_all_clients"
            rows = applications.get_all_client_table()
            text = '      Имя      | Номер телефона | Машина \n'
            for row in rows:
                text += row[1] + ' | ' + row[2] + ' | ' + row[3] + '\n'
            bot.send_message(function_call.message.chat.id, text)

        # Просмотр всех записей для администратора
        elif function_call.data == 'register_table':
            admin_state[function_call.message.chat.id] = "watch_all_records"
            text = 'date  | time   | Имя клиента | Номер телефона | info \n'
            rows = applications.dates_to_watch()
            for i in range(0, len(rows)):
                text += rows[i][0] + ' | ' + rows[i][1] + ' | ' + rows[i][2] + ' | ' + rows[i][3] + ' | ' + rows[i][4] + '\n'
            bot.send_message(function_call.message.chat.id, text)

        #Добавление новой записи администратором
        elif function_call.data == 'add_date':
            admin_state[function_call.message.chat.id] = "adding_dates"
            text = 'Напишите дату и свободное время через пробел (пример: 01.01 12:00 13:30): '
            bot.send_message(function_call.message.chat.id, text)

        #Удаление записи администратором
        elif function_call.data == 'delete_date':
            admin_state[function_call.message.chat.id] = "deleting_records"
            text = 'Выберите дату, которую нужно удалить'
            markup = telebot.types.InlineKeyboardMarkup(row_width = 7)
            dates = applications.get_dates()
            buttons = []
            button_date = telebot.types.InlineKeyboardButton(text=dates[0], callback_data='date_' + dates[0])
            buttons.append(button_date)
            for i in range (1, len(dates)):
                date = dates[i]
                if date != dates[i - 1]:
                    button_date = telebot.types.InlineKeyboardButton(text = date, callback_data = 'date_' + date)
                    buttons.append(button_date)

            for i in range(0, len(buttons), 7):
                markup.row(*buttons[i:i + 7])
            bot.send_message(function_call.message.chat.id, text, reply_markup = markup)

        elif function_call.data.split('_')[0] == 'date':
            date = function_call.data.split('_')[1]
            markup = telebot.types.InlineKeyboardMarkup(row_width=7)
            if applications.check_date_in_table(date):
                text = f'Выберите время, которое нужно удалить для {date}'
                rows = applications.get_all_date_table()
                buttons = []
                for i in range(1, len(rows)):
                    date_i = rows[i][1]
                    time = rows[i][2]
                    if date_i == date:
                        print(date, date_i, rows[i])
                        button_time = telebot.types.InlineKeyboardButton(text=time, callback_data='time_' + time + '_' + date)
                        buttons.append(button_time)

                for i in range(0, len(buttons), 7):
                    markup.row(*buttons[i:i + 7])
            else:
                text = 'Эта дата уже удалена'
                button = telebot.types.InlineKeyboardButton(text='Назад', callback_data=f'delete_date')
                markup.add(button)
            bot.send_message(function_call.message.chat.id, text, reply_markup=markup)

        elif function_call.data.split('_')[0] == 'time':
            time = function_call.data.split('_')[1]
            date = function_call.data.split('_')[2]
            if applications.check_record_in_table(date, time):
                text = f'Вы выбрали {date} {time} для удаления'
                button= telebot.types.InlineKeyboardButton(text='Подтвердить', callback_data=f'delete_{date}_{time}')
            else:
                text = 'Эта запись уже удалена'
                button = telebot.types.InlineKeyboardButton(text='Назад', callback_data=f'delete_date')
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(button)
            bot.send_message(function_call.message.chat.id, text, reply_markup = markup)

        elif function_call.data.split('_')[0] == 'delete':
            date = function_call.data.split('_')[1]
            time = function_call.data.split('_')[2]
            if applications.check_record_in_table(date, time):
                applications.delete_by_date_time(date, time)
                text = 'Запись удалена успешно'
            else:
                text = 'Запись уже удалена'
            markup = telebot.types.InlineKeyboardMarkup()
            button_back = telebot.types.InlineKeyboardButton(text='Назад', callback_data='admin_menu')
            markup.add(button_back)
            bot.send_message(function_call.message.chat.id, text, reply_markup = markup)
@bot.message_handler(content_types = ['contact'])
def handle_contact(message):
    text = "Спасибо. Напишите марку и модель вашей машины:"
    if message.contact is not None:
        client.state[message.chat.id] = 'writing_car_info'
        client.phone_number = message.contact.phone_number
    else: text = 'Напишите /start'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands = ['admin'])
def AdminBot(message):
    if message.from_user.id == 866916563:
        admin_state[message.chat.id] = "menu"
        text = "Меню"
        markup = telebot.types.InlineKeyboardMarkup(row_width = 2)
        button_client = telebot.types.InlineKeyboardButton(text = 'Посмотреть всех клиентов', callback_data = 'client_table')
        button_date = telebot.types.InlineKeyboardButton(text = 'Посмотреть все записи', callback_data = 'register_table')
        button_info = telebot.types.InlineKeyboardButton(text = 'Добавить дату', callback_data = 'add_date')
        button_register = telebot.types.InlineKeyboardButton(text = 'Удалить дату', callback_data = 'delete_date')
        markup.add(button_client, button_date, button_info, button_register)
        bot.send_message(message.chat.id, text, reply_markup = markup)


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

    elif client.state.get(message.chat.id) == "writing_info":
        if applications.is_busy_record(record.date, record.time):
            record.info = message.text
            text = f'Вы выбрали {record.date} {record.time}: {record.info}'
            button = telebot.types.InlineKeyboardButton(text='Подтвердить',
                                                        callback_data=f'service_record')
        else:
            text = 'Эта запись уже занята'
            button = telebot.types.InlineKeyboardButton(text='Назад', callback_data=f'service')
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(button)
        bot.send_message(message.chat.id, text, reply_markup=markup)

    #Конец регистрации

    #Изменения одного поля
    elif client.state.get(message.chat.id) == "correct_name":
        client.state[message.chat.id] = 'name_corrected'
        client.client_name = message.text
        applications.update_client_row(client, "client_name")
        text = "Имя изменено"
        markup = telebot.types.InlineKeyboardMarkup()
        button_back = telebot.types.InlineKeyboardButton(text='Назад', callback_data='account')
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
            button_back = telebot.types.InlineKeyboardButton(text='Назад', callback_data='account')
            markup.add(button_back)
            bot.send_message(message.chat.id, text, reply_markup=markup)

    elif client.state.get(message.chat.id) == "correct_car_info":
        client.state[message.chat.id] = 'car_info_corrected'
        client.car_info = message.text
        applications.update_client_row(client, "car_info")
        text = "Информация о машине изменена"
        markup = telebot.types.InlineKeyboardMarkup()
        button_back = telebot.types.InlineKeyboardButton(text='Назад', callback_data='account')
        markup.add(button_back)
        bot.send_message(message.chat.id, text, reply_markup=markup)

    elif client.state.get(message.chat.id) == "change_my_record":
        client.state[message.chat.id] = 'changed_my_record'
        client.car_info = message.text
        applications.update_record(record, "info", message.text)
        text = "Дополнительная информация изменена"
        markup = telebot.types.InlineKeyboardMarkup()
        button_back = telebot.types.InlineKeyboardButton(text='Назад', callback_data='see_records')
        markup.add(button_back)
        bot.send_message(message.chat.id, text, reply_markup=markup)

    elif admin_state.get(message.chat.id) == "adding_dates":
        text = applications.add_records(message.text)
        markup = telebot.types.InlineKeyboardMarkup()
        button_back = telebot.types.InlineKeyboardButton(text='Назад', callback_data='admin_menu')
        markup.add(button_back)
        bot.send_message(message.chat.id, text, reply_markup=markup)

    else:
        text = 'Напишите /start'
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button_send_phone = types.KeyboardButton('/start')
        markup.add(button_send_phone)
        bot.send_message(message.chat.id, text, reply_markup = markup)


bot.polling(none_stop=True, interval=0)