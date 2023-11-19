from openai import OpenAI
import os
from dotenv import load_dotenv
import ast


def predict_using_gpt(keywords: list[str], n: int, data: list[dict]) -> list[str]:
    try:
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You should behave like a similarity and search database in the advertisement field that understand the context of the input passed.",
                },
                {
                    "role": "user",
                    "content": f"From this json data {data} that I provide to you, find {n} entries that is having the Keywords \
                         field same or similar to these keywords: {keywords}. If there is no match also you should return at least {n} entries.\
                         Please Return those entries as a list of values. Please do not return any other text. \
                         The output should be comma seperated values. There should not be any other messages.",
                },
            ],
        )

        result = ast.literal_eval(response.choices[0].message.content)
        # print(result)

    except Exception as e:
        print(f"Exception occured!\n {e}")
        return
    return result


# print(predict_using_gpt(
#     [
#         "posts",
#         "https",
#         "freejobalert",
#         "latest-notifications",
#         "details",
#         "freejobalert.com",
#         "Human Resource",
#     ],
#     2,
#     [
#         {
#             "Url": "https://images.indianexpress.com/2022/09/Amazon-Flipkart-sale.jpg",
#             "Keywords": [
#                 "Great Indian Festival",
#                 "Starts 23rd Sep",
#                 "Samsung Galaxy M",
#                 "iQOO",
#                 "The Big Billion Days",
#                 "23rd - 30th Sep",
#                 "NOISE",
#                 "Flipkart Axis Bank Credit Card",
#                 "8% Off + 5% Cash Back",
#                 "Flipkart Pay Later",
#                 "Instant Credit",
#                 "Easy EMIs",
#                 "ICICI Bank",
#                 "10% Instant Discount",
#                 "ASUS",
#                 "POCO",
#                 "shopping",
#                 "sale event",
#                 "festival",
#                 "e-commerce",
#                 "online retail",
#                 "consumer electronics",
#                 "finance offers",
#                 "discounts",
#                 "Indian market",
#                 "promotions",
#                 "audience: shoppers",
#                 "consumers",
#             ],
#             "Id": 3456,
#         },
#         {
#             "Url": "https://www.geeksforgeeks.org/convert-class-object-to-json-in-python/",
#             "Keywords": ["kill", "mouth"],
#             "Id": 34,
#         },
#     ],
# ))
