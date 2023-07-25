from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from information import hotels, culture, attractions, history

from states import Tour
from states import Currency

import database
import states
import requests
import buttons


bot = Bot('TOKEN')
dp = Dispatcher(bot, storage=MemoryStorage())

# Глобальный словарь для хранения ticket_id пользователя
global_dict = {}

# Старт бота
@dp.message_handler(commands=['start'])
async def command_start(message):
    start_text = (f'✨ Здравствуйте, {message.from_user.first_name}! Вас приветствует ваш будущий путеводитель 📱\n\n'
                  f'/help - выдаст вам информацию, которая поможет ориентироваться в моем интерфейсе 📲\n\n'
                  f'/convert - нажмите на эту команду, чтобы конвертировать нужную вам валюту 💶')

    await message.answer(start_text, reply_markup=buttons.main_menu())

# Инструкция по использованию бота
@dp.message_handler(commands=['help'])
async def command_help(message):
    help_text = '• Все туры 🗺 - Краткое описание доступных путёвок. Полное описание есть на нашем сайте "ссылка", где также и оформляется покупка билета 🎫\n\n' \
                '• Мой тур 🗓 - Информация о вашем туре: даты и специальный гид, с помощью которого вы сможете ориентироваться во время отдыха 🏝\n\n' \
                '• Гид 📃 - тут вы сможете узнать:\n\n' \
                'О расписании ресторана в вашем отеле 🍽\n' \
                'Время работы бассейна 🏊‍♂\n' \
                'Информация о достопримечательностях города 🏛\n' \
                'Информация о традициях и культуре города ⛩\n' \
                'Информация об истории страны и города 📜'

    await message.answer(help_text)

# Конвертер валют
@dp.message_handler(commands=['convert'])
async def start_conversion(message):
    await message.answer("Введите сумму и название валюты в формате: <сумма> <валюта_из> <валюта_в>")

    # Переход на этап получения данных для конвертации
    await Currency.waiting_for_input.set()

# Конвертация валют
@dp.message_handler(state=states.Currency.waiting_for_input)
async def process_conversion(message, state=states.Currency.waiting_for_input):
    # Подключение к API Exchange Rate
    def get_exchange_rate(base_currency, target_currency):
        url = f'https://api.exchangerate-api.com/v4/latest/{base_currency}'
        # GET запрос к API для получения данных о курсе обмена
        response = requests.get(url)
        # Преобразование ответа в формат JSON
        data = response.json()
        # Извлечение курса обмена для целевой валюты (target_currency)
        exchange_rate = data['rates'][target_currency]
        return exchange_rate

    input_text = message.text.strip()
    input_args = input_text.split()

    if len(input_args) != 3:
        await message.answer('Неверный формат ввода данных. Пожалуйста, используйте формат <сумма> <валюта_из> <валюта_в>')
        return

    amount = float(input_args[0])
    base_currency = input_args[1].upper()
    target_currency = input_args[2].upper()

    # Получение курса валют
    exchange_rate = get_exchange_rate(base_currency, target_currency)

    # Выполнение конвертации
    converted_amount = amount * exchange_rate

    # Отправка результата пользователю
    await message.answer(f'{amount} {base_currency} = {converted_amount} {target_currency}')

    await state.finish()

