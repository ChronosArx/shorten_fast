import resend
from shorten_fast.settings import RESEND_API_KEY

resend.api_key = RESEND_API_KEY


def send_confirm_email(email: str, code: str):
    params = {
        "from": "LinkZips <noreply@linkzips.com>",
        "to": [email],
        "subject": "Confirm Code.",
        "html": f"<p>Your confirm code is <strong>{code}</strong> !!</p>",  # Cuerpo HTML
    }
    try:
        resend.Emails.send(params)
    except Exception as e:
        print("Error al enviar el correo:", str(e))
