from app import create_app, db
from app.models import Student

def add_student(first_name, last_name, email=None, phone=None):
    """Add a new student to the database"""
    app = create_app()
    
    with app.app_context():
        # Check if student already exists
        existing = Student.query.filter_by(
            first_name=first_name,
            last_name=last_name
        ).first()
        
        if existing:
            print(f"Student {first_name} {last_name} already exists!")
            return
        
        # Create new student
        student = Student(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
        )
        
        db.session.add(student)
        db.session.commit()
        print(f"Student {first_name} {last_name} added successfully with ID: {student.id}")

if __name__ == "__main__":
    # Add student named Murali
    add_student("Murali", "Mullapati", email="murali@example.com")
