FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./  /app

EXPOSE 8443

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8443"]
