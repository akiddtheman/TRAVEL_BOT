from aiogram.dispatcher.filters.state import State, StatesGroup

class Tour(StatesGroup):
    ticket_id = State()
    info_about_tour = State()
    info_about_info = State()

class Currency(StatesGroup):
    waiting_for_input = State()