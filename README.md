# Project 4 – Library Management System

## Overview
This project is a Python-based, object-oriented Library Management System developed
as a capstone-style integration assignment. The system brings together users,
library items, loans, persistence, reporting, and automated testing into a single,
cohesive application.

The project demonstrates:
- Object-Oriented Design
- Data Persistence using JSON
- Data Export using CSV
- Automated Testing using Python’s `unittest` framework
- Integration of multiple system components

---

## Project Structure

Project_04/
├── src/
│   ├── library_system.py
│   ├── catalog.py
│   ├── library_item.py
│   ├── loan.py
│   ├── user.py
│
├── tests/
│   ├── test_user_unit.py
│   ├── test_library_item_unit.py
│   ├── test_library_system_integration.py
│   ├── test_system_e2e.py
│   └── test_csv_export_system.py
│
├── output/
│   ├── e2e.json
│   ├── test_state.json
│   └── overdue_report.csv
│
├── docs/
│   └── testing.md
│
└── README.md

---

## How to Run the Program

From the project root directory, run:

python -m src.demo

This demonstration:
- Creates users and library items
- Performs checkout operations
- Saves the system state
- Generates output files

---

## Persistence (JSON)
The system supports saving and loading its complete state using JSON.

Generated files include:
- output/test_state.json
- output/e2e.json

These files store:
- Catalog data
- User data
- Loan records

---

## CSV Export
The system exports overdue loan information to a CSV file:

output/overdue_report.csv

CSV columns include:
- loan_id
- user_id
- item_id
- due_date
- days_overdue

---

## Testing
All tests are implemented using Python’s built-in unittest framework.

To run all tests:

python3 -m unittest discover -s tests -v

All tests pass successfully.

Detailed testing documentation is available in:
docs/testing.md

---

## Demo Video


---

## Author
(Student Name)
