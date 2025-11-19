import os
import json
import logging
from openai import OpenAI

class ApiHandler:
    def __init__(self):
        logging.getLogger(__name__).init("ApiHandler initialized")
        self.ai_prompt_assist = "### Dla podanej wcześniej kwerendy ustal priorytety pól danych które najbardziej jej odpowiadają i zwróć tylko jeden obiekt wszystkich pól razem z ich priorytetami - wyższy priorytet znaczy lepsze dopasowanie, jedyny tekst jaki masz wysłać to te pola i priorytet w formacie json, nie pisz nic innego poza rezultatem w formacie json, twoja wiadomość musi składać się tylko ze znaków które można zparsować na JSON, utrzymaj konsekwentnie następujący format: {\"propertyName\": priorityValue, \"propertyName\": priorityValue} - odpowiedź musi zawrzeć się tylko w jednym obiekcie, dane podane są poniżej: ###\n"

    def send_request(self, query, db, api_provider, model):
        response = None
        if api_provider == "huggingface":
            response = self.huggingface_request(query, db, model)
        else:
            raise ValueError("Wrong API provider specified, please verify")

        return response


    def huggingface_request(self, query, db, model):
        logging.getLogger(__name__).info("Sending request to HuggingFace API")
        logging.getLogger(__name__).info(f"Model: {model}")

        with open(f'{os.environ["AI_API_KEYS"]}', 'r') as f:
            api_keys = json.load(f)

        #find huggingface key by id
        hf_key = next((item['key'] for item in api_keys if item['id'] == 'huggingface2'), None)

        if hf_key is None:
            raise ValueError("Huggingface API key not found or is null in api keys .json")

        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=hf_key,
        )

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f"{query}" + self.ai_prompt_assist + str(db)
                }
            ],
        )

        logging.getLogger(__name__).info("Response received")
        return completion

        
