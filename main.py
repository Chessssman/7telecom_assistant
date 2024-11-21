import asyncio
from bot import TelegramDocumentBot

async def main():
    bot = TelegramDocumentBot()
    await bot.start()

if __name__ == '__main__':
    asyncio.run(main())