from datetime import date, timedelta
from typing import List, Set, Dict, Any


class LibraryItem:
    def __init__(self, item_id: str, title: str, creators: List[str], tags: Set[str], copies: int):
        self.item_id = item_id
        self.title = title
        self.creators = creators
        self.tags = tags
        self.available_copies = copies

    def is_available(self) -> bool:
        return self.available_copies > 0

    def checkout_copy(self) -> None:
        self.available_copies -= 1

    def return_copy(self) -> None:
        self.available_copies += 1

    def calculate_due_date(self, checkout: date, role: str) -> date:
        return checkout + timedelta(days=14)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "title": self.title,
            "creators": self.creators,
            "tags": list(self.tags),
            "available_copies": self.available_copies,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "LibraryItem":
        return cls(d["item_id"], d["title"], d["creators"], set(d["tags"]), d["available_copies"])


class Book(LibraryItem):
    pass


class DVD(LibraryItem):
    def calculate_due_date(self, checkout: date, role: str) -> date:
        return checkout + timedelta(days=7)


class EBook(LibraryItem):
    def is_available(self) -> bool:
        return True