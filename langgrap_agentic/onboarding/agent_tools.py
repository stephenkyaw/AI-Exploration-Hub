from langchain_core.tools import tool
from langchain_community.document_loaders import PyMuPDFLoader


def load_pdf(file_path):
    """
    Loads a PDF file and returns the content of all pages.
    
    Parameters:
    - file_path (str): Path to the PDF file.
    
    Returns:
    - str: Combined text content of all pages of the PDF, or an error message if something goes wrong.
    """
    try:
        # Initialize the PDF loader
        loader = PyMuPDFLoader(file_path)
        
        # Load the PDF content
        data = loader.load()
        
        # Check if any pages were loaded
        if not data:
            return "No data found in the PDF file."
        
        # Ensure data is a list of Document objects
        if not isinstance(data, list) or not all(hasattr(page, 'page_content') for page in data):
            return "Invalid data format."
        
        # Combine content of all pages
        full_text = "\n\n".join(page.page_content for page in data)
        return full_text

    except Exception as e:
        # Return error message if something goes wrong
        return f"An error occurred: {str(e)}"