
import unittest
from datetime import date
from pathlib import Path
from src.user import User
from src.library_item import Book
from src.library_system import LibrarySystem


class TestSystemEndToEnd(unittest.TestCase):

    def test_full_workflow(self):
        system = LibrarySystem("E2E Library")
        user = User("U9", "end user", "Student")
        book = Book("B9", "End Book", ["X"], {"tag"}, 1)

        system.add_user(user)
        system.add_item(book)

        loan = system.checkout_item("L9", "U9", "B9", date(2025, 2, 1))
        self.assertEqual(loan.loan_id, "L9")

        path = Path("output/e2e.json")
        path.parent.mkdir(exist_ok=True)
        system.save_state(path)

        loaded = LibrarySystem.load_state(path)
        self.assertIn("U9", loaded.users)
        self.assertIn("L9", loaded.loans)
