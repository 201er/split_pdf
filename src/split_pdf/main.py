import os
from pathlib import Path
import csv
from pypdf import PdfReader, PdfWriter

BASE_DIR = Path(__file__).resolve().parent

INPUT_PDF = BASE_DIR / "Confirm_Ladies.pdf"
CSV_FILE = BASE_DIR / "confirm_ladies.csv"
PAGES_PER_FILE = 14
OUTPUT_DIR = BASE_DIR / "confirm"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read names (first column, skip header if you have one)
with open(CSV_FILE, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    # next(reader)  # uncomment if the CSV has a header row
    names = [row[0].strip() for row in reader if row]

pdf = PdfReader(INPUT_PDF)
total_pages = len(pdf.pages)
num_files = total_pages // PAGES_PER_FILE   # 1078 / 14 = 77

print(f"Total pages: {total_pages}, files to create: {num_files}, names: {len(names)}")

if total_pages % PAGES_PER_FILE != 0:
    print("Warning: pages don't divide evenly; last chunk will be shorter.")
    num_files += 1

if len(names) < num_files:
    raise ValueError(f"Need {num_files} names but CSV only has {len(names)}")

for i in range(num_files):
    writer = PdfWriter()
    start = i * PAGES_PER_FILE
    end = min(start + PAGES_PER_FILE, total_pages)

    for p in range(start, end):
        writer.add_page(pdf.pages[p])

    # Remove characters not allowed in filenames
    safe_name = "".join(c for c in names[i] if c not in r'\/:*?"<>|').strip()
    out_path = os.path.join(OUTPUT_DIR, f"{safe_name}.pdf")

    with open(out_path, "wb") as out:
        writer.write(out)

print("Done!")