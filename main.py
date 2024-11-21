import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from config import Config
from document_processor import DocumentProcessor
from claude_assistant import ClaudeAssistant

logging.basicConfig(level=logging.INFO)


class TelegramClaudioBot:
    def __init__(self):
        self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        self.dp = Dispatcher()
        self.documents = DocumentProcessor.process_documents(Config.DOCUMENTS_DIR)
        self.claude = ClaudeAssistant(Config.CLAUDE_API_KEY)

        self._register_handlers()

    def _register_handlers(self):
        self.dp.message(CommandStart())(self.handle_start)
        self.dp.message(Command("help"))(self.handle_help)
        self.dp.message()(self.handle_query)

    async def handle_start(self, message: types.Message):
        await message.answer(
            "Welcome to Claude Document Assistant! "
            "Ask me a question about the documents in my directory."
        )

    async def handle_help(self, message: types.Message):
        await message.answer(
            "I can help you find answers in the documents. "
            "Simply ask a question, and I'll search through the available documents."
        )

    async def handle_query(self, message: types.Message):
        query = message.text
        context = ' '.join(self.documents.values())

        # Send "typing" status
        await message.chat.do('typing')

        # Generate answer
        answer = self.claude.generate_answer(query, context)

        # Check if answer is found
        if "cannot be directly found" in answer.lower():
            await message.answer(
                f"I couldn't find a precise answer in the documents. "
                f"You might want to check the full documents in: {Config.CLOUD_STORAGE_LINK}"
            )
        else:
            await message.answer(answer)

    async def start(self):
        try:
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logging.error(f"Error starting bot: {e}")


async def main():
    bot = TelegramClaudioBot()
    await bot.start()


if __name__ == '__main__':
    asyncio.run(main())