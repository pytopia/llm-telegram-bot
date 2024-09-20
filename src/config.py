import os

APPROVED_CHATS = [chat.strip().lower() for chat in os.getenv("APPROVED_CHATS", "").split(",")]
