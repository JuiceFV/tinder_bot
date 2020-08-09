FROM python:3.8

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN cat docker/docker_browser_replacement.py > /usr/local/lib/python3.8/site-packages/robobrowser/browser.py

RUN cd application && python3 entry.py -s 0
