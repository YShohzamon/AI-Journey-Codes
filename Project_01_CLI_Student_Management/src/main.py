"""
Project 01: CLI Student Management System (Talabalar Boshqaruv Tizimi)
Modul: main.py — Asosiy konsol interfeysi (CLI Dashboard & User Interface).
Muallif: AI Journey Shohzamon
"""

import sys
import os

# Terminal kodirovkasini UTF-8 ga moslash (Windows emoji xatolarini oldini olish)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Modullar importi
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from manager import StudentManager
from storage import StorageManager


def print_header(title: str):
    """Sarlavha chizig'ini formatlab chiqarish."""
    print("\n" + "=" * 65)
    print(f"  📌  {title.upper()}")
    print("=" * 65)


def print_student_table(students: list):
    """Talabalar ro'yxatini jadval ko'rinishida chiqarish."""
    if not students:
        print("\nℹ️  Hozircha tizimda talabalar mavjud emas.")
        return

    print("\n" + "-" * 75)
    print(f"{'ID':<5} | {'F.I.SH.':<22} | {'EMAIL':<22} | {'O\'RT.':<6} | {'STATUS':<15}")
    print("-" * 75)
    for s in students:
        avg = s.average_grade()
        status = s.academic_status()
        print(f"{s.student_id:<5} | {s.full_name:<22} | {s.email:<22} | {avg:<6.1f} | {status:<15}")
    print("-" * 75)


def handle_add_student(manager: StudentManager):
    """Yangi talaba qo'shish oynasi."""
    print_header("Yangi talaba qo'shish")
    try:
        name = input("👤 To'liq ism-familiya: ").strip()
        email = input("📧 Email manzili: ").strip()
        grades_input = input("📝 Boshlang'ich baholar (vergul bilan, masalan: 85, 90, 78 yoki bo'sh qoldiring): ").strip()

        grades = []
        if grades_input:
            raw_grades = grades_input.split(",")
            for g in raw_grades:
                val = float(g.strip())
                grades.append(val)

        student = manager.add_student(full_name=name, email=email, grades=grades)
        print(f"\n✅ Muvaffaqiyatli qo'shildi: {student.full_name} (ID: {student.student_id})")
    except ValueError as e:
        print(f"\n❌ Xatolik: {e}")
    except Exception as e:
        print(f"\n❌ Kutilmagan xatolik yuz berdi: {e}")


def handle_add_grade(manager: StudentManager):
    """Talabaga baho qo'shish."""
    print_header("Talabaga baho qo'shish")
    try:
        s_id = int(input("🆔 Talaba ID sini kiriting: ").strip())
        student = manager.get_student(s_id)
        if not student:
            print(f"❌ ID {s_id} bo'yicha talaba topilmadi!")
            return

        print(f"Tanlandi: {student.full_name} | Hozirgi baholari: {student.grades}")
        grade = float(input("Baho kiriting (0 - 100): ").strip())
        manager.add_grade(s_id, grade)
        print(f"\n✅ Baho qabul qilindi! Yangilangan o'rtacha: {student.average_grade()} ({student.academic_status()})")
    except ValueError as e:
        print(f"\n❌ Noto'g'ri son kiritildi yoki xatolik: {e}")


def handle_search(manager: StudentManager):
    """Qidiruv amali."""
    print_header("Talabani qidirish")
    query = input("🔍 Qidiruv so'zi (ism yoki email): ").strip()
    if not query:
        print("⚠️ Qidiruv so'zi bo'sh bo'lmasligi kerak.")
        return

    results = manager.search_students(query)
    print(f"\nNatijalar soni: {len(results)}")
    print_student_table(results)


def handle_update(manager: StudentManager):
    """Talaba ma'lumotlarini yangilash."""
    print_header("Talaba ma'lumotlarini tahrirlash")
    try:
        s_id = int(input("🆔 Tahrirlanadigan talaba ID sini kiriting: ").strip())
        student = manager.get_student(s_id)
        if not student:
            print(f"❌ ID {s_id} bo'yicha talaba topilmadi!")
            return

        print(f"Joriy ism: {student.full_name}")
        new_name = input("Yangi ism (o'zgarishsiz qoldirish uchun Enter): ").strip()
        print(f"Joriy email: {student.email}")
        new_email = input("Yangi email (o'zgarishsiz qoldirish uchun Enter): ").strip()

        manager.update_student(s_id, new_name=new_name if new_name else None, new_email=new_email if new_email else None)
        print(f"\n✅ Talaba ma'lumotlari yangilandi!")
    except ValueError as e:
        print(f"\n❌ Xatolik: {e}")