# Запрос получения айди тура
@dp.callback_query_handler()
async def login(callback_query: types.CallbackQuery):
    if callback_query.data == 'my_tour':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Введите пожалуйста ID вашего билета 🎫\n\n'
                             'Для того, чтобы узнать ID билета нужно зайди в свой аккаунт на нашем сайте "ссылка"', reply_markup=ReplyKeyboardRemove())
    if callback_query.data == 'all_tours':
        await bot.send_message(chat_id=callback_query.from_user.id, text='У нас путевки в такие страны, как Стамбул, Сингапур, Каир, Куала-лумпур, Москва и Дубаи. Вот краткий обзор на каждый из них 🔽\n\n'
                                                                         'Дубай – город и эмират на побережье Персидского залива в Объединенных Арабских Эмиратах, который славится своими роскошными магазинами, ультрасовременной архитектурой, ресторанами и ночными клубами. '
                                                                         'Силуэт города формируют бесчисленные небоскребы, в том числе Бурдж-Халифа высотой 830 метров.\n\n'
                                                                         'Стамбул – крупнейший город Турции на берегах пролива Босфор, который разделяет его на европейскую и азиатскую части. В Старом городе сохранились здания различных исторических эпох. '
                                                                         'В районе Султанахмет расположены возведенный римлянами Ипподром, где в течение многих столетий проводили гонки на колесницах, и Египетский обелиск.\n\n'
                                                                         'Куала-Лумпур – современная столица Малайзии, в силуэте которой доминирует небоскреб "Башни Петронас". Он представляет собой башни-близнецы из стекла и стали высотой 451 метр, и в его архитектуре прослеживаются исламские мотивы. '
                                                                         'Башни соединены крытым переходом, а на их вершине для посетителей открыты смотровые площадки.\n\n'
                                                                         'Каир – многолюдная столица Египта на реке Нил. В Гизе, пригороде Каира, находятся всемирно известные пирамиды и Большой сфинкс, '
                                                                         'датируемый XXVI в. до н. э. С Каирской телебашни высотой 187 м, возведенной в зеленом районе Замалек на острове Гезира, открывается великолепный вид на город.\n\n'
                                                                         'Сингапур – многонациональный город-государство, мировой финансовый центр. Он расположен на острове и граничит с южной частью Малайзии. Сердцем колониального центра города является поле для крикета Паданг, созданное в 1830-е годы. '
                                                                         'Оно окружено величественными зданиями, среди которых городская ратуша с 18 коринфскими колоннами.\n\n'
                                                                         'Москва – столица России, многонациональный город на Москве-реке в западной части страны. За северо-восточной стеной Кремля раскинулась Красная площадь – символический центр России. '
                                                                         'Здесь можно увидеть Мавзолей В. И. Ленина, Государственный исторический музей и собор Василия Блаженного с красочными луковичными куполами.')


    # Переход к получению айди тура
    await Tour.ticket_id.set()

# Процесс получения айди тура
@dp.message_handler(state=Tour.ticket_id)
async def get_login(message):
    # Получение введенного пользователем ticket_id
    ticket_id = message.text

    # Проверка есть-ли ticket_id в базе данных
    if database.check_ticket_id_in_database(ticket_id):
        # Сохранение ticket_id в глобальном словаре
        global_dict[message.from_user.id] = ticket_id
        await message.answer(f'{message.from_user.first_name}, вы успешно вошли в аккаунт своего тура!\n\n'
                             f'В кнопках ниже вы можете выбрать ваши последующие действия ⬇', reply_markup=buttons.mytour())
    else:
        await message.answer('Тур с указанным ID не найден. Посмотрите и проверьте ID вашего тура на нашем сайте "ссылка"')

    await Tour.info_about_tour.set()

