import asyncio
from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ChatAction
from aiogram.filters import CommandStart
from utils.llm_config import chain
from bot_settings import logger, selected_clients
from utils.create_history import log_dialog
from zoneinfo import ZoneInfo

start_router = Router()

@start_router.message(CommandStart())
async def start_command(msg: Message):
    await msg.answer("Здравствуйте!\n Для начала работы выберите клиента командой /client")
    
@start_router.message(lambda msg: not msg.text.startswith("/"))
async def handle_all_messages(msg: Message):
    user_id = msg.from_user.id
    user_input = msg.text
    msg_timestamp = msg.date.astimezone(ZoneInfo("Europe/Moscow")) 
    
    client = selected_clients.get(user_id)
    if not client:
        await msg.reply("Сначала выберите клиента командой /client")
        return

    crm_info = (
        f"Имя: {client['name']}, "
        f"Цена: {client['price']} долларов, "
        f"Прошлая покупка: {client['past_purchase']}, "
        f"Статус: {client['deal_status']}"
    )
    
    try:
        await msg.bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await asyncio.sleep(1.5)
        
        response = await chain.ainvoke(
            {"crm_json": crm_info, "user_input": user_input},
            config={"configurable": {"session_id": client['id']}}
        )
        log_dialog(client['id'], client['name'], msg_timestamp, user_input, response)
        await msg.reply(response)

    except Exception as e:
        logger.error(f"Ошибка генерации ответа: {e}")
        await msg.reply("Произошла ошибка. Попробуйте позже.")