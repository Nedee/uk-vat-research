
import csv
import re
from pathlib import Path

INPUT_FILE = Path("results/vat_results.csv")
OUTPUT_FILE = Path("results/vat_results_clean.csv")


def parse_response(response):
    response = response or ""

    result = {
        "status": "UNKNOWN",
        "business_name": "",
        "business_address": ""
    }

    if "HTTP ERROR 429" in response:
        result["status"] = "RATE_LIMITED"
        return result

    if "Valid UK VAT number" in response:
        result["status"] = "VALID"

        name_match = re.search(
            r"Registered business name\s*\n([^\n]+)",
            response
        )

        if name_match:
            result["business_name"] = name_match.group(1).strip()

        address_match = re.search(
            r"Registered business address\s*\n(.*?)"
            r"\n\s*GB\s*(?=\n|$)",
            response,
            re.DOTALL
        )

        if address_match:
            lines = [
                line.strip()
                for line in address_match.group(1).splitlines()
                if line.strip()
            ]
            result["business_address"] = ", ".join(lines) + ", GB"

        return result

    if "VAT registration not found" in response:
        result["status"] = "NOT_FOUND"
        return result

    if (
        "This page isn’t working" in response
        or "This page isn't working" in response
    ):
        result["status"] = "TECHNICAL_ERROR"
        return result

    return result


def main():
    if not INPUT_FILE.exists():
        print("Input file not found:", INPUT_FILE)
        return

    records = []

    with open(INPUT_FILE, encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            if len(row) < 2:
                continue

            records.append(row)

    if not records:
        print("No records found.")
        return

    # Detect whether the first row is a header
    first_row = [cell.strip().lower() for cell in records[0]]

    if (
        "vat_number" in first_row
        or "hmrc_response" in first_row
    ):
        records = records[1:]

    results = []

    for row in records:
        vat = row[0].strip()
        response = row[1]

        parsed = parse_response(response)

        results.append({
            "vat_number": vat,
            "status": parsed["status"],
            "business_name": parsed["business_name"],
            "business_address": parsed["business_address"]
        })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        columns = [
            "vat_number",
            "status",
            "business_name",
            "business_address"
        ]

        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(results)

    print("\nProcessing completed!")
    print("Total:", len(results))

    for status in [
        "VALID",
        "NOT_FOUND",
        "RATE_LIMITED",
        "TECHNICAL_ERROR",
        "UNKNOWN"
    ]:
        count = sum(r["status"] == status for r in results)
        print(f"{status}: {count}")

    print("\nSaved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
