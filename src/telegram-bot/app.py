import argparse
import sys

from bot import bot
from filters import IsAdmin
from handlers import handle_message, handle_reaction, handle_welcome
from loguru import logger


def configure_logger(verbose: bool):
    log_level = "DEBUG" if verbose else "INFO"
    logger.remove()  # Remove the default handler
    logger.add(sys.stderr, level=log_level)
    logger.add("logs/bot.log", rotation="100 MB", level="DEBUG")
    logger.info(f"Log level set to {log_level} for console and DEBUG for file")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Telegram Bot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    configure_logger(args.verbose)

    logger.info("Starting the bot...")
    bot.add_custom_filter(IsAdmin())
    bot.message_handler(commands=["start", "help"])(handle_welcome)
    bot.message_handler(func=lambda message: True, is_chat_admin=True)(handle_message)
    bot.edited_message_handler(func=lambda message: True, is_chat_admin=True)(handle_message)
    bot.message_reaction_handler(func=lambda message: message.new_reaction, is_chat_admin=True)(handle_reaction)

    bot.infinity_polling(
        allowed_updates=[
            "message",
            "message_reaction",
            "edited_message",
        ],
    )
