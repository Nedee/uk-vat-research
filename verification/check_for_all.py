
import csv
import re
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

HMRC_URL = (
    "https://www.tax.service.gov.uk/"
    "check-vat-number/enter-vat-details"
)

INPUT_FILE = Path("vat_inputs/vat_numbers.txt")
OUTPUT_FILE = Path("results/vat_results.csv")


def normalize_vat(vat):
    vat = vat.upper().replace(" ", "").strip()

    if vat.startswith("GB"):
        vat = vat[2:]

    if not re.fullmatch(r"\d{9}", vat):
        return None

    return "GB" + vat


def load_vat_numbers():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(INPUT_FILE)

    numbers = []

    with open(INPUT_FILE, encoding="utf-8") as file:
        for line in file:
            if line.strip():
                vat = normalize_vat(line)

                if vat:
                    numbers.append(vat)
                else:
                    print("Invalid format:", line.strip())

    # Remove duplicates, preserving order
    return list(dict.fromkeys(numbers))


def save_result(vat, response):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    file_exists = OUTPUT_FILE.exists()

    with open(
        OUTPUT_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "vat_number",
                "hmrc_response"
            ])

        writer.writerow([vat, response])


def main():
    vat_numbers = load_vat_numbers()

    print(f"\nFound {len(vat_numbers)} VAT numbers.")

    if not vat_numbers:
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            for index, vat in enumerate(vat_numbers, start=1):

                print(f"\n[{index}/{len(vat_numbers)}] Testing {vat}")

                input("Press ENTER to open HMRC checker...")

                page.goto(HMRC_URL)

                # Enter VAT number
                page.get_by_role("textbox").first.fill(vat)

                # Submit the form
                page.get_by_role(
                    "button",
                    name="Search"
                ).click()

                page.wait_for_load_state("domcontentloaded")

                # Allow the result page to render
                page.wait_for_timeout(1500)

                # Capture the complete visible response
                response = page.locator("body").inner_text()

                print("\nHMRC response:")
                print(response)

                save_result(vat, response)

                print("\nSaved to CSV.")

                time.sleep(2)

        finally:
            browser.close()

    print("\nFinished!")


if __name__ == "__main__":
    main()
