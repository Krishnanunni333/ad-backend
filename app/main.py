from fastapi import FastAPI
from pyairtable import Api
import os
from dotenv import load_dotenv
from utils.extract_keywords_from_image import convert
from utils. extract_keywords_from_web import get_keywords
from utils.predict import predict_using_gpt

from app.models import EmployeeCreate, UrlCreate,  UrlStore

app = FastAPI()

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_EMPLOYEE_TABLE_ID = os.getenv("AIRTABLE_EMPLOYEE_TABLE_ID")
AIRTABLE_URL_TABLE_ID = os.getenv("AIRTABLE_URL_TABLE_ID")


airtable_api = Api(AIRTABLE_API_KEY)


@app.get("/employees")
def get_all_employees():
    table = airtable_api.table(AIRTABLE_BASE_ID, AIRTABLE_EMPLOYEE_TABLE_ID)
    return table.all()

@app.post("/employees")
def create_employee(employee: EmployeeCreate):
    table = airtable_api.table(AIRTABLE_BASE_ID, AIRTABLE_EMPLOYEE_TABLE_ID)
    return table.create(employee.__dict__)

@app.get("/image-urls")
def get_all_image_urls():
    table = airtable_api.table(AIRTABLE_BASE_ID, AIRTABLE_URL_TABLE_ID)
    return table.all()

@app.post("/image-urls")
def create_image_url(url: UrlCreate):
    table = airtable_api.table(AIRTABLE_BASE_ID, AIRTABLE_URL_TABLE_ID)
    Keywords = convert(url.Url)
    print(Keywords)
    new_url = UrlStore(Id=url.Id, Url=url.Url, Keywords=Keywords)
    return table.create(new_url.__dict__, typecast=True)

@app.get("/predict")
def predict(url: str, employee_id: int):
    emp_table = airtable_api.table(AIRTABLE_BASE_ID, AIRTABLE_EMPLOYEE_TABLE_ID)
    filter_formula = f"{{Id}}='{employee_id}'"
    employee = emp_table.first(formula=filter_formula)
    keywords = get_keywords(url)
    keywords.append(employee["fields"]["Sector"])
    url_table = airtable_api.table(AIRTABLE_BASE_ID, AIRTABLE_URL_TABLE_ID)
    all_urls = url_table.all()
    fields_values = [record['fields'] for record in all_urls]
    print(keywords)
    print(fields_values)
    result = predict_using_gpt(keywords=keywords, n=2, data=fields_values)
    # print(result)
    return [record['Url'] for  record in result]