# Use Python 3.10 Slim for a smaller base image
FROM python:3.10-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files
# PYTHONUNBUFFERED: Ensures logs are flushed directly to terminal
# LIBGL_ALWAYS_SOFTWARE: Forces software rendering (CPU only) to avoid GPU errors
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LIBGL_ALWAYS_SOFTWARE=1

WORKDIR /app

# Install basic system tools needed for the build process
# We clean up apt lists immediately to keep layers small
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Chromium binary AND system dependencies
# --with-deps: Installs the OS libraries (alsa, nss, etc.) required by Chromium on the "slim" image
# chromium: We specificy ONLY chromium to save space (skips Firefox and WebKit)
RUN playwright install chromium --with-deps

# Copy the rest of the application
COPY . .

# Expose port 8000 (standard for Gunicorn)
EXPOSE 8000

# Run Gunicorn with:
# -w 1: 1 worker process (as requested)
# -b 0.0.0.0:8000: Bind to port 8000
# --timeout 120: Increased timeout because Playwright initialization can sometimes be slow
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "--timeout", "120", "app:app"]