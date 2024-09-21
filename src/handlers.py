
from src.bot import bot
from src.settings import (
    WELCOME_MESSAGE,
)
from src.filters import should_process_message, should_process_reaction
from src.processors import process_message, process_reaction
from src.telegram_utils import (
    send_telegram_message,
)


def handle_welcome(message):
    """Send welcome message for /start and /help commands."""
    send_telegram_message(
        bot,
        message.chat.id,
        WELCOME_MESSAGE,
        reply_to_message_id=message.id,
    )


def handle_message(message):
    """Handle incoming messages."""
    if should_process_message(message):
        process_message(message)


def handle_reaction(message):
    """Handle reactions to messages."""
    if should_process_reaction(message):
        process_reaction(message)
