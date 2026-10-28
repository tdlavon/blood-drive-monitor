import os
import resend
import requests
from bs4 import BeautifulSoup

URL = "https://www.redcrossblood.org/give.html/drive-results?order=DATE&range=10&zipSponsor=magiccastle"

TARGET_DATE = "Dec 15"

resend.api_key = os.environ["RESEND_API_KEY"]

ALERT_TO = os.environ["ALERT_TO"]

FROM_EMAIL = os.environ["FROM_EMAIL"]


def send_email(message):
    resend.Emails.send({
        "from": FROM_EMAIL,
        "to": ALERT_TO,
        "subject": "Blood Drive Slot Available",
        "text": message
    })


def check_page():
    response = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text(" ", strip=True)

    has_date = (
        "Dec 15" in page_text or
        "December 15" in page_text
    )

    availability_words = [
        "schedule",
        "appointment",
        "available",
        "book"
    ]

    available = any(
        word in page_text.lower()
        for word in availability_words
    )

    if has_date and available:
        send_email(
            f"""A possible appointment opening was detected.

URL:
{URL}
"""
        )
        print("Alert sent.")
    else:
        print("No availability found.")

send_email("Test message from GitHub Actions")
#if __name__ == "__main__":
#    check_page()