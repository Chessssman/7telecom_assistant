import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command

from config import TOKEN, DOCUMENTS_DIR, EMBEDDING_MODEL, SIMILARITY_THRESHOLD
from document_assistant import DocumentAssistant
from handlers import start_command, help_command, handle_question


class TelegramDocumentBot:
    def __init__(self):
        # Initialize bot and dispatcher
        self.bot = Bot(token=TOKEN)
        self.dp = Dispatcher()

        # Initialize document assistant
        self.assistant = DocumentAssistant(
            DOCUMENTS_DIR,
            EMBEDDING_MODEL,
            SIMILARITY_THRESHOLD
        )

        # Register handlers
        self.register_handlers()

    def register_handlers(self):
        """
        Register bot message handlers with correct async handling
        """
        self.dp.message.register(start_command, Command(commands=['start']))
        self.dp.message.register(help_command, Command(commands=['help']))

        # Use F.text to handle all text messages that are not commands
        self.dp.message.register(
            lambda message: handle_question(message, self.bot, self.assistant),
            ~Command(commands=['start', 'help']) & F.text
        )

    async def start(self):
        """
        Start the bot
        """
        logging.basicConfig(level=logging.INFO)

        try:
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logging.error(f"Bot error: {e}")
        finally:
            await self.bot.session.close()