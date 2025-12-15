# catalog.py
from typing import Dict
from library_item import LibraryItem
class Catalog:
    def __init__(self, name: str):
        self._name = name
        self._items: Dict[str, LibraryItem] = {}

    def add_item(self, item: LibraryItem) -> None:
        self._items[item.item_id] = item

    def get_item(self, item_id: str):
        return self._items.get(item_id)

    def to_dict(self):
        return {"name": self._name, "items": [i.to_dict() for i in self._items.values()]}

    @classmethod
    def from_dict(cls, d):
        c = cls(d["name"])
        for item in d["items"]:
            c.add_item(LibraryItem.from_dict(item))
        return c
# demo.py
from datetime import date
from pathlib import Path
from user import User
from library_item import Book, DVD, EBook
from library_system import LibrarySystem

print("=== PROJECT 4 DEMO ===")

system = LibrarySystem("Demo Library")

u1 = User("U1", "alice", "Student")
system.add_user(u1)

b = Book("B1", "Databases", ["Kim"], {"cs"}, 2)
d = DVD("D1", "Documentary", ["Doe"], {"video"}, 1)

system.add_item(b)
system.add_item(d)

loan = system.checkout_item("L1", "U1", "B1", date(2025, 3, 1))
print("Loan created:", loan.loan_id)

path = Path("output/state.json")
path.parent.mkdir(exist_ok=True)
system.save_state(path)
print("State saved")

# hold.py
from datetime import date
from typing import Dict, Any


class Hold:
    def __init__(self, hold_id: str, user_id: str, item_id: str, placed_on: date, expires_on: date):
        self._hold_id = hold_id
        self._user_id = user_id
        self._item_id = item_id
        self._placed_on = placed_on
        self._expires_on = expires_on

    def is_active(self, today: date) -> bool:
        return today <= self._expires_on

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hold_id": self._hold_id,
            "user_id": self._user_id,
            "item_id": self._item_id,
            "placed_on": self._placed_on.isoformat(),
            "expires_on": self._expires_on.isoformat(),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Hold":
        return cls(
            d["hold_id"],
            d["user_id"],
            d["item_id"],
            date.fromisoformat(d["placed_on"]),
            date.fromisoformat(d["expires_on"]),
        )

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

from datetime import date
from pathlib import Path
import json, csv

from catalog import Catalog
from user import User
from library_item import LibraryItem
from loan import Loan


class LibrarySystem:
    def __init__(self, name: str):
        self.catalog = Catalog(name)
        self.users = {}
        self.loans = {}

    def add_user(self, user: User):
        self.users[user.user_id] = user

    def add_item(self, item: LibraryItem):
        self.catalog.add_item(item)

    def checkout_item(self, loan_id: str, user_id: str, item_id: str, checkout: date):
        user = self.users[user_id]
        item = self.catalog.get_item(item_id)
        due = item.calculate_due_date(checkout, user.role)
        item.checkout_copy()
        loan = Loan(loan_id, user_id, item_id, due)
        self.loans[loan_id] = loan
        user.add_loan(loan_id)
        return loan

    def save_state(self, path: Path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:
            json.dump(
                {
                    "catalog": self.catalog.to_dict(),
                    "users": [u.to_dict() for u in self.users.values()],
                    "loans": [l.to_dict() for l in self.loans.values()],
                },
                f,
                indent=2,
            )

    @classmethod
    def load_state(cls, path: Path) -> "LibrarySystem":
        with Path(path).open("r", encoding="utf-8") as f:
            data = json.load(f)

        system = cls(data["catalog"]["name"])
        system.catalog = Catalog.from_dict(data["catalog"])

        for u in data["users"]:
            system.users[u["user_id"]] = User.from_dict(u)

        for l in data["loans"]:
            loan = Loan.from_dict(l)
            system.loans[loan.loan_id] = loan

        return system

    def export_overdue_loans_csv(self, out_path: Path, today: date) -> int:
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        overdue_loans = [
            loan for loan in self.loans.values()
            if loan.is_overdue(today)
        ]

        with out_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["loan_id", "user_id", "item_id", "due_date", "days_overdue"]
            )

            for loan in overdue_loans:
                writer.writerow([
                    loan.loan_id,
                    loan.user_id,
                    loan.item_id,
                    loan.due.isoformat(),
                    loan.days_overdue(today),
                ])

        return len(overdue_loans)

# loan.py
from datetime import date
from typing import Dict, Any


class Loan:
    def __init__(self, loan_id: str, user_id: str, item_id: str, due: date):
        self.loan_id = loan_id
        self.user_id = user_id
        self.item_id = item_id
        self.due = due
        self.returned = None

    @property
    def due_date(self) -> date:
        return self.due

    def is_overdue(self, today: date) -> bool:
        return self.returned is None and today > self.due

    def days_overdue(self, today: date) -> int:
        if not self.is_overdue(today):
            return 0
        return (today - self.due).days

    def to_dict(self) -> Dict[str, Any]:
        return {
            "loan_id": self.loan_id,
            "user_id": self.user_id,
            "item_id": self.item_id,
            "due": self.due.isoformat(),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Loan":
        return cls(
            d["loan_id"],
            d["user_id"],
            d["item_id"],
            date.fromisoformat(d["due"])
        )

# user.py
from datetime import date, timedelta
from typing import List, Dict, Any


def normalize_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split())


def validate_user_role(role: str) -> bool:
    return role in {"Student", "Faculty", "Staff", "Admin", "Public"}


def calculate_due_date(checkout_date: date, role: str) -> date:
    if role in {"Student", "Public"}:
        return checkout_date + timedelta(days=14)
    return checkout_date + timedelta(days=28)


class User:
    def __init__(self, user_id: str, name: str, role: str):
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")
        if not validate_user_role(role):
            raise ValueError(f"Invalid role: {role}")

        self._user_id = user_id.strip()
        self._name = normalize_name(name)
        self._role = role
        self._active_loan_ids: List[str] = []
        self._total_fines = 0.0

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def role(self) -> str:
        return self._role

    def add_loan(self, loan_id: str) -> None:
        self._active_loan_ids.append(loan_id)

    def remove_loan(self, loan_id: str) -> None:
        self._active_loan_ids.remove(loan_id)

    def add_fine(self, amount: float) -> None:
        self._total_fines += amount

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self._user_id,
            "name": self._name,
            "role": self._role,
            "active_loan_ids": list(self._active_loan_ids),
            "total_fines": self._total_fines,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        u = cls(data["user_id"], data["name"], data["role"])
        u._active_loan_ids = data.get("active_loan_ids", [])
        u._total_fines = data.get("total_fines", 0.0)
        return u
