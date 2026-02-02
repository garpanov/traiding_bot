FROM python:3.13-slim

WORKDIR /app/telegram_bot
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "-m", "telegram_bot.main"]