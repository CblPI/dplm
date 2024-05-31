import logging

from aiogram import types

from app.menu.menu_buttons import on_start

LOG = logging.getLogger(__name__)


__all__ = [
    'send_welcome',
    'on_start_filters'
]


msgs_map = {
    'start': 'Здравствуйте! Укажите что вы хотите сделать:',
    '/start': 'Здравствуйте! Укажите что вы хотите сделать:',
    'начало': 'Вы в начале.',
}


async def on_start_filters(msg: types.Message):
    if msg.text.lower() in msgs_map:
        return True
    return False


async def send_welcome(message: types.Message):
    await message.answer(
        text=msgs_map[message.text.lower()],
        reply_markup=on_start
    )

