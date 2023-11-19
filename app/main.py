from fastapi import FastAPI
from pyairtable import Api
import os
from dotenv import load_dotenv
from utils.extract_keywords_from_image import convert
from utils. extract_keywords_from_web import get_keywords
from utils.predict import predict_using_gpt
from utils.hasher import generate_unordered_hash

from app.models import UrlCreate,  UrlStore, HashCreate

app = FastAPI()

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_URL_TABLE_ID = os.getenv("AIRTABLE_URL_TABLE_ID")
AIRTABLE_HASH_TABLE_ID = os.getenv("AIRTABLE_HASH_TABLE_ID")


airtable_api = Api(AIRTABLE_API_KEY)


@app.get("/image-urls")
def get_all_image_urls():
    table = airtable_api.table(AIRTABLE_BASE_ID, AIRTABLE_URL_TABLE_ID)
    return table.all()

@app.post("/image-urls")
def create_image_url(url: UrlCreate):
    table = airtable_api.table(AIRTABLE_BASE_ID, AIRTABLE_URL_TABLE_ID)
    Keywords = convert(url.Url)
    print(Keywords)
    new_url = UrlStore(Url=url.Url, Keywords=Keywords)
    return table.create(new_url.__dict__, typecast=True)

@app.get("/predict")
def predict(url: str):

    keywords = get_keywords(url)
    hash_value = generate_unordered_hash(keywords)
    print(hash_value)
    filter_formula = f"{{HashValue}}='{hash_value}'"
    hash_table = airtable_api.table(AIRTABLE_BASE_ID, AIRTABLE_HASH_TABLE_ID)
    hash_value_entry = hash_table.first(formula=filter_formula)
    print(hash_value_entry)
    if hash_value_entry is None:
        url_table = airtable_api.table(AIRTABLE_BASE_ID, AIRTABLE_URL_TABLE_ID)
        all_urls = url_table.all()
        fields_values = [record['fields'] for record in all_urls]
        print(keywords)
        print(fields_values)
        result = predict_using_gpt(keywords=keywords, n=2, data=fields_values)
        final_urls = [record['Url'] for record in result]
        new_hash = HashCreate(HashValue=hash_value,Urls=final_urls)
        hash_table.create(new_hash.__dict__, typecast=True)
        print(final_urls)
        return final_urls
    return hash_value_entry["fields"]["Url"]