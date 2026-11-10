# Modul 01: Python Fundamentals — Portfolio Loyihasi: CLI Student Management System

> **Modul:** Modul 01: Python Fundamentals  
> **Loyiha turi:** Capstone Portfolio Project (Konsol dasturi)  
> **Texnologiyalar:** Pure Python 3.10+, OOP, JSON Persistence, File I/O, CLI  
> **GitHub Repo:** `https://github.com/shohzamon/cli-student-management`  
> **Status:** [✅] To'liq yakunlangan va sinovdan o'tgan  

---

## 🎯 1. Loyihaning Maqsadi va Dolzarbligi

Dasturlashni o'rganishda faqat alohida dars mashqlarini bajarish yetarli emas. Haqiqiy dasturchi va bo'lajak AI muhandisi sifatida fikrlash uchun barcha o'rganilgan tushunchalarni (o'zgaruvchilar, sikllar, funksiyalar, ma'lumot tuzilmalari, fayllar, xatolar bilan ishlash va OOP) yagona mustahkam tizimda birlashtirish zarur.

Ushbu **CLI Student Management System** (Talabalarni boshqarish konsol tizimi) loyihasi:
1. Talabalar ma'lumotlarini kiritish, tahrirlash, qidirish va o'chirish (CRUD).
2. Ularning imtihon baholarini hisoblash, GPA/o'rtacha ballni aniqlash va akademik statusini belgilash.
3. Diskdagi `students.json` fayli orqali ma'lumotlarni doimiy saqlash (dastur yopilsa ham ma'lumot yo'qolmaydi).
4. AI va Data Science bosqichiga tayyorgarlik sifatida agregat statistikalarni (guruh o'rtachasi, eng yuqori/past baholar, a'lochilar va qarzdorlar tahlili) avtomatlashtirish imkoniyatini beradi.

---

## 🏛 2. Tizim Arxitekturasi (System Architecture)

Loyiha qat'iy **Modulli Arxitektura** (Separation of Concerns) tamoyili asosida 4 ta mustaqil qatlamga ajratilgan:

```text
+-------------------------------------------------------------+
|                 PRESENTATION LAYER (main.py)                |
|  - Foydalanuvchi menyusi (1-9)                              |
|  - Kiritilgan ma'lumotlarni qabul qilish va tekshirish      |
|  - Ma'lumotlarni chiroyli jadval ko'rinishida chiqarish     |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                 BUSINESS LOGIC LAYER (manager.py)           |
|  - StudentManager: CRUD amallari                            |
|  - Qidiruv (Substring match) va Saralash (Top-5 Lambda)     |
|  - Statistik hisobotlar (sum, len, min, max, any, all)      |
+------------------------------+------------------------------+
                               |
            +------------------+------------------+
            |                                     |
            v                                     v
+-------------------------+     +-----------------------------+
|  DATA MODEL (models.py) |     |  STORAGE LAYER (storage.py) |
|  - Student klassi (OOP) |     |  - StorageManager           |
|  - Maydonlar validatsiyasi    |  - JSON Serialization       |
|  - to_dict() / from_dict()    |  - Xatolardan himoyalangan  |
|  - __str__() va __repr__()    |    fayl o'qish/yozish (UTF-8)|
+-------------------------+     +--------------+--------------+
                                               |
                                               v
                                +-----------------------------+
                                |  DATA STORE (students.json) |
                                |  Diskdagi JSON ma'lumotlar  |
                                +-----------------------------+
```

---

## 📂 3. Loyiha Papkalar Tuzilishi

```text
Project_01_CLI_Student_Management/
├── post.md                                 # Telegram kanali uchun anons
├── notion.md                               # Ushbu to'liq Notion arxitektura qo'llanmasi
├── Project_01_CLI_Student_Management.html  # 4 sahifali rasmiy qo'llanma (HTML)
├── Project_01_CLI_Student_Management.pdf   # Chop etiladigan rasmiy PDF qo'llanma
└── src/
    ├── models.py                           # Student sinfi va ma'lumotlar modeli
    ├── storage.py                          # JSON fayl tizimi bilan ishlash
    ├── manager.py                          # Biznes mantiq, saralash va tahlil
    ├── main.py                             # Konsol foydalanuvchi interfeysi (CLI)
    └── data/
        └── students.json                   # Avtomatik yaratiladigan talabalar bazasi
```

---

## 🔍 4. Modullar Tafsiloti va Kod Tahlili

### 4.1. `models.py` — Ma'lumotlar Modeli va Validatsiya
Talabaning shaxsiy ma'lumotlari va akademik ko'rsatkichlarini ifodalovchi ob'ekt:
- **Validatsiya:** Ism kamida 3 belgidan iborat bo'lishi, email `@` va `.` belgilariga ega bo'lishi, baholar `0` dan `100` gacha oraliqda bo'lishi qat'iy nazorat qilinadi.
- **Serialization (`to_dict`):** Ob'ektni JSON formatga yozish uchun oddiy Python lug'atiga (`dict`) aylantiradi.
- **Deserialization (`from_dict`):** JSON fayldan o'qilgan xom ma'lumotlardan yangi `Student` nusxasini yaratadi.
- **Dunder metodlar:** `__str__` chiroyli konsol qatori uchun, `__repr__` esa dasturchi uchun xotira holatini aks ettiradi.

