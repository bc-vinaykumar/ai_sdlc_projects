import unittest
from unittest.mock import MagicMock
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch
from reportlab.lib import colors

# Adjust import path to match the file structure
from resume_builder.utils.pdf_generator import PDFGenerator


## PDFGenerator Class Initialization Tests
class TestPDFGeneratorInitialization(unittest.TestCase):
    """
    Test suite for the PDFGenerator class initialization.
    """

    def test_default_initialization(self):
        """
        Test the default initialization of the PDFGenerator class.
        """
        generator: PDFGenerator = PDFGenerator()
        self.assertEqual(generator.default_font, "Helvetica")
        self.assertEqual(generator.default_font_size, 12)
        self.assertEqual(generator.margin, 0.5 * inch)
        self.assertIsInstance(generator.styles, dict)
        self.assertIsInstance(generator.normal_style, ParagraphStyle)
        self.assertIsInstance(generator.heading1_style, ParagraphStyle)
        self.assertIsInstance(generator.heading2_style, ParagraphStyle)

    def test_custom_initialization(self):
        """
        Test the initialization of the PDFGenerator class with custom parameters.
        """
        generator: PDFGenerator = PDFGenerator(default_font="Times-Roman", default_font_size=14, margin_inches=1.0)
        self.assertEqual(generator.default_font, "Times-Roman")
        self.assertEqual(generator.default_font_size, 14)
        self.assertEqual(generator.margin, 1.0 * inch)
        self.assertIsInstance(generator.styles, dict)
        self.assertIsInstance(generator.normal_style, ParagraphStyle)
        self.assertIsInstance(generator.heading1_style, ParagraphStyle)
        self.assertIsInstance(generator.heading2_style, ParagraphStyle)
        self.assertEqual(generator.normal_style.fontName, "Times-Roman")
        self.assertEqual(generator.normal_style.fontSize, 14)
        self.assertEqual(generator.heading1_style.fontName, "Times-Roman")
        self.assertEqual(generator.heading1_style.fontSize, 20)
        self.assertEqual(generator.heading2_style.fontName, "Times-Roman")
        self.assertEqual(generator.heading2_style.fontSize, 18)

## PDFGenerator Generate PDF Tests
class TestPDFGeneratorGeneratePDF(unittest.TestCase):
    """
    Test suite for the generate_pdf method of the PDFGenerator class.
    """

    def setUp(self):
        """
        Set up for the test cases.
        """
        self.generator: PDFGenerator = PDFGenerator()
        self.resume_data: dict = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '123-456-7890',
            'work_experience': [
                {
                    'title': 'Software Engineer',
                    'company': 'Acme Corp',
                    'start_date': '2020-01-01',
                    'end_date': '2022-01-01',
                    'description': 'Developed and maintained software applications.'
                }
            ],
            'education': [
                {
                    'degree': 'Bachelor of Science',
                    'major': 'Computer Science',
                    'institution': 'University of Example',
                    'graduation_date': '2019-05-01',
                    'description': 'Relevant coursework in data structures and algorithms.'
                }
            ],
            'skills': [
                {'skill': 'Python'},
                {'skill': 'Java'}
            ],
            'other_information': 'References available upon request.'
        }
        self.template: MagicMock = MagicMock()  # Replace with a real template if needed

    def test_generate_pdf_success(self):
        """
        Test the successful generation of a PDF file.
        """
        pdf_bytes: bytes = self.generator.generate_pdf(self.resume_data, self.template)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 0)

    def test_generate_pdf_empty_resume_data(self):
        """
        Test the generation of a PDF file with empty resume data.
        """
        empty_resume_data: dict = {}
        pdf_bytes: bytes = self.generator.generate_pdf(empty_resume_data, self.template)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 0)

    def test_generate_pdf_missing_data(self):
        """
        Test the generation of a PDF file with missing data fields.
        """
        resume_data: dict = {
            'name': 'Jane Doe',
            'email': 'jane.doe@example.com'
        }
        pdf_bytes: bytes = self.generator.generate_pdf(resume_data, self.template)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 0)

    def test_add_resume_content(self):
        """
        Test the add_resume_content method.
        """
        mock_canvas: MagicMock = MagicMock()
        x_pos: float = self.generator.margin
        y_pos: float = letter[1] - self.generator.margin
        mock_add_text: MagicMock = MagicMock(return_value=y_pos - 10)

        new_y: float = self.generator.add_resume_content(mock_canvas, self.resume_data, self.template, x_pos, y_pos, mock_add_text)

        self.assertIsInstance(new_y, float)
        self.assertLess(new_y, y_pos)
        self.assertTrue(mock_add_text.called)

    def test_add_resume_content_no_data(self):
        """
        Test the add_resume_content method with no resume data.
        """
        mock_canvas: MagicMock = MagicMock()
        x_pos: float = self.generator.margin
        y_pos: float = letter[1] - self.generator.margin
        mock_add_text: MagicMock = MagicMock(return_value=y_pos - 10)
        empty_resume_data: dict = {}

        new_y: float = self.generator.add_resume_content(mock_canvas, empty_resume_data, self.template, x_pos, y_pos, mock_add_text)

        self.assertEqual(new_y, y_pos)
        self.assertFalse(mock_add_text.called)

    def test_add_resume_content_missing_fields(self):
        """
        Test the add_resume_content method with missing fields in resume data.
        """
        mock_canvas: MagicMock = MagicMock()
        x_pos: float = self.generator.margin
        y_pos: float = letter[1] - self.generator.margin
        mock_add_text: MagicMock = MagicMock(return_value=y_pos - 10)
        resume_data: dict = {'name': 'Test User'}

        new_y: float = self.generator.add_resume_content(mock_canvas, resume_data, self.template, x_pos, y_pos, mock_add_text)

        self.assertIsInstance(new_y, float)
        self.assertLess(new_y, y_pos)
        self.assertTrue(mock_add_text.called)

    def test_generate_pdf_no_template(self):
        """
        Test the generation of a PDF file with no template.
        """
        pdf_bytes: bytes = self.generator.generate_pdf(self.resume_data, None)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 0)

