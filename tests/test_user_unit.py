
import unittest
from datetime import date
from src.user import User


class TestUserUnit(unittest.TestCase):

    def test_create_valid_user(self):
        u = User("U1", "alice smith", "Student")
        self.assertEqual(u.user_id, "U1")
        self.assertEqual(u.role, "Student")

    def test_invalid_role_raises(self):
        with self.assertRaises(ValueError):
            User("U2", "bob", "Hacker")

    def test_add_and_remove_loan(self):
        u = User("U3", "carol", "Faculty")
        u.add_loan("L1")
        self.assertEqual(len(u._active_loan_ids), 1)
        u.remove_loan("L1")
        self.assertEqual(len(u._active_loan_ids), 0)
