FROM python:3.9-slim

WORKDIR /src

COPY update_scores.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "update_scores.py"]