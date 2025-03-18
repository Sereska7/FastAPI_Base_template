FROM python:3.12

# VIRTUAL ENVIRONMENT
RUN mkdir /migrations
COPY pyproject.toml /migrations
COPY poetry.lock /migrations


RUN pip3 install poetry
RUN poetry config virtualenvs.create false
WORKDIR /migrations
RUN poetry install --no-dev

COPY . .


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
