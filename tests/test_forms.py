import unittest
from unittest.mock import patch
from wtforms import StringField, TextAreaField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from wtforms import Form
# Try importing FlaskForm, and if it fails, set a flag
try:
    from flask_wtf import FlaskForm
    flask_wtf_installed = True
except ImportError:
    flask_wtf_installed = False
    FlaskForm = Form  # Fallback to wtforms.Form if flask_wtf is not installed
    print("Warning: flask_wtf is not installed. Falling back to wtforms.Form. Install it for full functionality.")

# Assuming the forms.py file is in a directory named 'resume_builder'
# and the current file (test_forms.py) is in a directory named 'tests'
# which are both under a common root directory.
# Therefore, the relative import should be:
from resume_builder.forms import WorkExperienceForm, EducationForm, SkillsForm, ResumeForm


## WorkExperienceForm Tests
class TestWorkExperienceForm(unittest.TestCase):
    """
    Test suite for the WorkExperienceForm.
    """

    def setUp(self):
        """
        Setup method to create a new form instance for each test.
        """
        self.form = WorkExperienceForm()

    def test_valid_data(self):
        """
        Test case to verify the form's validity with valid data.
        """
        data: dict = {
            'title': 'Software Engineer',
            'company': 'Example Corp',
            'location': 'New York',
            'start_date': '2022-01-01',
            'end_date': '2023-01-01',
            'description': 'Developed web applications'
        }
        self.form = WorkExperienceForm(data=data)
        self.assertTrue(self.form.validate())

    def test_empty_title(self):
        """
        Test case to verify that the 'title' field is required.
        """
        data: dict = {
            'company': 'Example Corp',
            'location': 'New York',
            'start_date': '2022-01-01',
            'end_date': '2023-01-01',
            'description': 'Developed web applications'
        }
        self.form = WorkExperienceForm(data=data)
        self.assertFalse(self.form.validate())
        self.assertIn('This field is required.', self.form.title.errors)

    def test_long_title(self):
        """
        Test case to verify the 'title' field's maximum length.
        """
        long_string: str = 'a' * 101
        data: dict = {
            'title': long_string,
            'company': 'Example Corp',
            'location': 'New York',
            'start_date': '2022-01-01',
            'end_date': '2023-01-01',
            'description': 'Developed web applications'
        }
        self.form = WorkExperienceForm(data=data)
        self.assertFalse(self.form.validate())
        self.assertIn('Field must be between 1 and 100 characters long.', self.form.title.errors)

    def test_empty_company(self):
        """
        Test case to verify that the 'company' field is required.
        """
        data: dict = {
            'title': 'Software Engineer',
            'location': 'New York',
            'start_date': '2022-01-01',
            'end_date': '2023-01-01',
            'description': 'Developed web applications'
        }
        self.form = WorkExperienceForm(data=data)
        self.assertFalse(self.form.validate())
        self.assertIn('This field is required.', self.form.company.errors)

    def test_long_company(self):
        """
        Test case to verify the 'company' field's maximum length.
        """
        long_string: str = 'a' * 101
        data: dict = {
            'title': 'Software Engineer',
            'company': long_string,
            'location': 'New York',
            'start_date': '2022-01-01',
            'end_date': '2023-01-01',
            'description': 'Developed web applications'
        }
        self.form = WorkExperienceForm(data=data)
        self.assertFalse(self.form.validate())
        self.assertIn('Field must be between 1 and 100 characters long.', self.form.company.errors)

    def test_optional_location(self):
        """
        Test case to verify that the 'location' field is optional.
        """
        data: dict = {
            'title': 'Software Engineer',
            'company': 'Example Corp',
            'start_date': '2022-01-01',
            'end_date': '2023-01-01',
            'description': 'Developed web applications'
        }
        self.form = WorkExperienceForm(data=data)
        self.assertTrue(self.form.validate())

    def test_long_location(self):
        """
        Test case to verify the 'location' field's maximum length.
        """
        long_string: str = 'a' * 101
        data: dict = {
            'title': 'Software Engineer',
            'company': 'Example Corp',
            'location': long_string,
            'start_date': '2022-01-01',
            'end_date': '2023-01-01',
            'description': 'Developed web applications'
        }
        self.form = WorkExperienceForm(data=data)
        self.form.validate()
        self.assertFalse(self.form.validate())
        self.assertIn('Field must be between 1 and 100 characters long.', self.form.location.errors)

    def test_empty_start_date(self):
        """
        Test case to verify that the 'start_date' field is required.
        """
        data: dict = {
            'title': 'Software Engineer',
            'company': 'Example Corp',
            'location': 'New York',
            'end_date': '2023-01-01',
            'description': 'Developed web applications'
        }
        self.form = WorkExperienceForm(data=data)
        self.assertFalse(self.form.validate())
        self.assertIn('This field is required.', self.form.start_date.errors)

    def test_optional_end_date(self):
        """
        Test case to verify that the 'end_date' field is optional.
        """
        data: dict = {
            'title': 'Software Engineer',
            'company': 'Example Corp',
            'location': 'New York',
            'start_date': '2022-01-01',
            'description': 'Developed web applications'
        }
        self.form = WorkExperienceForm(data=data)
        self.assertTrue(self.form.validate())

    def test_optional_description(self):
        """
        Test case to verify that the 'description' field is optional.
        """
        data: dict = {
            'title': 'Software Engineer',
            'company': 'Example Corp',
            'location': 'New York',
            'start_date': '2022-01-01',
            'end_date': '2023-01-01',
        }
        self.form = WorkExperienceForm(data=data)
        self.assertTrue(self.form.validate())