def handle_delete(manager: StudentManager):
    """Talabani o'chirish."""
    print_header("Talabani o'chirish")
    try:
        s_id = int(input("🆔 O'chiriladigan talaba ID sini kiriting: ").strip())
        student = manager.get_student(s_id)
        if not student:
            print(f"❌ ID {s_id} bo'yicha talaba topilmadi!")
            return

        confirm = input(f"❓ Haqiqatdan ham '{student.full_name}' ni o'chirmoqchimisiz? (ha/yoq): ").strip().lower()
        if confirm in ["ha", "yes", "h", "y"]:
            manager.delete_student(s_id)
            print(f"\n🗑️ Talaba (ID: {s_id}) muvaffaqiyatli o'chirildi.")
        else:
            print("\n🚫 O'chirish bekor qilindi.")
    except ValueError:
        print("\n❌ Noto'g'ri ID kiritildi.")


def handle_top_students(manager: StudentManager):
    """Top talabalar ro'yxati."""
    print_header("Eng a'lochi talabalar (Top 5)")
    top_list = manager.get_top_students(5)
    print_student_table(top_list)


def handle_statistics(manager: StudentManager):
    """Umumiy analitika."""
    print_header("Tizim statistikasi & Hisobot")
    stats = manager.get_statistics()

    print(f"📊 Jami talabalar soni:        {stats['total_students']}")
    print(f"📝 Baholangan talabalar:       {stats['graded_count']}")
    print(f"📈 Guruh o'rtacha balli:        {stats['class_average']}")
    print(f"🥇 Eng yuqori o'rtacha ball:    {stats['highest_avg']}")
    print(f"📉 Eng past o'rtacha ball:      {stats['lowest_avg']}")
    print("-" * 50)
    print(f"🌟 A'lochilar soni (>=86):     {stats['honors_count']}")
    print(f"👍 O'tish ballini olganlar:     {stats['passing_count']}")
    print(f"❌ Qarzdorlar soni (<55):       {stats['failing_count']}")
    print(f"⚠️ Qarzdorlar mavjudmi:        {'Ha' if stats['has_failures'] else 'Yo\'q'}")
    print(f"🎯 Hamma imtihondan o'tdimi:   {'Ha' if stats['all_passing'] else 'Yo\'q'}")


def main_menu():
    """Asosiy interaktiv boshqaruv tsikli (Infinite Loop)."""
    manager = StudentManager()

    while True:
        print("\n" + "=" * 65)
        print("  🎓  TALABALARNI BOSHQARISH TIZIMI (CLI STUDENT SYSTEM)")
        print("=" * 65)
        print("  1. 📋 Barcha talabalarni ko'rish")
        print("  2. ➕ Yangi talaba qo'shish")
        print("  3. 📝 Talabaga baho qo'shish")
        print("  4. 🔍 Talabani qidirish")
        print("  5. ✏️  Talaba ma'lumotlarini yangilash")
        print("  6. 🗑️  Talabani o'chirish")
        print("  7. 🏆 Top talabalar reytingi (Top 5)")
        print("  8. 📊 Umumiy statistika va hisobot")
        print("  9. 🚪 Dasturdan chiqish")
        print("=" * 65)

        tanlov = input("👉 Tanlovingizni kiriting (1-9): ").strip()

        if tanlov == "1":
            print_header("Barcha talabalar ro'yxati")
            print_student_table(manager.get_all_students())
        elif tanlov == "2":
            handle_add_student(manager)
        elif tanlov == "3":
            handle_add_grade(manager)
        elif tanlov == "4":
            handle_search(manager)
        elif tanlov == "5":
            handle_update(manager)
        elif tanlov == "6":
            handle_delete(manager)
        elif tanlov == "7":
            handle_top_students(manager)
        elif tanlov == "8":
            handle_statistics(manager)
        elif tanlov == "9":
            print("\n👋 Tizimdan chiqildi. Barcha ma'lumotlar saqlandi. Xayr!")
            break
        else:
            print("\n⚠️ Noto'g'ri tanlov! Iltimos 1 dan 9 gacha bo'lgan raqamni kiriting.")


if __name__ == "__main__":
    main_menu()
