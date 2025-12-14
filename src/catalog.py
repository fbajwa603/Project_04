
from typing import Dict, List
from src.library_item import LibraryItem


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
