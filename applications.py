import psycopg2

class Client:
    client_name = ''
    phone_number = ''
    car_info = ''
    chat_id = ''
    state = {}

class Record:
    date = ''
    time = ''
    client_id = 0
    info = 'Свободно'

def get_column_names(table_name):
    if table_name == "client_info": return "id, client_name, phone_number, car_info, chat_id", "(%s, %s, %s, %s, %s)"
    return "id, date, time, client_id, info", "(%s, %s, %s, %s, %s)"

def get_connection():
    connection = psycopg2.connect(user="postgres",
                                  password="postgresql",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="work_db")
    return  connection

def add_row(table_name, data):
    try:
        connection = get_connection()
        cur = connection.cursor()
        cur.execute(f"""SELECT * FROM {table_name}""")
        rows = cur.fetchall()
        row = []
        if len(rows) != 0:
            id = rows[len(rows) - 1][0] + 1
        else: id = 1
        row.append(id)
        row += data

        column_names = get_column_names(table_name)
        insert_into = f"""
                INSERT INTO {table_name} ({column_names[0]})
                VALUES {column_names[1]}
                """
        cur.execute(insert_into, row)
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print("Произошла ошибка:", e)
        return False
    finally:
        cur.close()
        connection.close()

def transform_client_data(client):
    data = []
    data.append(client.client_name)
    data.append(client.phone_number)
    data.append(client.car_info)
    data.append(client.chat_id)
    return data

def transform_record_data(record):
    data = []
    data.append(record.date)
    data.append(record.time)
    data.append(record.client_id)
    data.append(record.info)
    return data

def update_client_row(client, field):
    connection = get_connection()
    cur = connection.cursor()
    sql_update_query = f"""Update {'client_info'} set {field} = %s where {'chat_id'} = %s"""
    if field == "client_name":
        cur.execute(sql_update_query, (client.client_name, client.chat_id))
    elif field == "phone_number":
        cur.execute(sql_update_query, (client.phone_number, client.chat_id))
    elif field == "car_info":
        cur.execute(sql_update_query, (client.car_info, client.chat_id))

    connection.commit()

def update_record(record, field, value):
    connection = get_connection()
    cur = connection.cursor()
    sql_update_query = f"""Update {'register_days'} set {field} = %s where {'date'} = %s and {'time'} = %s"""
    cur.execute(sql_update_query, (value, record.date, record.time))
    connection.commit()

def delete_client(client):
    try:
        connection = get_connection()
        cur = connection.cursor()
        table_name = 'client_info'
        column_names = get_column_names(table_name)
        delete_query = f"""DELETE FROM {table_name}
                    WHERE chat_id = {client.chat_id}
                    """
        cur.execute(delete_query)
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print("Произошла ошибка:", e)
        return False
    finally:
        cur.close()
        connection.close()

def delete_row_by_id(table_name, data):
    try:
        connection = get_connection()
        cur = connection.cursor()
        column_names = get_column_names(table_name)
        delete_query = f"""DELETE FROM {table_name}
                    WHERE id = {data}
                    """
        cur.execute(delete_query, data)
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print("Произошла ошибка:", e)
        return False
    finally:
        cur.close()
        connection.close()

def delete_by_date_time(date, time):
    try:
        connection = get_connection()
        cur = connection.cursor()
        table_name = 'register_days'
        delete_query = f"""DELETE FROM {table_name}
                    WHERE date = '{date}' AND time = '{time}'
                    """
        cur.execute(delete_query)
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print("Произошла ошибка:", e)
        return False
    finally:
        cur.close()
        connection.close()

def print_all_table(table_name):
    try:
        connection = get_connection()
        cur = connection.cursor()
        cur.execute(f"""SELECT * FROM {table_name}""")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        return True
    except Exception as e:
        connection.rollback()
        print("Произошла ошибка:", e)
        return False
    finally:
        cur.close()
        connection.close()

def get_all_date_table():
    try:
        table_name = 'register_days'
        connection = get_connection()
        cur = connection.cursor()
        cur.execute(f"""SELECT * FROM {table_name} ORDER BY date, time""")
        rows = cur.fetchall()
        return rows
    except Exception as e:
        connection.rollback()
        print("Произошла ошибка:", e)
        return False
    finally:
        cur.close()
        connection.close()

def get_all_client_table():
    try:
        table_name = 'client_info'
        connection = get_connection()
        cur = connection.cursor()
        cur.execute(f"""SELECT * FROM {table_name} ORDER BY id""")
        rows = cur.fetchall()
        return rows
    except Exception as e:
        connection.rollback()
        print("Произошла ошибка:", e)
        return False
    finally:
        cur.close()
        connection.close()

