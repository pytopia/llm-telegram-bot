import os

import telebot
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"), parse_mode="MARKDOWN")
BOT_USERNAME: str = bot.get_me().username
logger.info(f"Running bot with username: {BOT_USERNAME}")
