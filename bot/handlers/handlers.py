import os
from aiogram import Router, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramAPIError
from dotenv import load_dotenv

from database.db import get_user, get_user_by_phone, delete_user, register_user, get_all_users
from keyboards.keyboards import (
    main_menu, phone_keyboard, courses_keyboard,
    register_courses_keyboard, teachers_keyboard, admin_keyboard
)

load_dotenv()
router   = Router()
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

# ════════════════════════════════════
# O'qituvchilar
# ════════════════════════════════════
TEACHERS = {
    "teacher_mental": (
        "🔢 <b>Mental Arifmetika o'qituvchisi</b>\n\n"
        "👩‍🏫 Ism: Mohlaroyim Yusupova\n"
        "🎓 Tajriba: 5 yil\n"
        "📜 Sertifikat: Xalqaro Mental Arifmetika sertifikati\n"
        "⭐ Ustunligi: Bolalar bilan individual yondashuv,\n"
        "     tez natija beradigan metodika\n"
        "📞 Qabul vaqti: Du-Sha, 09:00–17:00"
    ),
    "teacher_math": (
        "📐 <b>Matematika o'qituvchisi</b>\n\n"
        "👨‍🏫 Ism: Sardor Rahimov\n"
        "🎓 Tajriba: 8 yil\n"
        "📜 Ta'lim: ToshDTU, Matematika fakulteti\n"
        "⭐ Ustunligi: Olimpiada matematikasi, chuqur nazariy\n"
        "     bilim va amaliy masalalar yechish\n"
        "📞 Qabul vaqti: Du-Sha, 10:00–18:00"
    ),
    "teacher_english": (
        "🇬🇧 <b>Ingliz tili o'qituvchisi</b>\n\n"
        "👩‍🏫 Ism: Nilufar Ergasheva\n"
        "🎓 Tajriba: 6 yil\n"
        "📜 Sertifikat: IELTS 7.5, Cambridge CELTA\n"
        "⭐ Ustunligi: Kommunikativ metod, so'zlashuv\n"
        "     malakasini tez rivojlantirish\n"
        "📞 Qabul vaqti: Du-Sha, 09:00–18:00"
    ),
    "teacher_german": (
        "🇩🇪 <b>Nemis tili o'qituvchisi</b>\n\n"
        "👨‍🏫 Ism: Jasur Nazarov\n"
        "🎓 Tajriba: 4 yil\n"
        "📜 Sertifikat: Goethe-Institut B2\n"
        "⭐ Ustunligi: Grammatika va og'zaki nutqni\n"
        "     bir vaqtda rivojlantirish\n"
        "📞 Qabul vaqti: Du-Sha, 10:00–17:00"
    ),
    "teacher_football": (
        "⚽ <b>Futbol murabbiyi</b>\n\n"
        "👨‍🏫 Ism: Bobur Toshmatov\n"
        "🎓 Tajriba: 10 yil\n"
        "📜 Toifa: UEFA C lisenziyasi\n"
        "⭐ Ustunligi: 5–16 yoshli bolalar bilan ishlash,\n"
        "     yozgi intensiv kurslar\n"
        "📞 Mashg'ulot vaqti: Du-Sha, 08:00–12:00 va 15:00–19:00"
    ),
}

