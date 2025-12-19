from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """
    Represents a user in the system.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    resumes = db.relationship('Resume', backref='user', lazy=True)

    def __init__(self, username: str, email: str, password: str):
        """
        Initializes a new User object.

        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str): The password of the user.
        """
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password: str):
        """
        Hashes the given password and stores it as the password_hash.

        Args:
            password (str): The password to hash.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Checks if the given password matches the stored password_hash.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Resume(db.Model):
    """
    Represents a resume in the system.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'), nullable=False, default=1)  # Default template
    data = db.Column(db.JSON, nullable=False, default={})
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id: int, template_id: int, data: dict):
        """
        Initializes a new Resume object.

        Args:
            user_id (int): The ID of the user who owns the resume.
            template_id (int): The ID of the template used for the resume.
            data (dict): The resume data.
        """
        self.user_id = user_id
        self.template_id = template_id
        self.data = data

    def update_data(self, data: dict):
        """
        Updates the resume data.

        Args:
            data (dict): The new resume data.
        """
        self.data = data

    def get_data(self) -> dict:
        """
        Returns the resume data.

        Returns:
            dict: The resume data.
        """
        return self.data

    def __repr__(self):
        return f'<Resume {self.id}>'


class Template(db.Model):
    """
    Represents a resume template.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    fields = db.Column(db.JSON, nullable=False, default=[])
    preview_image = db.Column(db.String(200), nullable=True)
    resumes = db.relationship('Resume', backref='template', lazy=True)

    def __init__(self, name: str, description: str, fields: list, preview_image: str = None):
        """
        Initializes a new Template object.

        Args:
            name (str): The name of the template.
            description (str): A description of the template.
            fields (list): A list of fields required for the template.
            preview_image (str, optional): The URL of the template preview image. Defaults to None.
        """
        self.name = name
        self.description = description
        self.fields = fields
        self.preview_image = preview_image

    def get_fields(self) -> list:
        """
        Returns the list of fields required for the template.

        Returns:
            list: The list of fields.
        """
        return self.fields

    def render(self, data: dict) -> str:
        """
        Renders the template with the given data.  This is a placeholder.
        The actual rendering logic will depend on the templating engine.

        Args:
            data (dict): The data to render the template with.

        Returns:
            str: The rendered template.
        """
        # Placeholder for template rendering logic
        return f"Template: {self.name} rendered with data: {data}"

    def __repr__(self):
        return f'<Template {self.name}>'
