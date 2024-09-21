
from bot import bot
from filters import is_actionable_message, is_actionable_reaction
from processors import process_message, process_reaction
from settings import (
    WELCOME_MESSAGE,
)
from telegram_utils import (
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
    if is_actionable_message(message):
        process_message(message)


def handle_reaction(message):
    """Handle reactions to messages."""
    if is_actionable_reaction(message):
        process_reaction(message)
