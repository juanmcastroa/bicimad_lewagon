####### 👇 SIMPLE SOLUTION 👇 ########
FROM python:3.8.12-buster
WORKDIR /prod
COPY bicimad_lewagon bicimad_lewagon
COPY requirements.txt requirements.txt
COPY setup.py setup.py
COPY .env .env
COPY fit_OHE.pkl fit_OHE.pkl
COPY fit_standard.pkl fit_standard.pkl
COPY scripts scripts
COPY model model
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python -c 'from dotenv import load_dotenv, find_dotenv; load_dotenv(find_dotenv())'



CMD uvicorn bicimad_lewagon.api.api:app --host 0.0.0.0 --port $PORT
