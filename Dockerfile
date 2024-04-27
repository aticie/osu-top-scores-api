FROM node:19 AS frontend_public

WORKDIR /usr/src/app

RUN npm init vite@latest score-tracker-frontend --template svelte

WORKDIR /usr/src/app

ADD ./frontend ./score-tracker-frontend

WORKDIR /usr/src/app/score-tracker-frontend

RUN npm install

RUN npm run build

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

WORKDIR /src

COPY --from=frontend_public /usr/src/app/score-tracker-frontend/dist ./dist

COPY src /src

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]