## EducationForm Tests
class TestEducationForm(unittest.TestCase):
    """
    Test suite for the EducationForm.
    """

    def setUp(self):
        """
        Setup method to create a new form instance for each test.
        """
        self.form = EducationForm()

    def test_valid_data(self):
        """
        Test case to verify the form's validity with valid data.
        """
        data: dict = {
            'institution': 'Example University',
            'degree': 'Bachelor of Science',
            'major': 'Computer Science',
            'graduation_date': '2022-05-01',
            'description': 'Relevant coursework...'
        }
        self.form = EducationForm(data=data)
        self.assertTrue(self.form.validate())

    def test_empty_institution(self):
        """
        Test case to verify that the 'institution' field is required.
        """
        data: dict = {
            'degree': 'Bachelor of Science',
            'major': 'Computer Science',
            'graduation_date': '2022-05-01',
            'description': 'Relevant coursework...'
        }
        self.form = EducationForm(data=data)
        self.assertFalse(self.form.validate())
        self.assertIn('This field is required.', self.form.institution.errors)

    def test_long_institution(self):
        """
        Test case to verify the 'institution' field's maximum length.
        """
        long_string: str = 'a' * 101
        data: dict = {
            'institution': long_string,
            'degree': 'Bachelor of Science',
            'major': 'Computer Science',
            'graduation_date': '2022-05-01',
            'description': 'Relevant coursework...'
        }
        self.form = EducationForm(data=data)
        self.assertFalse(self.form.validate())
        self.assertIn('Field must be between 1 and 100 characters long.', self.form.institution.errors)

    def test_empty_degree(self):
        """
        Test case to verify that the 'degree' field is required.
        """
        data: dict = {
            'institution': 'Example University',
            'major': 'Computer Science',
            'graduation_date': '2022-05-01',
            'description': 'Relevant coursework...'
        }
        self.form = EducationForm(data=data)
        self.assertFalse(self.form.validate())
        self.assertIn('This field is required.', self.form.degree.errors)

    def test_long_degree(self):
        """
        Test case to verify the 'degree' field's maximum length.
        """
        long_string: str = 'a' * 101
        data: dict = {
            'institution': 'Example University',
            'degree': long_string,
            'major': 'Computer Science',
            'graduation_date': '2022-05-01',
            'description': 'Relevant coursework...'
        }
        self.form = EducationForm(data=data)
        self.assertFalse(self.form.validate())
        self.assertIn('Field must be between 1 and 100 characters long.', self.form.degree.errors)

    def test_empty_major(self):
        """
        Test case to verify that the 'major' field is required.
        """
        data: dict = {
            'institution': 'Example University',
            'degree': 'Bachelor of Science',
            'graduation_date': '2022-05-01',
            'description': 'Relevant coursework...'
        }
        self.form = EducationForm(data=data)
        self.assertFalse(self.form.validate())
        self.assertIn('This field is required.', self.form.major.errors)

    def test_long_major(self):
        """
        Test case to verify the 'major' field's maximum length.
        """
        long_string: str = 'a' * 101
        data: dict = {
            'institution': 'Example University',
            'degree': 'Bachelor of Science',
            'major': long_string,
            'graduation_date': '2022-05-01',
            'description': 'Relevant coursework...'
        }
        self.form = EducationForm(data=data)
        self.assertFalse(self.form.validate())
        self.assertIn('Field must be between 1 and 100 characters long.', self.form.major.errors)

    def test_empty_graduation_date(self):
        """
        Test case to verify that the 'graduation_date' field is required.
        """
        data: dict = {
            'institution': 'Example University',
            'degree': 'Bachelor of Science',
            'major': 'Computer Science',
            'description': 'Relevant coursework...'
        }
        self.form = EducationForm(data=data)
        self.assertFalse(self.form.validate())
        self.assertIn('This field is required.', self.form.graduation_date.errors)

    def test_optional_description(self):
        """
        Test case to verify that the 'description' field is optional.
        """
        data: dict = {
            'institution': 'Example University',
            'degree': 'Bachelor of Science',
            'major': 'Computer Science',
            'graduation_date': '2022-05-01',
        }
        self.form = EducationForm(data=data)
        self.assertTrue(self.form.validate())


