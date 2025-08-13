from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Configure the app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    
    # Set database path - ensure directory exists with proper permissions
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    db_dir = os.path.join(base_dir, 'instance')
    os.makedirs(db_dir, exist_ok=True)
    
    # Use a file path that SQLite can definitely access
    db_file = os.path.join(db_dir, 'attendance.db')
    db_uri = os.environ.get('DATABASE_URL', f'sqlite:///{db_file}')
    
    print(f"Using database at: {db_file}")
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    
    # Register blueprints
    from app.routes import main, admin, auth
    from app.api.routes import api_bp
    
    app.register_blueprint(main.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Register CLI commands
    from app import cli
    cli.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
