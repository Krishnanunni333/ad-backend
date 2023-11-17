import pymysql
from fastapi import FastAPI
from model import CurrencyPredictionRequest, CurrencyPredictionResponse
from sqlalchemy import create_engine
from sqlalchemy import text
import os 
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title='Currency Prediction API',)

user = os.getenv('user')
password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')
database = os.getenv('database')


def establish_connection():
    engine = create_engine(
        url=f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
    return engine

@app.get("/")
async def root():
    docs_path = 'http://127.0.0.1:8000/docs'
    return f"Hello welcome to the Currency Forecast API. Visit {docs_path} to try out."


@app.post("/predict")
async def predictions(request_text: CurrencyPredictionRequest):
    try:
        engine = establish_connection()
        with engine.connect() as eng:
            query = f"SELECT Date,SGD, SGD_explain FROM mindsdb.currency_predictor WHERE Date = '{request_text.Date}'"
            result = eng.execute(text(query))
            for row in result:
                res = CurrencyPredictionResponse()
                res.Date = request_text.Date
                res.message = f'Request processed successfully.'
                res.currency = row[1]
                res.status_code = 200
                res.details = row[2]
                return res
    except Exception as e:
        print("Couldn't connect to the database:\n", e)
