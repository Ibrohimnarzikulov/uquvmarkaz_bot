# 🎓 MAQSAD O'quv Markazi — Telegram Bot

## ⚙️ O'rnatish

```bash
pip install -r requirements.txt
```

## 🔧 .env faylini sozlang

`.env` faylini oching va **ADMIN_ID** ni o'zgartiring:

```
BOT_TOKEN=8691461678:AAEHD8o7M5KEsi7TIoM5uNIpP3vvn2TgUME
ADMIN_ID=123456789        ← bu yerga o'z Telegram ID ingizni yozing
DATABASE_URL=postgresql://postgres:password@localhost:5432/maqsad
```

> **ADMIN_ID** olish: @userinfobot ga yozing → raqamni oling

## 🗄️ PostgreSQL

```sql
CREATE DATABASE maqsad;
```
Jadvallar bot ishganda avtomatik yaratiladi.

## ▶️ Ishga tushirish

```bash
python main.py
```

---

## 🤖 Bot imkoniyatlari

### Foydalanuvchi:
- 📚 **Kurslar** — 6 ta kurs haqida batafsil ma'lumot
- 👨‍🏫 **O'qituvchilar** — har bir o'qituvchi haqida ma'lumot
- ℹ️ **Biz haqimizda** — markaz haqida
- 📞 **Bog'lanish** — telefon va manzil
- 📝 **Ro'yxatdan o'tish** — to'liq FSM (ism → yosh → telefon → kurs)
- 👤 **Profilim** — shaxsiy ma'lumotlar

### Admin (`/admin`):
- 👥 Barcha o'quvchilar ro'yxati
- 📊 Kurslar bo'yicha statistika
- 🔔 Har yangi ro'yxatdan o'tishda **avtomatik xabar** keladi

---

## 📋 Kurslar
| Kurs | |
|------|-|
| 🔢 Mental Arifmetika | |
| 📐 Matematika | |
| 🇬🇧 Ingliz tili | |
| 🇩🇪 Nemis tili | |
| ⚽ Futbol | |
| ☀️ Futbol — Yozgi kurs | |
