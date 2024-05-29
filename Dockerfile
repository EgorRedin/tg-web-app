FROM python:3.12

WORKDIR /app

COPY db_create.py .
COPY requirements.txt .
COPY  database_init.py models.py config.py queries.py .env  bot.py bot_web.py ./
COPY main.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD python db_create.py && python bot.py && python main.py