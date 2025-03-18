#!/bin/bash

echo "Initializing Airflow database..."
airflow db migrate

echo "Creating Airflow admin user..."
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email ngnhan2609@gmail.com \
    --password admin

echo "Starting Airflow Scheduler & Webserver..."
airflow scheduler & airflow webserver