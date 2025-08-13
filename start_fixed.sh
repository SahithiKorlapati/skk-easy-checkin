#!/bin/bash

# Start development server for Easy CheckIn with fixed database permissions
echo "Starting Easy CheckIn with fixed database permissions..."

# Set environment variables
export FLASK_APP=run.py
export FLASK_ENV=development

# Create and set permissions for the database directory
DB_DIR="/root/git/skk-easy-checkin/instance"
mkdir -p "$DB_DIR"
chmod 777 "$DB_DIR"

# Set the database URL to an absolute path
export DATABASE_URL="sqlite:////root/git/skk-easy-checkin/instance/attendance.db"

# Ensure the database file exists and is writable
touch "$DB_DIR/attendance.db"
chmod 666 "$DB_DIR/attendance.db"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Activated virtual environment"
fi

# Install dependencies if needed
if [ "$1" == "--install" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Reset database if requested
if [ "$1" == "--reset-db" ] || [ "$2" == "--reset-db" ]; then
    echo "Resetting database..."
    python3 -c "
import os
from app import create_app, db
app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    print('Database reset complete')
"
fi

# Run the Flask application
echo "Starting Flask development server..."
flask run --host=0.0.0.0 --port=5000

# Deactivate virtual environment when done
deactivate 2>/dev/null || true
