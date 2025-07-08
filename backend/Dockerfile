FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app

# UV Install
ENV UV_SYSTEM_PYTHON=1
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --locked

RUN adduser --disabled-password --gecos "" myuser && \
    chown -R myuser:myuser /app

ENV PATH="/home/myuser/.local/bin:$PATH"
ENV GRPC_VERBOSITY=ERROR
ENV GLOG_minloglevel=2
ENV GOOGLE_GENAI_USE_VERTEXAI=TRUE
ENV GOOGLE_CLOUD_LOCATION=us-central1

COPY templates /app/templates/
COPY doc_agent /app/doc_agent/
COPY app.py .
COPY backend_functions.py .

USER myuser

CMD ["sh", "-c", "uv run uvicorn app:app --host 0.0.0.0 --port $PORT"]