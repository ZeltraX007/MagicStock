# Stage 1: Build dependencies
FROM python:3.12.9-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory for install
WORKDIR /install

# Install system dependencies required for pip packages (like pandas)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install only requirements
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

# Stage 2: Final minimal image
FROM python:3.12.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /install /usr/local

# Copy project files
COPY . .

# Expose Flask app port
EXPOSE 5000

# Run the app
CMD ["python", "main.py"]