# Testing Strategy – Project 4 Library Management System

## Overview
This project uses automated testing to verify correctness, integration, and system
reliability. All tests are written using Python’s built-in unittest framework.

---

## Testing Framework
- Framework: Python unittest
- Test Type: Automated
- Execution Method: Command-line test discovery

To run all tests from the project root directory:

```python -m unittest discover -s tests -v```

All tests are expected to pass with no errors.

---

## Test Categories

### Unit Tests
Unit tests verify individual classes and methods in isolation.

Goals:
- Validate object creation
- Ensure input constraints are enforced
- Confirm correct method behavior

Covered components:
- User
- LibraryItem and subclasses (Book, DVD)
- Loan state tracking

Test files:
- tests/test_user_unit.py
- tests/test_library_item_unit.py

---

### Integration Tests
Integration tests verify interaction between multiple system components.

Goals:
- Ensure users, items, and loans coordinate correctly
- Validate JSON save and load functionality

Covered scenarios:
- Checkout workflow
- System state serialization and restoration

Test file:
- tests/test_library_system_integration.py

---

### System / End-to-End Tests
System tests validate complete workflows from start to finish.

Goals:
- Simulate real-world usage
- Verify system-wide behavior
- Confirm output generation

Covered scenarios:
- End-to-end checkout and persistence
- CSV export of overdue loan reports

Test files:
- tests/test_system_e2e.py
- tests/test_csv_export_system.py

---

## CSV Export Verification
Automated system testing verifies the CSV export feature by confirming:
- CSV file creation
- Correct output directory usage
- Presence of data rows beyond the header

---

## Test Coverage Summary
The test suite provides coverage for:
- Core business logic
- Component integration
- JSON persistence
- CSV export functionality
- Error handling and edge cases

---

## Expected Results
Successful test execution produces output similar to:

Ran X tests in Y.YYYs

OK