# Информация о туре
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'info_about_tour', state=Tour.info_about_tour)
async def info_about_tour(callback_query: types.CallbackQuery):
    # Получение сохраненного ticket_id пользователя из словаря
    ticket_id = global_dict.get(callback_query.from_user.id)

    if ticket_id and database.check_ticket_id_in_database(ticket_id):
        country = database.check_country_of_ticket_id(ticket_id)
        if country == 'Стамбул':
            data = database.sql.execute('SELECT * FROM info_turkey').fetchone()
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ниже представлена информация о вашем туре ⬇\n\n"
                                                                             f"🇹🇷 Страна/Город - {data[0]}/{data[1]}\n"
                                                                             f"📆 Дата - {data[2]}\n"
                                                                             f"🛫 Место отправки - {data[4]}\n"
                                                                             f"🕐 Время - {data[3]}\n"
                                                                             f"🛬 Место посадки - {data[5]}\n"
                                                                             f"🕐 Время - {data[6]}\n"
                                                                             f"🏨 Отель - {data[7]}\n"
                                                                             f"💷 Валюта - {data[8]}\n\n"
                                                                             f"Обратный рейс:\n\n"
                                                                             f"📆 Дата -{data[11]} \n"
                                                                             f"🛫 Место отправки - {data[9]}\n"
                                                                             f"🕐 Время - {data[12]}\n"
                                                                             f"🛬 Место посадки - {data[10]}\n"
                                                                             f"🕐 Время - {data[13]}\n")
        elif country == 'Каир':
            data = database.sql.execute('SELECT * FROM info_egypt').fetchone()
            await bot.send_message(chat_id=callback_query.from_user.id,text=f"Ниже представлена информация о вашем туре ⬇\n\n"
                                                                            f"🇪🇬 Страна/Город - {data[0]}/{data[1]}\n"
                                                                            f"📆 Дата - {data[2]}\n"
                                                                            f"🛫 Место отправки - {data[4]}\n"
                                                                            f"🕐 Время - {data[3]}\n"
                                                                            f"🛬 Место посадки - {data[5]}\n"
                                                                            f"🕐 Время - {data[6]}\n"
                                                                            f"🏨 Отель - {data[7]}\n"
                                                                            f"💷 Валюта - {data[8]}\n\n"
                                                                            f"Обратный рейс:\n\n"
                                                                            f"📆 Дата -{data[11]} \n"
                                                                            f"🛫 Место отправки - {data[9]}\n"
                                                                            f"🕐 Время - {data[12]}\n"
                                                                            f"🛬 Место посадки - {data[10]}\n"
                                                                            f"🕐 Время - {data[13]}\n")

        elif country == 'Сингапур':
            data = database.sql.execute('SELECT * FROM info_singapore').fetchone()
            await bot.send_message(chat_id=callback_query.from_user.id,text=f"Ниже представлена информация о вашем туре ⬇\n\n"
                                                                            f"🇸🇬 Страна/Город - {data[0]}/{data[1]}\n"
                                                                            f"📆 Дата - {data[2]}\n"
                                                                            f"🛫 Место отправки - {data[4]}\n"
                                                                            f"🕐 Время - {data[3]}\n"
                                                                            f"🛬 Место посадки - {data[5]}\n"
                                                                            f"🕐 Время - {data[6]}\n"
                                                                            f"🏨 Отель - {data[7]}\n"
                                                                            f"💷 Валюта - {data[8]}\n\n"
                                                                            f"Обратный рейс:\n\n"
                                                                            f"📆 Дата -{data[11]} \n"
                                                                            f"🛫 Место отправки - {data[9]}\n"
                                                                            f"🕐 Время - {data[12]}\n"
                                                                            f"🛬 Место посадки - {data[10]}\n"
                                                                            f"🕐 Время - {data[13]}\n")
        elif country == 'Москва':
            data = database.sql.execute('SELECT * FROM info_russia').fetchone()
            await bot.send_message(chat_id=callback_query.from_user.id,text=f"Ниже представлена информация о вашем туре ⬇\n\n"
                                                                            f"🇷🇺 Страна/Город - {data[0]}/{data[1]}\n"
                                                                            f"📆 Дата - {data[2]}\n"
                                                                            f"🛫 Место отправки - {data[4]}\n"
                                                                            f"🕐 Время - {data[3]}\n"
                                                                            f"🛬 Место посадки - {data[5]}\n"
                                                                            f"🕐 Время - {data[6]}\n"
                                                                            f"🏨 Отель - {data[7]}\n"
                                                                            f"💷 Валюта - {data[8]}\n\n"
                                                                            f"Обратный рейс:\n\n"
                                                                            f"📆 Дата -{data[11]} \n"
                                                                            f"🛫 Место отправки - {data[9]}\n"
                                                                            f"🕐 Время - {data[12]}\n"
                                                                            f"🛬 Место посадки - {data[10]}\n"
                                                                            f"🕐 Время - {data[13]}\n")

        elif country == 'Куала-лумпур':
            data = database.sql.execute('SELECT * FROM info_malaysia').fetchone()
            await bot.send_message(chat_id=callback_query.from_user.id,text=f"Ниже представлена информация о вашем туре ⬇\n\n"
                                                                            f"🇲🇾 Страна/Город - {data[0]}/{data[1]}\n"
                                                                            f"📆 Дата - {data[2]}\n"
                                                                            f"🛫 Место отправки - {data[4]}\n"
                                                                            f"🕐 Время - {data[3]}\n"
                                                                            f"🛬 Место посадки - {data[5]}\n"
                                                                            f"🕐 Время - {data[6]}\n"
                                                                            f"🏨 Отель - {data[7]}\n"
                                                                            f"💷 Валюта - {data[8]}\n\n"
                                                                            f"Обратный рейс:\n\n"
                                                                            f"📆 Дата -{data[11]} \n"
                                                                            f"🛫 Место отправки - {data[9]}\n"
                                                                            f"🕐 Время - {data[12]}\n"
                                                                            f"🛬 Место посадки - {data[10]}\n"
                                                                            f"🕐 Время - {data[13]}\n")
        elif country == 'Дубаи':
            data = database.sql.execute('SELECT * FROM info_uae').fetchone()
            await bot.send_message(chat_id=callback_query.from_user.id,text=f"Ниже представлена информация о вашем туре ⬇\n\n"
                                                                            f"🇦🇪 Страна/Город - {data[0]}/{data[1]}\n"
                                                                            f"📆 Дата - {data[2]}\n"
                                                                            f"🛫 Место отправки - {data[4]}\n"
                                                                            f"🕐 Время - {data[3]}\n"
                                                                            f"🛬 Место посадки - {data[5]}\n"
                                                                            f"🕐 Время - {data[6]}\n"
                                                                            f"🏨 Отель - {data[7]}\n"
                                                                            f"💷 Валюта - {data[8]}\n\n"
                                                                            f"Обратный рейс:\n\n"
                                                                            f"📆 Дата -{data[11]} \n"
                                                                            f"🛫 Место отправки - {data[9]}\n"
                                                                            f"🕐 Время - {data[12]}\n"
                                                                            f"🛬 Место посадки - {data[10]}\n"
                                                                            f"🕐 Время - {data[13]}\n")
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text='Информация по туру еще не составлена, пока разработчики работают над этим вы моежете посмотреть обзор на наши остальные путевки 🔽')

    await Tour.info_about_tour.set()

