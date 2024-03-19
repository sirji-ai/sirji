from .base import BaseContentHandler
import os
import requests
import PyPDF2
from markdownify import markdownify as md

class PDFHandler(BaseContentHandler):
    def handle(self, url, output_dir):
        response = requests.get(url)
        temp_pdf_path = os.path.join(output_dir, 'temp.pdf')
        with open(temp_pdf_path, 'wb') as f:
            f.write(response.content)
        try:
            with open(temp_pdf_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text_content = '\n'.join(page.extract_text() for page in reader.pages if page.extract_text())
            markdown_content = md(text_content)
            self.save_content(markdown_content, url, output_dir, 'md')
        
        except Exception as e:
            print(f"Failed to convert PDF to markdown: {e}")
        
        finally:
            os.remove(temp_pdf_path)
