from openai import OpenAI

# Point the OpenAI client to Ollama's server
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="arbitrary placeholder"  # (arbitrary placeholder)
)

response = client.chat.completions.create(
    model="deepseek-r1:1.5b",  # Your local Ollama model name
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
