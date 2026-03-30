# Use Python 3.10 Slim for a much smaller base image
FROM python:3.10-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files
# PYTHONUNBUFFERED: Ensures logs are flushed directly to terminal
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 8000 for Gunicorn mapping
EXPOSE 8000

# Run Gunicorn with:
# -w 1: 1 worker process
# -b 0.0.0.0:8000: Bind to port 8000
# --timeout 60: Standard timeout
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "--timeout", "60", "app:app"]