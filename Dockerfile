FROM --platform=linux/x86_64 public.ecr.aws/docker/library/python:3.12.4-slim as python-base
WORKDIR /usr/src

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    \
    VIRTUAL_ENV="/usr/src/venv" \
    \
    NODE_MAJOR=18

ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH"
RUN python -m venv $VIRTUAL_ENV
ENV PYTHONPATH="/usr/src:$PYTHONPATH"

################################
# BUILDER-BASE
# Used to build deps + create our virtual environment
################################
FROM python-base as builder-base
RUN apt-get update && \
    apt-get install -y \
    apt-transport-https \
    gnupg \
    ca-certificates \
    build-essential \
    git \
    nano \
    libmagic1 \
    curl

RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python -
ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH"

WORKDIR /usr/src
COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev


FROM python-base as development
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates libmagic1 && \
    apt-get clean

ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH"

WORKDIR /usr/src

COPY ./ ./

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $VIRTUAL_ENV $VIRTUAL_ENV

WORKDIR /usr/src

CMD ["python", "main.py"]