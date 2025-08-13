#!/bin/bash

# Docker deployment script for Easy CheckIn
echo "Starting Easy CheckIn using Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Create database directory if it doesn't exist
mkdir -p database

# Build and start the containers
echo "Building and starting Docker containers..."
docker-compose up --build -d

# Check if containers are running
if [ $? -eq 0 ]; then
    echo "Dance Attendance Application is now running!"
    echo "You can access it at: http://localhost:5000"
    
    # Provide instructions for creating an admin user
    echo ""
    echo "To create an admin user, run:"
    echo "docker-compose exec web flask create-admin"
    echo ""
    echo "To stop the application, run:"
    echo "docker-compose down"
else
    echo "Failed to start Docker containers. Please check the logs for more information."
    echo "docker-compose logs"
fi
