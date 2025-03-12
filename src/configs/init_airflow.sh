#!/bin/bash

echo "Initializing Airflow database..."
airflow db init

echo "Creating Airflow admin user..."
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

echo "Starting Airflow Scheduler & Webserver..."
airflow scheduler & airflow webserver