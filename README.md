# LLM Telegram Bot

This project is a Telegram bot powered by GPT-4, designed to answer questions and provide assistance in approved chat groups.

Here is the project structure:

```
.
├── src/
│   ├── app.py
│   ├── bot.py
│   ├── config.py
│   ├── constants.py
│   ├── enums.py
│   ├── filters.py
│   ├── handlers.py
│   ├── llm.py
│   ├── processors.py
│   └── telegram_utils.py
├── .dockerignore
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
└── ruff.toml
```

## Setup and Running

1. **Environment Variables**: Copy the `.env.example` file to `.env` and fill in the required values:

```
BOT_TOKEN="your_telegram_bot_token"
APPROVED_CHATS="chat1,chat2"
OPENAI_API_KEY="your_openai_api_key"
```

2. **Install Dependencies**: Install the required packages:

```
pip install -r requirements.txt
```

3. **Run the Bot**: You can run the bot directly using Python:

```
python src/app.py
```

   Or use Docker Compose:

```
docker-compose up --build
```

## Key Components

- `src/app.py`: Main entry point of the application.
- `src/bot.py`: Initializes the Telegram bot.
- `src/llm.py`: Handles interactions with the GPT-4 model.
- `src/handlers.py`: Contains message and reaction handlers.
- `src/processors.py`: Processes messages and reactions.
- `src/filters.py`: Defines filters for message processing.
- `src/telegram_utils.py`: Utility functions for Telegram operations.

## Features

- Responds to messages when mentioned in approved chat groups.
- Processes reactions to messages.
- Uses GPT-4 to generate responses.
- Supports admin-only operations.

## Logging

Logs are stored in the `logs/` directory. The log level can be adjusted by running the bot with the `--verbose` flag:

```
python src/app.py --verbose
```

## Contributing

Feel free to submit issues or pull requests if you have suggestions for improvements or find any bugs.