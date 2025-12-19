import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash

# Initialize Flask app for testing
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for testing
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import models after initializing db
from resume_builder.models import User, Resume, Template

class TestModels(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        app.app_context().push()
        db.create_all()
        self.app = app
        self.db = db

    def tearDown(self):
        """Tear down for test methods."""
        db.session.remove()
        db.drop_all()
        app.app_context().pop()

    ## User Model Tests
    def test_user_creation(self):
        """Test user object creation and attribute assignment."""
        user: User = User(username='testuser', email='test@example.com', password='password')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.password_hash is not None)

    def test_set_password(self):
        """Test password hashing."""
        user: User = User(username='testuser', email='test@example.com', password='password')
        password_hash_original: str = user.password_hash
        user.set_password('new_password')
        self.assertNotEqual(user.password_hash, password_hash_original)

    def test_check_password(self):
        """Test password checking."""
        user: User = User(username='testuser', email='test@example.com', password='password')
        self.assertTrue(user.check_password('password'))
        self.assertFalse(user.check_password('wrong_password'))

    def test_user_repr(self):
        """Test the user representation."""
        user: User = User(username='testuser', email='test@example.com', password='password')
        self.assertEqual(repr(user), '<User testuser>')

    def test_user_persistance(self):
        """Test user persistance in the database."""
        user: User = User(username='testuser', email='test@example.com', password='password')
        self.db.session.add(user)
        self.db.session.commit()

        retrieved_user: User = User.query.filter_by(username='testuser').first()
        self.assertEqual(retrieved_user.username, 'testuser')
        self.assertEqual(retrieved_user.email, 'test@example.com')
        self.assertTrue(retrieved_user.check_password('password'))

    ## Resume Model Tests
    def test_resume_creation(self):
        """Test resume object creation and attribute assignment."""
        user: User = User(username='testuser', email='test@example.com', password='password')
        self.db.session.add(user)
        self.db.session.commit()
        user_id: int = user.id
        resume: Resume = Resume(user_id=user_id, template_id=2, data={'name': 'John Doe'})
        self.assertEqual(resume.user_id, user_id)
        self.assertEqual(resume.template_id, 2)
        self.assertEqual(resume.data, {'name': 'John Doe'})
        self.assertTrue(isinstance(resume.created_at, datetime))

    def test_resume_default_template(self):
        """Test resume creation with default template ID."""
        user: User = User(username='testuser', email='test@example.com', password='password')
        self.db.session.add(user)
        self.db.session.commit()
        user_id: int = user.id
        resume: Resume = Resume(user_id=user_id, template_id=1, data={'name': 'John Doe'})
        self.assertEqual(resume.template_id, 1)

    def test_resume_update_data(self):
        """Test updating resume data."""
        user: User = User(username='testuser', email='test@example.com', password='password')
        self.db.session.add(user)
        self.db.session.commit()
        user_id: int = user.id
        resume: Resume = Resume(user_id=user_id, template_id=2, data={'name': 'John Doe'})
        resume.update_data({'name': 'Jane Doe', 'age': 30})
        self.assertEqual(resume.data, {'name': 'Jane Doe', 'age': 30})

    def test_resume_get_data(self):
        """Test getting resume data."""
        user: User = User(username='testuser', email='test@example.com', password='password')
        self.db.session.add(user)
        self.db.session.commit()
        user_id: int = user.id
        resume: Resume = Resume(user_id=user_id, template_id=2, data={'name': 'John Doe'})
        self.assertEqual(resume.get_data(), {'name': 'John Doe'})

    def test_resume_repr(self):
        """Test the resume representation."""
        user: User = User(username='testuser', email='test@example.com', password='password')
        self.db.session.add(user)
        self.db.session.commit()
        user_id: int = user.id
        resume: Resume = Resume(user_id=user_id, template_id=2, data={'name': 'John Doe'})
        self.db.session.add(resume)
        self.db.session.commit()
        self.assertEqual(repr(resume), f'<Resume {resume.id}>')

    def test_resume_persistance(self):
        """Test resume persistance in the database."""
        user: User = User(username='testuser', email='test@example.com', password='password')
        self.db.session.add(user)
        self.db.session.commit()
        user_id: int = user.id
        resume: Resume = Resume(user_id=user_id, template_id=2, data={'name': 'John Doe'})
        self.db.session.add(resume)
        self.db.session.commit()

        retrieved_resume: Resume = Resume.query.filter_by(user_id=user_id).first()
        self.assertEqual(retrieved_resume.user_id, user_id)
        self.assertEqual(retrieved_resume.template_id, 2)
        self.assertEqual(retrieved_resume.data, {'name': 'John Doe'})

    ## Template Model Tests
    def test_template_creation(self):
        """Test template object creation and attribute assignment."""
        template: Template = Template(name='Simple', description='A simple template', fields=['name', 'email'])
        self.assertEqual(template.name, 'Simple')
        self.assertEqual(template.description, 'A simple template')
        self.assertEqual(template.fields, ['name', 'email'])
        self.assertEqual(template.preview_image, None)

    def test_template_creation_with_preview_image(self):
        """Test template object creation with a preview image."""
        template: Template = Template(name='Simple', description='A simple template', fields=['name', 'email'], preview_image='http://example.com/image.png')
        self.assertEqual(template.preview_image, 'http://example.com/image.png')

    def test_template_get_fields(self):
        """Test getting template fields."""
        template: Template = Template(name='Simple', description='A simple template', fields=['name', 'email'])
        self.assertEqual(template.get_fields(), ['name', 'email'])

    def test_template_render(self):
        """Test template rendering (placeholder)."""
        template: Template = Template(name='Simple', description='A simple template', fields=['name', 'email'])
        data: dict = {'name': 'John Doe', 'email': 'john@example.com'}
        rendered_template: str = template.render(data)
        self.assertEqual(rendered_template, "Template: Simple rendered with data: {'name': 'John Doe', 'email': 'john@example.com'}")

    def test_template_repr(self):
        """Test the template representation."""
        template: Template = Template(name='Simple', description='A simple template', fields=['name', 'email'])
        self.assertEqual(repr(template), '<Template Simple>')

    def test_template_persistance(self):
        """Test template persistance in the database."""
        template: Template = Template(name='Simple', description='A simple template', fields=['name', 'email'])
        self.db.session.add(template)
        self.db.session.commit()

        retrieved_template: Template = Template.query.filter_by(name='Simple').first()
        self.assertEqual(retrieved_template.name, 'Simple')
        self.assertEqual(retrieved_template.description, 'A simple template')
        self.assertEqual(retrieved_template.fields, ['name', 'email'])

if __name__ == '__main__':
    unittest.main()
