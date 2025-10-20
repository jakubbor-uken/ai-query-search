import json
from openai import OpenAI

#read API key
with open('api_keys.json', 'r') as f:
    api_keys = json.load(f)

#find huggingface key by id
hf_key = next((item['key'] for item in api_keys if item['id'] == 'huggingface'), None)

if hf_key is None:
    raise ValueError("Huggingface API key not found or is null in api_keys.json")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=hf_key,
)

completion = client.chat.completions.create(
    model="moonshotai/Kimi-K2-Instruct-0905",
    messages=[
        {
            "role": "user",
            "content": "Write a short story about a robot learning to love."
        }
    ],
)

print(completion.choices[0].message)