# Dockerfile for alpha-gpt
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specification first (layer-cache friendly)
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install . --no-cache-dir

# Copy application source
COPY src/ ./src/
COPY langgraph.json ./

# Create non-root user for security
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

# Default command
CMD ["python", "-m", "src.main"]
