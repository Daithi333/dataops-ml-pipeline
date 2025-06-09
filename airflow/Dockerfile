FROM apache/airflow:3.0.1-python3.10

USER root

RUN curl -sSL https://install.python-poetry.org | python3 && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --without dev

COPY ./src /opt/airflow/src

ENV PYTHONPATH="/opt/airflow:/opt/airflow/src"
ENV AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/src/pipeline/dags

USER airflow
