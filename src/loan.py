
from datetime import date
from typing import Dict, Any
from src.library_item import LibraryItem


class Loan:
    def __init__(self, loan_id: str, user_id: str, item_id: str, due: date):
        self.loan_id = loan_id
        self.user_id = user_id
        self.item_id = item_id
        self.due = due
        self.returned = None

    def is_overdue(self, today: date) -> bool:
        return self.returned is None and today > self.due

    def to_dict(self) -> Dict[str, Any]:
        return {
            "loan_id": self.loan_id,
            "user_id": self.user_id,
            "item_id": self.item_id,
            "due": self.due.isoformat(),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Loan":
        return cls(d["loan_id"], d["user_id"], d["item_id"], date.fromisoformat(d["due"]))
