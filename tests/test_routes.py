import unittest
import os
from flask import Flask, session
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_testing import TestCase
from io import BytesIO

# Assuming your project structure is like this:
# resume_builder/
#     __init__.py
#     routes.py
#     models.py
#     forms.py
# tests/
#     test_routes.py
# You might need to adjust the import paths accordingly
from resume_builder.routes import app, db, login_manager
from resume_builder.models import User, Resume, Template
from resume_builder.forms import ResumeForm
from resume_builder.utils.pdf_generator import PDFGenerator


##
## SETUP AND TEARDOWN
##
class TestRoutes(TestCase):
    """
    Test suite for the Flask routes in the resume builder application.
    """

    def create_app(self):
        """
        Creates a Flask app instance for testing.
        """
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        app.config['LOGIN_DISABLED'] = False
        return app

    def setUp(self):
        """
        Sets up the test environment before each test.
        """
        db.create_all()
        self.client = self.app.test_client()

        # Create a default template
        default_template = Template(
            name='Default Template',
            description='A simple, clean template.',
            fields=['name', 'email', 'phone', 'work_experience', 'education', 'skills', 'other_information'],
            preview_image='url_to_default_template_preview_image'
        )
        db.session.add(default_template)
        db.session.commit()

        # Create a test user
        self.username = 'testuser'
        self.email = 'test@example.com'
        self.password = 'password'
        self.hashed_password = generate_password_hash(self.password)
        self.user = User(username=self.username, email=self.email, password=self.password)
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """
        Tears down the test environment after each test.
        """
        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        """
        Helper function to log in a user.
        """
        return self.client.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def logout(self):
        """
        Helper function to log out a user.
        """
        return self.client.get('/logout', follow_redirects=True)

