import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch
from reportlab.lib import colors

class PDFGenerator:
    """
    Generates PDF files from resume data and templates using ReportLab.
    """

    def __init__(self, default_font: str = "Helvetica", default_font_size: int = 12, margin_inches: float = 0.5):
        """
        Initializes the PDFGenerator with default settings.

        Args:
            default_font (str): The default font to use for the PDF. Defaults to "Helvetica".
            default_font_size (int): The default font size to use for the PDF. Defaults to 12.
            margin_inches (float): The margin size in inches for the PDF. Defaults to 0.5.
        """
        self.default_font = default_font
        self.default_font_size = default_font_size
        self.margin = margin_inches * inch
        self.styles = getSampleStyleSheet()
        self.normal_style = ParagraphStyle(
            name='Normal',
            parent=self.styles['Normal'],
            fontName=self.default_font,
            fontSize=self.default_font_size,
            leading=1.2 * self.default_font_size,
        )
        self.heading1_style = ParagraphStyle(
            name='Heading1',
            parent=self.styles['Heading1'],
            fontName=self.default_font,
            fontSize=self.default_font_size + 6,
            leading=1.2 * (self.default_font_size + 6),
            spaceAfter=0.2 * inch,
        )
        self.heading2_style = ParagraphStyle(
            name='Heading2',
            parent=self.styles['Heading2'],
            fontName=self.default_font,
            fontSize=self.default_font_size + 4,
            leading=1.2 * (self.default_font_size + 4),
            spaceBefore=0.1 * inch,
            spaceAfter=0.1 * inch,
        )

    def generate_pdf(self, resume_data: dict, template) -> bytes:
        """
        Generates a PDF file from the given resume data and template.

        Args:
            resume_data (dict): The resume data.
            template (Template): The template object.

        Returns:
            bytes: The PDF file as bytes.
        """
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setStrokeColorRGB(0, 0, 0)
        c.setFont(self.default_font, self.default_font_size)

        # Initial position
        x = self.margin
        y = letter[1] - self.margin

        # Function to add text with word wrapping
        def add_text(text: str, style: ParagraphStyle, x_pos: float, y_pos: float) -> float:
            """Adds text to the canvas with word wrapping.

            Args:
                text (str): The text to add.
                style (ParagraphStyle): The style to apply to the text.
                x_pos (float): The x-coordinate of the text.
                y_pos (float): The y-coordinate of the text.

            Returns:
                float: The new y-coordinate after adding the text.
            """
            p = Paragraph(text, style)
            w, h = p.wrapOn(c, letter[0] - 2 * self.margin, letter[1])  # Available width
            p.drawOn(c, x_pos, y_pos - h)
            return y_pos - h

        # Add resume content based on the template and data
        y = self.add_resume_content(c, resume_data, template, x, y, add_text)

        c.save()
        buffer.seek(0)
        return buffer.read()

    def add_resume_content(self, canvas, resume_data: dict, template, x: float, y: float, add_text) -> float:
        """Adds the resume content to the canvas based on the template and data.

        Args:
            canvas: The ReportLab canvas object.
            resume_data (dict): The resume data.
            template: The template object.
            x (float): The current x-coordinate.
            y (float): The current y-coordinate.
            add_text: The function to add text to the canvas.

        Returns:
            float: The updated y-coordinate.
        """
        # Example: Add name and contact information (assuming they are in resume_data)
        if 'name' in resume_data:
            y = add_text(resume_data['name'], self.heading1_style, x, y)
        if 'email' in resume_data:
            y = add_text(resume_data['email'], self.normal_style, x, y)
        if 'phone' in resume_data:
            y = add_text(resume_data['phone'], self.normal_style, x, y)

        # Add work experience
        if 'work_experience' in resume_data:
            y = add_text("Work Experience", self.heading2_style, x, y)
            for exp in resume_data['work_experience']:
                company_title = f"{exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}"
                y = add_text(company_title, self.normal_style, x, y)
                dates = f"{exp.get('start_date', 'N/A')} - {exp.get('end_date', 'Present')}"
                y = add_text(dates, self.normal_style, x, y)
                description = exp.get('description', '')
                y = add_text(description, self.normal_style, x, y)

        # Add education
        if 'education' in resume_data:
            y = add_text("Education", self.heading2_style, x, y)
            for edu in resume_data['education']:
                institution_degree = f"{edu.get('degree', 'N/A')} in {edu.get('major', 'N/A')} from {edu.get('institution', 'N/A')}"
                y = add_text(institution_degree, self.normal_style, x, y)
                graduation_date = f"Graduated: {edu.get('graduation_date', 'N/A')}"
                y = add_text(graduation_date, self.normal_style, x, y)
                description = edu.get('description', '')
                y = add_text(description, self.normal_style, x, y)

        # Add skills
        if 'skills' in resume_data:
            y = add_text("Skills", self.heading2_style, x, y)
            skills_text = ", ".join([skill.get('skill', 'N/A') for skill in resume_data['skills']])
            y = add_text(skills_text, self.normal_style, x, y)

        # Add other information
        if 'other_information' in resume_data:
            y = add_text("Other Information", self.heading2_style, x, y)
            y = add_text(resume_data['other_information'], self.normal_style, x, y)

        return y
