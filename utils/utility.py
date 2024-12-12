import json
import os
import subprocess

def load_js(file_path):
    # Open the file and load the JSON data
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

import subprocess
import os

def doc_to_pdf(input_docx, output_pdf):
    """
    Convert DOCX to PDF using LibreOffice on Linux.
    Arguments:
        input_docx: Path to the DOCX file.
        output_pdf: Path to the output PDF file.
    """
    try:
        # Ensure the input file exists
        if not os.path.exists(input_docx):
            raise FileNotFoundError(f"Input DOCX file not found: {input_docx}")
        
        # Get the output directory
        output_dir = os.path.dirname(output_pdf)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Run LibreOffice with a timeout
        subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", output_dir, input_docx],
            check=True,
            timeout=30  # Timeout in seconds
        )
        return True
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except subprocess.TimeoutExpired:
        return "timeout"
    except subprocess.CalledProcessError as e:
        print(f"Error converting DOCX to PDF: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

