FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt .//requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./  ./

EXPOSE 8000

CMD ["sh", "entrypoint.sh"]
