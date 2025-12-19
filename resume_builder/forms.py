from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Email, Optional
from wtforms import ValidationError

class WorkExperienceForm(FlaskForm):
    """
    Form for a single work experience entry.
    """
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    company = StringField('Company', validators=[DataRequired(), Length(max=100)])
    location = StringField('Location', validators=[Optional(), Length(max=100)])
    start_date = StringField('Start Date', validators=[DataRequired()])  # Consider using DateField with format
    end_date = StringField('End Date', validators=[Optional()])  # Consider using DateField with format
    description = TextAreaField('Description', validators=[Optional()])


class EducationForm(FlaskForm):
    """
    Form for a single education entry.
    """
    institution = StringField('Institution', validators=[DataRequired(), Length(max=100)])
    degree = StringField('Degree', validators=[DataRequired(), Length(max=100)])
    major = StringField('Major', validators=[DataRequired(), Length(max=100)])
    graduation_date = StringField('Graduation Date', validators=[DataRequired()])  # Consider using DateField with format
    description = TextAreaField('Description', validators=[Optional()])


class SkillsForm(FlaskForm):
    """
    Form for a single skill entry.
    """
    skill = StringField('Skill', validators=[DataRequired(), Length(max=100)])
    level = StringField('Level', validators=[Optional(), Length(max=50)])  # e.g., "Beginner", "Intermediate", "Expert"


class ResumeForm(FlaskForm):
    """
    Main form for creating/editing a resume.
    """
    work_experience = FieldList(FormField(WorkExperienceForm), min_entries=1, label='Work Experience')
    education = FieldList(FormField(EducationForm), min_entries=1, label='Education')
    skills = FieldList(FormField(SkillsForm), min_entries=3, label='Skills')
    other_information = TextAreaField('Other Information', validators=[Optional()])
    submit = SubmitField('Save Resume')

    def validate(self):
        """
        Custom validation logic for the entire form.

        Returns:
            bool: True if the form is valid, False otherwise.
        """
        if not FlaskForm.validate(self):
            return False

        # Add any custom validation logic here, e.g., checking date formats,
        # ensuring that at least one skill is provided, etc.

        # Example: Check if start date is before end date for work experiences
        for exp in self.work_experience.entries:
            start_date = exp.form.start_date.data
            end_date = exp.form.end_date.data
            if start_date and end_date:
                # Basic string comparison for date validation (YYYY-MM-DD).  Consider using a proper date parsing library.
                if start_date > end_date:
                    exp.form.end_date.errors.append("End date must be after start date.")
                    return False

        return True
