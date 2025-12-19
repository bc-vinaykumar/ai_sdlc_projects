"""
Test suite for the Flask application.
"""
import os
import unittest
from unittest.mock import patch
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# Add the project root to the Python path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the app and models
from resume_builder import app as app_module
from resume_builder import models
from resume_builder.app import create_app, load_user

## Test Configuration
class TestConfig:
    """
    Configuration class for testing.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use an in-memory database for testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test_secret_key'

## Test App Initialization
class TestAppInitialization(unittest.TestCase):
    """
    Test suite for the Flask application initialization.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        self.app = Flask(__name__)
        self.app.config.from_object(TestConfig)
        self.db = SQLAlchemy(self.app)
        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)
        self.login_manager.login_view = 'login'

        @self.login_manager.user_loader
        def load_user(user_id: int):
            """
            User loader callback for Flask-Login.
            """
            return models.User.query.get(int(user_id))

        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db.create_all()

        # Create a test client
        self.client = self.app.test_client()

    def tearDown(self):
        """
        Tear down the test environment.
        """
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()

    def test_app_instance(self):
        """
        Test that the Flask app is created successfully.
        """
        self.assertIsInstance(self.app, Flask)

    def test_secret_key_configuration(self):
        """
        Test that the secret key is configured correctly.
        """
        self.assertEqual(self.app.config['SECRET_KEY'], 'test_secret_key')

    def test_database_uri_configuration(self):
        """
        Test that the database URI is configured correctly.
        """
        self.assertEqual(self.app.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///:memory:')

    def test_sqlalchemy_track_modifications_configuration(self):
        """
        Test that SQLALCHEMY_TRACK_MODIFICATIONS is configured correctly.
        """
        self.assertFalse(self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])

    def test_db_instance(self):
        """
        Test that the SQLAlchemy instance is created successfully.
        """
        self.assertIsInstance(self.db, SQLAlchemy)

    def test_login_manager_instance(self):
        """
        Test that the LoginManager instance is created successfully.
        """
        self.assertIsInstance(self.login_manager, LoginManager)
        self.assertEqual(self.login_manager.login_view, 'login')

    def test_load_user_callback(self):
        """
        Test the load_user callback function.
        """
        # Create a test user
        test_user = models.User(username='testuser', email='test@example.com', password='password')
        self.db.session.add(test_user)
        self.db.session.commit()

        # Load the user using the callback
        loaded_user = load_user(test_user.id)

        # Assert that the loaded user is correct
        self.assertEqual(loaded_user.id, test_user.id)
        self.assertEqual(loaded_user.username, test_user.username)

    def test_create_app_function(self):
        """
        Test the create_app function.
        """
        app = create_app()
        self.assertIsInstance(app, Flask)
        self.assertEqual(app.config['SECRET_KEY'], 'your_default_secret_key') # Check default value if env var is not set

    @patch.dict(os.environ, {"SECRET_KEY": "test_secret"})
    def test_create_app_function_with_env_vars(self):
        """
        Test the create_app function with environment variables set.
        """
        app = create_app()
        self.assertIsInstance(app, Flask)
        self.assertEqual(app.config['SECRET_KEY'], 'test_secret')

    def test_default_template_creation(self):
        """
        Test that the default template is created if it doesn't exist.
        """
        app = create_app()
        with app.app_context():
            template = models.Template.query.first()
            self.assertIsNotNone(template)
            self.assertEqual(template.name, 'Default Template')
            self.assertEqual(template.description, 'A simple, clean template.')
            self.assertEqual(template.fields, ['name', 'email', 'phone', 'work_experience', 'education', 'skills', 'other_information'])
            self.assertEqual(template.preview_image, 'url_to_default_template_preview_image')

## Test Routes Initialization
class TestRoutesInitialization(unittest.TestCase):
    """
    Test suite for the routes initialization.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        self.app = create_app()
        self.app.config.from_object(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = SQLAlchemy(self.app)
        self.db.create_all()

    def tearDown(self):
        """
        Tear down the test environment.
        """
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()

    def test_index_route(self):
        """
        Test the index route.
        """
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)  # Assuming index route exists and returns 200

    def test_login_route(self):
        """
        Test the login route.
        """
        with self.client:
            response = self.client.get('/login')
            self.assertEqual(response.status_code, 200)  # Assuming login route exists and returns 200

    def test_register_route(self):
        """
        Test the register route.
        """
        with self.client:
            response = self.client.get('/register')
            self.assertEqual(response.status_code, 200)  # Assuming register route exists and returns 200

## Test Environment Variable Loading
class TestEnvVarLoading(unittest.TestCase):
    """
    Test suite for environment variable loading.
    """

    def test_dotenv_loading(self):
        """
        Test that the .env file is loaded successfully.
        """
        load_dotenv()
        # Check if an environment variable is loaded (assuming you have one in .env)
        self.assertTrue(os.environ.get('FLASK_ENV') is not None or os.environ.get('DATABASE_URL') is not None or os.environ.get('SECRET_KEY') is not None)

if __name__ == '__main__':
    unittest.main()
