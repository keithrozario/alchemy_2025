FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app/backend/

# UV Install
ENV UV_SYSTEM_PYTHON=1
COPY backend/pyproject.toml .
COPY backend/uv.lock .
RUN uv sync --locked

RUN mkdir -p /app/frontend/build/web/
RUN adduser --disabled-password --gecos "" myuser && \
    chown -R myuser:myuser /app

ENV PATH="/home/myuser/.local/bin:$PATH"
ENV GRPC_VERBOSITY=ERROR
ENV GLOG_minloglevel=2
ENV GOOGLE_GENAI_USE_VERTEXAI=TRUE
ENV GOOGLE_CLOUD_LOCATION=us-central1

COPY backend/templates /app/backend/templates/
COPY backend/doc_agent /app/backend/doc_agent/
COPY backend/app.py /app/backend/
COPY backend/backend_functions.py /app/backend/

# Makes the directory in cloudrun mimic our repository and dev environment
COPY frontend/build/web /app/frontend/build/web/
RUN ls -lah /app
RUN chown -R myuser:myuser /app/frontend/build/
RUN ls -lah /app/frontend/build/web

USER myuser

CMD ["sh", "-c", "uv run uvicorn app:app --host 0.0.0.0 --port $PORT"]
