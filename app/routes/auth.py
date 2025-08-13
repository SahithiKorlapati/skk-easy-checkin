from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash
from app.models import User
from app import db
from app.forms import RegistrationForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login')
def login():
    """User login page - now just redirects to home as login is disabled"""
    flash('Login functionality has been disabled. All pages are now accessible without authentication.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/logout')
def logout():
    """User logout - now just redirects to home as login is disabled"""
    flash('Login functionality has been disabled. All pages are now accessible without authentication.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user - simplified version without authentication"""
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.', 'error')
            return render_template('auth/register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'error')
            return render_template('auth/register.html', form=form)
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            is_admin=form.is_admin.data,
            is_instructor=form.is_instructor.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f'User {form.username.data} has been created!', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('auth/register.html', form=form)
