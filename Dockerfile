####### 👇 SIMPLE SOLUTION 👇 ########
FROM python:3.8.12-buster
WORKDIR /prod
COPY bicimad_lewagon bicimad_lewagon
COPY requirements.txt requirements.txt
COPY setup.py setup.py
COPY .env .env
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn bicimad_lewagon.api.api:app --host 0.0.0.0 --port $PORT
