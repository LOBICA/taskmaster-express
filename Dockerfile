FROM python:3.11 AS base

RUN pip install poetry
RUN pip install poetry-plugin-export
WORKDIR /usr/src/app

FROM base AS req

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt

FROM req AS code

COPY . .
RUN pip install -e .

FROM code AS dev
RUN poetry export -f requirements.txt --output requirements.txt --only dev
RUN pip install -r requirements.txt

FROM code AS prod
RUN chmod a+x scripts/launch-api.prod.sh
CMD ["scripts/launch-api.prod.sh"]
