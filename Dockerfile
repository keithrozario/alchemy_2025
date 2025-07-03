# FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
FROM python:3.12-slim
WORKDIR /app

# Decided to use regular pip instead of uv as more people are familiar with this
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# UV Install
# ENV UV_SYSTEM_PYTHON=1
# COPY uv.lock .
# COPY pyproject.toml .
# RUN uv sync --locked

RUN adduser --disabled-password --gecos "" myuser && \
    chown -R myuser:myuser /app

# Better solution is to provide env vars when spinning up cloudrun 
# TO-DO
ENV PATH="/home/myuser/.local/bin:$PATH"
ENV GOOGLE_GENAI_USE_VERTEXAI=TRUE
ENV GOOGLE_CLOUD_PROJECT=project-alchemy-team12
ENV GOOGLE_CLOUD_LOCATION=us-central1

# It's embarassing I have to hard-code this :(
ENV LOAN_GCS_BUCKET=alchemy-loan-documents-uploads

COPY templates /app/templates/
COPY doc_agent /app/doc_agent/
COPY app.py .
COPY backend_functions.py .

USER myuser

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]

# gcloud builds submit --tag asia-southeast1-docker.pkg.dev/default-krozario/gcloudbuilds/alchemy:latest