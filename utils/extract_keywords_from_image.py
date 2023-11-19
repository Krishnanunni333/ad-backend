from openai import OpenAI
import os
from dotenv import load_dotenv



def convert(url: str) -> list[str]:
    try:
        load_dotenv()
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract keywords from the image. Also extract the websites, business domian, target audience, technology if any, occasion if any, and any other information that is mentioned in the image. Specification regarding the person in the image is not needed.The output should be comma seperated values. There should not be any other messages."},
                {
                "type": "image_url",
                "image_url": {
                    "url": url,
                },
                },
            ],
            }
        ],
        max_tokens=300,
        )
        
        result = [
            item.strip()
            for item in response.choices[0].message.content.split(",")
            if item
        ]
        print(result)

    except Exception as e:
        print(f"Exception occured!\n {e}")
        return
    return result
