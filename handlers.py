from aiogram import Router, F, Bot
from aiogram.types import (
    Message, 
    CallbackQuery, 
    ChatJoinRequest, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()
user_languages = {}

# Все тексты как в оригинале
TEXTS = {
    "ru": {
        "welcome": lambda username: f"""
        <b>👋 Hello, {username}!</b>

        Please, choose the language:
        """,
        "start": lambda username: f"""
        <b>✨Добро пожаловать в закрытое сообщество!!</b>

       Чтобы присоединиться к нашему каналу с эксклюзивным контентом:

🔹 Шаг 1 — Нажми «Подать заявку» ниже.
🔹 Шаг 2 — Пройди быструю проверку (это займет 20 секунд!).
🔹 Шаг 3 — Открой доступ к приватным материалам, новостям и чату единомышленников.

🎉 Что внутри?
— Ранние анонсы проектов;
— Закрытые голосования;
— Личный чат с авторами.
        """,
        "apply": "🚀 Подать заявку",
        "captcha": """
        <b>🔐 Проверка</b>

        Реши пример: <code>2 + 2 = ?</code>
        Ответь числом в течение 2 минут.
        """,
        "success": """
        <b>🎉 Проверка пройдена!</b>

        Теперь можешь перейти в наш канал:
        https://t.me/+y-tPOw0ehQg0NjYy
        """,
        "wrong": "❌ Неверный ответ. Попробуй еще раз.",
        "join": lambda username: f"""
        <b>👋 Hello, {username}!</b>

        To complete registration, click the button below:
        """,
        "join_button": "🔑 Начать проверку",
        "channel_button": "🔗 Перейти в канал",
        "language_set": "Язык установлен"
    },
    "en": {
        "welcome": lambda username: f"""
        <b>👋 Hello, {username}!</b>

        Please select language:
        """,
        "start": lambda username: f"""
        <b>✨Welcome to our exclusive community!</b>

       To join the channel with premium content:

🔹 Step 1 — Click "Apply Now" below.
🔹 Step 2 — Pass a quick verification (it takes just 20 seconds!).
🔹 Step 3 — Unlock private materials, updates, and chats with like-minded members.

🎉 What's inside?
— Early project announcements;
— Exclusive polls and votes;
— Direct communication with creators.
        """,
        "apply": "🚀 Apply to join",
        "captcha": """
        <b>🔐 Verification</b>

        Solve the example: <code>2 + 2 = ?</code>
        Reply with a number within 2 minutes.
        """,
        "success": """
        <b>🎉 Verification passed!</b>

        Now you can join our channel:
        https://t.me/+y-tPOw0ehQg0NjYy
        """,
        "wrong": "❌ Wrong answer. Please try again.",
        "join": lambda username: f"""
        <b>👋 Hello, {username}!</b>

        Click the button below to complete registration:
        """,
        "join_button": "🔑 Start verification",
        "channel_button": "🔗 Join channel",
        "language_set": "Language set"
    }
}

def get_user_name(user):
    return f"@{user.username}" if user.username else user.full_name or "User"

def language_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_language_ru"),
        InlineKeyboardButton(text="🇬🇧 English", callback_data="set_language_en")
    )
    return builder.as_markup()

def apply_keyboard(lang):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=TEXTS[lang]["apply"], callback_data="apply_to_channel")]
        ]
    )

def channel_link_keyboard(lang):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=TEXTS[lang]["channel_button"], url="https://t.me/+y-tPOw0ehQg0NjYy")]
        ]
    )

@router.message(Command("start"))
async def cmd_start(message: Message):
    user = message.from_user
    username = get_user_name(user)
    
    if user.id not in user_languages:
        await message.answer(
            text=TEXTS["ru"]["welcome"](username),
            reply_markup=language_keyboard()
        )
        return
    
    lang = user_languages.get(user.id, "ru")
    await message.answer(
        text=TEXTS[lang]["start"](username),
        reply_markup=apply_keyboard(lang)
    )

@router.callback_query(F.data.startswith("set_language_"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split("_")[-1]
    user_languages[callback.from_user.id] = lang
    await callback.answer(TEXTS[lang]["language_set"])
    
    username = get_user_name(callback.from_user)
    await callback.message.edit_text(
        text=TEXTS[lang]["start"](username),
        reply_markup=apply_keyboard(lang)
    )

@router.callback_query(F.data == "apply_to_channel")
async def handle_application(callback: CallbackQuery):
    lang = user_languages.get(callback.from_user.id, "ru")
    await callback.message.edit_text(
        text=TEXTS[lang]["captcha"]
    )
    await callback.answer()

@router.message(F.text)
async def check_captcha(message: Message):
    lang = user_languages.get(message.from_user.id, "ru")
    
    if message.text.strip() == "4":
        await message.answer(
            text=TEXTS[lang]["success"],
            reply_markup=channel_link_keyboard(lang)
        )
    else:
        await message.answer(TEXTS[lang]["wrong"])

@router.chat_join_request()
async def handle_join_request(request: ChatJoinRequest, bot: Bot):
    user = request.from_user
    lang = user_languages.get(user.id, "ru")
    username = get_user_name(user)
    deep_link = f"https://t.me/{bot._me.username}?start=join_{user.id}"
    
    try:
        await bot.send_message(
            chat_id=user.id,
            text=TEXTS[lang]["join"](username),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(
                        text=TEXTS[lang]["join_button"],
                        url=deep_link
                    )
                ]]
            )
        )
    except:
        pass