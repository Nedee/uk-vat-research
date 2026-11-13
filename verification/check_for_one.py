
from playwright.sync_api import sync_playwright
import re

HMRC_URL = (
    "https://www.tax.service.gov.uk/"
    "check-vat-number/enter-vat-details"
)


def verify_vat(vat):
    with sync_playwright() as p:
        print(vat)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Open HMRC form
        page.goto(HMRC_URL)

        # Find VAT input and enter number
        page.get_by_role("textbox").first.fill(vat)

        # Click Search
        page.get_by_role("button", name="Search").click()

        # Wait for HMRC response
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        # Read visible page text
        result = page.locator("body").inner_text()

        print("\n--- HMRC RESPONSE ---")
        print(result)

        input("\nPress ENTER to close browser...")
        browser.close()


if __name__ == "__main__":
    candidate = input("Enter candidate VAT number: ")
    verify_vat(candidate)
