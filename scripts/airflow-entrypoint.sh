#!/bin/bash
set -e

# Initialize Airflow DB if not already initialized
airflow db migrate

# Create default connections
airflow connections create-default-connections

# Start the appropriate Airflow component
exec airflow "$@"
