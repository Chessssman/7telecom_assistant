import os

# Telegram Bot Configuration
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Document and Storage Paths
DOCUMENTS_DIR = './documents'
CLOUD_LINK = 'https://your-cloud-storage-link.com'

# Neural Model Configuration
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
SIMILARITY_THRESHOLD = 0.5