# ════════════════════════════════════
# Kurslar
# ════════════════════════════════════
COURSES = {
    "course_mental": (
        "🔢 <b>Mental Arifmetika kursi</b>\n\n"
        "📖 Abakus asosida hisoblash, xotira va diqqatni rivojlantirish\n"
        "👶 Yosh: 5–12 yosh\n"
        "⏱ Davomiyligi: 12 oy\n"
        "📅 Dars: haftada 2 marta\n"
        "💰 Narxi: markazga murojaat qiling\n\n"
        "✅ Xalqaro sertifikat beriladi"
    ),
    "course_math": (
        "📐 <b>Matematika kursi</b>\n\n"
        "📖 Maktab matematikasi, olimpiada masalalari, imtihonga tayyorlov\n"
        "👶 Yosh: 7–18 yosh\n"
        "⏱ Davomiyligi: 6–12 oy\n"
        "📅 Dars: haftada 3 marta\n"
        "💰 Narxi: markazga murojaat qiling\n\n"
        "✅ Sertifikat beriladi"
    ),
    "course_english": (
        "🇬🇧 <b>Ingliz tili kursi</b>\n\n"
        "📖 A1 dan C1 gacha barcha darajalar, IELTS tayyorlov\n"
        "👶 Yosh: 6 yoshdan kattalar\n"
        "⏱ Davomiyligi: 6–12 oy\n"
        "📅 Dars: haftada 3 marta\n"
        "💰 Narxi: markazga murojaat qiling\n\n"
        "✅ Xalqaro sertifikat beriladi"
    ),
    "course_german": (
        "🇩🇪 <b>Nemis tili kursi</b>\n\n"
        "📖 A1 dan B2 gacha darajalar, Goethe sertifikatiga tayyorlov\n"
        "👶 Yosh: 10 yoshdan kattalar\n"
        "⏱ Davomiyligi: 8–12 oy\n"
        "📅 Dars: haftada 3 marta\n"
        "💰 Narxi: markazga murojaat qiling\n\n"
        "✅ Goethe-Institut sertifikati"
    ),
    "course_football": (
        "⚽ <b>Futbol kursi</b>\n\n"
        "📖 Texnika, taktika, jismoniy tayyorgarlik\n"
        "👶 Yosh: 5–16 yosh\n"
        "⏱ Davomiyligi: yil davomida\n"
        "📅 Mashg'ulot: haftada 3 marta\n"
        "💰 Narxi: markazga murojaat qiling\n\n"
        "✅ UEFA litsenziyali murabbiy"
    ),
    "course_football_summer": (
        "☀️ <b>Futbol — Yozgi kurs</b>\n\n"
        "📖 Intensiv yozgi futbol kursi: texnika, jamoaviy o'yin, musobaqalar\n"
        "👶 Yosh: 6–16 yosh\n"
        "⏱ Davomiyligi: Iyun–Avgust (3 oy)\n"
        "📅 Mashg'ulot: hafta ichida har kuni ertalab\n"
        "💰 Narxi: markazga murojaat qiling\n\n"
        "🏆 Kurs oxirida ichki musobaqa o'tkaziladi"
    ),
}

# ════════════════════════════════════
# FSM — Ro'yxat bosqichlari
# ════════════════════════════════════
class Reg(StatesGroup):
    full_name = State()
    age       = State()
    phone     = State()
    course    = State()

# ── Ro'yxat ichida faqat bitta message ID saqlanadi ──────────
# state data: { full_name, age, phone, selected_courses, reg_msg_id }

def _cancel_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="reg_cancel")]
    ])

def _phone_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="reg_back_age")],
    ])

# ════════════════════════════════════
# /start
# ════════════════════════════════════
@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f"🎓 <b>MAQSAD O'quv Markazi</b>ga xush kelibsiz!\n\n"
        f"Salom, <b>{message.from_user.full_name}</b>! 👋\n\n"
        f"Bizda quyidagi yo'nalishlar mavjud:\n"
        f"🔢 Mental Arifmetika  📐 Matematika\n"
        f"🇬🇧 Ingliz tili  🇩🇪 Nemis tili  ⚽ Futbol\n\n"
        f"Quyidagi bo'limdan birini tanlang:",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

# ════════════════════════════════════
# Kurslar
# ════════════════════════════════════
@router.message(F.text == "📚 Kurslar")
async def courses_handler(message: Message):
    await message.answer(
        "📚 <b>Bizning kurslar</b>\n\nQiziqtirgan kursni tanlang:",
        parse_mode="HTML",
        reply_markup=courses_keyboard()
    )

@router.callback_query(F.data.startswith("course_"))
async def course_detail(callback: CallbackQuery):
    text = COURSES.get(callback.data)
    if text:
        await callback.message.edit_text(
            text + "\n\n📝 <i>Ro'yxatdan o'tish uchun asosiy menyuga qayting.</i>",
            parse_mode="HTML",
            reply_markup=courses_keyboard()
        )
    await callback.answer()

# ════════════════════════════════════
# O'qituvchilar
# ════════════════════════════════════
@router.message(F.text == "👨‍🏫 O'qituvchilar")
async def teachers_handler(message: Message):
    await message.answer(
        "👨‍🏫 <b>Bizning o'qituvchilar</b>\n\nQaysi o'qituvchi haqida bilmoqchisiz?",
        parse_mode="HTML",
        reply_markup=teachers_keyboard()
    )

