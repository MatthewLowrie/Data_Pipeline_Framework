import csv
import json


def run_pipeline() -> None:
    # Extract from CSV
    records = []
    with open("data/sales.csv", "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(dict(row))

    # Filter out rows where amount is empty
    filtered = [r for r in records if r.get("amount") not in ("", None)]

    # Load to JSON
    with open("output/sales_clean.json", "w") as f:
        json.dump(filtered, f, indent=2)

    print(f"Records processed: {len(filtered)}")


if __name__ == "__main__":
    run_pipeline()