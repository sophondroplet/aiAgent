import os
from openai import OpenAI
import time

message = []

sysprompt = input("enter system prompt: ")
message.append({"role": "system", "content": sysprompt})

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

messages = [{"role": "system", "content": "You are a helpful assistant"}]

while True:
    prompt = input("say something: ")
    message.append({"role": "user", "content": prompt})  # Changed from "system" to "user"

    start_time = time.time()

    completion = client.chat.completions.create(
        model="google/gemini-2.0-flash-lite-preview-02-05:free",  # Using the same model as in pydanticai_openrouter
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
    elapsed_time = end_time - start_time

    print(f"\nTime spent {elapsed_time:.2f} seconds\n")  # Newline after response
    message.append({"role": "assistant", "content": full_response}) 