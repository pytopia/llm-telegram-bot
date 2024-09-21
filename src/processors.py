
import emoji
from loguru import logger

from bot import BOT_USERNAME, bot
from src.settings import (
    LLM_MODEL,
    REPLY_SYSTEM_PROMPT,
    SYSTEM_PROMPT,
    WAITING_MESSAGE,
)
from src.enums import Emoji
from src.llm import call_llm
from src.telegram_utils import (
    get_message_content,
    send_telegram_message,
)


def process_message(message):
    """Process messages where the bot is mentioned."""
    reply_to_message = message.reply_to_message
    message_text = get_message_content(message.chat.id, reply_to_message.message_id)
    waiting_message = send_telegram_message(
        bot, message.chat.id, WAITING_MESSAGE, reply_to_message_id=reply_to_message.id,
    )

    reply_guideline = message.text.replace(f"@{BOT_USERNAME}", "")
    response = call_llm(
        message_text,
        LLM_MODEL,
        REPLY_SYSTEM_PROMPT.format(reply_guideline=reply_guideline),
    )

    send_llm_response(waiting_message, response)


def process_reaction(message):
    """Process reactions to messages."""
    if not hasattr(message.new_reaction[-1], "emoji"):
        return

    reaction = emoji.demojize(message.new_reaction[-1].emoji)
    logger.debug(f"Reaction: {reaction}")

    if reaction in [Emoji.HIGH_VOLTAGE.value]:
        message_text = get_message_content(message.chat.id, message.message_id)
        waiting_message = send_telegram_message(
            bot,
            message.chat.id,
            WAITING_MESSAGE,
            reply_to_message_id=message.message_id,
        )
        response = call_llm(message_text, LLM_MODEL, SYSTEM_PROMPT)

        send_llm_response(waiting_message, response)
    elif reaction in [Emoji.PILE_OF_POO.value]:
        bot.delete_message(message.chat.id, message.message_id)


def send_llm_response(message, response):
    """Send response, handling long messages with a 'Show More' button."""
    send_telegram_message(bot, message.chat.id, response, edit_message_id=message.id)
