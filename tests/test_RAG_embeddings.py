import asyncio
import requests
import os
from dataclasses import dataclass
from typing import List, Dict, Any
from openai import AsyncOpenAI
import json

#hugging face embedding model setup

hf_token = os.environ["HF_API_KEY"]
model_id = "sentence-transformers/all-MiniLM-L6-v2"
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}

#get the embedding for the chunk

async def get_embedding(chunk: str) -> List[float]:
    response = requests.post(api_url, headers=headers, json={"inputs": chunk, "options":{"wait_for_model":True}})
    print(response.json())

asyncio.run(get_embedding("What is the Marius?"))

