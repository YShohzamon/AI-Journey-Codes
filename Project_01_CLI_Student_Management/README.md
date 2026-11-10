# 🎓 CLI Student Management System (Talabalar Boshqaruv Tizimi)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![AI Journey](https://img.shields.io/badge/AI_Journey-Modul_01_Project-orange.svg)](https://t.me/AijourneyShohzamon)

Ushbu loyiha **AI Journey | Shohzamon** kursining **1-moduli (Python Fundamentals)** bo'yicha yakuniy amaliy portfolio loyihasi hisoblanadi. Tizim talabalar ma'lumotlarini qabul qilish, tahrirlash, tahlil qilish va qattiq diskka (JSON) doimiy saqlashni to'liq avtomatlashtiruvchi modulli konsol dasturidir.

---

## 🌟 Asosiy Imkoniyatlar

- 📋 **To'liq CRUD operatsiyalari:** Talaba qo'shish, ro'yxatni ko'rish, ma'lumotlarni tahrirlash va o'chirish.
- 📝 **Akademik baholash:** Har bir talabaga baholar qo'shish, o'rtacha ballni hisoblash va avtomatik akademik status (A'lochi, Yaxshi, Qoniqarli, Qarzdor) belgilash.
- 🔍 **Tezkor qidiruv:** Ism-familiya yoki email bo'yicha filter qilish.
- 🏆 **Reyting tizimi:** Lambda funksiyalari orqali guruhning eng a'lochi (Top 5) talabalarini aniqlash.
- 📊 **Agregat statistika:** Guruh o'rtacha balli, eng yuqori/past baholar, a'lochilar va qarzdorlar tahlili.
- 💾 **Doimiy xotira (JSON Persistence):** Barcha o'zgarishlar darhol `data/students.json` fayliga serialization qilinadi. Dastur qayta ochilganda barcha ma'lumotlar tiklanadi.
- 🛡️ **Xatoliklardan himoya:** Noto'g'ri qiymatlar kiritilganda dastur to'xtab qolmaydi (`try-except` himoyasi).

---

## 🏗️ Arxitektura va Modullar Tuzilishi

Loyiha toza **OOP (Obyektga Yo'naltirilgan Dasturlash)** va **Separation of Concerns** tamoyillari asosida modullarga ajratilgan:

```
Project_01_CLI_Student_Management/
│
├── src/
│   ├── models.py        # Student klassi (Data Model, Validatsiya, Hisob-kitob)
│   ├── manager.py       # StudentManager klassi (Biznes mantiq, CRUD, Statistika)
│   ├── storage.py       # StorageManager klassi (JSON Serialization & Deserialization)
│   ├── main.py          # Asosiy CLI interfeysi va foydalanuvchi menyusi
│   └── data/
│       └── students.json # Ma'lumotlar bazasi (JSON formatida)
│
├── .gitignore           # Keraksiz va kesh fayllarni chetlab o'tish
└── README.md            # Loyiha hujjatlashuvi
```

---

## 🚀 O'rnatish va Ishga Tushirish

### 1. Reponi klonlash
```bash
git clone https://github.com/<GITHUB_PROFILINGIZ>/CLI-Student-Management-System.git
cd CLI-Student-Management-System
```

### 2. Standart kutubxona
Loyiha faqat Python'ning standart kutubxonalaridan (`json`, `os`, `sys`) foydalanadi, shuning uchun qo'shimcha paketlar o'rnatish talab qilinmaydi.

### 3. Dasturni yurgizish
```bash
# Windows / macOS / Linux
python src/main.py
```

---

## 🖥️ Interfeysdan Namunalar

```text
=================================================================
  🎓  TALABALARNI BOSHQARISH TIZIMI (CLI STUDENT SYSTEM)
=================================================================
  1. 📋 Barcha talabalarni ko'rish
  2. ➕ Yangi talaba qo'shish
  3. 📝 Talabaga baho qo'shish
  4. 🔍 Talabani qidirish
  5. ✏️  Talaba ma'lumotlarini yangilash
  6. 🗑️  Talabani o'chirish
  7. 🏆 Top talabalar reytingi (Top 5)
  8. 📊 Umumiy statistika va hisobot
  9. 🚪 Dasturdan chiqish
=================================================================
👉 Tanlovingizni kiriting (1-9):
```

---

## 👨‍💻 Muallif

* **Shohzamon** — [Telegram Kanal](https://t.me/AijourneyShohzamon)
* Loyiha: **AI Journey** (Data Science & AI ta'lim loyihasi)

