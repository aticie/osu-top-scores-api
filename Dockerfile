FROM node:14 AS frontend_public

WORKDIR /usr/src/app

RUN npm init vite@latest score-tracker-frontend --template svelte

WORKDIR /usr/src/app/score-tracker-frontend

COPY ./frontend/public ./public
COPY ./frontend/index.html ./index.html
COPY ./frontend/src ./src
COPY ./frontend/package.json ./package.json

RUN npm install

RUN npm run build

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

WORKDIR /src

COPY --from=frontend_public /usr/src/app/score-tracker-frontend/dist ./dist

COPY src /src

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]