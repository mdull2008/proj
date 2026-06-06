"""Telegram booking bot for a nail master.

Run with:
    TELEGRAM_BOT_TOKEN=123:ABC python3 manicure_bot.py
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from html import escape
from pathlib import Path
from typing import Any

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class Service:
    code: str
    title: str
    duration: str
    price: int


MASTER_NAME = os.getenv("MASTER_NAME", "мастер маникюра Анна")
MASTER_CHAT_ID = os.getenv("MASTER_CHAT_ID")
BOOKINGS_FILE = Path(os.getenv("BOOKINGS_FILE", "bot_bookings.json"))

SERVICES: dict[str, Service] = {
    "classic": Service("classic", "Маникюр без покрытия", "60 мин", 1200),
    "gel": Service("gel", "Маникюр + гель-лак", "120 мин", 2500),
    "strengthening": Service("strengthening", "Маникюр + укрепление", "150 мин", 3000),
    "design": Service("design", "Дизайн ногтей", "30-60 мин", 500),
    "removal": Service("removal", "Снятие покрытия", "30 мин", 500),
}

WORKING_TIMES = ("10:00", "12:00", "14:00", "16:00", "18:00")
FLOW_STATE = "flow_state"
BOOKING = "booking"
AWAITING_NAME = "awaiting_name"
AWAITING_PHONE = "awaiting_phone"
WEEKDAYS = ("пн", "вт", "ср", "чт", "пт", "сб", "вс")


def price_list_text() -> str:
    rows = [
        f"• <b>{escape(service.title)}</b> — {service.price} ₽ ({escape(service.duration)})"
        for service in SERVICES.values()
    ]
    return "💅 <b>Прайс</b>\n\n" + "\n".join(rows)


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💅 Прайс", callback_data="menu:prices")],
            [InlineKeyboardButton("📅 Записаться", callback_data="menu:book")],
            [InlineKeyboardButton("📍 Контакты", callback_data="menu:contacts")],
        ]
    )


def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ В меню", callback_data="menu:home")]])


def services_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(service.title, callback_data=f"book:service:{service.code}")]
        for service in SERVICES.values()
    ]
    buttons.append([InlineKeyboardButton("⬅️ В меню", callback_data="menu:home")])
    return InlineKeyboardMarkup(buttons)


def upcoming_dates(limit: int = 10) -> list[date]:
    days: list[date] = []
    current = date.today()

    while len(days) < limit:
        # Sunday is left closed by default.
        if current.weekday() != 6:
            days.append(current)
        current += timedelta(days=1)

    return days


def format_date_label(day: date) -> str:
    return f"{day.strftime('%d.%m')} ({WEEKDAYS[day.weekday()]})"


def dates_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(format_date_label(day), callback_data=f"book:date:{day.isoformat()}")]
        for day in upcoming_dates()
    ]
    buttons.append([InlineKeyboardButton("⬅️ Назад к услугам", callback_data="menu:book")])
    return InlineKeyboardMarkup(buttons)


def load_bookings() -> list[dict[str, Any]]:
    if not BOOKINGS_FILE.exists():
        return []

    try:
        raw_bookings = json.loads(BOOKINGS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        LOGGER.warning("Cannot parse %s, starting with empty bookings", BOOKINGS_FILE)
        return []

    if not isinstance(raw_bookings, list):
        return []

    return [booking for booking in raw_bookings if isinstance(booking, dict)]


def save_bookings(bookings: list[dict[str, Any]]) -> None:
    BOOKINGS_FILE.write_text(
        json.dumps(bookings, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def slot_is_taken(day: str, time: str) -> bool:
    return any(
        booking.get("date") == day
        and booking.get("time") == time
        and booking.get("status") != "cancelled"
        for booking in load_bookings()
    )


def available_times_keyboard(day: str) -> InlineKeyboardMarkup:
    buttons: list[list[InlineKeyboardButton]] = []

    for time in WORKING_TIMES:
        if slot_is_taken(day, time):
            label = f"❌ {time} занято"
            callback_data = "book:busy"
        else:
            label = f"✅ {time}"
            callback_data = f"book:time:{time}"
        buttons.append([InlineKeyboardButton(label, callback_data=callback_data)])

    buttons.append([InlineKeyboardButton("⬅️ Назад к датам", callback_data="book:dates")])
    return InlineKeyboardMarkup(buttons)


def booking_summary(booking: dict[str, Any]) -> str:
    service = SERVICES.get(str(booking.get("service_code")))
    service_title = service.title if service else "услуга"
    service_price = f"{service.price} ₽" if service else "цена уточняется"
    booking_date = datetime.fromisoformat(str(booking["date"])).date()

    return (
        "Проверьте запись:\n\n"
        f"💅 Услуга: <b>{escape(service_title)}</b>\n"
        f"💰 Цена: <b>{escape(service_price)}</b>\n"
        f"📅 Дата: <b>{escape(format_date_label(booking_date))}</b>\n"
        f"🕒 Время: <b>{escape(str(booking['time']))}</b>\n"
        f"👤 Имя: <b>{escape(str(booking['name']))}</b>\n"
        f"📞 Телефон: <b>{escape(str(booking['phone']))}</b>"
    )


def confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("✅ Подтвердить запись", callback_data="book:confirm")],
            [InlineKeyboardButton("❌ Отменить", callback_data="book:cancel")],
        ]
    )


async def send_home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.pop(FLOW_STATE, None)
    context.user_data.pop(BOOKING, None)
    text = (
        f"Здравствуйте! Я бот для записи к мастеру: <b>{escape(MASTER_NAME)}</b>.\n\n"
        "Здесь можно посмотреть прайс и выбрать удобное время."
    )

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=main_menu_keyboard(),
            parse_mode=ParseMode.HTML,
        )
    elif update.message:
        await update.message.reply_text(
            text,
            reply_markup=main_menu_keyboard(),
            parse_mode=ParseMode.HTML,
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_home(update, context)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            "Команды:\n"
            "/start — открыть меню\n"
            "/myid — узнать свой Telegram chat ID\n"
            "/bookings — показать записи мастеру"
        )


async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat and update.message:
        await update.message.reply_text(f"Ваш chat ID: {update.effective_chat.id}")


async def bookings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_chat or not update.message:
        return

    if MASTER_CHAT_ID and str(update.effective_chat.id) != MASTER_CHAT_ID:
        await update.message.reply_text("Эта команда доступна только мастеру.")
        return

    bookings = load_bookings()
    if not bookings:
        await update.message.reply_text("Пока записей нет.")
        return

    lines = ["Ближайшие записи:"]
    for booking in bookings[-15:]:
        service = SERVICES.get(str(booking.get("service_code")))
        service_title = service.title if service else str(booking.get("service_code", "услуга"))
        lines.append(
            "\n"
            f"{booking.get('date')} в {booking.get('time')}\n"
            f"{service_title}\n"
            f"{booking.get('name')} — {booking.get('phone')}"
        )

    await update.message.reply_text("\n".join(lines))


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return

    await query.answer()
    data = query.data or ""

    if data == "menu:home":
        await send_home(update, context)
        return

    if data == "menu:prices":
        await query.edit_message_text(
            price_list_text(),
            reply_markup=back_keyboard(),
            parse_mode=ParseMode.HTML,
        )
        return

    if data == "menu:contacts":
        await query.edit_message_text(
            "📍 <b>Контакты</b>\n\n"
            "Адрес: укажите адрес салона\n"
            "Телефон: +7 999 000-00-00\n"
            "Instagram/Telegram: @your_profile\n\n"
            "Эти данные можно поменять в файле manicure_bot.py.",
            reply_markup=back_keyboard(),
            parse_mode=ParseMode.HTML,
        )
        return

    if data == "menu:book":
        context.user_data[BOOKING] = {}
        await query.edit_message_text(
            "Выберите услугу:",
            reply_markup=services_keyboard(),
        )
        return

    if data.startswith("book:service:"):
        service_code = data.removeprefix("book:service:")
        context.user_data[BOOKING] = {"service_code": service_code}
        await query.edit_message_text(
            "Выберите дату:",
            reply_markup=dates_keyboard(),
        )
        return

    if data == "book:dates":
        await query.edit_message_text(
            "Выберите дату:",
            reply_markup=dates_keyboard(),
        )
        return

    if data.startswith("book:date:"):
        booking = context.user_data.setdefault(BOOKING, {})
        booking["date"] = data.removeprefix("book:date:")
        await query.edit_message_text(
            "Выберите свободное время:",
            reply_markup=available_times_keyboard(str(booking["date"])),
        )
        return

    if data == "book:busy":
        await query.answer("Это время уже занято. Выберите другое.", show_alert=True)
        return

    if data.startswith("book:time:"):
        booking = context.user_data.setdefault(BOOKING, {})
        selected_time = data.removeprefix("book:time:")
        selected_day = str(booking.get("date", ""))

        if slot_is_taken(selected_day, selected_time):
            await query.answer("Это время только что заняли. Выберите другое.", show_alert=True)
            await query.edit_message_reply_markup(reply_markup=available_times_keyboard(selected_day))
            return

        booking["time"] = selected_time
        context.user_data[FLOW_STATE] = AWAITING_NAME
        await query.edit_message_text("Напишите ваше имя:")
        return

    if data == "book:cancel":
        context.user_data.pop(FLOW_STATE, None)
        context.user_data.pop(BOOKING, None)
        await query.edit_message_text("Запись отменена.", reply_markup=back_keyboard())
        return

    if data == "book:confirm":
        await confirm_booking(update, context)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    state = context.user_data.get(FLOW_STATE)
    text = update.message.text.strip() if update.message.text else ""

    if state == AWAITING_NAME:
        if len(text) < 2:
            await update.message.reply_text("Напишите имя минимум из 2 символов.")
            return

        booking = context.user_data.setdefault(BOOKING, {})
        booking["name"] = text
        context.user_data[FLOW_STATE] = AWAITING_PHONE
        await update.message.reply_text("Напишите номер телефона для связи:")
        return

    if state == AWAITING_PHONE:
        if len(text) < 5:
            await update.message.reply_text("Похоже, номер слишком короткий. Напишите телефон еще раз.")
            return

        booking = context.user_data.setdefault(BOOKING, {})
        booking["phone"] = text
        context.user_data.pop(FLOW_STATE, None)
        await update.message.reply_text(
            booking_summary(booking),
            reply_markup=confirm_keyboard(),
            parse_mode=ParseMode.HTML,
        )
        return

    await update.message.reply_text(
        "Нажмите /start, чтобы открыть меню и записаться.",
        reply_markup=main_menu_keyboard(),
    )


async def confirm_booking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return

    booking = context.user_data.get(BOOKING)
    if not isinstance(booking, dict):
        await query.edit_message_text("Не нашла данные записи. Начните заново через /start.")
        return

    required_fields = {"service_code", "date", "time", "name", "phone"}
    if not required_fields.issubset(booking):
        await query.edit_message_text("В записи не хватает данных. Начните заново через /start.")
        return

    if slot_is_taken(str(booking["date"]), str(booking["time"])):
        await query.edit_message_text(
            "Это время уже занято. Пожалуйста, выберите другое.",
            reply_markup=dates_keyboard(),
        )
        return

    user = update.effective_user
    saved_booking = {
        **booking,
        "id": f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{user.id if user else 'guest'}",
        "telegram_user_id": user.id if user else None,
        "telegram_username": user.username if user else None,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "new",
    }

    bookings = load_bookings()
    bookings.append(saved_booking)
    save_bookings(bookings)

    context.user_data.pop(FLOW_STATE, None)
    context.user_data.pop(BOOKING, None)

    await query.edit_message_text(
        "✅ Запись создана!\n\n"
        "Мастер получил заявку и свяжется с вами, если нужно уточнение.",
        reply_markup=back_keyboard(),
    )

    await notify_master(context, saved_booking)


async def notify_master(context: ContextTypes.DEFAULT_TYPE, booking: dict[str, Any]) -> None:
    if not MASTER_CHAT_ID:
        return

    username = booking.get("telegram_username")
    username_line = f"\nTelegram: @{escape(str(username))}" if username else ""

    await context.bot.send_message(
        chat_id=MASTER_CHAT_ID,
        text=(
            "Новая запись 💅\n\n"
            + booking_summary(booking).replace("Проверьте запись:\n\n", "")
            + username_line
        ),
        parse_mode=ParseMode.HTML,
    )


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN environment variable before running the bot.")

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("myid", myid))
    application.add_handler(CommandHandler("bookings", bookings_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    LOGGER.info("Manicure bot is running")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