## PDFGenerator Edge Cases and Error Handling Tests
class TestPDFGeneratorEdgeCases(unittest.TestCase):
    """
    Test suite for edge cases and error handling in the PDFGenerator class.
    """

    def setUp(self):
        """
        Set up for the test cases.
        """
        self.generator: PDFGenerator = PDFGenerator()
        self.resume_data: dict = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '123-456-7890',
            'work_experience': [
                {
                    'title': 'Software Engineer',
                    'company': 'Acme Corp',
                    'start_date': '2020-01-01',
                    'end_date': '2022-01-01',
                    'description': 'Developed and maintained software applications.'
                }
            ],
            'education': [
                {
                    'degree': 'Bachelor of Science',
                    'major': 'Computer Science',
                    'institution': 'University of Example',
                    'graduation_date': '2019-05-01',
                    'description': 'Relevant coursework in data structures and algorithms.'
                }
            ],
            'skills': [
                {'skill': 'Python'},
                {'skill': 'Java'}
            ],
            'other_information': 'References available upon request.'
        }
        self.template: MagicMock = MagicMock()

    def test_empty_work_experience(self):
        """
        Test with empty work experience list.
        """
        self.resume_data['work_experience'] = []
        pdf_bytes: bytes = self.generator.generate_pdf(self.resume_data, self.template)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 0)

    def test_empty_education(self):
        """
        Test with empty education list.
        """
        self.resume_data['education'] = []
        pdf_bytes: bytes = self.generator.generate_pdf(self.resume_data, self.template)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 0)

    def test_empty_skills(self):
        """
        Test with empty skills list.
        """
        self.resume_data['skills'] = []
        pdf_bytes: bytes = self.generator.generate_pdf(self.resume_data, self.template)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 0)

    def test_missing_work_experience_fields(self):
        """
        Test with missing fields in work experience.
        """
        self.resume_data['work_experience'] = [{'company': 'Test Company'}]
        pdf_bytes: bytes = self.generator.generate_pdf(self.resume_data, self.template)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 0)

    def test_missing_education_fields(self):
        """
        Test with missing fields in education.
        """
        self.resume_data['education'] = [{'institution': 'Test Institution'}]
        pdf_bytes: bytes = self.generator.generate_pdf(self.resume_data, self.template)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 0)

    def test_long_text_fields(self):
        """
        Test with very long text fields to ensure word wrapping works correctly.
        """
        long_text: str = "This is a very long string of text that should wrap around to the next line when it reaches the end of the available width. " * 20
        self.resume_data['other_information'] = long_text
        pdf_bytes: bytes = self.generator.generate_pdf(self.resume_data, self.template)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 0)

    def test_unicode_characters(self):
        """
        Test with unicode characters in the resume data.
        """
        self.resume_data['name'] = 'Jöhn Döé'
        self.resume_data['other_information'] = '© 2024'
        pdf_bytes: bytes = self.generator.generate_pdf(self.resume_data, self.template)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 0)

    def test_numeric_values_as_strings(self):
        """
        Test with numeric values passed as strings.
        """
        self.resume_data['phone'] = '1234567890'
        pdf_bytes: bytes = self.generator.generate_pdf(self.resume_data, self.template)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 0)

    def test_xss_attack_prevention(self):
        """
        Test to prevent XSS attacks by sanitizing input.  This is a basic example and may need more robust handling.
        """
        self.resume_data['name'] = '<script>alert("XSS");</script> John Doe'
        pdf_bytes: bytes = self.generator.generate_pdf(self.resume_data, self.template)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 0)
        # Basic check to ensure the script tag is not present in the output (crude, but a start)
        self.assertNotIn(b'<script>', pdf_bytes)

if __name__ == '__main__':
    unittest.main()
