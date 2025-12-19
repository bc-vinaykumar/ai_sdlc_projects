"""
This module initializes and configures the Flask application,
including database setup, route registration, and other configurations.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration settings
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Specify the login view

@login_manager.user_loader
def load_user(user_id: int):
    """
    User loader callback for Flask-Login.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        User: The User object if found, otherwise None.
    """
    from models import User  # Import here to avoid circular imports
    return User.query.get(int(user_id))

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    # Import routes to register them with the app
    import routes
    routes.init_routes(app)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

        # Create a default template if it doesn't exist
        from models import Template
        if not Template.query.first():
            default_template = Template(
                name='Default Template',
                description='A simple, clean template.',
                fields=['name', 'email', 'phone', 'work_experience', 'education', 'skills', 'other_information'],
                preview_image='url_to_default_template_preview_image'  # Replace with an actual URL
            )
            db.session.add(default_template)
            db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