### 4.2. `storage.py` — Qattiq Disk Bilan Aloqa
- **Nisbiy yo'l muammosini hal qilish:** `os.path.abspath(__file__)` orqali dastur qaysi papkadan ishga tushirilishidan qat'i nazar, ma'lumot har doim `src/data/students.json` manziliga xavfsiz yo'naltiriladi.
- **Xatolardan himoya (Exception Handling):** Agar fayl diskda mavjud bo'lmasa, dastur qulamasdan bo'sh ro'yxat (`[]`) qaytaradi. JSON fayli buzilgan bo'lsa, `json.JSONDecodeError` ushlab qolinadi.
- **UTF-8 kodirovkasi:** Ismlardagi o'zbekcha harflar (`o'`, `g'`, `sh`, `ch`) hech qachon buzilmasligi ta'minlanadi.

### 4.3. `manager.py` — Biznes Mantiq va Tahlil
- **Avtomatik ID berish:** Tizim mavjud talabalar ichidagi eng katta ID ga 1 qo'shib yangi unikal ID yaratadi (`max(..., default=0) + 1`).
- **Unikal Email tekshiruvi:** Bir xil email bilan ikkita talaba qo'shilishi taqiqlanadi.
- **Top Talabalar Reytingi:** `sorted(students, key=lambda s: s.average_grade(), reverse=True)` orqali eng yuqori natijadorlar saralab olinadi.
- **Data Science Agregat Statistikasi:** Guruh o'rtachasi (`sum / len`), eng yuqori (`max`), eng past (`min`), barcha talabalar o'tganligini tekshirish (`all`), va qarzdorlar bor-yo'qligini tekshirish (`any`).

### 4.4. `main.py` — Interaktiv CLI va Boshqaruv
- **Windows UTF-8 moslashuvi:** `sys.stdout.reconfigure(encoding="utf-8")` kodi orqali Windows konsolidagi emoji xatoliklari (charmap codec crash) 100% bartaraf etiladi.
- **Jadval ko'rinishi:** `ID`, `F.I.SH.`, `EMAIL`, `O'RTACHA BALL` va `STATUS` chiroyli formatlangan kenglikda chop etiladi.
- **Xavfsiz O'chirish:** Talabani o'chirishdan oldin foydalanuvchidan `ha/yoq` tasdiqlash so'raladi.

---

## 🗺 5. Modul 01 Mavzularining Loyihadagi In'ikosi

| Dars Raqami | Dars Mavzusi | Loyihada Qo'llanilgan Joyi |
| :--- | :--- | :--- |
| **M01-L02** | Variables & Data Types | `student_id` (int), `full_name` (str), `grades` (list of float), `enrolled_date` (str) |
| **M01-L03** | Operatorlar & I/O | Matnlarni formatlab chiqarish (`f-strings`), `input()` orqali ma'lumot olish |
| **M01-L04** | Shart operatorlari (`if/elif/else`) | Akademik statusni baholash (Honors, Passing, Failing), tasdiqlash so'rovlari |
| **M01-L05** | Takrorlanish (`for/while`) | Boshqaruv menyusi uchun cheksiz `while True` sikli va ro'yxatni aylanib chiqish |
| **M01-L06** | Functions & Scope | Yordamchi UI funksiyalari, parametrlarni uzatish, lambda ifodasi |
| **M01-L07** | List, Tuple, Set, Dict | Talabalar ro'yxati (`list`), JSON lug'atlar (`dict`), qidiruv to'plamlari |
| **M01-L08** | Strings & Built-ins | `.strip()`, `.title()`, `.lower()`, `sum()`, `len()`, `max()`, `min()`, `all()`, `any()` |
| **M01-L09** | File Handling (JSON) | `json.dump()` va `json.load()` yordamida ma'lumotlarni qattiq diskka doimiy saqlash |
| **M01-L10** | Exception Handling | `try/except ValueError`, `json.JSONDecodeError` orqali kiritish xatolarini ushlash |
| **M01-L11** | OOP asoslari | `Student` klassi, `StorageManager`, metodlar, `self`, inkapsulyatsiya, `__init__` |

---

## 🚀 6. Loyihani Ishga Tushirish Qo'llanmasi

1. Loyiha papkasiga o'ting:
   ```bash
   cd "Modules/Modul_01_Python_Fundamentals/Project_01_CLI_Student_Management"
   ```

2. Dasturni ishga tushiring:
   ```bash
   python src/main.py
   ```

3. Interaktiv menyudan foydalaning:
   - `1` — Mavjud barcha talabalar ro'yxatini jadvalda ko'rish
   - `2` — Yangi talaba va uning baholarini kiritish
   - `3` — Mavjud talabaga yangi imtihon bahosini biriktirish
   - `4` — Ism yoki email bo'yicha tezkor qidiruv
   - `5` — Ma'lumotlarni yangilash
   - `6` — Talabani tizimdan o'chirish
   - `7` — Eng a'lochi 5 talaba reytingi
   - `8` — Umumiy kurs statistikasi va ko'rsatkichlar
   - `9` — Dasturdan chiqish (o'zgarishlar saqlangan holda)

---

## 🏆 7. Mustaqil Kengaytirish Uchun Vazifalar (Challenges)

Loyihani yanada takomillashtirish va o'z portfolioingizni boyitish uchun quyidagi imkoniyatlarni qo'shib ko'ring:
1. **CSV Export:** Barcha talabalar ro'yxatini va statistikalarni `students.csv` fayliga eksport qilish funksiyasini qo'shing (`csv` moduli orqali).
2. **Fanlar bo'yicha baholash:** Baholarni shunchaki raqamlar ro'yxati emas, balki fanlar lug'ati ko'rinishida saqlang: `{"Matematika": [90, 85], "Python": [95, 100]}`.
3. **Davomat tizimi (Attendance):** Talabaning dars qoldirish foizini hisoblovchi mexanizm joriy qiling.
