FROM apache/airflow:2.9.0-python3.12

# use root user to make script executable
USER root

COPY ./scripts/airflow-entrypoint.sh /scripts/airflow-entrypoint.sh
RUN chmod +x /scripts/airflow-entrypoint.sh

# Switch back to airflow user
USER airflow

RUN pip install pipenv

WORKDIR /opt/airflow

COPY Pipfile* /opt/airflow/
RUN pipenv install --deploy --system

ENTRYPOINT ["/bin/bash", "/scripts/airflow-entrypoint.sh"]

CMD ["webserver"]