@router.callback_query(F.data.startswith("teacher_"))
async def teacher_detail(callback: CallbackQuery):
    text = TEACHERS.get(callback.data)
    if text:
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=teachers_keyboard())
    await callback.answer()

# ════════════════════════════════════
# Biz haqimizda
# ════════════════════════════════════
@router.message(F.text == "ℹ️ Biz haqimizda")
async def about_handler(message: Message):
    await message.answer(
        "🏫 <b>MAQSAD O'quv Markazi</b>\n\n"
        "📌 Biz — sifatli ta'lim beruvchi zamonaviy markaz!\n\n"
        "✅ Tajribali va sertifikatlangan o'qituvchilar\n"
        "✅ Kichik guruhlar — individual yondashuv\n"
        "✅ Amaliy va nazariy ta'lim\n"
        "✅ Kurs yakunida sertifikat beriladi\n"
        "✅ Qulay va iliq muhit\n\n"
        "🎯 Maqsadimiz — har bir o'quvchini muvaffaqiyatga yetaklash!\n\n"
        "📍 <b>Manzil:</b> Davlatobot, Dehqon bozori yon tarafi (Lenin bozor)\n"
        "📱 <b>Telefon:</b> +998 99 563 87 69\n"
        "🕐 <b>Ish vaqti:</b> Du-Sha, 08:00–20:00",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

# ════════════════════════════════════
# Bog'lanish
# ════════════════════════════════════
@router.message(F.text == "📞 Bog'lanish")
async def contact_handler(message: Message):
    await message.answer(
        "📞 <b>Biz bilan bog'laning</b>\n\n"
        "📱 Telefon: <b>+998 99 563 87 69</b>\n\n"
        "📍 Manzil: <b>Davlatobot, Dehqon bozori yon tarafi (Lenin bozor)</b>\n\n"
        "🕐 Qabul vaqti: Du-Sha, 08:00–20:00",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

# ════════════════════════════════════
# Profil
# ════════════════════════════════════
@router.message(F.text == "👤 Mening profilim")
async def profile_handler(message: Message):
    user = await get_user(message.from_user.id)
    if user:
        await message.answer(
            f"👤 <b>Sizning profilingiz</b>\n\n"
            f"📛 Ism: {user['full_name']}\n"
            f"🎂 Yosh: {user['age']}\n"
            f"📱 Telefon: {user['phone']}\n"
            f"📚 Kurs: {user['course']}\n"
            f"📅 Ro'yxat sanasi: {user['registered_at'].strftime('%d.%m.%Y')}",
            parse_mode="HTML",
            reply_markup=main_menu()
        )
    else:
        await message.answer(
            "❌ Siz hali ro'yxatdan o'tmagansiz!\n"
            "📝 «Ro'yxatdan o'tish» tugmasini bosing.",
            reply_markup=main_menu()
        )

# ════════════════════════════════════
# Ro'yxatdan o'tish — bitta message
# ════════════════════════════════════
@router.message(F.text == "📝 Ro'yxatdan o'tish")
async def register_start(message: Message, state: FSMContext):
    if await get_user(message.from_user.id):
        await message.answer(
            "✅ Siz allaqachon ro'yxatdan o'tgansiz!\n"
            "👤 «Mening profilim» tugmasidan ma'lumotlaringizni ko'ring.",
            reply_markup=main_menu()
        )
        return
    await state.set_state(Reg.full_name)
    msg = await message.answer(
        "📝 <b>Ro'yxatdan o'tish</b>\n\n"
        "1️⃣ To'liq ismingizni <b>yozing</b>:\n"
        "<i>Masalan: Aliyev Abdulloh</i>",
        parse_mode="HTML",
        reply_markup=_cancel_kb()
    )
    await state.update_data(reg_msg_id=msg.message_id)


# ── 1: Ism ───────────────────────────────────────────────────
@router.message(Reg.full_name)
async def reg_name(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    await state.update_data(full_name=message.text.strip())
    await state.set_state(Reg.age)
    await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["reg_msg_id"],
        text=(
            "📝 <b>Ro'yxatdan o'tish</b>\n\n"
            f"👤 Ism: <b>{message.text.strip()}</b>\n\n"
            "2️⃣ Yoshingizni <b>yozing</b>:\n"
            "<i>Masalan: 12</i>"
        ),
        parse_mode="HTML",
        reply_markup=_cancel_kb()
    )


# ── 2: Yosh ──────────────────────────────────────────────────
@router.message(Reg.age)
async def reg_age(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    if not message.text.isdigit() or not (4 <= int(message.text) <= 80):
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["reg_msg_id"],
            text=(
                "📝 <b>Ro'yxatdan o'tish</b>\n\n"
                f"👤 Ism: <b>{data['full_name']}</b>\n\n"
                "⚠️ Yosh 4–80 oralig'ida bo'lishi kerak!\n"
                "2️⃣ Yoshingizni qayta <b>yozing</b>:"
            ),
            parse_mode="HTML",
            reply_markup=_cancel_kb()
        )
        return
    await state.update_data(age=int(message.text))
    await state.set_state(Reg.phone)
    await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["reg_msg_id"],
        text=(
            "📝 <b>Ro'yxatdan o'tish</b>\n\n"
            f"👤 Ism: <b>{data['full_name']}</b>\n"
            f"🎂 Yosh: <b>{message.text}</b>\n\n"
            "3️⃣ Telefon raqamingizni <b>yozing</b>:\n"
            "<i>Masalan: +998991234567</i>"
        ),
        parse_mode="HTML",
        reply_markup=_cancel_kb()
    )


# ── 3: Telefon (matn orqali) ──────────────────────────────────
@router.message(Reg.phone, F.text)
async def reg_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    await state.update_data(phone=message.text.strip(), selected_courses=[])
    await state.set_state(Reg.course)
    await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["reg_msg_id"],
        text=(
            "📝 <b>Ro'yxatdan o'tish</b>\n\n"
            f"👤 Ism: <b>{data['full_name']}</b>\n"
            f"🎂 Yosh: <b>{data['age']}</b>\n"
            f"📱 Tel: <b>{message.text.strip()}</b>\n\n"
            "4️⃣ Kurslarga <b>bosing</b> (bir yoki bir nechta):\n"
            "<i>Tanlab bo'lgach ✅ Tasdiqlash tugmasini bosing</i>"
        ),
        parse_mode="HTML",
        reply_markup=register_courses_keyboard([])
    )


