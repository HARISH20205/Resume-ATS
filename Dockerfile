# Base image with Python
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
    git \
    tesseract-ocr \
    poppler-utils \
    build-essential \
    python3-dev \
    # Clean up in the same layer to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . /app/


# Make sure manage.py is executable
RUN chmod +x /app/manage.py

# Expose the port Hugging Face will use
EXPOSE 7860

# Create a non-root user for security
RUN adduser --disabled-password --gecos "" appuser
RUN chown -R appuser:appuser /app
USER appuser

# Start the application - Hugging Face expects the app to listen on port 7860
CMD ["python", "app.py"]
