#!/bin/bash
set -e

echo "Upgrading Airflow DB..."
airflow db migrate

if ! airflow users list | grep -q admin; then
  echo "Creating admin user..."
  airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --email admin@example.com
fi

echo "Starting Airflow component..."
exec airflow "$@"
