"""
Project 01: CLI Student Management System
Modul: manager.py — CRUD operatsiyalari, tahlil va biznes mantiq (Business Logic).
"""

from models import Student
from storage import StorageManager


class StudentManager:
    """
    Talabalar bazasini boshqaruvchi markaziy tizim (Service Layer).
    Barcha qo'shish, o'chirish, yangilash, saralash va statistik hisob-kitoblarni amalga oshiradi.
    """

    def __init__(self, storage: StorageManager = None):
        self.storage = storage if storage else StorageManager()
        self.students: list[Student] = self.storage.load_students()

    def _generate_next_id(self) -> int:
        """Yangi talaba uchun ketma-ket unikal ID generatsiya qilish."""
        if not self.students:
            return 1
        return max(s.student_id for s in self.students) + 1

    def add_student(self, full_name: str, email: str, grades: list[float] = None) -> Student:
        """
        Yangi talaba qo'shish va diskka saqlash.
        Email unikal bo'lishi tekshiriladi.
        """
        # Email unikal ekanligini tekshirish
        for s in self.students:
            if s.email.lower() == email.strip().lower():
                raise ValueError(f"'{email}' emaili bilan ro'yxatdan o'tgan talaba allaqachon mavjud! (ID: {s.student_id})")

        new_id = self._generate_next_id()
        new_student = Student(student_id=new_id, full_name=full_name, email=email, grades=grades)
        self.students.append(new_student)
        self.storage.save_students(self.students)
        return new_student

    def get_student(self, student_id: int) -> Student | None:
        """ID bo'yicha talabani topish."""
        for s in self.students:
            if s.student_id == student_id:
                return s
        return None

    def search_students(self, query: str) -> list[Student]:
        """
        Ism yoki email bo'yicha qidiruv (case-insensitive substring match).
        """
        q = query.strip().lower()
        return [s for s in self.students if q in s.full_name.lower() or q in s.email.lower()]

    def update_student(self, student_id: int, new_name: str = None, new_email: str = None) -> bool:
        """Talaba ismini yoki emailini yangilash."""
        student = self.get_student(student_id)
        if not student:
            return False

        if new_email and new_email.strip().lower() != student.email:
            # Yangi email boshqa talabada yo'qligini tekshirish
            for s in self.students:
                if s.student_id != student_id and s.email.lower() == new_email.strip().lower():
                    raise ValueError(f"'{new_email}' emaili boshqa talabaga tegishli!")
            student.email = new_email.strip().lower()

        if new_name:
            student.full_name = new_name.strip().title()

        student._validate()
        return self.storage.save_students(self.students)

    def add_grade(self, student_id: int, grade: float) -> bool:
        """Mavjud talabaga yangi baho biriktirish."""
        student = self.get_student(student_id)
        if not student:
            return False

        student.add_grade(grade)
        return self.storage.save_students(self.students)

    def delete_student(self, student_id: int) -> bool:
        """ID bo'yicha talabani ro'yxatdan va diskdan butunlay o'chirish."""
        student = self.get_student(student_id)
        if not student:
            return False

        self.students.remove(student)
        return self.storage.save_students(self.students)

    def get_all_students(self) -> list[Student]:
        """Barcha talabalar ro'yxatini qaytaradi."""
        return self.students

    def get_top_students(self, top_n: int = 5) -> list[Student]:
        """
        O'rtacha bahosi eng yuqori bo'lgan top talabalarni saralab qaytarish.
        Higher-Order funktsiya va lambda ifodasi qo'llaniladi.
        """
        graded = [s for s in self.students if s.grades]
        return sorted(graded, key=lambda s: s.average_grade(), reverse=True)[:top_n]

    def get_statistics(self) -> dict:
        """
        Tizimdagi umumiy analitik ko'rsatkichlarni hisoblash.
        AI va Data Science uchun ma'lumotlar agregatsiyasi (sum, len, min, max, all, any).
        """
        total = len(self.students)
        if total == 0:
            return {
                "total_students": 0,
                "graded_count": 0,
                "class_average": 0.0,
                "highest_avg": 0.0,
                "lowest_avg": 0.0,
                "honors_count": 0,
                "passing_count": 0,
                "failing_count": 0,
                "has_failures": False,
                "all_passing": False
            }

        graded = [s for s in self.students if s.grades]
        averages = [s.average_grade() for s in graded]

        honors = [s for s in graded if s.average_grade() >= 86.0]
        passing = [s for s in graded if 55.0 <= s.average_grade() < 86.0]
        failing = [s for s in graded if s.average_grade() < 55.0]

        class_avg = round(sum(averages) / len(averages), 2) if averages else 0.0
        max_avg = max(averages) if averages else 0.0
        min_avg = min(averages) if averages else 0.0

        return {
            "total_students": total,
            "graded_count": len(graded),
            "class_average": class_avg,
            "highest_avg": max_avg,
            "lowest_avg": min_avg,
            "honors_count": len(honors),
            "passing_count": len(passing),
            "failing_count": len(failing),
            "has_failures": any(s.average_grade() < 55.0 for s in graded),
            "all_passing": all(s.average_grade() >= 55.0 for s in graded) if graded else False
        }
