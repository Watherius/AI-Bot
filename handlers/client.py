from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from bot_settings import crm_data, selected_clients

client_router = Router()

@client_router.message(Command('client'))
async def create_btn_client(msg: Message): 
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    buttons = []
    
    for client in crm_data:
        label = client["name"]
        btn = InlineKeyboardButton(text=label, callback_data=f"choose_client_{client['id']}")
        buttons.append(btn)
    
    for i in range(0, len(buttons), 2):
        row = buttons[i:i+2]
        keyboard.inline_keyboard.append(row)

    await msg.answer("Выберите, клиента:", reply_markup=keyboard)
    
@client_router.callback_query(F.data.startswith("choose_client_"))
async def choice_client(call: CallbackQuery):
    client_id = int(call.data.split("_")[-1])
    client = next((c for c in crm_data if int(c["id"]) == client_id), None)
    
    if client:
        selected_clients[call.from_user.id] = client
        await call.message.answer(f"Выбран клиент <b>{client['name']}</b>.\nНачните диалог с ассистентом", parse_mode="HTML")
    else:
        await call.message.answer("Не удалось найти клиента.")
    
    await call.answer()