from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# ── Asosiy menyu ─────────────────────────────────────────────
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📚 Kurslar"),        KeyboardButton(text="👨‍🏫 O'qituvchilar")],
            [KeyboardButton(text="ℹ️ Biz haqimizda"),  KeyboardButton(text="📞 Bog'lanish")],
            [KeyboardButton(text="📝 Ro'yxatdan o'tish")],
            [KeyboardButton(text="👤 Mening profilim")],
        ],
        resize_keyboard=True
    )

# ── Telefon tugmasi ───────────────────────────────────────────
def phone_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)],
            [KeyboardButton(text="🔙 Orqaga")],
        ],
        resize_keyboard=True
    )

# ── Kurslar ro'yxati (inline) ─────────────────────────────────
def courses_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔢 Mental Arifmetika",  callback_data="course_mental")],
        [InlineKeyboardButton(text="📐 Matematika",          callback_data="course_math")],
        [InlineKeyboardButton(text="🇬🇧 Ingliz tili",        callback_data="course_english")],
        [InlineKeyboardButton(text="🇩🇪 Nemis tili",         callback_data="course_german")],
        [InlineKeyboardButton(text="⚽ Futbol",              callback_data="course_football")],
        [InlineKeyboardButton(text="☀️ Futbol (Yozgi kurs)", callback_data="course_football_summer")],
        [InlineKeyboardButton(text="🔙 Orqaga",             callback_data="back_main")],
    ])

# ── Ro'yxatda kurs tanlash — multi-select (inline) ───────────
COURSE_LIST = [
    ("🔢 Mental Arifmetika", "Mental Arifmetika"),
    ("📐 Matematika",         "Matematika"),
    ("🇬🇧 Ingliz tili",       "Ingliz tili"),
    ("🇩🇪 Nemis tili",        "Nemis tili"),
    ("⚽ Futbol",             "Futbol"),
    ("☀️ Futbol Yozgi kurs", "Futbol Yozgi kurs"),
]

def register_courses_keyboard(selected: list = None):
    if selected is None:
        selected = []
    rows = []
    for emoji_name, value in COURSE_LIST:
        check = "✅ " if value in selected else ""
        rows.append([InlineKeyboardButton(
            text=f"{check}{emoji_name}",
            callback_data=f"sel_{value.replace(' ', '_')}"
        )])
    rows.append([
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data="reg_cancel"),
        InlineKeyboardButton(
            text=f"✅ Tasdiqlash ({len(selected)})" if selected else "✅ Tasdiqlash",
            callback_data="reg_confirm"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)

# ── O'qituvchilar ro'yxati (inline) ──────────────────────────
def teachers_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔢 Mental Arifmetika o'qituvchisi", callback_data="teacher_mental")],
        [InlineKeyboardButton(text="📐 Matematika o'qituvchisi",         callback_data="teacher_math")],
        [InlineKeyboardButton(text="🇬🇧 Ingliz tili o'qituvchisi",       callback_data="teacher_english")],
        [InlineKeyboardButton(text="🇩🇪 Nemis tili o'qituvchisi",        callback_data="teacher_german")],
        [InlineKeyboardButton(text="⚽ Futbol murabbiyi",                 callback_data="teacher_football")],
        [InlineKeyboardButton(text="🔙 Orqaga",                          callback_data="back_main")],
    ])

# ── Admin panel ───────────────────────────────────────────────
def admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👥 Barcha o'quvchilar"), KeyboardButton(text="📊 Statistika")],
            [KeyboardButton(text="🔙 Asosiy menyu")],
        ],
        resize_keyboard=True
    )