# Отдел Гид
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'guide', state=Tour.info_about_tour)
async def info_about_tour(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id, text="Добро пожаловать в отдел гид 📑\n\n"
                                                                     "Ниже вы можете выбрать то, что вам интересно 🔽", reply_markup=buttons.gid())

    await Tour.info_about_info.set()

# Информация об отеле
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'hotel', state=Tour.info_about_info)
async def info_about_hotels(callback_query: types.CallbackQuery):
    # Получение сохраненного ticket_id пользователя из словаря
    ticket_id = global_dict.get(callback_query.from_user.id)

    if ticket_id and database.check_ticket_id_in_database(ticket_id):
        country = database.check_country_of_ticket_id(ticket_id)
        if country == 'Стамбул':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{hotels.hotel_for_turkey}")
        elif country == 'Каир':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{hotels.hotel_for_egypt}")
        elif country == 'Сингапур':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{hotels.hotel_for_singapore}")
        elif country == 'Москва':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{hotels.hotel_for_russia}")
        elif country == 'Малайзия':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{hotels.hotel_for_malaysia}")
        elif country == 'Дубаи':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{hotels.hotel_for_uae}")


# Информация об истории страны/города
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'history', state=Tour.info_about_info)
async def info_about_history(callback_query: types.CallbackQuery):
    # Получение сохраненного ticket_id пользователя из словаря
    ticket_id = global_dict.get(callback_query.from_user.id)

    if ticket_id and database.check_ticket_id_in_database(ticket_id):
        country = database.check_country_of_ticket_id(ticket_id)
        if country == 'Стамбул':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{history.history_for_turkey}")
        elif country == 'Каир':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{history.history_for_egypt}")
        elif country == 'Сингапур':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{history.history_for_singapore}")
        elif country == 'Москва':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{history.history_for_russia}")
        elif country == 'Малайзия':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{history.history_for_malaysia}")
        elif country == 'Дубаи':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{history.history_for_uae}")


# Информация о культуре страны/города
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'culture', state=Tour.info_about_info)
async def info_about_culture(callback_query: types.CallbackQuery):
    # Получение сохраненного ticket_id пользователя из словаря
    ticket_id = global_dict.get(callback_query.from_user.id)

    if ticket_id and database.check_ticket_id_in_database(ticket_id):
        country = database.check_country_of_ticket_id(ticket_id)
        if country == 'Стамбул':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{culture.culture_of_turkey}")
        elif country == 'Каир':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{culture.culture_of_egypt}")
        elif country == 'Сингапур':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{culture.culture_of_singapore}")
        elif country == 'Москва':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{culture.culture_of_russia}")
        elif country == 'Малайзия':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{culture.culture_of_malaysia}")
        elif country == 'Дубаи':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{culture.culture_of_uae}")


# Информация о достопримечательностях города
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'attraction', state=Tour.info_about_info)
async def info_about_attractions(callback_query: types.CallbackQuery, state=Tour.info_about_info):
    # Получение сохраненного ticket_id пользователя из словаря
    ticket_id = global_dict.get(callback_query.from_user.id)

    if ticket_id and database.check_ticket_id_in_database(ticket_id):
        country = database.check_country_of_ticket_id(ticket_id)
        if country == 'Стамбул':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{attractions.attractions_of_turkey}")
        elif country == 'Каир':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{attractions.attractions_of_egypt}")
        elif country == 'Сингапур':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{attractions.attractions_of_singapore}")
        elif country == 'Москва':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{attractions.attractions_of_russia}")
        elif country == 'Малайзия':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{attractions.attractions_of_malaysia}")
        elif country == 'Дубаи':
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"{attractions.attractions_of_uae}")


executor.start_polling(dp)
