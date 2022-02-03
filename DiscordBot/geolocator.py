import os

from dotenv import load_dotenv
from geopy import GoogleV3
from geopy.adapters import AioHTTPAdapter
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


async def get_timezone_from_location(input_location):
    async with GoogleV3(
            api_key=GOOGLE_API_KEY,
            adapter_factory=AioHTTPAdapter,
    ) as geolocator:
        location = await geolocator.geocode(input_location)
        if location is None:
            raise LookupError("Invalid location")
        tz = await geolocator.reverse_timezone((location.latitude, location.longitude))
        return tz
