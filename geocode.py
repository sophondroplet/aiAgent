import asyncio
import os
from httpx import AsyncClient

async def main():

    data = ''

    params = {
        'q': "Hong Kong, Ma On Shan, the Entrance",
        'api_key': os.getenv("GEOLOG_API_KEY"),
    }

    async with AsyncClient() as client:
        data = await client.get('https://geocode.maps.co/search', params=params)
        data = data.json()

    first_location = data[0]

    lat = first_location["lat"]
    lon = first_location["lon"]
    name = first_location["display_name"]
    
    print(f"Name: {name} Lat, long: {lat}, {lon}")

asyncio.run(main())
