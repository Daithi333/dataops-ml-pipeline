#!/bin/bash

# Airflow installation is brittle, so it is recommended to use a constraint file
# This is not supported by default using pipenv, so this script is for doing so
# https://pypi.org/project/apache-airflow/

set -e

EXTRAS="postgres"

echo "Installing Apache Airflow ${AIRFLOW_VERSION} with Python ${PYTHON_VERSION}..."

export AIRFLOW_VERSION=2.9.0
export PYTHON_VERSION=3.10
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

# Ensure pipenv shell is activated and working
if ! pipenv --venv &>/dev/null; then
  echo "Creating pipenv environment..."
  pipenv --python ${PYTHON_VERSION}
fi

echo "Installing Airflow..."
pipenv run pip install "apache-airflow[${EXTRAS}]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

echo "Airflow installation complete."
