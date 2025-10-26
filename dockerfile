FROM python:3.13.7

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir \
    dbt-core \
    dbt-postgres \
    prefect-dbt \
    prefect-shell

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["python", "orchestration/data_pipeline.py"]