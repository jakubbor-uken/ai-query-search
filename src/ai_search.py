import os
import json
from openai import OpenAI



class AISearch():
    def __init__(self):
        pass



    def ai_search(query):
        with open(f'{os.environ["AI_SEARCH_PATH"]}', 'r') as f:
            api_keys = json.load(f)

        #find huggingface key by id
        hf_key = next((item['key'] for item in api_keys if item['id'] == 'huggingface'), None)

        if hf_key is None:
            raise ValueError("Huggingface API key not found or is null in api keys .json")

        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=hf_key,
        )

        completion = client.chat.completions.create(
            model="moonshotai/Kimi-K2-Instruct-0905",
            messages=[
                {
                    "role": "user",
                    "content": f"{query}"
                }
            ],
        )

        print(completion.choices[0].message)








