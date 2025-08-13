#!/bin/bash

# Start development server for Easy CheckIn
echo "Starting Easy CheckIn in development mode..."

# Set environment variables
export FLASK_APP=run.py
export FLASK_ENV=development

# Use a consistent database path
export DATABASE_URL="sqlite:///$(pwd)/instance/attendance.db"

# Create instance directory with proper permissions
mkdir -p instance
chmod 777 instance

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi
# Check if reset flag is provided
if [ "$1" == "--reset-db" ]; then
    echo "Resetting database..."
    # Create a temporary script to reset the database
    cat > reset_db_temp.py << 'EOF'
#!/usr/bin/env python
"""
Script to reset the database and recreate tables with the updated schema.
"""
import os
import sys
from app import create_app, db

def reset_database():
    """Reset the database and recreate tables"""
    app = create_app()
    
    with app.app_context():
        # Get the database path from environment or config
        db_uri = os.environ.get('DATABASE_URL') or app.config.get('SQLALCHEMY_DATABASE_URI')
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
        else:
            db_path = db_uri.replace('sqlite://', '')
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Check if the database file exists
        if os.path.exists(db_path):
            print(f"Removing existing database at {db_path}")
            # Close all connections to the database
            db.session.close_all()
            # Remove the file
            os.remove(db_path)
            print("Database file removed.")
        
        # Create all tables
        print("Creating new database tables...")
        db.create_all()
        print("Database tables created successfully!")

if __name__ == "__main__":
    reset_database()
    print("Database reset complete. You'll need to recreate any necessary data.")
EOF
    # Execute the script
    python reset_db_temp.py
    # Remove the temporary script
    rm reset_db_temp.py
fi

# Run the Flask application
echo "Starting Flask development server..."
flask run --host=0.0.0.0

# Deactivate virtual environment when done
deactivate
