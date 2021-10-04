FROM node:14 AS frontend_public

WORKDIR /usr/src/app

RUN npm init vite@latest score-tracker-frontend --template svelte

WORKDIR /usr/src/app/score-tracker-frontend

RUN npm install
RUN npm install axios

COPY ./frontend/public ./score-tracker-frontend/public
COPY ./frontend/index.html ./score-tracker-frontend/index.html
COPY ./frontend/src ./score-tracker-frontend/src

RUN npm run build

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

WORKDIR /src

COPY --from=frontend_public /usr/src/app/score-tracker-frontend/dist ./dist

COPY src /src

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]