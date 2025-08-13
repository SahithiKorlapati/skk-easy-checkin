import os
import sys
import getpass
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User

def create_admin_user():
    """Create an admin user for the application"""
    print("Creating admin user for Easy CheckIn")
    print("--------------------------------------------------")
    
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    
    # Check if user already exists
    app = create_app()
    with app.app_context():
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"Error: User with username '{username}' already exists.")
            sys.exit(1)
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            print(f"Error: User with email '{email}' already exists.")
            sys.exit(1)
        
        # Get password securely
        password = getpass.getpass("Enter admin password: ")
        confirm_password = getpass.getpass("Confirm admin password: ")
        
        if password != confirm_password:
            print("Error: Passwords do not match.")
            sys.exit(1)
        
        if len(password) < 8:
            print("Error: Password must be at least 8 characters long.")
            sys.exit(1)
        
        # Create admin user
        admin = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=True,
            is_instructor=True
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print(f"\nAdmin user '{username}' created successfully!")
        print("You can now log in to the application.")

if __name__ == "__main__":
    create_admin_user()
