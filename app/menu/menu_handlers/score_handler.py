from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from app.manager.event_manager import EventManager
from app.menu.menu_buttons.menu_score import score, cancel

event_manager = EventManager()


async def score_handler(msg: types.Message):
    if msg.text.lower() == 'счет':
        await msg.answer(
            "Счета:",
            reply_markup=score
        )


class Form(StatesGroup):
    waiting_for_account_name = State()
    waiting_for_account_balance = State()


class FormDel(StatesGroup):
    waiting_for_account_name_del = State()


async def delete_score(msg: types.Message):
    if msg.text.lower() == 'удалить счет':

        scores = await event_manager.get_user_score(msg['from']['id'])

        await msg.reply(
            f"Ваши счета: {scores} ",
            reply_markup=score
        )

        await msg.reply("Введите название счета:",
                        reply_markup=cancel)

        await FormDel.waiting_for_account_name_del.set()


async def get_score(msg: types.Message):
    if msg.text.lower() == 'мои счета':
        try:
            result = await event_manager.get_user_score(msg['from']['id'])

            await msg.reply(
                f"Ваши счета: {result} ",
                reply_markup=score
            )

        except Exception as e:
            pass


async def proces_delete_score(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if msg.text.lower() == 'отмена':
            await state.finish()
            await msg.reply(
                "Операция отменена",
                reply_markup=score
            )
            return

        data['account_name'] = msg.text
        await event_manager.del_user_score(msg['from']['id'], data['account_name'])

        await msg.reply(
            text=f"Данные о счете: {data['account_name']} удалены",
            reply_markup=score
        )
        await state.finish()


async def add_score(msg: types.Message):
    if msg.text.lower() == 'добавить счет':

        await msg.reply("Введите название счета:",
                        reply_markup=cancel)
        await Form.waiting_for_account_name.set()


async def process_account_name(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if msg.text.lower() == 'отмена':
            await state.finish()
            await msg.reply(
                "Операция отменена",
                reply_markup=score
            )
            await state.finish()
            return
        data['account_name'] = msg.text
    await msg.reply("Теперь введите сумму на счете:",
                    reply_markup=cancel)

    await Form.next()


async def process_account_balance(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if msg.text.lower() == 'отмена':
            await state.finish()
            await msg.reply(
                "Операция отменена",
                reply_markup=score
            )
            return

        data['account_balance'] = msg.text

    try:
        await event_manager.insert_new_score(
            msg['from']['id'],
            data['account_name'],
            data['account_balance']
        )
    except Exception as e:
        await msg.reply(
            text=f"Возникла ошибка пожалуйста попробуйте позже.",
            reply_markup=score
        )

        await state.finish()
        return

    await msg.reply(
        text=f"Данные сохранены: Название счета - {data['account_name']}, Сумма - {data['account_balance']}",
        reply_markup=score
    )

    await state.finish()


async def cancel_operation(msg: types.Message):
    await msg.reply(
        text=f"Операция отменена!",
        reply_markup=score
    )





