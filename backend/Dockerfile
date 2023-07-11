#
FROM python:3.10-slim as requirements-stage

# 
WORKDIR /tmp

# 
RUN pip install poetry

# 
COPY ./pyproject.toml ./poetry.lock* /tmp/

# 
RUN poetry export --only backend -f requirements.txt --output requirements.txt --without-hashes

# 
FROM python:3.10-slim

# 
WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat-traditional gcc \
    && apt-get clean

# install python dependencies
RUN pip install --upgrade pip

#
COPY --from=requirements-stage /tmp/requirements.txt /backend/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

# 
COPY . /backend