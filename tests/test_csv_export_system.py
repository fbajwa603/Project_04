import unittest
from datetime import date
from pathlib import Path

from src.user import User
from src.library_item import Book
from src.library_system import LibrarySystem


class TestCSVExportSystem(unittest.TestCase):

    def test_overdue_csv_created_and_populated(self):
        system = LibrarySystem("CSV Test Library")

        user = User("U1", "alice", "Student")
        book = Book("B1", "Test Book", ["Author"], {"cs"}, 1)

        system.add_user(user)
        system.add_item(book)

        system.checkout_item(
            loan_id="L1",
            user_id="U1",
            item_id="B1",
            checkout=date(2025, 1, 1),
        )

        csv_path = Path("output/overdue_report.csv")

        count = system.export_overdue_loans_csv(
            csv_path,
            today=date(2025, 2, 1),
        )

        self.assertTrue(csv_path.exists(), "CSV file was not created")
        self.assertGreaterEqual(count, 1, "No overdue loans were written")

        with csv_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()
            self.assertGreaterEqual(len(lines), 2)
