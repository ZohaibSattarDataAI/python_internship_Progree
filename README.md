# Python Programming Tasks

Progree internship ke liye Python tasks (Task 2, 3, 4). Task 1 (LinkedIn post) already complete hai, is liye is folder mein sirf code deliverables hain.

## Folder Structure

```
python_tasks/
├── task2_fibonacci.py         # Fibonacci generation module
├── task3_file_organizer.py    # File sorting + regex log parser
├── task4_chatbot.py           # Rule-based terminal chatbot
└── README.md
```

---

## Task 2 — Core Algorithmic Fibonacci Generation Module

**File:** `task2_fibonacci.py`

- `generate_fibonacci(n)` — first `n` Fibonacci numbers, returned as a list.
- `generate_fibonacci_upto(limit)` — all Fibonacci numbers `<= limit`.
- **Parameter sanitization:** raises `TypeError` for non-integers and `ValueError` for negative bounds.
- **Benchmarking:** `benchmark()` uses Python's built-in `timeit` module to measure execution time over 1000 runs and prints average time per call in microseconds.

Run it:
```bash
python3 task2_fibonacci.py
```

---

## Task 3 — Automated File Operating & Text-Parsing Script

**File:** `task3_file_organizer.py`

- `sort_files_by_extension(source_dir)` — scans a directory and moves each file into an extension-based subfolder (`Images/`, `Documents/`, `Logs/`, etc.), auto-creating folders and avoiding name collisions.
- `extract_patterns_from_file(file_path)` — uses regex to pull **emails** and **transaction IDs** (`TXN-123456` style patterns) out of a text/log file.
- `scan_logs_to_csv(logs_dir, output_csv)` — walks all `.txt`/`.log` files in a folder, extracts every match, and writes a clean **master CSV** (`source_file, type, value, scanned_at`).
- Built entirely with standard library: `os`, `shutil`, `re`, `pathlib`, `csv`, `datetime`.

Run it (creates a `demo_workspace/` with sample files to demonstrate sorting + extraction):
```bash
python3 task3_file_organizer.py
```

To use on your own folder, import the functions and call:
```python
from task3_file_organizer import sort_files_by_extension, scan_logs_to_csv

sort_files_by_extension("path/to/messy_folder")
scan_logs_to_csv("path/to/messy_folder/Logs", "master_report.csv")
```

---

## Task 4 — Multi-Intent Rule-Based Chatbot (Mini Project)

**File:** `task4_chatbot.py`

- `normalize_text()` — lowercases input, strips punctuation, and collapses whitespace.
- `detect_intent()` — nested `if-elif-else` logic layered on top of a keyword **dictionary map** (`INTENT_KEYWORDS`) to classify user intent (greeting, farewell, order status, account help, support, thanks, small talk, fallback).
- `INTENT_HANDLERS` — a functional dictionary map routing each detected intent to its handler function.
- `ChatSession` class — keeps simple session state: user's name, last topic discussed, order ID.
- Graceful fallback replies when input isn't understood, referencing the last topic for context.
- Runs as an interactive terminal loop (`run_chat_loop()`), exits on "bye"/"exit"/"quit".

Run it interactively:
```bash
python3 task4_chatbot.py
```

Example session:
```
Bot: Hi! Type 'bye' anytime to exit.
You: hi
Bot: Hi there! I'm your assistant bot. What's your name?
You: my name is Ali
Bot: Nice to meet you, Ali! How can I help — orders, account, or general support?
You: order 123456
Bot: Checking status for order #123456... it's currently in transit and expected soon.
You: bye
Bot: Goodbye, Ali! Have a great day.
```

---

## Requirements

- Python 3.8+
- No external dependencies — only standard library modules are used (`timeit`, `os`, `re`, `shutil`, `pathlib`, `csv`, `datetime`).
