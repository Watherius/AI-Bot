import asyncio
from bot_settings import bot, dp
from handlers.start import start_router
from handlers.client import client_router

async def main():
  dp.include_router(start_router) 
  dp.include_router(client_router) 
  await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")