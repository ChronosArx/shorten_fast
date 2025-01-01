import resend
from shorten_fast.settings import RESEND_API_KEY

resend.api_key = RESEND_API_KEY


def send_confirm_email(email: str, code: str):
    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        "to": ["chronos.software.dev@gmail.com"],
        "subject": "hello world",
        "html": f"<strong>Your code is {code}!</strong>",
    }
    resend.Emails.send(params)
