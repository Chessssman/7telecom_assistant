from aiogram import Bot, types
from aiogram.filters import Command
from config import CLOUD_LINK


async def start_command(message: types.Message, bot: Bot):
    """
    Handle /start command
    """
    await message.answer(
        "Hello! I'm a document assistant bot. "
        "Ask me questions about the documents in my directory."
    )


async def help_command(message: types.Message, bot: Bot):
    """
    Handle /help command
    """
    await message.answer(
        "Usage:\n"
        "- Ask a question about the documents\n"
        "- If no answer is found, I'll provide a cloud link"
    )


async def handle_question(message: types.Message, bot: Bot, assistant):
    """
    Handle user questions and find best document match
    """
    query = message.text

    # Find best matching document
    answer = assistant.find_best_answer(query)

    if answer:
        # Truncate answer if too long for Telegram
        if len(answer) > 4000:
            answer = answer[:4000] + '...'
        await message.answer(answer)
    else:
        # No answer found, send cloud link
        await message.answer(f"I couldn't find an answer in the documents. Check: {CLOUD_LINK}")