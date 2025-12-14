
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
