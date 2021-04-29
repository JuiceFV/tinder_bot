  
FROM python:3.8

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN python3 setup.py develop

RUN cat docker/browser_replacement.py > "$(find /usr -type f -iwholename '*/robobrowser/browser.py')"