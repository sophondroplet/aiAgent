from __future__ import annotations as _annotations

import asyncio
import os
from dataclasses import dataclass
from typing import Any

import logfire
from devtools import debug
from httpx import AsyncClient

from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.openai import OpenAIModel

#logfire stuff 


#define model dependecies & final output cconstraints 
@dataclass
class Deps:
    latlong_key: str
    weather_key: str

#defibe model client, agent parameters
client = OpenAIModel(
    'google/gemini-2.0-flash-lite-preview-02-05:free',
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

weather_agent = Agent(
    model = client, 
    system_prompt = (
        'Be concise, reply with one sentence.'
        'Use the `get_lat_lng` tool to get the latitude and longitude of the locations, '
        'then use the `get_weather` tool to get the weather.'
        ),
    deps_type = Deps
    )

@weather_agent.tool
async def get_lat_long (ctx:RunContext[Deps], location:str) -> dict [str,int]:
    """
    returns lat long coordinates of a specified lcaotion
    args:
        ctx: The context.
        location_description: A description of a location.
    """
    if ctx.deps.latlong_key is None:
        return {"lat":2.2323232, "long":2.232323}    

    #make request throguh the geogrphy api using the weather keys, store response andd add them to context

@weather_agent.tool
async def get_weather (ctx:RunContext[Deps], lat:float, long:float) -> str:
    """reaturns weather of the locations given its lat long coordinates
    
    """
    #make request throguh the geogrphy api using the weather keys, store response andd add them to context

    if ctx.deps.weather_key is None:
        # if no API key is provided, return a dummy response
        return {'temperature': '21 °C', 'description': 'Sunny'}



async def main():
    result = await weather_agent.run("tell me the weather in Beijing", deps=Deps(None,None))
    print(result.data)


if __name__ == "__main__":
    asyncio.run(main())