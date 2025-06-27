FROM python:3.13-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN adduser --disabled-password --gecos "" myuser && \
    chown -R myuser:myuser /app

# Better solution is to provide env vars when spinning up cloudrun 
# TO-DO
ENV PATH="/home/myuser/.local/bin:$PATH"
ENV GOOGLE_GENAI_USE_VERTEXAI=TRUE
ENV GOOGLE_CLOUD_PROJECT=default-krozario
ENV GOOGLE_CLOUD_LOCATION=us-central1

COPY templates /app/templates/
COPY doc_agent /app/doc_agent/
COPY app.py .
COPY backend_functions.py .
USER myuser

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]

