FROM python:3.12-slim
WORKDIR /app
COPY src/telegram-bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY .env .
COPY . .
ENV PYTHONPATH "${PYTHONPATH}:${PWD}"
CMD ["python", "src/telegram-bot/app.py"]
