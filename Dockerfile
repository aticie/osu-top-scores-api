FROM python:3.9.5-slim

COPY src /src

WORKDIR /src

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]