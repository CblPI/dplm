
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from app.manager.event_manager import EventManager
from app.menu.menu_buttons.menu_credit import credit, credit_cancel
from app.menu.menu_buttons.menu_score import score, cancel

class FormCreditAdd(StatesGroup):
    """Создаем форму для последовательного заполнения данных."""

    waiting_for_credit_name = State()
    waiting_for_credit_percent = State()
    waiting_for_credit_start_date = State()
    waiting_for_credit_end_date = State()
    waiting_for_credit_balance = State()
    waiting_for_credit_score = State()


class FormCreditDel(StatesGroup):
    """Форма для удаления кредита."""

    waiting_for_credit_name = State()


class CreditHandler:
    """Класс для работы с кредитом"""

    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager

    @staticmethod
    async def main_credit_handler(msg: types.Message):
        if msg.text.lower() == 'кредиты':
            await msg.reply(
                "Раздел кредитов: ",
                reply_markup=credit
            )
    @staticmethod
    async def __cancel_action(msg, state):
        await state.finish()
        await msg.reply(
            "Операция отменена",
            reply_markup=credit
        )
        return

    async def get_credit(self, msg: types.Message):
        if msg.text.lower() == 'посмотреть кредиты':
            result = await self.event_manager.get_credits(msg['from']['id'])

            await msg.answer(
                text=f"Ваши кредиты: {result}",
                reply_markup=credit
            )

    async def set_credit(self, msg: types.Message):
        """Внесение нового кредита/ипотеки/итд."""

        if msg.text.lower() == 'добавить кредит':
            await msg.reply(
                text="Введите наименование банка:",
                reply_markup=credit_cancel
            )
            await FormCreditAdd.waiting_for_credit_name.set()


    async def del_credit(self, msg: types.Message):
        """Удаление кредита по названию."""

        if msg.text.lower() == 'удалить кредит':
            await msg.reply(
                text="Введите наименование банка:",
                reply_markup=credit_cancel
            )

            await FormCreditDel.waiting_for_credit_name.set()


    # PROCESS SET METHODS

    async def process_set_credit_name(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if msg.text.lower() == 'отмена':
                return await self.__cancel_action(msg, state)

            data['credit_name'] = msg.text

            await msg.reply(
                text="Теперь введите процент ставки:",
                reply_markup=credit_cancel
            )

            await FormCreditAdd.next()

    async def process_set_credit_percent(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if msg.text.lower() == 'отмена':
                return await self.__cancel_action(msg, state)

            data['credit_percent'] = msg.text

            await msg.reply(
                text="Теперь введите дату начала кредита:",
                reply_markup=credit_cancel
            )

            await FormCreditAdd.next()

    async def process_set_credit_start_date(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if msg.text.lower() == 'отмена':
                return await self.__cancel_action(msg, state)

            data['credit_start'] = msg.text

            await msg.reply(
                text="Теперь введите дату окончания кредита:",
                reply_markup=credit_cancel
            )

            await FormCreditAdd.next()

    async def process_set_credit_end_date(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if msg.text.lower() == 'отмена':
                return await self.__cancel_action(msg, state)

            data['credit_end'] = msg.text

            await msg.reply(
                text="Теперь введите сумму кредита:",
                reply_markup=credit_cancel
            )

            await FormCreditAdd.next()

    async def process_set_credit_balance(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if msg.text.lower() == 'отмена':
                return await self.__cancel_action(msg, state)

            data['credit_balance'] = msg.text

            await msg.reply(
                text="Теперь введите название счета:",
                reply_markup=credit_cancel
            )

            await FormCreditAdd.next()

    async def process_set_credit_score(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if msg.text.lower() == 'отмена':
                return await self.__cancel_action(msg, state)

            data['credit_score'] = msg.text

            try:
                await self.event_manager.set_credit(
                    data['credit_name'],
                    data['credit_percent'],
                    data['credit_start'],
                    data['credit_end'],
                    data['credit_balance'],
                    data['credit_score'],
                    msg['from']['id']
                )

                await msg.reply(
                    text="Кредит успешно добавлен!:",
                    reply_markup=credit
                )

            except Exception as e:
                print(e)

                await state.finish()

            await state.finish()

    # PROCESS DEL METHODS

    async def process_del_credit_name(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if msg.text.lower() == 'отмена':
                return await self.__cancel_action(msg, state)

            data['credit_name'] = msg.text

            try:
                await self.event_manager.del_credit(
                    data['credit_name'],
                    msg['from']['id']
                )

                await msg.reply(
                    text="Кредит успешно удален!:",
                    reply_markup=credit
                )

            except Exception as e:
                print(e)

                await state.finish()

            await state.finish()