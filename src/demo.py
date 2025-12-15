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