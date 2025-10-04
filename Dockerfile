FROM python:3.12-alpine

RUN apk add --no-cache curl

ENV APP_HOME=/home/app/
WORKDIR $APP_HOME

RUN mkdir ./src

RUN pip install uv
COPY ./pyproject.toml  $APP_HOME
COPY ./alembic.ini  $APP_HOME
RUN uv pip install -e . --system

COPY ./src/ $APP_HOME/src/

CMD ["sh", "-c", "alembic -c alembic.ini upgrade head && uvicorn --factory app.bootstrap.entrypoints.api:create_app --host 0.0.0.0 --port 8000"]
