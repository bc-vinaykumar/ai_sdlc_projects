from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import ResumeForm, WorkExperienceForm, EducationForm, SkillsForm
from models import User, Resume, Template, db
from utils.pdf_generator import PDFGenerator
from io import BytesIO
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_default_secret_key')  # Set a default value
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db')  # Set a default value
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    """
    User loader callback for Flask-Login.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        User: The User object if found, otherwise None.
    """
    return User.query.get(int(user_id))

# Define routes
@app.route('/')
def index():
    """
    Route for the home page.

    Returns:
        str: Rendered HTML template for the home page.
    """
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route for user registration.

    Returns:
        str: Rendered HTML template for the registration page, or a redirect to the home page upon successful registration.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the username or email already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists. Please use a different one.', 'danger')
            return render_template('register.html')

        # Create a new user
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for user login.

    Returns:
        str: Rendered HTML template for the login page, or a redirect to the home page upon successful login.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """
    Route for user logout.

    Returns:
        str: Redirect to the home page after logging out.
    """
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/resume_form', methods=['GET', 'POST'])
@login_required
def resume_form():
    """
    Route for displaying and handling the resume form.

    Returns:
        str: Rendered HTML template for the resume form, or a redirect to the resume preview page upon successful form submission.
    """
    form = ResumeForm()

    if form.validate_on_submit():
        # Get the current user's ID
        user_id = current_user.id

        # Get the form data
        work_experience_data = []
        for work_experience in form.work_experience:
            work_experience_data.append({
                'title': work_experience.title.data,
                'company': work_experience.company.data,
                'location': work_experience.location.data,
                'start_date': work_experience.start_date.data,
                'end_date': work_experience.end_date.data,
                'description': work_experience.description.data
            })

        education_data = []
        for education in form.education:
            education_data.append({
                'institution': education.institution.data,
                'degree': education.degree.data,
                'major': education.major.data,
                'graduation_date': education.graduation_date.data,
                'description': education.description.data
            })

        skills_data = []
        for skill in form.skills:
            skills_data.append({
                'skill': skill.skill.data,
                'level': skill.level.data
            })

        other_information = form.other_information.data

        # Create a dictionary to store all the resume data
        resume_data = {
            'name': current_user.username,  # Example: Add user's name
            'email': current_user.email,    # Example: Add user's email
            'work_experience': work_experience_data,
            'education': education_data,
            'skills': skills_data,
            'other_information': other_information
        }

        # Create a new resume or update an existing one
        resume = Resume.query.filter_by(user_id=user_id).first()
        if resume:
            resume.update_data(resume_data)
        else:
            # Assuming template_id=1 is the default template
            resume = Resume(user_id=user_id, template_id=1, data=resume_data)
            db.session.add(resume)

        db.session.commit()

        flash('Resume saved successfully!', 'success')
        return redirect(url_for('resume_templates'))

    return render_template('resume_form.html', form=form)

@app.route('/resume_templates')
@login_required
def resume_templates():
    """
    Route for displaying available resume templates.

    Returns:
        str: Rendered HTML template for displaying resume templates.
    """
    templates = Template.query.all()
    return render_template('resume_templates.html', templates=templates)

@app.route('/resume_preview/<int:template_id>')
@login_required
def resume_preview(template_id):
    """
    Route for displaying a preview of the resume.

    Args:
        template_id (int): The ID of the selected template.

    Returns:
        str: Rendered HTML template for displaying the resume preview.
    """
    user_id = current_user.id
    resume = Resume.query.filter_by(user_id=user_id).first()
    template = Template.query.get(template_id)

    if not resume:
        flash('Please create a resume first.', 'warning')
        return redirect(url_for('resume_form'))

    resume_data = resume.get_data()
    return render_template('resume_preview.html', resume_data=resume_data, template=template)

@app.route('/generate_pdf/<int:template_id>')
@login_required
def generate_pdf(template_id):
    """
    Route for generating and downloading the resume as a PDF file.

    Args:
        template_id (int): The ID of the selected template.

    Returns:
        Response: A Flask response containing the PDF file for download.
    """
    user_id = current_user.id
    resume = Resume.query.filter_by(user_id=user_id).first()
    template = Template.query.get(template_id)

    if not resume:
        flash('Please create a resume first.', 'warning')
        return redirect(url_for('resume_form'))

    resume_data = resume.get_data()

    # Generate PDF
    pdf_generator = PDFGenerator()
    pdf_bytes = pdf_generator.generate_pdf(resume_data, template)

    # Create a response with the PDF file
    response = send_file(
        BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='resume.pdf'
    )

    return response

if __name__ == '__main__':
    # Create the database tables within the app context
    with app.app_context():
        db.create_all()

        # Create a default template if it doesn't exist
        if not Template.query.first():
            default_template = Template(
                name='Default Template',
                description='A simple, clean template.',
                fields=['name', 'email', 'phone', 'work_experience', 'education', 'skills', 'other_information'],
                preview_image='url_to_default_template_preview_image'  # Replace with an actual URL
            )
            db.session.add(default_template)
            db.session.commit()

    app.run(debug=True)