# ── 3: Telefon (kontakt orqali) ───────────────────────────────
@router.message(Reg.phone, F.contact)
async def reg_phone_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    phone = message.contact.phone_number
    await message.delete()
    await state.update_data(phone=phone, selected_courses=[])
    await state.set_state(Reg.course)
    await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["reg_msg_id"],
        text=(
            "📝 <b>Ro'yxatdan o'tish</b>\n\n"
            f"👤 Ism: <b>{data['full_name']}</b>\n"
            f"🎂 Yosh: <b>{data['age']}</b>\n"
            f"📱 Tel: <b>{phone}</b>\n\n"
            "4️⃣ Kurslarga <b>bosing</b> (bir yoki bir nechta):\n"
            "<i>Tanlab bo'lgach ✅ Tasdiqlash tugmasini bosing</i>"
        ),
        parse_mode="HTML",
        reply_markup=register_courses_keyboard([])
    )


# ── 4: Kurs toggle ────────────────────────────────────────────
@router.callback_query(F.data.startswith("sel_"), Reg.course)
async def toggle_course(callback: CallbackQuery, state: FSMContext):
    value = callback.data[4:].replace("_", " ")
    data  = await state.get_data()
    selected: list = list(data.get("selected_courses", []))
    if value in selected:
        selected.remove(value)
    else:
        selected.append(value)
    await state.update_data(selected_courses=selected)

    sel_text = ", ".join(selected) if selected else "—"
    await callback.message.edit_text(
        "📝 <b>Ro'yxatdan o'tish</b>\n\n"
        f"👤 Ism: <b>{data['full_name']}</b>\n"
        f"🎂 Yosh: <b>{data['age']}</b>\n"
        f"📱 Tel: <b>{data['phone']}</b>\n"
        f"📚 Tanlangan: <b>{sel_text}</b>\n\n"
        "4️⃣ Kurslarga <b>bosing</b> (bir yoki bir nechta):\n"
        "<i>Tanlab bo'lgach ✅ Tasdiqlash tugmasini bosing</i>",
        parse_mode="HTML",
        reply_markup=register_courses_keyboard(selected)
    )
    await callback.answer()


