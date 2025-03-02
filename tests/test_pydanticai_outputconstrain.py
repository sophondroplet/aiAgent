import os

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel

import logfire

logfire.configure(send_to_logfire = os.getenv("LOGFIRE_TOKEN"))

class MyModel(BaseModel):
    meeting_location: str
    host_name: str
    number_of_participants: int
    meeting_time: str
    meeting_date_day: int
    date_month: int

model = OpenAIModel(
    'google/gemini-2.0-flash-lite-preview-02-05:free',
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

print(f'Using model: {model}')
agent = Agent(model, result_type=MyModel)

if __name__ == '__main__':
    result = agent.run_sync('My name is lek, I am hosting meeting with nine other people. Can you schedule a meeting at 8:30am, at the Johns cafe, on February 3rd')
    print(result.data)
    # print(result.usage())

