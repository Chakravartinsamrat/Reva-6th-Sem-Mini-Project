import os
import docx
import pytesseract
from pdf2image import convert_from_path
from newspaper import Article
import nltk
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Download NLTK data on first run
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class DocumentProcessor:
    @staticmethod
    def extract_text_from_pdf(file_path):
        """Extract text from PDF files using OCR if needed."""
        try:
            # Convert PDF to images
            poppler_path = r"C:\Users\piyus\Documents\popper\poppler-24.08.0\Library\bin"
            images = convert_from_path(file_path,poppler_path=poppler_path)
            text = ""
            
            # Extract text from each page
            for img in images:
                text += pytesseract.image_to_string(img) + "\n\n"
                
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    @staticmethod
    def extract_text_from_docx(file_path):
        """Extract text from DOCX files."""
        try:
            doc = docx.Document(file_path)
            text = "\n\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error extracting text from DOCX: {e}")
            return ""
    
    @staticmethod
    def extract_text_from_txt(file_path):
        """Extract text from TXT files."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error extracting text from TXT: {e}")
            return ""
    
    @staticmethod
    def extract_text_from_url(url):
        """Extract text from a news article or blog URL."""
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text
        except Exception as e:
            print(f"Error extracting text from URL: {e}")
            return ""
    
    @staticmethod
    def process_file(file_path, file_type):
        """Process file based on its type."""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return DocumentProcessor.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            return DocumentProcessor.extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            return DocumentProcessor.extract_text_from_txt(file_path)
        elif file_extension in ['.html', '.htm'] or file_path.startswith('http'):
            return DocumentProcessor.extract_text_from_url(file_path)
        else:
            return "Unsupported file format"