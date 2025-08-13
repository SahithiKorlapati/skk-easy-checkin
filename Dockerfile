FROM python:3.9-slim

# Run everything as root
USER root

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create app directory
RUN mkdir -p /code
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create the instance directory and database file with full permissions
RUN mkdir -p /code/instance && \
    touch /code/instance/attendance.db && \
    chmod 777 /code/instance && \
    chmod 777 /code/instance/attendance.db

# Expose the port the app runs on
EXPOSE 5000

# Run the application as root
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "run:app"]
