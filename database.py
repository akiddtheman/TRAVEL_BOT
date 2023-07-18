import sqlite3

connection = sqlite3.connect('travel.db')
sql = connection.cursor()

# sql.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);')
# sql.execute('CREATE TABLE tours (ticket_id INTEGER PRIMARY KEY AUTOINCREMENT);')
# sql.execute('CREATE TABLE countries (turkey TEXT, singapore TEXT, egypt TEXT, uae TEXT, russia TEXT, malaysia TEXT);')
# sql.execute('CREATE TABLE info_turkey (country TEXT, city TEXT,
#             'date1 DATE, time1 TIME, '
#             'airport1 TEXT, airport2 TEXT, '
#             'time2 TIME,'
#             'hotel TEXT, currency TEXT,'
#             'airport3 TEXT, airport4 TEXT,'
#             'date2 DATE, time3 TIME, time4 TIME);')
# sql.execute('CREATE TABLE info_singapore (country TEXT, city TEXT, '
#             'date1 DATE, time1 TIME, '
#             'airport1 TEXT, airport2 TEXT, '
#             'time2 TIME,'
#             'hotel TEXT, currency TEXT,'
#             'airport3 TEXT, airport4 TEXT,'
#             'date2 DATE, time3 TIME, time4 TIME);')
# sql.execute('CREATE TABLE info_egypt (country TEXT, city TEXT, '
#             'date1 DATE, time1 TIME, '
#             'airport1 TEXT, airport2 TEXT, '
#             'time2 TIME,'
#             'hotel TEXT, currency TEXT,'
#             'airport3 TEXT, airport4 TEXT,'
#             'date2 DATE, time3 TIME, time4 TIME);')
# sql.execute('CREATE TABLE info_uae (country TEXT, city TEXT, '
#             'date1 DATE, time1 TIME, '
#             'airport1 TEXT, airport2 TEXT, '
#             'time2 TIME,'
#             'hotel TEXT, currency TEXT,'
#             'airport3 TEXT, airport4 TEXT,'
#             'date2 DATE, time3 TIME, time4 TIME);')
# sql.execute('CREATE TABLE info_russia (country TEXT, city TEXT, '
#             'date1 DATE, time1 TIME, '
#             'airport1 TEXT, airport2 TEXT, '
#             'time2 TIME,'
#             'hotel TEXT, currency TEXT,'
#             'airport3 TEXT, airport4 TEXT,'
#             'date2 DATE, time3 TIME, time4 TIME);')
# sql.execute('CREATE TABLE info_malaysia (country TEXT, city TEXT, '
#             'date1 DATE, time1 TIME, '
#             'airport1 TEXT, airport2 TEXT, '
#             'time2 TIME,'
#             'hotel TEXT, currency TEXT,'
#             'airport3 TEXT, airport4 TEXT,'
#             'date2 DATE, time3 TIME, time4 TIME);')

# Функция для проверки ticket_id в базе данных
def check_ticket_id_in_database(ticket_id):
    connection = sqlite3.connect('travel.db')
    sql = connection.cursor()

    checker_ticket_id = sql.execute('SELECT ticket_id FROM tours WHERE ticket_id=?;', (ticket_id,))
    if checker_ticket_id.fetchone():
        return True
    else:
        return False

def check_country_of_ticket_id(ticket_id):
    connection = sqlite3.connect('travel.db')
    sql = connection.cursor()

    countries = ['turkey', 'singapore', 'egypt', 'uae', 'russia', 'malaysia']
    for country in countries:
        checker_ticket_id = sql.execute(f'SELECT {country} FROM countries WHERE {country}=?;', (ticket_id,))
        if checker_ticket_id.fetchone():
            if country == 'turkey':
                return 'Стамбул'
            elif country == 'egypt':
                return 'Каир'
            elif country == 'singapore':
                return 'Сингапур'
            elif country == 'uae':
                return "Дубаи"
            elif country == 'russia':
                return 'Москва'
            elif country == 'malaysia':
                return 'Куала-лумупр'
            else:
                return country

    return None


# def get_info_about_tours(ticket_id):
#     connection = sqlite3.connect('travel.db')
#     sql = connection.cursor()
#
#     get_info = sql.execute('SELECT turkey FROM info_about_tours WHERE turkey=?;', (ticket_id,))
#
#     return get_info.fetchone()



# sql.execute('SELECT * FROM info_about_tours;')
# result = sql.fetchall()
# print(result)

