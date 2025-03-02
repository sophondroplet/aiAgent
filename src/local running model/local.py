from openai import OpenAI
import os
import time

message = []

sysprompt = input("enter system prompt: ")
message.append({"role": "system", "content": sysprompt})

client = OpenAI(
  base_url="http://localhost:11434/v1",
  api_key="arbitrary placeholder"  # (arbitrary placeholder)
)

while True:
  prompt = input("say something: ")
  message.append({"role": "system", "content": prompt})

  start_time = time.time()

  completion = client.chat.completions.create(
    model="deepseek-r1:7b",
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

