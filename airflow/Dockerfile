FROM apache/airflow:3.1.3

USER root

# Install required OS dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install uv (system-wide)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv

# Keep Airflow's default working directory
WORKDIR /opt/airflow

# Copy pyproject and lockfile
COPY pyproject.toml uv.lock ./

# Install deps inside Airflow’s existing venv
RUN uv sync --frozen --no-editable --python /usr/local/bin/python

# Ensure uv-installed venv remains under /opt/airflow/.venv
ENV PATH="/opt/airflow/.venv/bin:${PATH}"

# Keep required Airflow folders
RUN mkdir -p /opt/airflow/dags /opt/airflow/logs /opt/airflow/plugins

USER airflow