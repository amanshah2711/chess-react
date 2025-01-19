FROM python:3.9.7-slim

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
    && apt-get update && apt-get install -y yarn \
    && apt-get clean

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt 

RUN yarn install

EXPOSE 5000

CMD [ "python", "/app/server.py" ]