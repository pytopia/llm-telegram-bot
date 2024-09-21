import telebot
from bot import BOT_USERNAME, bot

from src.db import UserDatabase


class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    # Class will check whether the user is admin or creator in group or not
    key = "is_chat_admin"

    @staticmethod
    def check(message: telebot.types.Message):
        from_user = message.user if isinstance(message, telebot.types.MessageReactionUpdated) else message.from_user
        return bot.get_chat_member(message.chat.id, from_user.id).status in ["administrator", "creator"]


def is_bot_mentioned(message, bot_username):
    """Check if the bot is mentioned in the message."""
    if not message.entities:
        return False

    for entity in message.entities:
        if entity.type == "mention":
            mentioned_user = message.text[entity.offset : entity.offset + entity.length]
            if mentioned_user == f"@{bot_username}":
                return True
    return False


def is_message_from_authorized_user(message):
    from_user = message.user if isinstance(message, telebot.types.MessageReactionUpdated) else message.from_user
    username = from_user.username.lower()
    with UserDatabase() as db:
        return db.is_user_authorized(username) and not db.is_rate_limited(username)


def is_message_reply_to_message(message):
    return message.reply_to_message is not None


def is_actionable_message(message):
    conditions = [
        is_bot_mentioned(message, BOT_USERNAME),
        is_message_reply_to_message(message),
        is_message_from_authorized_user(message),
    ]

    return all(conditions)


def is_actionable_reaction(message):
    conditions = [
        is_message_from_authorized_user(message),
    ]
    return all(conditions)
