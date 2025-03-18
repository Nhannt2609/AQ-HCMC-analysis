FROM apache/airflow:2.7.3

# Cài đặt các package hệ thống và Python packages
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Cài đặt Python packages
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Chuyển về người dùng airflow
USER airflow