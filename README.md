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
[View on YouTube](https://youtu.be/aPYhjW7IkR4?si=J2Y5gitzK-6nlqWE)