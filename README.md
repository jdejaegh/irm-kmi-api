# Async API to retrieve data from the Belgian IRM KMI in Python

The package exposes the data from the [mobile application of the Belgian IRM KMI](https://www.meteo.be/en/info/faq/products-services/the-rmi-weather-app) as a Python module. 

See more information in the wiki: https://github.com/jdejaegh/irm-kmi-api/wiki

## Quick start example

```python
import aiohttp
import asyncio
from zoneinfo import ZoneInfo
from irm_kmi_api import IrmKmiApiClientHa

async def print_weather():
    session = aiohttp.ClientSession()
    client = IrmKmiApiClientHa(session=session, user_agent="jdejaegh/irm-kmi-api README example")
    await client.refresh_forecasts_coord({'lat': 50.47, 'long': 4.87})
    await session.close()

    weather = client.get_current_weather(tz=ZoneInfo('Europe/Brussels'))
    city = client.get_city()

    print(f"{weather['temperature']}°C with wind of {weather['wind_speed']} km/h in {city}")


if __name__ == '__main__':
    asyncio.run(print_weather())
```


## Features

The package provides the following:  
1. Current weather
2. Hourly and daily forecast
3. Rain radar forecast and animation
4. Warning data (for extreme weather condition such as storm, thunder, floods)
5. Pollen data

<details>
<summary>Screenshots of the rain radar animation</summary>
<img src="https://github.com/jdejaegh/irm-kmi-api/raw/main/img/camera_light.png"/>  <br>
<img src="https://github.com/jdejaegh/irm-kmi-api/raw/main/img/camera_dark.png"/>  <br>
<img src="https://github.com/jdejaegh/irm-kmi-api/raw/main/img/camera_sat.png"/>  
</details>

## Limitations

The package does not provide the 14-days forcast as in the application.  

This package will not implement any feature that is not available via the API (e.g., humidity and dew point data is not
provided by the API and thus is not available in this package).


## Usage considerations

The API is not publicly documented and has been reversed engineered: it can change at any time without notice and break this package.  

Be mindful when using the API: put a meaningful User-Agent string when creating an `IrmKmiApiClient` and apply rate-limiting for your queries.


## Contributions

Contributions are welcome.  Please discuss major changes in an issue before submitting a pull request.



## Disclaimer

This is a personal project and isn't in any way affiliated with, sponsored or endorsed by [The Royal Meteorological 
Institute of Belgium](https://www.meteo.be).

All product names, trademarks and registered trademarks in (the images in) this repository, are property of their 
respective owners. All images in this repository are used by the project for identification purposes only.
