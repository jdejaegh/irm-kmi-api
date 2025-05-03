import json
import time
from datetime import datetime as dt, timedelta
from unittest.mock import AsyncMock, MagicMock
from zoneinfo import ZoneInfo

import freezegun
import pytest

from irm_kmi_api.api import IrmKmiApiClient, IrmKmiApiClientHa
from irm_kmi_api.data import CurrentWeatherData
from irm_kmi_api.pollen import PollenParser


@freezegun.freeze_time(dt.fromisoformat('2025-05-03T17:30:00+00:00'))
async def test_get_forecast_coord_api_called() -> None:
    api = IrmKmiApiClient(session=MagicMock(), user_agent="test-user-agent")
    mocked_response = b"""
    {
    "cityName": "Floreffe",
    "country": "BE",
    "obs": {
        "temp": -2,
        "timestamp": "2024-01-12T10:10:00+01:00",
        "ww": 27,
        "dayNight": "d"
    },
    "other": "things"
    }
    """

    api._api_wrapper = AsyncMock(return_value=mocked_response)

    result = await api.get_forecasts_coord({'lat': 12.123456789123456, 'long': 42})

    assert result == json.loads(mocked_response)
    params = {'s': 'getForecasts', 'k': '17ab82306446289383960bb13b3dcee4', 'lat': 12.123457, 'long': 42}
    api._api_wrapper.assert_called_once_with(params=params)
    api._api_wrapper.assert_awaited_once_with(params=params)


async def test_get_svg_api_called() -> None:
    api = IrmKmiApiClient(session=MagicMock(), user_agent="test-user-agent")
    mocked_response = b"""<svg>HEY</svg"""

    api._api_wrapper = AsyncMock(return_value=mocked_response)

    url = "my://best-url"
    result = await api.get_svg(url=url)

    assert result == mocked_response.decode()
    api._api_wrapper.assert_called_once_with(params={}, base_url=url)
    api._api_wrapper.assert_awaited_once_with(params={}, base_url=url)


async def test_get_image_api_called() -> None:
    api = IrmKmiApiClient(session=MagicMock(), user_agent="test-user-agent")
    mocked_response = b"""//PNG-data-here"""

    api._api_wrapper = AsyncMock(return_value=mocked_response)

    url = "my://best-url"
    result = await api.get_image(url=url)

    assert result == mocked_response
    api._api_wrapper.assert_called_once_with(params={}, base_url=url)
    api._api_wrapper.assert_awaited_once_with(params={}, base_url=url)


def test_expire_cache_clears_items() -> None:
    api = IrmKmiApiClient(session=MagicMock(), user_agent="test-user-agent")
    assert api.cache_max_age == 60 * 60 * 2

    api.cache = {
        'first-url': {
            'timestamp': time.time() - timedelta(hours=3).seconds,
            'response': 'wowo',
            'etag': 'etag-1'
        },
        'second-url': {
            'timestamp': time.time() - timedelta(hours=1).seconds,
            'response': 'wowo',
            'etag': 'etag-2'
        }
    }

    assert len(api.cache) == 2

    api.expire_cache()

    assert len(api.cache) == 1
    assert 'second-url' in api.cache


async def test_api_wrapper_puts_response_in_cache() -> None:
    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.status = 200
    response.read = AsyncMock(return_value=b"response value")
    response.headers = {'ETag': 'test-etag'}

    session = MagicMock()
    session.request = AsyncMock(return_value=response)

    api = IrmKmiApiClient(session=session, user_agent="test-user-agent")

    r = await api._api_wrapper(params={}, base_url='test-url')

    assert r == b"response value"
    assert len(api.cache) == 1
    assert 'test-url' in api.cache

    session.request.assert_awaited_once_with(
        method='get', url='test-url', headers={'User-Agent': 'test-user-agent'}, json=None, params={}
    )


async def test_api_wrapper_gets_response_from_cache() -> None:
    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.status = 304
    response.read = AsyncMock(side_effect=AssertionError("Should not read the response"))
    response.headers = {'ETag': 'test-etag'}

    session = MagicMock()
    session.request = AsyncMock(return_value=response)

    api = IrmKmiApiClient(session=session, user_agent="test-user-agent")
    api.cache = {
        'test-url': {
            'timestamp': time.time(),
            'response': b"response value",
            'etag': 'test-etag'
        }
    }

    r = await api._api_wrapper(params={}, base_url='test-url')

    assert r == b"response value"
    assert len(api.cache) == 1
    assert 'test-url' in api.cache

    session.request.assert_awaited_once_with(
        method='get',
        url='test-url',
        headers={'User-Agent': 'test-user-agent', 'If-None-Match': 'test-etag'},
        json=None,
        params={}
    )


async def test_default_value_when_empty_data() -> None:
    api = IrmKmiApiClientHa(session=MagicMock(), user_agent='hey', cdt_map={})
    tz = ZoneInfo('Europe/Brussels')
    lang = 'en'

    assert api.get_city() is None

    assert api.get_country() is None

    assert api.get_current_weather(tz) == CurrentWeatherData(
        condition=None,
        temperature=None,
        wind_speed=None,
        wind_gust_speed=None,
        wind_bearing=None,
        pressure=None,
        uv_index=None
    )

    assert api._get_uv_index() is None

    assert api._get_now_hourly(tz) is None

    assert api.get_daily_forecast(tz, lang) == []

    assert api.get_hourly_forecast(tz) == []

    assert api.get_radar_forecast() == []

    with pytest.raises(ValueError):
        api.get_animation_data(tz, lang, 'style', True)

    assert api.get_warnings(lang) == []

    assert await api.get_pollen() == PollenParser.get_default_data()


