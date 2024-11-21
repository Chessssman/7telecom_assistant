import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

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
        Register bot message handlers
        """
        # Start command handler
        self.dp.message.register(
            start_command,
            Command(commands=['start'])
        )

        # Help command handler
        self.dp.message.register(
            help_command,
            Command(commands=['help'])
        )

        # Text message handler for questions
        self.dp.message.register(
            self.process_message,
            F.text
        )

    async def process_message(self, message: Message):
        """
        Process incoming text messages
        """
        try:
            logging.info(f"Received message: {message.text}")
            await handle_question(message, self.bot, self.assistant)
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            await message.answer("Sorry, an error occurred while processing your message.")

    async def start(self):
        """
        Start the bot
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        try:
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logging.error(f"Bot error: {e}")
        finally:
            await self.bot.session.close()