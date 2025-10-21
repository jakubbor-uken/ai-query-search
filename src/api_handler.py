import os
import json
from openai import OpenAI

class ApiHandler:
    def __init__(self):
        print("ApiHandler initialized")
        self.ai_prompt_assist = "### Dla podanej wcześniej kwerendy ustal priorytety danych które najbardziej jej odpowiadają i zwróć je, dane podane są poniżej: ###\n"

    def send_request(self, query, db, api_provider):
        response = None
        if api_provider == "huggingface":
            response = self.huggingface_request(query, db)
        else:
            raise ValueError("Wrong API provider specified, please verify")

        return response


    def huggingface_request(self, query, db):
        print("Sending request to HuggingFace API")

        with open(f'{os.environ["AI_API_KEYS"]}', 'r') as f:
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
                    "content": f"{query}" + self.ai_prompt_assist + str(db)
                }
            ],
        )

        print("Response received")
        return completion

        
