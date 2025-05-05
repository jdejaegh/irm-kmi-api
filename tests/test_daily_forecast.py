from datetime import datetime
from zoneinfo import ZoneInfo

from freezegun import freeze_time

from irm_kmi_api import ConditionEvol, ExtendedForecast
from tests.conftest import get_api_with_data
from tests.const import ATTR_CONDITION_PARTLYCLOUDY


@freeze_time(datetime.fromisoformat('2023-12-26T18:30:00+01:00'))
async def test_daily_forecast() -> None:
    api = get_api_with_data("forecast.json")
    tz = ZoneInfo("Europe/Brussels")

    result = api.get_daily_forecast(tz, 'fr')

    assert isinstance(result, list)
    assert len(result) == 8
    assert result[0]['datetime'] == '2023-12-26'
    assert not result[0]['is_daytime']
    expected = ExtendedForecast(
        datetime='2023-12-27',
        condition=ATTR_CONDITION_PARTLYCLOUDY,
        condition_2=None,
        condition_evol=ConditionEvol.TWO_WAYS,
        native_precipitation=0,
        native_temperature=9,
        native_templow=4,
        native_wind_gust_speed=50,
        native_wind_speed=20,
        precipitation_probability=0,
        wind_bearing=180,
        is_daytime=True,
        text='Bar',
        sunrise="2023-12-27T08:44:00+01:00",
        sunset="2023-12-27T16:43:00+01:00"
    )

    assert result[1] == expected


@freeze_time(datetime.fromisoformat('2024-05-31T00:10:00+02:00'))
async def test_daily_forecast_midnight_bug() -> None:
    api = get_api_with_data("midnight-bug-31-05-2024T00-13.json")
    tz = ZoneInfo("Europe/Brussels")

    result = api.get_daily_forecast(tz, 'en')

    assert result[0]['datetime'] == '2024-05-31'
    assert not result[0]['is_daytime']

    assert result[1]['datetime'] == '2024-05-31'
    assert result[1]['is_daytime']

    assert result[2]['datetime'] == '2024-06-01'
    assert result[2]['is_daytime']

    assert result[3]['datetime'] == '2024-06-02'
    assert result[3]['is_daytime']


@freeze_time("2024-06-09T13:40:00+00:00")
async def test_datetime_daily_forecast_nl() -> None:
    api = get_api_with_data("forecast_ams_no_ww.json")
    tz = ZoneInfo("Europe/Brussels")

    result = api.get_daily_forecast(tz, 'en')

    assert result[0]['datetime'] == '2024-06-09'
    assert result[0]['is_daytime']

    assert result[1]['datetime'] == '2024-06-10'
    assert not result[1]['is_daytime']

    assert result[2]['datetime'] == '2024-06-10'
    assert result[2]['is_daytime']


@freeze_time("2024-06-09T13:40:00+00:00")
async def test_sunrise_sunset_nl() -> None:
    api = get_api_with_data("forecast_ams_no_ww.json")
    tz = ZoneInfo("Europe/Brussels")

    result = api.get_daily_forecast(tz, 'en')

    assert result[0]['sunrise'] == '2024-06-09T05:19:28+02:00'
    assert result[0]['sunset'] == '2024-06-09T22:01:09+02:00'

    assert result[1]['sunrise'] is None
    assert result[1]['sunset'] is None

    assert result[2]['sunrise'] == '2024-06-10T05:19:08+02:00'
    assert result[2]['sunset'] == '2024-06-10T22:01:53+02:00'


@freeze_time("2023-12-26T18:30:00+01:00")
async def test_sunrise_sunset_be() -> None:
    api = get_api_with_data("forecast.json")
    tz = ZoneInfo("Europe/Brussels")

    result = api.get_daily_forecast(tz, 'en')

    assert result[1]['sunrise'] == '2023-12-27T08:44:00+01:00'
    assert result[1]['sunset'] == '2023-12-27T16:43:00+01:00'

    assert result[2]['sunrise'] == '2023-12-28T08:45:00+01:00'
    assert result[2]['sunset'] == '2023-12-28T16:43:00+01:00'
