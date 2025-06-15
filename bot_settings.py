import logging
import json
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from decouple import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

selected_clients: dict[int, dict] = {}

def load_crm_data():
	with open("./config/crm_data.json", "r", encoding="utf-8") as f:
		try:
			return json.load(f)
		except json.JSONDecodeError as e:
			print(f"Error decoding JSON: {e}")
			return None
 
crm_data = load_crm_data()