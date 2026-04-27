# -------- Base image --------
FROM python:3.11-slim AS base

WORKDIR /app

# Install system deps (minimal)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# -------- Dependencies layer --------
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# -------- App layer --------
COPY . .

# -------- Runtime --------
ENV PYTHONUNBUFFERED=1

# No CMD here → Railway will handle it