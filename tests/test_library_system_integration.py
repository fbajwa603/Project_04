import unittest
from datetime import date
from pathlib import Path
from src.user import User
from src.library_item import Book
from src.library_system import LibrarySystem


class TestLibrarySystemIntegration(unittest.TestCase):

    def setUp(self):
        self.system = LibrarySystem("Test Library")
        self.user = User("U1", "alice", "Student")
        self.book = Book("B1", "DB Book", ["Kim"], {"cs"}, 1)
        self.system.add_user(self.user)
        self.system.add_item(self.book)

    def test_checkout_flow(self):
        loan = self.system.checkout_item("L1", "U1", "B1", date(2025, 1, 1))
        self.assertEqual(loan.user_id, "U1")
        self.assertFalse(self.book.is_available())

    def test_save_and_load(self):
        self.system.checkout_item("L1", "U1", "B1", date(2025, 1, 1))
        path = Path("output/test_state.json")
        path.parent.mkdir(exist_ok=True)
        self.system.save_state(path)
        loaded = LibrarySystem.load_state(path)
        self.assertEqual(len(loaded.users), 1)
        self.assertEqual(len(loaded.loans), 1)