## SkillsForm Tests
class TestSkillsForm(unittest.TestCase):
    """
    Test suite for the SkillsForm.
    """

    def setUp(self):
        """
        Setup method to create a new form instance for each test.
        """
        self.form = SkillsForm()

    def test_valid_data(self):
        """
        Test case to verify the form's validity with valid data.
        """
        data: dict = {
            'skill': 'Python',
            'level': 'Intermediate'
        }
        self.form = SkillsForm(data=data)
        self.assertTrue(self.form.validate())

    def test_empty_skill(self):
        """
        Test case to verify that the 'skill' field is required.
        """
        data: dict = {
            'level': 'Intermediate'
        }
        self.form = SkillsForm(data=data)
        self.assertFalse(self.form.validate())
        self.assertIn('This field is required.', self.form.skill.errors)

    def test_long_skill(self):
        """
        Test case to verify the 'skill' field's maximum length.
        """
        long_string: str = 'a' * 101
        data: dict = {
            'skill': long_string,
            'level': 'Intermediate'
        }
        self.form = SkillsForm(data=data)
        self.assertFalse(self.form.validate())
        self.assertIn('Field must be between 1 and 100 characters long.', self.form.skill.errors)

    def test_optional_level(self):
        """
        Test case to verify that the 'level' field is optional.
        """
        data: dict = {
            'skill': 'Python'
        }
        self.form = SkillsForm(data=data)
        self.assertTrue(self.form.validate())

    def test_long_level(self):
        """
        Test case to verify the 'level' field's maximum length.
        """
        long_string: str = 'a' * 51
        data: dict = {
            'skill': 'Python',
            'level': long_string
        }
        self.form = SkillsForm(data=data)
        self.form.validate()
        self.assertFalse(self.form.validate())
        self.assertIn('Field must be between 1 and 50 characters long.', self.form.level.errors)


