FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/ /usr/src/app

CMD gunicorn -w 2 -b 0.0.0.0:8050 -t 100000 --max-requests 20 --reload app:server & python dashboard.py