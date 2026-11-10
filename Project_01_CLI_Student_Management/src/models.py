"""
Project 01: CLI Student Management System
Modul: models.py — Student (Talaba) ma'lumotlar modeli va validatsiyasi (OOP).
"""

from datetime import datetime


class Student:
    """
    Talaba ob'ektini ifodalovchi sinf (OOP).
    Barcha shaxsiy ma'lumotlar, baholar va hisoblash metodlarini o'z ichiga oladi.
    """

    def __init__(self, student_id: int, full_name: str, email: str, grades: list[float] = None, enrolled_date: str = None):
        self.student_id = student_id
        self.full_name = full_name.strip().title()
        self.email = email.strip().lower()
        self.grades = grades if grades is not None else []
        self.enrolled_date = enrolled_date if enrolled_date else datetime.now().strftime("%Y-%m-%d")

        # Validatsiya
        self._validate()

    def _validate(self):
        """Ma'lumotlar to'g'riligini tekshirish (Data Validation)."""
        if not self.full_name or len(self.full_name) < 3:
            raise ValueError(f"Talaba ismi kamida 3 ta belgidan iborat bo'lishi kerak! Kiritildi: '{self.full_name}'")

        if "@" not in self.email or "." not in self.email:
            raise ValueError(f"Email manzili noto'g'ri formatda! Kiritildi: '{self.email}'")

        for g in self.grades:
            if not (0 <= g <= 100):
                raise ValueError(f"Baho 0 va 100 oralig'ida bo'lishi kerak! Kiritildi: {g}")

    def add_grade(self, grade: float):
        """Yangi baho qo'shish."""
        if not (0 <= grade <= 100):
            raise ValueError(f"Baho 0 va 100 oralig'ida bo'lishi shart! Kiritildi: {grade}")
        self.grades.append(round(float(grade), 1))

    def average_grade(self) -> float:
        """O'rtacha bahoni hisoblash."""
        if not self.grades:
            return 0.0
        return round(sum(self.grades) / len(self.grades), 2)

    def academic_status(self) -> str:
        """Akademik o'zlashtirish holatini aniqlash (Shart operatorlari)."""
        avg = self.average_grade()
        if not self.grades:
            return "Baholanmagan"
        elif avg >= 86.0:
            return "A'lochi (Honors) 🌟"
        elif avg >= 71.0:
            return "Yaxshi (Good) 👍"
        elif avg >= 55.0:
            return "Qoniqarli (Passing) ⚠️"
        else:
            return "Qarzdor (Failing) ❌"

    def to_dict(self) -> dict:
        """JSON saqlash uchun lug'atga aylantirish (Serialization)."""
        return {
            "id": self.student_id,
            "full_name": self.full_name,
            "email": self.email,
            "grades": self.grades,
            "enrolled_date": self.enrolled_date
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        """Lug'atdan yangi Student ob'ektini tiklash (Deserialization)."""
        return cls(
            student_id=data["id"],
            full_name=data["full_name"],
            email=data["email"],
            grades=data.get("grades", []),
            enrolled_date=data.get("enrolled_date")
        )

    def __str__(self) -> str:
        avg = self.average_grade()
        status = self.academic_status()
        return f"[ID: {self.student_id:03d}] {self.full_name:<22} | O'rtacha: {avg:5.1f} | Holat: {status}"

    def __repr__(self) -> str:
        return f"Student(id={self.student_id}, name='{self.full_name}', avg={self.average_grade()})"
