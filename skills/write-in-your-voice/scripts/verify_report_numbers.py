#!/usr/bin/env python
"""Re-check the arithmetic that a finished report states, from its own text.

Usage:
    python verify_report_numbers.py report.pdf      (needs the pdftotext command)
    python verify_report_numbers.py report.txt

It reads the report text and recomputes every worked subtraction of the form
"a - b  c" or "a - b = c" (table cells or prose, ASCII or Unicode minus) and
every percentage of the form "100 x a / b = c". The exit code is 1 if a stated
result differs from the recomputed one by more than --tol (default 0.005).

The script only checks what is written in the report. It does not compare the
report with the result files; build the tables from the result files for that.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

NUM = r"\d+(?:\.\d+)?"
MINUS = "[-−–]"
SUB = re.compile(rf"({NUM})\s*{MINUS}\s*({NUM})\s*(?:=\s*)?([+\-−]\s*{NUM})(?:\s*pp)?")
PCT = re.compile(rf"100\s*[x×*]\s*({NUM})\s*/\s*({NUM})\s*=\s*({NUM})\s*%")


def read_text(path):
    path = Path(path)
    if path.suffix.lower() == ".pdf":
        result = subprocess.run(["pdftotext", "-layout", str(path), "-"],
                                capture_output=True, text=True, check=True)
        return result.stdout
    return path.read_text(encoding="utf-8")


def signed(text):
    return float(text.replace("−", "-").replace(" ", ""))


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("report")
    parser.add_argument("--tol", type=float, default=0.005)
    args = parser.parse_args()
    text = read_text(args.report)

    checked, failed = 0, 0
    for a, b, stated in SUB.findall(text):
        checked += 1
        value = float(a) - float(b)
        if abs(value - signed(stated)) > args.tol:
            failed += 1
            print(f"MISMATCH  {a} - {b} = {value:+.2f}, report says {stated}")
    for a, b, stated in PCT.findall(text):
        checked += 1
        value = 100.0 * float(a) / float(b)
        if abs(value - float(stated)) > args.tol:
            failed += 1
            print(f"MISMATCH  100 x {a} / {b} = {value:.2f}, report says {stated}")

    print(f"checked {checked} worked calculations, {failed} mismatch(es)")
    if checked == 0:
        print("No worked calculation was recognised; check the text extraction.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
