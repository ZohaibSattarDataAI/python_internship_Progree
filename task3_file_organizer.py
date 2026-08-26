"""
TASK 3: Automated File Operating & Text-Parsing Script
--------------------------------------------------------
Objective : Build a background automation utility that organizes a messy
            directory into extension-based subfolders AND extracts
            structured data (emails / transaction IDs) from flat log/text
            files using regular expressions, writing results to a master
            CSV file.

Standard library only: os, shutil, re, pathlib, csv, datetime.
"""

import os
import re
import csv
import shutil
from pathlib import Path
from datetime import datetime


# ------------------------------------------------------------------
# Regex patterns for extraction
# ------------------------------------------------------------------
EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
TRANSACTION_ID_PATTERN = re.compile(r"\bTXN[-_]?\d{6,12}\b", re.IGNORECASE)

# Extension -> destination subfolder mapping
EXTENSION_MAP = {
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images",
    ".pdf": "Documents", ".docx": "Documents", ".doc": "Documents", ".txt": "TextFiles",
    ".log": "Logs", ".csv": "Spreadsheets", ".xlsx": "Spreadsheets",
    ".mp4": "Videos", ".mp3": "Audio", ".zip": "Archives", ".rar": "Archives",
    ".py": "Scripts", ".json": "DataFiles",
}


def sort_files_by_extension(source_dir: str) -> dict:
    """
    Scan `source_dir` and move each file into a subfolder based on its
    extension (creating subfolders as needed).

    Returns
    -------
    dict
        A summary: {extension: number_of_files_moved}
    """
    source_path = Path(source_dir)
    if not source_path.exists() or not source_path.is_dir():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    summary = {}

    for item in source_path.iterdir():
        if item.is_file():
            ext = item.suffix.lower()
            folder_name = EXTENSION_MAP.get(ext, "Others")
            dest_folder = source_path / folder_name
            dest_folder.mkdir(exist_ok=True)

            destination = dest_folder / item.name
            # avoid overwriting existing files with the same name
            counter = 1
            while destination.exists():
                destination = dest_folder / f"{item.stem}_{counter}{item.suffix}"
                counter += 1

            shutil.move(str(item), str(destination))
            summary[ext or "no_extension"] = summary.get(ext or "no_extension", 0) + 1

    return summary


def extract_patterns_from_file(file_path: str) -> dict:
    """
    Read a text/log file and extract all emails and transaction IDs found.

    Returns
    -------
    dict
        {"emails": [...], "transaction_ids": [...]}
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except OSError as e:
        print(f"Could not read {file_path}: {e}")
        return {"emails": [], "transaction_ids": []}

    emails = EMAIL_PATTERN.findall(content)
    transaction_ids = TRANSACTION_ID_PATTERN.findall(content)

    return {"emails": emails, "transaction_ids": transaction_ids}


def scan_logs_to_csv(logs_dir: str, output_csv: str) -> int:
    """
    Walk through `logs_dir`, extract emails and transaction IDs from every
    .txt / .log file, and write a clean master CSV report.

    Returns
    -------
    int
        Total number of records written.
    """
    logs_path = Path(logs_dir)
    if not logs_path.exists():
        raise FileNotFoundError(f"Logs directory not found: {logs_dir}")

    records = []
    for file_path in logs_path.rglob("*"):
        if file_path.suffix.lower() in (".txt", ".log") and file_path.is_file():
            results = extract_patterns_from_file(str(file_path))
            for email in results["emails"]:
                records.append({
                    "source_file": file_path.name,
                    "type": "email",
                    "value": email,
                    "scanned_at": datetime.now().isoformat(timespec="seconds"),
                })
            for txn in results["transaction_ids"]:
                records.append({
                    "source_file": file_path.name,
                    "type": "transaction_id",
                    "value": txn,
                    "scanned_at": datetime.now().isoformat(timespec="seconds"),
                })

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["source_file", "type", "value", "scanned_at"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    return len(records)


if __name__ == "__main__":
    # ---- Demo setup: creates a sample messy folder to show functionality ----
    demo_dir = "demo_workspace"
    os.makedirs(demo_dir, exist_ok=True)

    sample_files = {
        "photo1.jpg": "binary-image-data",
        "report.pdf": "pdf-content",
        "notes.txt": "just some notes",
        "access.log": (
            "User login from john.doe@example.com at 10:02am\n"
            "Payment processed TXN-004821 for jane_smith99@mail.co\n"
            "Failed login attempt from unknown@corp.io, ref TXN991234567\n"
        ),
    }
    for filename, content in sample_files.items():
        with open(os.path.join(demo_dir, filename), "w", encoding="utf-8") as f:
            f.write(content)

    # 1) Sort files into subfolders by extension
    result = sort_files_by_extension(demo_dir)
    print("Files organized:", result)

    # 2) Extract emails / transaction IDs from logs and write master CSV
    logs_subfolder = os.path.join(demo_dir, "Logs")
    output_csv_path = os.path.join(demo_dir, "master_report.csv")
    total = scan_logs_to_csv(logs_subfolder, output_csv_path)
    print(f"Extracted {total} records -> {output_csv_path}")
