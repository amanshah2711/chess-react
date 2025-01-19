FROM python:3.9.7-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt && npm install

EXPOSE 5000

CMD [ "python", "/app/server.py" ]