# ── 5: Tasdiqlash ─────────────────────────────────────────────
@router.callback_query(F.data == "reg_confirm", Reg.course)
async def reg_confirm(callback: CallbackQuery, state: FSMContext):
    data     = await state.get_data()
    selected = data.get("selected_courses", [])
    if not selected:
        await callback.answer("⚠️ Kamida 1 ta kurs tanlang!", show_alert=True)
        return

    courses_str = ", ".join(selected)
    await register_user(
        tg_id=callback.from_user.id,
        username=callback.from_user.username or "",
        full_name=data["full_name"],
        phone=data["phone"],
        age=data["age"],
        course=courses_str
    )
    await state.clear()

    await callback.message.edit_text(
        f"✅ <b>Ro'yxatdan muvaffaqiyatli o'tdingiz!</b>\n\n"
        f"📛 Ism: {data['full_name']}\n"
        f"🎂 Yosh: {data['age']}\n"
        f"📱 Telefon: {data['phone']}\n"
        f"📚 Kurslar: {courses_str}\n\n"
        f"📞 Tez orada administrator siz bilan bog'lanadi!\n"
        f"📍 Davlatobot, Dehqon bozori yon tarafi (Lenin bozor)\n"
        f"📱 Tel: +998 99 563 87 69",
        parse_mode="HTML"
    )

    uname = f"@{callback.from_user.username}" if callback.from_user.username else "Yo'q"
    await _notify_admin(
        callback.bot,
        f"🆕 <b>Yangi o'quvchi!</b>\n\n"
        f"👤 Ism: {data['full_name']}\n"
        f"🎂 Yosh: {data['age']}\n"
        f"📱 Telefon: {data['phone']}\n"
        f"📚 Kurslar: {courses_str}\n"
        f"🔗 Telegram: {uname}\n"
        f"🆔 TG ID: <code>{callback.from_user.id}</code>"
    )
    await callback.answer("✅ Ro'yxatdan o'tdingiz!")


# ── Bekor qilish ──────────────────────────────────────────────
@router.callback_query(F.data == "reg_cancel")
async def reg_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "❌ Ro'yxatdan o'tish bekor qilindi.\n\n"
        "Qaytadan boshlash uchun «📝 Ro'yxatdan o'tish» tugmasini bosing.",
        parse_mode="HTML"
    )
    await callback.answer()


async def _notify_admin(bot, text: str):
    try:
        await bot.send_message(ADMIN_ID, text, parse_mode="HTML")
    except TelegramAPIError:
        pass


# ════════════════════════════════════
# Admin
# ════════════════════════════════════
@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Siz admin emassiz!")
        return
    await message.answer(
        "🔐 <b>Admin Panel</b>\n\n"
        "📌 Buyruqlar:\n"
        "/del <code>ID</code> — o'quvchini o'chirish (TG ID bo'yicha)\n"
        "/vaqt <code>ID</code> <code>soat</code> — mijozga vaqt yuborish\n\n"
        "<i>Masalan: /del 123456789</i>\n"
        "<i>Masalan: /vaqt 123456789 14:00</i>",
        parse_mode="HTML",
        reply_markup=admin_keyboard()
    )


