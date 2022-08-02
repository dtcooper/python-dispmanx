FROM ghcr.io/dtcooper/raspberrypi-os:python3.10

ARG POETRY_VERSION=1.1.14

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="/root/.poetry/bin:${PATH}"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        libraspberrypi0 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock /app/
WORKDIR /app
RUN poetry install --extras numpy

COPY . /app
