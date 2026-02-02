FROM python:3.13-slim

WORKDIR /project/src

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/project
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["sh", "-c", "python -m src.config && uvicorn main:app --host 0.0.0.0 --port 8080"]