##
## INDEX ROUTE TESTS
##
    def test_index_route(self):
        """
        Test case for the index route.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Resume Builder', response.data)

##
## REGISTER ROUTE TESTS
##
    def test_register_route_get(self):
        """
        Test case for the register route (GET request).
        """
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_register_route_post_success(self):
        """
        Test case for successful user registration (POST request).
        """
        response = self.client.post(
            '/register',
            data=dict(username='newuser', email='new@example.com', password='password'),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful! Please log in.', response.data)
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)

    def test_register_route_post_username_exists(self):
        """
        Test case for user registration with an existing username (POST request).
        """
        response = self.client.post(
            '/register',
            data=dict(username=self.username, email='new@example.com', password='password'),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username already exists', response.data)

    def test_register_route_post_email_exists(self):
        """
        Test case for user registration with an existing email (POST request).
        """
        response = self.client.post(
            '/register',
            data=dict(username='newuser', email=self.email, password='password'),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email already exists', response.data)

##
## LOGIN ROUTE TESTS
##
    def test_login_route_get(self):
        """
        Test case for the login route (GET request).
        """
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_login_route_post_success(self):
        """
        Test case for successful user login (POST request).
        """
        response = self.login(self.username, self.password)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', response.data)

    def test_login_route_post_invalid_credentials(self):
        """
        Test case for user login with invalid credentials (POST request).
        """
        response = self.client.post(
            '/login',
            data=dict(username=self.username, password='wrongpassword'),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

##
## LOGOUT ROUTE TESTS
##
    def test_logout_route(self):
        """
        Test case for the logout route.
        """
        self.login(self.username, self.password)
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged out successfully!', response.data)

##
## RESUME FORM ROUTE TESTS
##
    def test_resume_form_route_get_logged_in(self):
        """
        Test case for the resume form route (GET request) when logged in.
        """
        self.login(self.username, self.password)
        response = self.client.get('/resume_form', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Resume Form', response.data)

    def test_resume_form_route_get_not_logged_in(self):
        """
        Test case for the resume form route (GET request) when not logged in.
        """
        response = self.client.get('/resume_form', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Redirected to login

    def test_resume_form_route_post_success(self):
        """
        Test case for successful resume form submission (POST request).
        """
        self.login(self.username, self.password)
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.user.id

            form = ResumeForm(meta={'csrf': False})
            form.work_experience.append_entry()
            form.education.append_entry()
            form.skills.append_entry()

            form.work_experience[0].title.data = 'Software Engineer'
            form.work_experience[0].company.data = 'Example Corp'
            form.work_experience[0].location.data = 'New York'
            form.work_experience[0].start_date.data = '2020-01-01'
            form.work_experience[0].end_date.data = '2022-01-01'
            form.work_experience[0].description.data = 'Developed awesome software'

            form.education[0].institution.data = 'Example University'
            form.education[0].degree.data = 'BS'
            form.education[0].major.data = 'Computer Science'
            form.education[0].graduation_date.data = '2020-01-01'
            form.education[0].description.data = 'Learned a lot'

            form.skills[0].skill.data = 'Python'
            form.skills[0].level.data = 'Expert'

            form.other_information.data = 'Some other info'

            response = c.post(
                '/resume_form',
                data=form.data,
                follow_redirects=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Resume saved successfully!', response.data)
            resume = Resume.query.filter_by(user_id=self.user.id).first()
            self.assertIsNotNone(resume)
            self.assertEqual(resume.data['work_experience'][0]['title'], 'Software Engineer')

##
## RESUME TEMPLATES ROUTE TESTS
##
    def test_resume_templates_route_logged_in(self):
        """
        Test case for the resume templates route when logged in.
        """
        self.login(self.username, self.password)
        response = self.client.get('/resume_templates')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Default Template', response.data)

    def test_resume_templates_route_not_logged_in(self):
        """
        Test case for the resume templates route when not logged in.
        """
        response = self.client.get('/resume_templates', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Redirected to login

##
## RESUME PREVIEW ROUTE TESTS
##
    def test_resume_preview_route_logged_in_resume_exists(self):
        """
        Test case for the resume preview route when logged in and a resume exists.
        """
        self.login(self.username, self.password)

        # Create a resume for the user
        resume_data = {'name': 'Test User', 'email': 'test@example.com'}
        resume = Resume(user_id=self.user.id, template_id=1, data=resume_data)
        db.session.add(resume)
        db.session.commit()

        response = self.client.get('/resume_preview/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

    def test_resume_preview_route_logged_in_resume_does_not_exist(self):
        """
        Test case for the resume preview route when logged in but no resume exists.
        """
        self.login(self.username, self.password)
        response = self.client.get('/resume_preview/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please create a resume first.', response.data)
        self.assertIn(b'Resume Form', response.data)

    def test_resume_preview_route_not_logged_in(self):
        """
        Test case for the resume preview route when not logged in.
        """
        response = self.client.get('/resume_preview/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Redirected to login

##
## GENERATE PDF ROUTE TESTS
##
    def test_generate_pdf_route_logged_in_resume_exists(self):
        """
        Test case for the generate PDF route when logged in and a resume exists.
        """
        self.login(self.username, self.password)

        # Create a resume for the user
        resume_data = {'name': 'Test User', 'email': 'test@example.com'}
        resume = Resume(user_id=self.user.id, template_id=1, data=resume_data)
        db.session.add(resume)
        db.session.commit()

        response = self.client.get('/generate_pdf/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/pdf')
        self.assertEqual(response.headers['Content-Disposition'], 'attachment; filename=resume.pdf')

    def test_generate_pdf_route_logged_in_resume_does_not_exist(self):
        """
        Test case for the generate PDF route when logged in but no resume exists.
        """
        self.login(self.username, self.password)
        response = self.client.get('/generate_pdf/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please create a resume first.', response.data)
        self.assertIn(b'Resume Form', response.data)

    def test_generate_pdf_route_not_logged_in(self):
        """
        Test case for the generate PDF route when not logged in.
        """
        response = self.client.get('/generate_pdf/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Redirected to login

if __name__ == '__main__':
    unittest.main()