# ── /del — o'quvchini o'chirish ───────────────────────────────
# Ishlatish: /del 123456789
@router.message(Command("del"))
async def del_user(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    args = message.text.split()
    if len(args) < 2:
        await message.answer(
            "❌ Noto'g'ri format!\n\n"
            "To'g'ri ishlatish:\n"
            "<code>/del 123456789</code>\n\n"
            "💡 TG ID ni «👥 Barcha o'quvchilar» bo'limidan toping.",
            parse_mode="HTML"
        )
        return

    try:
        tg_id = int(args[1])
    except ValueError:
        await message.answer("❌ ID raqam bo'lishi kerak!", parse_mode="HTML")
        return

    user = await get_user(tg_id)
    if not user:
        await message.answer(
            f"⚠️ <code>{tg_id}</code> ID li o'quvchi topilmadi!",
            parse_mode="HTML"
        )
        return

    await delete_user(tg_id)
    await message.answer(
        f"✅ <b>{user['full_name']}</b> o'chirildi!\n\n"
        f"📱 Tel: {user['phone']}\n"
        f"📚 Kurs: {user['course']}\n"
        f"🆔 ID: <code>{tg_id}</code>",
        parse_mode="HTML"
    )

    # Foydalanuvchiga xabar yuborish (ixtiyoriy)
    try:
        await message.bot.send_message(
            tg_id,
            "ℹ️ Sizning ma'lumotlaringiz tizimdan o'chirildi.\n"
            "Qayta ro'yxatdan o'tish uchun /start bosing."
        )
    except TelegramAPIError:
        pass


# ── /vaqt — mijozga kelish vaqtini yuborish ──────────────────
# Ishlatish: /vaqt 123456789 14:00
@router.message(Command("vaqt"))
async def send_time(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    args = message.text.split()
    if len(args) < 3:
        await message.answer(
            "❌ Noto'g'ri format!\n\n"
            "To'g'ri ishlatish:\n"
            "<code>/vaqt 123456789 14:00</code>\n\n"
            "💡 TG ID ni «👥 Barcha o'quvchilar» bo'limidan toping.",
            parse_mode="HTML"
        )
        return

    try:
        tg_id = int(args[1])
    except ValueError:
        await message.answer("❌ ID raqam bo'lishi kerak!", parse_mode="HTML")
        return

    soat = args[2]
    user = await get_user(tg_id)

    if not user:
        await message.answer(
            f"⚠️ <code>{tg_id}</code> ID li o'quvchi topilmadi!",
            parse_mode="HTML"
        )
        return

    try:
        await message.bot.send_message(
            tg_id,
            f"📅 <b>MAQSAD O'quv Markazi</b>\n\n"
            f"Hurmatli <b>{user['full_name']}</b>!\n\n"
            f"Siz bugun soat <b>{soat}</b> da kelishingiz kutilmoqda.\n\n"
            f"📍 Manzil: Davlatobot, Dehqon bozori yon tarafi (Lenin bozor)\n"
            f"📱 Telefon: +998 99 563 87 69\n\n"
            f"✅ Sizni kutib qolamiz!",
            parse_mode="HTML"
        )
        await message.answer(
            f"✅ <b>{user['full_name']}</b> ga soat <b>{soat}</b> da kelish\n"
            f"haqida xabar yuborildi!",
            parse_mode="HTML"
        )
    except TelegramAPIError:
        await message.answer(
            f"⚠️ Xabar yuborib bo'lmadi!\n"
            f"Foydalanuvchi botni bloklagan bo'lishi mumkin.",
            parse_mode="HTML"
        )


@router.message(F.text == "👥 Barcha o'quvchilar")
async def all_students(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    users = await get_all_users()
    if not users:
        await message.answer("📭 Hali ro'yxatdan o'tgan o'quvchi yo'q.")
        return
    text = f"👥 <b>Jami: {len(users)} ta o'quvchi</b>\n\n"
    for i, u in enumerate(users, 1):
        un = f"@{u['username']}" if u['username'] else "—"
        text += (
            f"{i}. <b>{u['full_name']}</b> | {u['age']} yosh\n"
            f"   📱 {u['phone']} | 📚 {u['course']}\n"
            f"   🔗 {un} | 🆔 <code>{u['tg_id']}</code>\n\n"
        )
        if len(text) > 3500:
            await message.answer(text, parse_mode="HTML")
            text = ""
    if text:
        await message.answer(text, parse_mode="HTML")


@router.message(F.text == "📊 Statistika")
async def statistics(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    users = await get_all_users()
    courses: dict = {}
    for u in users:
        courses[u['course']] = courses.get(u['course'], 0) + 1
    text = f"📊 <b>Statistika</b>\n\n👥 Jami: <b>{len(users)} ta</b>\n\n<b>Kurslar bo'yicha:</b>\n"
    for c, cnt in sorted(courses.items(), key=lambda x: -x[1]):
        text += f"• {c}: {cnt} ta\n"
    await message.answer(text, parse_mode="HTML")


@router.message(F.text == "🔙 Asosiy menyu")
async def back_to_main(message: Message):
    await message.answer("Asosiy menyu:", reply_markup=main_menu())


@router.callback_query(F.data == "back_main")
async def back_main_cb(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()
