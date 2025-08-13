from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
from app.models import Student, DanceClass, Attendance, User
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Home page - kiosk mode for students to mark attendance"""
    today = date.today()
    # Get classes for today
    today_classes = DanceClass.query.filter_by(day_of_week=today.strftime('%A')).all()
    return render_template('index.html', classes=today_classes, today=today)

@bp.route('/kiosk/<int:class_id>')
def kiosk(class_id):
    """Kiosk mode for a specific class"""
    dance_class = DanceClass.query.get_or_404(class_id)
    students = Student.query.order_by(Student.last_name).all()
    today = date.today()
    
    # Get students who have already checked in
    checked_in = Attendance.query.filter_by(
        class_id=class_id,
        date=today
    ).with_entities(Attendance.student_id).all()
    
    checked_in_ids = [record[0] for record in checked_in]
    
    return render_template('kiosk.html', 
                          dance_class=dance_class, 
                          students=students, 
                          checked_in_ids=checked_in_ids,
                          today=today)

@bp.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    """Mark attendance for a student"""
    student_id = request.form.get('student_id')
    class_id = request.form.get('class_id')
    
    if not student_id or not class_id:
        flash('Missing required information', 'error')
        return redirect(request.referrer)
    
    # Check if student is already marked for today
    today = date.today()
    existing = Attendance.query.filter_by(
        student_id=student_id,
        class_id=class_id,
        date=today
    ).first()
    
    student = Student.query.get(student_id)
    dance_class = DanceClass.query.get(class_id)
    
    if not student or not dance_class:
        flash('Invalid student or class', 'error')
        return redirect(request.referrer)
    
    if existing:
        # Already checked in, just show confirmation
        return render_template('attendance_confirmation.html', 
                              student=student, 
                              dance_class=dance_class, 
                              already_checked_in=True,
                              time=existing.time_in)
    else:
        # Create new attendance record
        attendance = Attendance(
            student_id=student_id,
            class_id=class_id,
            date=today,
            time_in=datetime.now()
        )
        db.session.add(attendance)
        db.session.commit()
        
        # Show confirmation page
        return render_template('attendance_confirmation.html', 
                              student=student, 
                              dance_class=dance_class, 
                              already_checked_in=False,
                              time=attendance.time_in)

@bp.route('/search_students')
def search_students():
    """API endpoint to search for students by name"""
    query = request.args.get('query', '')
    class_id = request.args.get('class_id')
    
    # If query is empty, return all students (limited to 100)
    if not query:
        students = Student.query.order_by(Student.last_name).limit(100).all()
    else:
        # Search for students by name
        students = Student.query.filter(
            (Student.first_name.ilike(f'%{query}%') | 
             Student.last_name.ilike(f'%{query}%'))
        ).order_by(Student.last_name).limit(20).all()
    
    today = date.today()
    
    # Get students who have already checked in for this class
    checked_in = []
    if class_id:
        checked_in = Attendance.query.filter_by(
            class_id=class_id,
            date=today
        ).with_entities(Attendance.student_id).all()
        checked_in = [record[0] for record in checked_in]
    
    # Format student data for JSON response
    student_list = [{
        'id': student.id,
        'name': student.full_name,
        'checked_in': student.id in checked_in
    } for student in students]
    
    return jsonify({'students': student_list})

@bp.route('/uncheck_attendance', methods=['POST'])
def uncheck_attendance():
    """Un-check attendance for a student"""
    student_id = request.form.get('student_id')
    class_id = request.form.get('class_id')
    
    if not student_id or not class_id:
        flash('Missing required information', 'error')
        return redirect(request.referrer)
    
    # Find the attendance record for today
    today = date.today()
    attendance = Attendance.query.filter_by(
        student_id=student_id,
        class_id=class_id,
        date=today
    ).first()
    
    student = Student.query.get(student_id)
    dance_class = DanceClass.query.get(class_id)
    
    if not student or not dance_class:
        flash('Invalid student or class', 'error')
        return redirect(request.referrer)
    
    if attendance:
        # Delete the attendance record
        db.session.delete(attendance)
        db.session.commit()
        flash(f'{student.full_name} has been un-checked in from {dance_class.name}', 'success')
    else:
        flash(f'{student.full_name} was not checked in today', 'warning')
    
    # Redirect back to the kiosk page
    return redirect(url_for('main.kiosk', class_id=class_id))

@bp.route('/mark_attendance_batch', methods=['POST'])
def mark_attendance_batch():
    """Mark attendance for multiple students at once"""
    data = request.get_json()
    student_ids = data.get('student_ids', [])
    class_id = data.get('class_id')
    
    if not student_ids or not class_id:
        return jsonify({'success': False, 'message': 'Missing required information'})
    
    # Check if class exists
    dance_class = DanceClass.query.get(class_id)
    if not dance_class:
        return jsonify({'success': False, 'message': 'Invalid class'})
    
    today = date.today()
    now = datetime.now()
    checked_in_students = []
    
    for student_id in student_ids:
        # Check if student exists
        student = Student.query.get(student_id)
        if not student:
            continue
        
        # Check if student is already marked for today
        existing = Attendance.query.filter_by(
            student_id=student_id,
            class_id=class_id,
            date=today
        ).first()
        
        if not existing:
            # Create new attendance record
            attendance = Attendance(
                student_id=student_id,
                class_id=class_id,
                date=today,
                time_in=now
            )
            db.session.add(attendance)
            
            # Add to checked in students list
            checked_in_students.append({
                'id': student.id,
                'name': student.full_name,
                'checked_in': True
            })
    
    # Commit all changes at once
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': f'Successfully checked in {len(checked_in_students)} students',
        'students': checked_in_students
    })

@bp.route('/dashboard')
def dashboard():
    """Dashboard for instructors and admins"""
    # Show all classes (no login required)
    classes = DanceClass.query.all()
    today = date.today()
    
    return render_template('dashboard.html', classes=classes, today=today)
