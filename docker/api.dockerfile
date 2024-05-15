FROM python:3.11 AS base

RUN pip install poetry
WORKDIR /usr/src/app

FROM base AS req

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config virtualenvs.create true && \
    poetry config && \
    poetry install --no-dev --no-root

FROM req AS code

COPY . .
RUN poetry install

FROM code AS app
