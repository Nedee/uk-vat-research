
import requests
from urllib.parse import quote
import os
from dotenv import load_dotenv

load_dotenv()

# ----------------------------------
# 1. HMRC SANDBOX CREDENTIALS
# ----------------------------------


CLIENT_ID = os.getenv("HMRC_CLIENT_ID")
CLIENT_SECRET = os.getenv("HMRC_CLIENT_SECRET")

BASE_URL = "https://test-api.service.hmrc.gov.uk"


# ----------------------------------
# 2. GET ACCESS TOKEN
# ----------------------------------

def get_access_token():

    url = f"{BASE_URL}/oauth/token"

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(
        url,
        data=payload,
        headers=headers,
        timeout=30
    )

    if response.status_code != 200:
        print("Authentication failed!")
        print(response.status_code)
        print(response.text)
        response.raise_for_status()

    token = response.json()["access_token"]

    print("Successfully authenticated with HMRC!")

    return token


# ----------------------------------
# 3. CHECK VAT NUMBER
# ----------------------------------

def check_vat_number(vat_number, token):

    vat_number = vat_number.strip().upper().replace(" ", "")

    url = (
        f"{BASE_URL}/organisations/vat/"
        f"check-vat-number/lookup/{quote(vat_number, safe='')}"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.hmrc.2.0+json"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    print("\nHTTP Status:", response.status_code)

    try:
        result = response.json()
    except ValueError:
        result = {"response": response.text}

    return result


# ----------------------------------
# 4. RUN THE PROGRAM
# ----------------------------------

if __name__ == "__main__":

    try:
        # Authenticate once
        access_token = get_access_token()

        # Ask user for VAT number
        vat_number = input("\nEnter UK VAT number: ")

        # Check VAT number
        result = check_vat_number(vat_number, access_token)

        # Display HMRC response
        print("\nHMRC API RESPONSE:")
        print(result)

    except requests.exceptions.RequestException as error:
        print("\nRequest error:", error)

    except (KeyError, ValueError) as error:
        print("\nUnexpected response:", error)
