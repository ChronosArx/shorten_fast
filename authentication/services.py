import resend
from shorten_fast.settings import RESEND_API_KEY

resend.api_key = RESEND_API_KEY


def send_confirm_email(email: str, code: str):
    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        "to": [f"{email}"],
        "subject": "Confirm Code.",
        "html": f"<p>Your confirm code is <strong>{code}</strong> !!</p>",
    }
    resend.Emails.send(params)
