import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
    DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), 'documents')
    CLOUD_STORAGE_LINK = os.getenv('CLOUD_STORAGE_LINK', 'https://example.com/cloud-storage')