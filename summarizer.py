"""Device Log Summarizer CLI.

Reads a telemetry CSV, aggregates per device, filters out devices whose
average temperature is above a threshold, writes JSON and prints a table.

Usage:
    python summarizer.py --input device_telemetry.csv --output output.json
"""

import argparse
import csv
import json
import math
import sys
from collections import defaultdict

REQUIRED_COLUMNS = {"device_id", "status", "temperature"}
MAX_AVG_TEMPERATURE = 80.0


def parse_args():
    parser = argparse.ArgumentParser(description="Summarize device telemetry CSV.")
    parser.add_argument("--input", default="device_telemetry.csv", help="Input CSV path")
    parser.add_argument("--output", default="output.json", help="Output JSON path")
    parser.add_argument(
        "--max-avg-temp",
        type=float,
        default=MAX_AVG_TEMPERATURE,
        help="Exclude devices whose average temperature is above this value",
    )
    return parser.parse_args()


def read_rows(path):
    """Yield (row_number, row_dict) from the CSV. Exits cleanly on file problems."""
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                sys.exit(f"Error: '{path}' is empty.")
            reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]
            missing = REQUIRED_COLUMNS - set(reader.fieldnames)
            if missing:
                sys.exit(f"Error: missing column(s) in CSV: {', '.join(sorted(missing))}")
            for row_number, row in enumerate(reader, start=2):
                yield row_number, row
    except FileNotFoundError:
        sys.exit(f"Error: file '{path}' not found.")
    except PermissionError:
        sys.exit(f"Error: no permission to read '{path}'.")
    except UnicodeDecodeError:
        sys.exit(f"Error: '{path}' is not a valid text/CSV file.")


def parse_row(row):
    """Return (device_id, status, temperature) or None if the row is invalid."""
    device_id = (row.get("device_id") or "").strip()
    status = (row.get("status") or "").strip().upper()
    if not device_id:
        return None
    try:
        temperature = float((row.get("temperature") or "").strip())
    except ValueError:
        return None
    if math.isnan(temperature) or math.isinf(temperature):
        return None
    return device_id, status, temperature


def aggregate(path):
    """Group rows by device and return (stats_by_device, skipped_row_count)."""
    stats = defaultdict(lambda: {"total_records": 0, "temp_sum": 0.0, "error_count": 0})
    skipped = 0
    for _row_number, row in read_rows(path):
        parsed = parse_row(row)
        if parsed is None:
            skipped += 1
            continue
        device_id, status, temperature = parsed
        entry = stats[device_id]
        entry["total_records"] += 1
        entry["temp_sum"] += temperature
        if status == "ERROR":
            entry["error_count"] += 1
    return stats, skipped


def build_results(stats, max_avg_temp):
    """Compute averages and drop devices whose average exceeds the threshold."""
    results = []
    for device_id in sorted(stats):
        entry = stats[device_id]
        average = entry["temp_sum"] / entry["total_records"]
        if average > max_avg_temp:
            continue
        results.append(
            {
                "device_id": device_id,
                "total_records": entry["total_records"],
                "avg_temperature": round(average, 2),
                "error_count": entry["error_count"],
            }
        )
    return results


def save_json(results, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
    except OSError as exc:
        sys.exit(f"Error: could not write '{path}': {exc}")


def print_table(results):
    header = f"{'Device':<12}{'Records':>10}{'Avg Temp':>12}{'Errors':>10}"
    print(header)
    print("-" * len(header))
    for r in results:
        print(
            f"{r['device_id']:<12}{r['total_records']:>10}"
            f"{r['avg_temperature']:>12.2f}{r['error_count']:>10}"
        )


def main():
    args = parse_args()
    stats, skipped = aggregate(args.input)
    if skipped:
        print(f"Warning: skipped {skipped} invalid row(s).", file=sys.stderr)
    if not stats:
        sys.exit("Error: no valid records found in the input file.")

    results = build_results(stats, args.max_avg_temp)
    save_json(results, args.output)

    excluded = len(stats) - len(results)
    print_table(results)
    print(f"\n{len(results)} device(s) kept, {excluded} excluded (avg temp > {args.max_avg_temp}).")
    print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()