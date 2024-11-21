import os
import PyPDF2
import docx
import markdown
import re

class DocumentProcessor:
    @staticmethod
    def read_pdf(file_path):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        return text

    @staticmethod
    def read_docx(file_path):
        doc = docx.Document(file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

    @staticmethod
    def read_markdown(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return markdown.markdown(file.read())

    @staticmethod
    def read_txt(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    @classmethod
    def process_documents(cls, directory):
        documents = {}
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if filename.endswith('.pdf'):
                documents[filename] = cls.read_pdf(file_path)
            elif filename.endswith('.docx'):
                documents[filename] = cls.read_docx(file_path)
            elif filename.endswith('.md'):
                documents[filename] = cls.read_markdown(file_path)
            elif filename.endswith('.txt'):
                documents[filename] = cls.read_txt(file_path)
        return documents