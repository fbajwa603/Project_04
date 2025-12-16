from datetime import date
from pathlib import Path
import json, csv

from src.catalog import Catalog
from src.user import User
from src.library_item import LibraryItem
from src.loan import Loan


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
        """
        Export overdue loans to a CSV file.

        Columns:
            loan_id,user_id,item_id,due_date,days_overdue

        Returns:
            Number of overdue loans written
        """
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