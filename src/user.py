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