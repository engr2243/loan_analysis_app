import json
import os
from docx import Document
import camelot
import pdfplumber
from PIL import Image
import pytesseract
import tabula  # pip install tabula-py
import pandas as pd


cwd = os.getcwd()

class Data_extractor:
    def __init__(self):
        self.data = {}

    def CR_to_text(self, file_path):
        # Determine file extension
        _, extension = os.path.splitext(file_path)
        extension = extension.lower()

        tables = []

        if extension in ['.doc', '.docx']:
            # Original Word table extraction logic
            document = Document(file_path)

            for table in document.tables:
                # Get all rows in the table
                rows = table.rows
                
                table_content = []
                for row in rows[1:]:
                    row_data = ":".join([cell.text.strip() for cell in row.cells])
                    table_content.append(row_data)
            
                tables.append(table_content)

            self.data["registration_tables"] = json.dumps(tables)

        elif extension == '.pdf':
            # Open the PDF file
            with pdfplumber.open(file_path) as pdf:                
                # Iterate through each page in the PDF
                for page_number, page in enumerate(pdf.pages, start=1):
                    tables = page.extract_tables()
                    
                    # Process each table on the page
                    for table_index, table in enumerate(tables):
                        if not table or not table[0]:  # Skip empty tables
                            continue

                        # Prepare the Markdown table header
                        header = [str(cell) if cell is not None else "" for cell in table[0]]
                        markdown_table = "| " + " | ".join(header) + " |\n"
                        markdown_table += "| " + " | ".join(["---"] * len(header)) + " |\n"
                        
                        # Add rows
                        for row in table[1:]:
                            formatted_row = [str(cell) if cell is not None else "" for cell in row]
                            markdown_table += "| " + " | ".join(formatted_row) + " |\n"
                        
                        tables.append(f"\n\n" + markdown_table)
            tables = "\n\n".join(tables)
            self.data["registration_tables"] = tables

        else:
            # If the file is not a recognized extension, you can raise an error or return an empty dict
            raise ValueError(f"Unsupported file extension: {extension}")
    
    def IL_to_text(self, file_path: str) -> str:
        """
        Extracts text from an image using Tesseract OCR.

        Args:
            image_path (str): Path to the image file.

        Returns:
            str: The extracted text from the image.
        """
        try:
            # Open the image file
            image = Image.open(file_path)
            
            # Use Tesseract to extract text
            extracted_text_eng = pytesseract.image_to_string(image, lang='eng')
            extracted_text_ara = pytesseract.image_to_string(image, lang='ara')

            final_text = f"{extracted_text_eng}/n{extracted_text_ara}"
            self.data["industrial_licence"] = final_text
        except Exception as e:
            return f"Error extracting text: {str(e)}"


    def market_data(self, file_path):
        # Load the Excel file
        df = pd.read_excel(file_path, sheet_name="Market Database  ", header=[0, 1])
        df = df.dropna(how='all')
        df = df.drop(index=20)
        df = df.ffill()
        # Initialize the dictionary
        market_data = []
        
        # Populate the dictionary
        for index, row in df.iterrows():
            data = {}
            data["Sector"] = row["Sector"].values[0]
            data["Product"] = row["Products "].values[0]
            data["Unit"] = row['Unit'].values[0]

            # Historical Sales Growth Rate
            data['Historical Sales Growth Rate'] = {
                '2020': f"{int(row["Historical Sales growth rate"][2020]*100)}%",
                '2021': f"{int(row["Historical Sales growth rate"][2021]*100)}%",
                '2022': f"{int(row["Historical Sales growth rate"][2022]*100)}%",
                '2023': f"{int(row["Historical Sales growth rate"][2023]*100)}%"
            }        
            # Projected Sales Growth Rate
            data['Projected Sales Growth Rate'] = {
                '2024': f"{int(row["Projected Sales growth rate"][2024]*100)}%",
                '2025': f"{int(row["Projected Sales growth rate"][2025]*100)}%",
                '2026': f"{int(row["Projected Sales growth rate"][2026]*100)}%",
                '2027': f"{int(row["Projected Sales growth rate"][2027]*100)}%"
            }
            
            # Competitors Prices
            data['Competitors Prices'] = str(row["Competitors' prices (SR/unit)"].values[0])
            
            # Traders Importers Prices
            data['Traders Importers Prices'] = str(row["Traders/Importers prices (SR/unit)"].values[0])
            market_data.append(data)
        self.data["market_data"] = market_data

    def get(self, cr_name, il_name):
        cr_path = os.path.join(cwd, f'data/{cr_name}')
        il_path = os.path.join(cwd, f'data/{il_name}')
        md_path = os.path.join(cwd,'data/market_database.xlsx')

        self.CR_to_text(file_path=cr_path)
        self.IL_to_text(file_path=il_path)
        self.market_data(file_path=md_path)
        return self.data