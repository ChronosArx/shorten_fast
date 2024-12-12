import resend
import os

resend.api_key = os.environ["RESEND_API_KEY"]


def send_confirm_email(email: str, code: str):
    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        "to": [email],
        "subject": "Code to verification.",
        "html": f"<strong>Your code is {code}!</strong>",
    }

    resend.Emails.send(params)
