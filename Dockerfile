# Base image with Python optimized for Hugging Face Spaces
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=7860
ENV PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Install essential system dependencies including build-essential
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tesseract-ocr \
    poppler-utils \
    build-essential \
    python3-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


# Copy only necessary application code
COPY app.py /app/
COPY Process/ /app/Process/
COPY ResumeATS/ /app/ResumeATS/
COPY manage.py /app/

# Create a non-root user for security
RUN adduser --disabled-password --gecos "" appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose the port Hugging Face Spaces will use
EXPOSE 7860

# Healthcheck to verify the service is running
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/ || exit 1

# Run app.py as required for Hugging Face Spaces
CMD ["python", "app.py"]
