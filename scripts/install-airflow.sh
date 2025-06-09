#!/bin/bash

# Airflow installation is brittle, so it is recommended to use a constraint file
# This is not supported by default using pipenv, so this script is for doing so
# https://pypi.org/project/apache-airflow/

EXTRAS="postgres"

export AIRFLOW_VERSION=3.0.1
export PYTHON_VERSION=3.10
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

echo "Installing Apache Airflow ${AIRFLOW_VERSION} with Python ${PYTHON_VERSION}..."

pip install "apache-airflow[${EXTRAS}]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
if [ $? -ne 0 ]; then
  echo "airflow install with constraints file, attempting standard install"
  pip install "apache-airflow[${EXTRAS}]==${AIRFLOW_VERSION}"
fi

if f [ $? -eq 0 ]; then
  echo "Airflow installation complete"
fi
