from pymupdf import pymupdf

def read_pdf(file_path):
    """
    Reads a PDF file and returns the concatenated text content of all pages.
    
    Parameters:
    - file_path (str): Path to the PDF file.
    
    Returns:
    - str: Concatenated text content of all pages.
    """
    try:
        # Open the PDF file
        document = pymupdf.open(file_path)
        
        # Initialize an empty string to store the text
        full_text = ""
        
        # Loop through each page
        for page_num in range(document.page_count):
            page = document.load_page(page_num)
            text = page.get_text("text")
            
            # Append the text of the current page to full_text
            full_text += text + "\n\n"  # Add new lines between pages for separation
        
        return full_text.strip()  # Strip extra whitespace from the beginning and end
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""