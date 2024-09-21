FROM python:3.12-slim
WORKDIR /app
COPY src/streamlit-app/requirements.txt .
RUN pip install -r requirements.txt
COPY .env .
COPY . .
ENV PYTHONPATH "${PYTHONPATH}:${PWD}"
CMD ["streamlit", "run", "src/streamlit-app/app.py"]