def get_all_dates():
    rows = get_all_date_table()
    dates = []
    for row in rows:
        date = row[1] + ' ' + row[2]
        dates.append(date)
    return dates

def validate_date(date, time):
    if len(date) == len(time) == 5:
        if date[2] == '.':
            month = date.split('.')[1]
            day = date.split('.')[0]
            if not(1 <= int(month) <= 12 and len(month) == 2): return False
            if not(1 <= int(day) <= 31 and len(day) == 2): return False
        else: return False

        if time[2] == '-':
            str = time[:2]
            str += ':'
            str += time[3:]
            time = str

        if time[2] == ':':
            hour = time.split(':')[0]
            min = time.split(':')[1]
            if not(1 <= int(hour) <= 23 and len(hour) == 2): return False
            if not(0 <= int(min) <= 59 and len(min) == 2): return False
        else: return False
        return True
    return False

def form_record(date, time):
    record = Record
    record.date = date
    record.time = time
    return record

def search_similar_records(record):
    rows = get_all_date_table()
    for row in rows:
        if row[1] == record.date and row[2] == record.time:
            return True
            break
    return False


def add_records(data):
    data = data.split(' ')
    date = data[0]
    f = 0
    for i in range(1, len(data)):
        time = data[i]
        if validate_date(date, time):
            if time[2] == '-':
                str = time[:2]
                str += ':'
                str += time[3:]
                time = str
            record = form_record(date, time)
            if search_similar_records(record):
                return 'Запись уже была добавлена'
            else:
                f = 1
                row = transform_record_data(record)
                add_row('register_days', row)
        else:
            return 'Запись введена некорректно. Попробуйте еще раз'
    if f == 1:
        return 'Запись добавлена успешно'

def dates_to_watch():
    data = []
    dates = get_all_date_table()
    clients = get_all_client_table()
    for date in dates:
        a = []
        a.append(date[1])
        a.append(date[2])
        i = 0
        f = 0
        while i < len(clients):
            if date[3] == clients[i][0]:
                f = 1
                break
            i += 1
        if f == 0:
            a.append('  Нет записи  ')
            a.append(' ' * 35)
        else:
            client = clients[i]
            a.append(client[1])
            a.append(client[2])
        a.append(date[4])
        data.append(a)
    return data

def check_date_in_table(date):
    rows = get_all_date_table()
    f = False
    for row in rows:
        if row[1] == date:
            f = True
    return f

def check_record_in_table(date, time):
    rows = get_all_date_table()
    f = False
    for row in rows:
        if row[1] == date and row[2] == time:
            f = True
    return f

def quick_sort_dates(dates):
    if len(dates) <= 1:
        return dates
    else:
        pivot = dates[0]
        less = [date for date in dates[1:] if compare_dates(date, pivot)]
        greater = [date for date in dates[1:] if not compare_dates(date, pivot)]
        return quick_sort_dates(less) + [pivot] + quick_sort_dates(greater)

def compare_dates(date1, date2):
    day1, month1 = map(int, date1.split('.'))
    day2, month2 = map(int, date2.split('.'))

    if month1 < month2:
        return True
    elif month1 == month2:
        return day1 < day2
    else:
        return False

def get_dates():
    rows = get_all_date_table()
    dates = []
    for row in rows:
        dates.append(row[1])
    return quick_sort_dates(dates)

def date_sign(date, time, chat_id, info):
    rows = get_all_client_table()
    client_id = 0
    for row in rows:
        if row[4] == chat_id:
            client_id = row[0]
    connection = get_connection()
    cur = connection.cursor()
    sql_update_query = f"""Update {'register_days'} set {'client_id'} = %s, {'info'} = %s where {'date'} = %s and {'time'} = %s"""
    cur.execute(sql_update_query, (client_id, info, date, time))
    connection.commit()

def is_busy_record(date, time):
    rows = get_all_date_table()
    for row in rows:
        if row[1] == date and row[2] == time and row[3] != 0:
            return False
    return True

def is_busy_date(date):
    rows = get_all_date_table()
    f = 0
    for row in rows:
        if row[1] == date and row[3] == 0:
            return True
    return False

def get_client_records(client):
    rows = get_all_client_table()
    client_id = 0
    data = []
    for row in rows:
        if row[4] == client.chat_id:
            client_id = row[0]
    rows = get_all_date_table()
    i = 1
    for row in rows:
        if row[3] == client_id:
            data.append([row[1], row[2], row[4]])
            i += 1
    return data
