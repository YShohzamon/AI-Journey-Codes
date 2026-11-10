"""
Project 01: CLI Student Management System
Modul: storage.py — Fayllar bilan ishlash (File Handling, JSON, Exception Handling).
"""

import json
import os
from models import Student


class StorageManager:
    """
    Ma'lumotlarni qattiq diskdagi JSON fayliga saqlash va o'qishni boshqaruvchi sinf.
    """

    def __init__(self, file_path: str = None):
        if file_path is None:
            # Standart saqlash manzili: data/students.json
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(base_dir, "data")
            os.makedirs(data_dir, exist_ok=True)
            self.file_path = os.path.join(data_dir, "students.json")
        else:
            self.file_path = file_path

    def load_students(self) -> list[Student]:
        """
        JSON faylidan barcha talabalar ro'yxatini yuklaydi.
        Agar fayl bo'lmasa yoki bo'sh bo'lsa, xatosiz bo'sh ro'yxat qaytaradi.
        """
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, mode="r", encoding="utf-8") as f:
                data = json.load(f)
                return [Student.from_dict(item) for item in data]
        except json.JSONDecodeError:
            print("⚠️ Ogohlantirish: JSON fayl formati buzilgan yoki bo'sh. Bo'sh ro'yxat yaratildi.")
            return []
        except Exception as e:
            print(f"❌ Faylni o'qishda xatolik: {e}")
            return []

    def save_students(self, students: list[Student]) -> bool:
        """
        Talabalar ro'yxatini JSON fayliga saqlaydi.
        """
        try:
            data = [s.to_dict() for s in students]
            with open(self.file_path, mode="w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Ma'lumotlarni saqlashda xatolik yuz berdi: {e}")
            return False
