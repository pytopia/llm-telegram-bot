# Telegram Bot with User Management Dashboard

This project consists of a Telegram bot with an accompanying Streamlit dashboard for user management.

## Features

- Telegram bot with AI-powered responses
- User authorization and rate limiting
- Admin dashboard for user management
- Docker containerization for easy deployment

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in the required values
3. Build and run the Docker containers:

```bash
docker-compose up --build
```

## Components

### Telegram Bot

- Located in `src/telegram-bot/`
- Handles message processing and AI responses
- Uses OpenAI's API for generating responses

### Streamlit Dashboard

- Located in `src/streamlit-app/`
- Provides an interface for managing bot users
- Accessible at `http://localhost:8501`

### Database

- SQLite database for storing user information
- Managed through `src/db.py`

## Usage

- Interact with the bot on Telegram
- Access the admin dashboard to manage users

## Development

To run the project locally without Docker:

1. Install requirements for both the bot and dashboard
2. Run the bot: `python src/telegram-bot/app.py`
3. Run the dashboard: `streamlit run src/streamlit-app/app.py`
