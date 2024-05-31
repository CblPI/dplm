import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from app.manager.event_manager import EventManager, Libowsky
from app.menu.menu_buttons import income

__all__ = [
    'IncomeHandler',
    'income_filters'
]

from app.menu.menu_buttons.menu_income import income_category, income_cancel

event_manager = EventManager()

async def income_filters(msg: types.Message):
    if msg.text.lower() == 'доходы':
        return True
    return False


async def income_category_filters(msg: types.Message):
    if msg.text.lower() == 'категории':
        return True
    return False


class FormIncome(StatesGroup):
    waiting_for_income_name = State()
    waiting_for_balance = State()
    waiting_category_name = State()
    waiting_for_score_name = State()


class FormIncomeDel(StatesGroup):
    waiting_for_income_name = State()


class FormIncomeCatAdd(StatesGroup):
    waiting_for_income_cat_name = State()

class FormIncomeCatDel(StatesGroup):
    waiting_for_income_cat_name_del = State()

class IncomeHandler:

    def __init__(self, event_manager):
        self.event_manager = event_manager

    async def income_handler(self, message: types.Message):
        await message.answer(
            f"Раздел доходов:",
            reply_markup=income
        )

    async def check_income(self, msg: types.Message):
        if msg.text.lower() == 'посмотреть доходы':
            res = await self.event_manager.get_incomes(msg['from']['id'])
            if res is None:
                answer = 'Ничего не найдено.'
            else:
                answer = 'Ваши доходы:'

            await msg.answer(
                answer + '\n' + str(res),
            )

    async def add_income(self, msg: types.Message):
        if msg.text.lower() == 'добавить доход':
            await msg.reply("Введите название дохода:",
                            reply_markup=income_cancel)
            await FormIncome.waiting_for_income_name.set()

    async def delete_income(self, msg: types.Message):
        if msg.text.lower() == 'удалить доход':
            await msg.reply("Введите название дохода:",

                            reply_markup=income_cancel)
            await FormIncomeDel.waiting_for_income_name.set()

    async def get_incomes(self, msg: types.Message):
        if msg.text.lower() == 'посмотреть доходы':
            result = await self.event_manager.get_incomes(msg['from']['id'])
            re = [str(res) + '\n' for res in result]
            await msg.reply(
                f"Доходы: {re}"
            )

    async def income_category(self, msg: types.Message):
        if msg.text.lower() == 'категории дохода':
            await msg.reply(
                "Раздел категории",
                reply_markup=income_category
            )

    async def get_income_category(self, msg: types.Message):
        if msg.text.lower() == 'посмотреть категории доходов':
            result = await self.event_manager.get_income_category(msg['from']['id'])
            await msg.reply(
                f"Категории: {result}"
            )

    async def add_incom_category(self, msg: types.Message):
        if msg.text.lower() == 'добавить категорию расходов':
            await msg.reply(
                f"Введите название категории:"
            )

            await FormIncomeCatAdd.waiting_for_income_cat_name.set()

    async def delete_income_category(self, msg: types.Message):
        if msg.text.lower() == 'удалить категорию доходов':
            await msg.reply(
                f"Введите название категории для удаления",
                reply_markup=income_cancel
            )

            await FormIncomeCatDel.waiting_for_income_cat_name_del.set()

    async def process_del_income_category(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if msg.text.lower() == 'отмена':
                await state.finish()
                await msg.reply(
                    "Операция отменена",
                    reply_markup=income_category
                )
                return

            data['category_name'] = msg.text

            await self.event_manager.del_income_category(
                data['category_name']
            )

            await msg.reply(
                "Категория успешно удалена",
                reply_markup=income_category
            )

            await state.finish()

    async def process_add_income_category(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if msg.text.lower() == 'отмена':
                await state.finish()
                await msg.reply(
                    "Операция отменена",
                    reply_markup=income
                )
                return

            data['category_name'] = msg.text

            await self.event_manager.add_income_category(
                data['category_name']
            )

            await state.finish()

            await msg.reply(
                f"Вы успешно добавили категорию: {data['category_name']}",
                reply_markup=income
            )

    async def process_delete_income_name(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if msg.text.lower() == 'отмена':
                await state.finish()
                await msg.reply(
                    "Операция отменена",
                    reply_markup=income
                )
                return

            data['income_name'] = msg.text

            await self.event_manager.delete_income(data['income_name'], msg['from']['id'])
            await msg.reply(
                f"Вы успешно удалили доход: {data['income_name']}.",
                reply_markup=income
            )

            await state.finish()

    async def process_add_income_name(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if msg.text.lower() == 'отмена':
                await state.finish()
                await msg.reply(
                    "Операция отменена",
                    reply_markup=income
                )
                return
            data['income_name'] = msg.text
            await msg.reply("Теперь введите сумму средств:",
                            reply_markup=income_cancel)

            await FormIncome.next()

    async def process_add_income_balance(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if msg.text.lower() == 'отмена':
                await state.finish()
                await msg.reply(
                    "Операция отменена",
                    reply_markup=income
                )
                return

            data['income_sum'] = msg.text

            await msg.reply(
                "Теперь введите название категории:",
                reply_markup=income_cancel
            )

            await FormIncome.next()

    async def process_add_income_category_name(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if msg.text.lower() == 'отмена':
                await state.finish()
                await msg.reply(
                    "Операция отменена",
                    reply_markup=income
                )
                return

            data['income_category_name'] = msg.text

            await msg.reply("Теперь введите название счета:",
                            reply_markup=income_cancel)

            await FormIncome.next()

    async def process_add_income_score_name(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if msg.text.lower() == 'отмена':
                await state.finish()
                await msg.reply(
                    "Операция отменена",
                    reply_markup=income
                )
                return

            data['income_score_name'] = msg.text

            try:
                result = await self.event_manager.add_new_income(
                    data['income_name'],
                    data['income_sum'],
                    data['income_category_name'],
                    data['income_score_name'],
                    msg['from']['id']

                )

                await msg.reply(f"Вы успешно добавили {data['income_name']}.",
                                reply_markup=income)

                await state.finish()

            except Libowsky as e:
                await msg.reply(
                    f"Ошибка: {e}",
                    reply_markup=income
                )

            except Exception as e:
                await msg.reply("Ошибка.",
                                reply_markup=income
                                )

                await state.finish()