## ResumeForm Tests
class TestResumeForm(unittest.TestCase):
    """
    Test suite for the ResumeForm.
    """

    def setUp(self):
        """
        Setup method to create a new form instance for each test.
        """
        self.form = ResumeForm()

    def test_valid_data(self):
        """
        Test case to verify the form's validity with valid data.
        """
        data: dict = {
            'work_experience': [
                {
                    'title': 'Software Engineer',
                    'company': 'Example Corp',
                    'location': 'New York',
                    'start_date': '2022-01-01',
                    'end_date': '2023-01-01',
                    'description': 'Developed web applications'
                }
            ],
            'education': [
                {
                    'institution': 'Example University',
                    'degree': 'Bachelor of Science',
                    'major': 'Computer Science',
                    'graduation_date': '2022-05-01',
                    'description': 'Relevant coursework...'
                }
            ],
            'skills': [
                {'skill': 'Python', 'level': 'Intermediate'},
                {'skill': 'Java', 'level': 'Beginner'},
                {'skill': 'C++', 'level': 'Advanced'}
            ],
            'other_information': 'Additional details...'
        }
        self.form = ResumeForm(data=data)
        # Manually populate the FieldList entries
        for field_name in ['work_experience', 'education', 'skills']:
            field = getattr(self.form, field_name)
            field.entries = []
            for item_data in data[field_name]:
                if field_name == 'work_experience':
                    form = WorkExperienceForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                elif field_name == 'education':
                    form = EducationForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                else:
                    form = SkillsForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                field.entries.append(form)

        self.assertTrue(self.form.validate())

    def test_min_entries_work_experience(self):
        """
        Test case to verify the minimum number of work experience entries.
        """
        data: dict = {
            'work_experience': [],
            'education': [
                {
                    'institution': 'Example University',
                    'degree': 'Bachelor of Science',
                    'major': 'Computer Science',
                    'graduation_date': '2022-05-01',
                    'description': 'Relevant coursework...'
                }
            ],
            'skills': [
                {'skill': 'Python', 'level': 'Intermediate'},
                {'skill': 'Java', 'level': 'Beginner'},
                {'skill': 'C++', 'level': 'Advanced'}
            ],
            'other_information': 'Additional details...'
        }
        self.form = ResumeForm(data=data)
        # Manually populate the FieldList entries
        for field_name in ['work_experience', 'education', 'skills']:
            field = getattr(self.form, field_name)
            field.entries = []
            for item_data in data[field_name]:
                if field_name == 'work_experience':
                    form = WorkExperienceForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                elif field_name == 'education':
                    form = EducationForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                else:
                    form = SkillsForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                field.entries.append(form)
        self.form.work_experience.min_entries = 1
        self.assertFalse(self.form.validate())

    def test_min_entries_education(self):
        """
        Test case to verify the minimum number of education entries.
        """
        data: dict = {
            'work_experience': [
                {
                    'title': 'Software Engineer',
                    'company': 'Example Corp',
                    'location': 'New York',
                    'start_date': '2022-01-01',
                    'end_date': '2023-01-01',
                    'description': 'Developed web applications'
                }
            ],
            'education': [],
            'skills': [
                {'skill': 'Python', 'level': 'Intermediate'},
                {'skill': 'Java', 'level': 'Beginner'},
                {'skill': 'C++', 'level': 'Advanced'}
            ],
            'other_information': 'Additional details...'
        }
        self.form = ResumeForm(data=data)
        # Manually populate the FieldList entries
        for field_name in ['work_experience', 'education', 'skills']:
            field = getattr(self.form, field_name)
            field.entries = []
            for item_data in data[field_name]:
                if field_name == 'work_experience':
                    form = WorkExperienceForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                elif field_name == 'education':
                    form = EducationForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                else:
                    form = SkillsForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                field.entries.append(form)
        self.form.education.min_entries = 1
        self.assertFalse(self.form.validate())

    def test_min_entries_skills(self):
        """
        Test case to verify the minimum number of skills entries.
        """
        data: dict = {
            'work_experience': [
                {
                    'title': 'Software Engineer',
                    'company': 'Example Corp',
                    'location': 'New York',
                    'start_date': '2022-01-01',
                    'end_date': '2023-01-01',
                    'description': 'Developed web applications'
                }
            ],
            'education': [
                {
                    'institution': 'Example University',
                    'degree': 'Bachelor of Science',
                    'major': 'Computer Science',
                    'graduation_date': '2022-05-01',
                    'description': 'Relevant coursework...'
                }
            ],
            'skills': [],
            'other_information': 'Additional details...'
        }
        self.form = ResumeForm(data=data)
        # Manually populate the FieldList entries
        for field_name in ['work_experience', 'education', 'skills']:
            field = getattr(self.form, field_name)
            field.entries = []
            for item_data in data[field_name]:
                if field_name == 'work_experience':
                    form = WorkExperienceForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                elif field_name == 'education':
                    form = EducationForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                else:
                    form = SkillsForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                field.entries.append(form)
        self.form.skills.min_entries = 3
        self.assertFalse(self.form.validate())

    def test_optional_other_information(self):
        """
        Test case to verify that the 'other_information' field is optional.
        """
        data: dict = {
            'work_experience': [
                {
                    'title': 'Software Engineer',
                    'company': 'Example Corp',
                    'location': 'New York',
                    'start_date': '2022-01-01',
                    'end_date': '2023-01-01',
                    'description': 'Developed web applications'
                }
            ],
            'education': [
                {
                    'institution': 'Example University',
                    'degree': 'Bachelor of Science',
                    'major': 'Computer Science',
                    'graduation_date': '2022-05-01',
                    'description': 'Relevant coursework...'
                }
            ],
            'skills': [
                {'skill': 'Python', 'level': 'Intermediate'},
                {'skill': 'Java', 'level': 'Beginner'},
                {'skill': 'C++', 'level': 'Advanced'}
            ]
        }
        self.form = ResumeForm(data=data)
        # Manually populate the FieldList entries
        for field_name in ['work_experience', 'education', 'skills']:
            field = getattr(self.form, field_name)
            field.entries = []
            for item_data in data[field_name]:
                if field_name == 'work_experience':
                    form = WorkExperienceForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                elif field_name == 'education':
                    form = EducationForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                else:
                    form = SkillsForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                field.entries.append(form)
        self.assertTrue(self.form.validate())

    def test_date_validation(self):
        """
        Test case to verify the custom date validation logic.
        """
        data: dict = {
            'work_experience': [
                {
                    'title': 'Software Engineer',
                    'company': 'Example Corp',
                    'location': 'New York',
                    'start_date': '2023-01-01',
                    'end_date': '2022-01-01',
                    'description': 'Developed web applications'
                }
            ],
            'education': [
                {
                    'institution': 'Example University',
                    'degree': 'Bachelor of Science',
                    'major': 'Computer Science',
                    'graduation_date': '2022-05-01',
                    'description': 'Relevant coursework...'
                }
            ],
            'skills': [
                {'skill': 'Python', 'level': 'Intermediate'},
                {'skill': 'Java', 'level': 'Beginner'},
                {'skill': 'C++', 'level': 'Advanced'}
            ],
            'other_information': 'Additional details...'
        }
        self.form = ResumeForm(data=data)
        # Manually populate the FieldList entries
        for field_name in ['work_experience', 'education', 'skills']:
            field = getattr(self.form, field_name)
            field.entries = []
            for item_data in data[field_name]:
                if field_name == 'work_experience':
                    form = WorkExperienceForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                elif field_name == 'education':
                    form = EducationForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                else:
                    form = SkillsForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                field.entries.append(form)

        self.assertFalse(self.form.validate())
        self.assertIn("End date must be after start date.", self.form.work_experience[0].form.end_date.errors)

    def test_validate_method_calls_flaskform_validate(self):
        """
        Test that the validate method calls the FlaskForm.validate method.
        """
        with patch.object(FlaskForm, 'validate') as mock_flaskform_validate:
            data: dict = {
                'work_experience': [
                    {
                        'title': 'Software Engineer',
                        'company': 'Example Corp',
                        'location': 'New York',
                        'start_date': '2022-01-01',
                        'end_date': '2023-01-01',
                        'description': 'Developed web applications'
                    }
                ],
                'education': [
                    {
                        'institution': 'Example University',
                        'degree': 'Bachelor of Science',
                        'major': 'Computer Science',
                        'graduation_date': '2022-05-01',
                        'description': 'Relevant coursework...'
                    }
                ],
                'skills': [
                    {'skill': 'Python', 'level': 'Intermediate'},
                    {'skill': 'Java', 'level': 'Beginner'},
                    {'skill': 'C++', 'level': 'Advanced'}
                ],
                'other_information': 'Additional details...'
            }
            self.form = ResumeForm(data=data)
            # Manually populate the FieldList entries
            for field_name in ['work_experience', 'education', 'skills']:
                field = getattr(self.form, field_name)
                field.entries = []
                for item_data in data[field_name]:
                    if field_name == 'work_experience':
                        form = WorkExperienceForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                    elif field_name == 'education':
                        form = EducationForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                    else:
                        form = SkillsForm(data=item_data, prefix=field.prefix + '-' + str(len(field.entries)))
                    field.entries.append(form)
            self.form.validate()
            mock_flaskform_validate.assert_called_once_with(self.form)

if __name__ == '__main__':
    unittest.main()
