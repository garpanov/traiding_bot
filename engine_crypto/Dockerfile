FROM python:3.13-slim

WORKDIR /app/src

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["sh", "-c", "python -m src.main"]