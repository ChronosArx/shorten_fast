FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./  /app

EXPOSE 8443

CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8443 shorten_fast.wsgi:application"]
