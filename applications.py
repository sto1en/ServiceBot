import psycopg2

def get_column_names(table_name):
    if table_name == "client_info": return "id, client_name, phone_number, car_info", "(%s, %s, %s, %s)"
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

def delete_by_date_time(table_name, data):
    try:
        connection = get_connection()
        cur = connection.cursor()
        column_names = get_column_names(table_name)
        delete_query = f"""DELETE FROM {table_name}
                    WHERE date = '{data[0]}' AND time = '{data[1]}'
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

def validate_date(data):
    date = data[0]
    f1 = f2 = 0
    if date[2] == '.':
        month = date.split('.')[1]
        day = date.split('.')[0]
        if not(1 <= int(month) <= 12 and len(month) == 2): return False
        if not(1 <= int(day) <= 31 and len(day) == 2): return False
    else: return False

    time = data[1]
    if time[2] == ':':
        hour = time.split(':')[0]
        min = time.split(':')[1]
        if not(1 <= int(hour) <= 23 and len(hour) == 2): return False
        if not(0 <= int(min) <= 59 and len(min) == 2): return False
    else: return False
    return True

def transform_date_to_add(date):
    date = date.split(' ')
    data = []
    for i in range(1, len(date)):
        a = []
        a.append(date[0])
        a.append(date[i])
        if not(validate_date(a)): return False
        a.append(0)
        a.append('Свободно')
        data.append(a)
    return data

def transform_date_to_delete(date):
    date = date.split(' ')
    data = []
    for i in range(1, len(date)):
        data.append(date[0])
        data.append(date[i])
        if not(validate_date(data)): return False
    return data

def add_rows(table_name, data):
    for i in range(0,len(data)):
        func = add_row(table_name, data[i])
        if not func:
            return False
    return True

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

def check_date_in_table(dates):
    table = get_all_date_table()
    for date in dates:
        day = date[0]
        time = date[1]
        for row in table:
            if row[1] == day and row[2] == time:
                return False
    return True

