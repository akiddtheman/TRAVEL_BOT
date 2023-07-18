from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    all_tours = InlineKeyboardButton(text='Все туры', callback_data='all_tours')
    my_tour = InlineKeyboardButton(text='Мой тур', callback_data='my_tour')

    kb.add(all_tours, my_tour)

    return kb

def mytour():
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    info_about_tour = InlineKeyboardButton('Информация о туре', callback_data='info_about_tour')
    guide = InlineKeyboardButton('Гид', callback_data='guide')

    kb.add(info_about_tour, guide)

    return kb

def gid():
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    hotel = InlineKeyboardButton('Отель', callback_data='hotel')
    attraction = InlineKeyboardButton('Достопримечательности', callback_data='attraction')
    culture = InlineKeyboardButton('Культура', callback_data='culture')
    history = InlineKeyboardButton('История', callback_data='history')

    kb.add(hotel, attraction, culture, history)

    return kb


















