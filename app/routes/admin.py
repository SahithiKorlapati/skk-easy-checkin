from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import User, Student, DanceClass, Attendance
from app import db
from app.forms import StudentForm, ClassForm
from datetime import datetime, date, timedelta

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
def index():
    """Admin dashboard"""
    return redirect(url_for('admin.students'))

@bp.route('/users')
def users():
    """Manage users (admin only)"""
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/students')
def students():
    """Manage students"""
    students = Student.query.order_by(Student.last_name).all()
    return render_template('admin/students.html', students=students)

@bp.route('/student/new', methods=['GET', 'POST'])
def new_student():
    """Add a new student"""
    form = StudentForm()
    if form.validate_on_submit():
        # Check if student with same email already exists (only if email is provided)
        email = form.email.data.strip() if form.email.data else None
        if email and Student.query.filter_by(email=email).first():
            flash('A student with this email already exists.', 'error')
            return render_template('admin/student_form.html', form=form, title='New Student')
        
        student = Student(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=email,  # Use None if email is empty
            phone=form.phone.data
        )
        db.session.add(student)
        db.session.commit()
        flash(f'Student {student.full_name} has been added!', 'success')
        return redirect(url_for('admin.students'))
    
    return render_template('admin/student_form.html', form=form, title='New Student')

@bp.route('/student/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    """Edit a student"""
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    
    if form.validate_on_submit():
        # Process email - use None if empty
        email = form.email.data.strip() if form.email.data else None
        
        # Check if email is being changed and already exists
        if email and email != student.email and Student.query.filter_by(email=email).first():
            flash('A student with this email already exists.', 'error')
            return render_template('admin/student_form.html', form=form, title='Edit Student')
        
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.email = email  # Use None if email is empty
        student.phone = form.phone.data
        
        db.session.commit()
        flash(f'Student {student.full_name} has been updated!', 'success')
        return redirect(url_for('admin.students'))
    
    return render_template('admin/student_form.html', form=form, title='Edit Student')

@bp.route('/classes')
def classes():
    """Manage dance classes"""
    # Show all classes
    classes = DanceClass.query.all()
    today = date.today()
    
    return render_template('admin/classes.html', classes=classes, today=today)

@bp.route('/class/new', methods=['GET', 'POST'])
def new_class():
    """Add a new dance class"""
    form = ClassForm()
    
    if form.validate_on_submit():
        # Create a new class with instructor name instead of ID
        dance_class = DanceClass(
            name=form.name.data,
            instructor_name=form.instructor_name.data,  # Use instructor name directly
            day_of_week=form.day_of_week.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            description=form.description.data
        )
        db.session.add(dance_class)
        db.session.commit()
        flash(f'Class {dance_class.name} has been added!', 'success')
        return redirect(url_for('admin.classes'))
    
    return render_template('admin/class_form.html', form=form, title='New Class')

@bp.route('/class/edit/<int:id>', methods=['GET', 'POST'])
def edit_class(id):
    """Edit a dance class"""
    dance_class = DanceClass.query.get_or_404(id)
    form = ClassForm(obj=dance_class)
    
    if form.validate_on_submit():
        dance_class.name = form.name.data
        dance_class.instructor_name = form.instructor_name.data
        dance_class.day_of_week = form.day_of_week.data
        dance_class.start_time = form.start_time.data
        dance_class.end_time = form.end_time.data
        dance_class.description = form.description.data
        
        db.session.commit()
        flash(f'Class {dance_class.name} has been updated!', 'success')
        return redirect(url_for('admin.classes'))
    
    return render_template('admin/class_form.html', form=form, title='Edit Class')

@bp.route('/attendance/report')
def attendance_report():
    """View attendance reports"""
    # Get parameters
    class_id = request.args.get('class_id', type=int)
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # Default to last 7 days if no dates provided
    today = date.today()
    if not start_date_str:
        start_date = today - timedelta(days=7)
    else:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    
    if not end_date_str:
        end_date = today
    else:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    
    # Show all classes
    classes = DanceClass.query.all()
    
    # If class_id is specified, filter attendance for that class
    attendance_data = []
    if class_id:
        dance_class = DanceClass.query.get_or_404(class_id)
        
        # Get attendance records for the specified class and date range
        attendance_records = Attendance.query.filter(
            Attendance.class_id == class_id,
            Attendance.date >= start_date,
            Attendance.date <= end_date
        ).order_by(Attendance.date.desc()).all()
        
        # Group by date
        attendance_by_date = {}
        for record in attendance_records:
            if record.date not in attendance_by_date:
                attendance_by_date[record.date] = []
            attendance_by_date[record.date].append(record)
        
        attendance_data = [
            {
                'date': date_obj,
                'count': len(records),
                'records': records
            }
            for date_obj, records in sorted(attendance_by_date.items(), key=lambda x: x[0], reverse=True)
        ]
    
    return render_template(
        'admin/attendance_report.html',
        classes=classes,
        selected_class_id=class_id,
        start_date=start_date,
        end_date=end_date,
        attendance_data=attendance_data
    )
