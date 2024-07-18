import unittest
from agent_tools import read_pdf



class TestReadPDF(unittest.TestCase):

    def test_read_pdf(self):
        # Replace with the path to a sample PDF file for testing
        pdf_path = "./docs/KYAW MYO AUNG RESUME.pdf"
        
        # Call the function
        pdf_text = read_pdf(pdf_path)
        
        # Perform assertions to verify the expected behavior
        self.assertIsInstance(pdf_text, str)
        self.assertGreater(len(pdf_text), 0)
        self.assertIn("info.kyawmyo@gamil.com", pdf_text)  # Replace with expected text
        self.assertIn("Ultimate AWS Certified Developer Associate 2024 NEW DVA-C02",pdf_text)


if __name__ == '__main__':
    unittest.main()