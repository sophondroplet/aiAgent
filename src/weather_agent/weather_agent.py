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

from weather_codes import code_lookup

#logfire stuff 
logfire.configure(send_to_logfire = os.getenv("LOGFIRE_TOKEN"))

#define model dependecies & final output cconstraints 
@dataclass
class Deps:
    client: AsyncClient
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
    returns lat long coordinates of a specified loaction
    args:
        ctx: The context.
        location_description: A description of a location.
    """
    # if ctx.deps.latlong_key is None:
    #     return {"lat":-121.173649, "long":35.861967}    
    
    params = {
        'q': location,
        'api_key': ctx.deps.latlong_key
    }


    # with logfire.span('calling geocode API', params=params) as span:
    #     r = await ctx.deps.client.get('https://geocode.maps.co/search', params=params)
    #     r.raise_for_status()
    #     data = r.json()
    #     span.set_attribute('response', data)

    r = await ctx.deps.client.get('https://geocode.maps.co/search', params=params)
    data = r.json()

    return {'lat': data[0]['lat'], 'long': data[0]['lon']} 
 
@weather_agent.tool
async def get_weather (ctx:RunContext[Deps], lat:float, long:float) -> dict [str, Any]:
    """reaturns weather of the locations given its lat long coordinates
    
    """
    if ctx.deps.weather_key is None:
        # if no API key is provided, return a dummy response
        return {'temperature': '21 °C', 'description': 'Sunny'}
    
    #make request throguh the geogrphy api using the weather keys, store response andd add them to context
    params = {
        'apikey': ctx.deps.weather_key,
        'location': f'{lat},{long}',
        'units': 'metric',
    }

    raw_data = await ctx.deps.client.get('https://api.tomorrow.io/v4/weather/realtime', params = params)   
    data = raw_data.json()
    values = data['data']['values']
    return {
        'temperature': f'{values["temperatureApparent"]:0.0f}°C',
        'description': code_lookup.get(values['weatherCode'], 'Unknown'),
    }

async def main():
    latkey = os.getenv("GEOLOC_API_KEY")
    weatherkey = os.getenv("WEATHER_API_KEY")
    user_input = input("ask about the weather in some location")
    result = await weather_agent.run(user_input, deps = Deps(client = AsyncClient(), latlong_key = latkey, weather_key = weatherkey))
    print(result.data)

if __name__ == "__main__":
    asyncio.run(main())