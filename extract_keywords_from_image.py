from openai import OpenAI
import os
from dotenv import load_dotenv



def convert(url: str) -> bool:
    try:
        load_dotenv()
        client = OpenAI(api_key=os.getenv('openai'))

        # response = client.chat.completions.create(
        # model="gpt-4-vision-preview",
        # messages=[
        #     {
        #     "role": "user",
        #     "content": [
        #         {"type": "text", "text": "Extract keywords from the image. Also extract the websites, business domian, target audience, technology if any, occasion if any, mentioned in the image. Specification regarding the person in the image is not needed.The output should be comma seperated values. There should not be any other messages."},
        #         {
        #         "type": "image_url",
        #         "image_url": {
        #             "url": url,
        #         },
        #         },
        #     ],
        #     }
        # ],
        # max_tokens=300,
        # )

        # print(response.choices[0].message.content)

    except Exception as e:
        print(f"Exception occured!\n {e}")
        return False
    return True