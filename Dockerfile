FROM node:14 AS frontend_public

WORKDIR /usr/src/app

RUN npm init vite@latest score-tracker-frontend --template svelte

COPY ./frontend/public ./score-tracker-frontend/public
COPY ./frontend/src ./score-tracker-frontend/src

WORKDIR /usr/src/app/score-tracker-frontend

RUN npm install
RUN npm install axios
RUN npm run build

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

COPY --from=frontend_public /usr/src/app/score-tracker-frontend/dist ./dist

COPY src /src

WORKDIR /src

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]