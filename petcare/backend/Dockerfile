FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Em development usa --reload (hot reload via volume mount).
# Em production remova --reload definindo ENVIRONMENT=production no compose.
CMD ["sh", "-c", "if [ \"$ENVIRONMENT\" = 'production' ]; then uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2; else uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload; fi"]
