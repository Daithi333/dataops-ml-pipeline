FROM apache/airflow:2.9.0-python3.12

USER root

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY ./scripts/airflow-entrypoint.sh /scripts/airflow-entrypoint.sh
RUN chmod +x /scripts/airflow-entrypoint.sh

WORKDIR /opt/airflow

COPY pyproject.toml poetry.lock /opt/airflow/

RUN poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

# Switch back to airflow user for runtime
USER airflow

ENTRYPOINT ["/bin/bash", "/scripts/airflow-entrypoint.sh"]
CMD ["webserver"]
