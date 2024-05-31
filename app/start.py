import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils import executor
from aiogram import types
import app.menu.menu_handlers as handler
from app.manager.event_manager import EventManager
from app.menu.menu_handlers.credit_handlers import CreditHandler, FormCreditAdd, FormCreditDel
from app.menu.menu_handlers.handlers_income import income_filters, income_category_filters, IncomeHandler, FormIncome, \
    FormIncomeDel, FormIncomeCatAdd, FormIncomeCatDel
from app.menu.menu_handlers.main_handlers import on_start_filters
from app.menu.menu_handlers.score_handler import score_handler, add_score, Form, process_account_name, \
    process_account_balance, get_score, delete_score, FormDel, proces_delete_score

API_TOKEN = 'YOUR_API_TOKEN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token="5976410534:AAFfz--gi__ylH8INMBeblPgW_XrUBzaOHU")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.message_handlers.once = False


logging.basicConfig(level=logging.INFO)


def register_credit_handlers(event_manager: EventManager):
    """Регестрируем обработчики кредитных операций."""

    credit_h = CreditHandler(event_manager)

    dp.register_message_handler(
        credit_h.main_credit_handler
    )

    dp.register_message_handler(
        credit_h.set_credit
    )

    dp.register_message_handler(
        credit_h.del_credit
    )

    dp.register_message_handler(
        credit_h.get_credit
    )

    dp.register_message_handler(
        credit_h.process_del_credit_name,
        state=FormCreditDel.waiting_for_credit_name
    )

    dp.register_message_handler(
        credit_h.process_set_credit_name,
        state=FormCreditAdd.waiting_for_credit_name
    )
    dp.register_message_handler(
        credit_h.process_set_credit_percent,
        state=FormCreditAdd.waiting_for_credit_percent
    )
    dp.register_message_handler(
        credit_h.process_set_credit_start_date,
        state=FormCreditAdd.waiting_for_credit_start_date
    )
    dp.register_message_handler(
        credit_h.process_set_credit_end_date,
        state=FormCreditAdd.waiting_for_credit_end_date
    )
    dp.register_message_handler(
        credit_h.process_set_credit_balance,
        state=FormCreditAdd.waiting_for_credit_balance
    )
    dp.register_message_handler(
        credit_h.process_set_credit_score,
        state=FormCreditAdd.waiting_for_credit_score
    )

def register_income_handlers(event_manager: EventManager):

    income_h = IncomeHandler(event_manager)

    dp.register_message_handler(
        income_h.income_handler,
        income_filters
    )

    dp.register_message_handler(
        income_h.income_category,
    )

    dp.register_message_handler(
        income_h.check_income
    )

    dp.register_message_handler(
        income_h.process_add_income_category,
        state=FormIncomeCatAdd.waiting_for_income_cat_name
    )

    dp.register_message_handler(
        income_h.delete_income_category
    )

    dp.register_message_handler(
        income_h.process_del_income_category,
        state=FormIncomeCatDel.waiting_for_income_cat_name_del
    )

    dp.register_message_handler(
        income_h.add_incom_category
    )

    dp.register_message_handler(
        income_h.add_income
    )

    dp.register_message_handler(
        income_h.process_add_income_name,
        state=FormIncome.waiting_for_income_name
    )

    dp.register_message_handler(
        income_h.process_add_income_balance,
        state=FormIncome.waiting_for_balance
    )

    dp.register_message_handler(
        income_h.process_add_income_category_name,
        state=FormIncome.waiting_category_name
    )

    dp.register_message_handler(
        income_h.process_add_income_score_name,
        state=FormIncome.waiting_for_score_name
    )

    dp.register_message_handler(
        income_h.delete_income
    )

    dp.register_message_handler(
        income_h.process_delete_income_name,
        state=FormIncomeDel.waiting_for_income_name
    )

    dp.register_message_handler(
        income_h.get_income_category,
    )

def register_handlers():

    event_manager = EventManager()

    register_income_handlers(event_manager)

    register_credit_handlers(event_manager)

    dp.register_message_handler(
        handler.send_welcome,
        on_start_filters
    )

    dp.register_message_handler(
        score_handler
    )

    dp.register_message_handler(
        add_score
    )

    dp.register_message_handler(
        process_account_name,
        state=Form.waiting_for_account_name
    )

    dp.register_message_handler(
        process_account_balance,
        state=Form.waiting_for_account_balance
    )

    dp.register_message_handler(
        delete_score
    )

    dp.register_message_handler(
        proces_delete_score,
        state=FormDel.waiting_for_account_name_del
    )

    dp.register_message_handler(
        get_score
    )


def run_chat_bot() -> None:

    register_handlers()
    executor.start_polling(dp, skip_updates=True)