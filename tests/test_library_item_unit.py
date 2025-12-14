
import unittest
from datetime import date
from src.library_item import Book, DVD


class TestLibraryItemUnit(unittest.TestCase):

    def test_book_checkout_and_return(self):
        b = Book("B1", "Test Book", ["Author"], {"tag"}, 2)
        self.assertTrue(b.is_available())
        b.checkout_copy()
        self.assertEqual(b.available_copies, 1)
        b.return_copy()
        self.assertEqual(b.available_copies, 2)

    def test_dvd_due_date(self):
        d = DVD("D1", "Movie", ["Dir"], {"video"}, 1)
        due = d.calculate_due_date(date(2025, 1, 1), "Student")
        self.assertEqual((due - date(2025, 1, 1)).days, 7)
