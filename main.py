import os
from openai import AzureOpenAI

inital_prompt = input("say something: ")

messages = []

client = AzureOpenAI(
  api_version = "2024-07-01-preview",
  api_key = os.getenv("AZUREOPENAI_API_KEY"),
  azure_endpoint= "https://deepseektestin0528333273.openai.azure.com/"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": inital_prompt},
  ],
)

print(completion.choices[0].message.content)



