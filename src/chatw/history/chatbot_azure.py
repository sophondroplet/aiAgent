import os
from openai import AzureOpenAI
import time

message = []

sysprompt = input("enter system prompt: ")
message.append({"role": "system", "content": sysprompt})

client = AzureOpenAI(
  api_version = "2024-07-01-preview",
  api_key = os.getenv("AZUREOPENAI_API_KEY"),
  azure_endpoint= "https://deepseektestin0528333273.openai.azure.com/"
)

messages = [{"role": "system", "content": "You are a helpful assistant"}]

while True:

  prompt = input("say something: ")
  message.append({"role": "system", "content": prompt})

  start_time = time.time()

  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=message,
    stream=True
  )

  print("\nAssistant: ", end="")  # Start printing response

  full_response = ""  # Store the full response

  for chunk in completion:
      if hasattr(chunk, "choices") and chunk.choices:  # Ensure chunk has choices
          delta = chunk.choices[0].delta
          if hasattr(delta, "content") and delta.content:  # Ensure content exists
              print(delta.content, end="", flush=True)
              full_response += delta.content
      time.sleep(0.01)

  end_time = time.time()
  elpased_time = end_time - start_time

  print(f" time spent {elpased_time:.2f} seconds \n")  # Newline after response
  message.append({"role": "assistant", "content": full_response}) 



