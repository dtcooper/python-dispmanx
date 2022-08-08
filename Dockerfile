FROM dtcooper/raspberrypi-os:python3.9

ARG POETRY_VERSION=1.1.14

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml poetry.lock /app/
WORKDIR /app

# Need to use pip to actual install to properly support piwheel.org
RUN poetry export --without-hashes --dev --extras numpy -o requirements.txt \
    && pip install -r requirements.txt

COPY . /app
