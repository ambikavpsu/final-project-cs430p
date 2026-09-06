FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p db_data

COPY server.py .

COPY ./db_data/entries.db ./db_data/entries.db

EXPOSE 8080

CMD ["python", "server.py", "http"]
