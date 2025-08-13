import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from app import db
from app.models import User

@click.command('create-admin')
@with_appcontext
def create_admin_command():
    """Create an admin user via command line."""
    click.echo('Creating Easy CheckIn admin user...')
    
    username = click.prompt('Username', type=str)
    email = click.prompt('Email', type=str)
    password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
    
    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        click.echo(f"Error: User with username '{username}' already exists.")
        return
    
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        click.echo(f"Error: User with email '{email}' already exists.")
        return
    
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
    
    click.echo(f"Admin user '{username}' created successfully!")

def init_app(app):
    """Register CLI commands with the app."""
    app.cli.add_command(create_admin_command)
