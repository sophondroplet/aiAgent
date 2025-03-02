import os
from openai import AsyncAzureOpenAI

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel


class MyModel(BaseModel):
    meeting_location: str
    host_name: str
    number_of_participants: int
    meeting_time: str
    meeting_date_day: int
    date_month: int


client = AsyncAzureOpenAI(
    azure_endpoint= 'https://deepseektestin0528333273.openai.azure.com/',
    api_version='2024-07-01-preview',
    api_key = os.getenv("AZUREOPENAI_API_KEY"),
)

model = OpenAIModel('gpt-4o-mini', openai_client=client)
print(f'Using model: {model}')
agent = Agent(model, result_type=MyModel)

if __name__ == '__main__':
    result = agent.run_sync('My name is lek, I am hosting meeting with nine other people. Can you schedule a meeting on the 8:30am, at the Johns cafe, on feburary 3rd')
    print(result.data)
    # print(result.usage())