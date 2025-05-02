from datetime import datetime
from zoneinfo import ZoneInfo

from freezegun import freeze_time

from irm_kmi_api.data import CurrentWeatherData, IrmKmiRadarForecast, Forecast, IrmKmiForecast
from tests.conftest import get_api_with_data
from tests.const import ATTR_CONDITION_PARTLYCLOUDY, ATTR_CONDITION_CLOUDY, ATTR_CONDITION_RAINY

pytest_plugins = ('pytest_asyncio',)



@freeze_time(datetime.fromisoformat('2024-01-12T07:10:00+00:00'))
async def test_warning_data() -> None:
    api = get_api_with_data("be_forecast_warning.json")

    result = api.get_warnings(lang='en')

    assert isinstance(result, list)
    assert len(result) == 2

    first = result[0]
    assert first.get('starts_at').replace(tzinfo=None) < datetime.now()
    assert first.get('ends_at').replace(tzinfo=None) > datetime.now()

    assert first.get('slug') == 'fog'
    assert first.get('friendly_name') == 'Fog'
    assert first.get('id') == 7
    assert first.get('level') == 1


@freeze_time(datetime.fromisoformat('2023-12-26T17:30:00+00:00'))
async def test_current_weather_be() -> None:
    api = get_api_with_data("forecast.json")
    tz = ZoneInfo("Europe/Brussels")
    result = await api.get_current_weather(tz)

    expected = CurrentWeatherData(
        condition=ATTR_CONDITION_CLOUDY,
        temperature=7,
        wind_speed=5,
        wind_gust_speed=None,
        wind_bearing=248,
        pressure=1020,
        uv_index=.7
    )

    assert result == expected


@freeze_time(datetime.fromisoformat("2023-12-28T15:30:00"))
async def test_current_weather_nl() -> None:
    api = get_api_with_data("forecast_nl.json")
    tz = ZoneInfo("Europe/Brussels")
    result = await api.get_current_weather(tz)

    expected = CurrentWeatherData(
        condition=ATTR_CONDITION_CLOUDY,
        temperature=11,
        wind_speed=40,
        wind_gust_speed=None,
        wind_bearing=225,
        pressure=1008,
        uv_index=1
    )

    assert expected == result


@freeze_time(datetime.fromisoformat('2023-12-26T18:30:00+01:00'))
async def test_daily_forecast() -> None:
    api = get_api_with_data("forecast.json")
    tz = ZoneInfo("Europe/Brussels")

    result = await api.get_daily_forecast(tz, 'fr')

    assert isinstance(result, list)
    assert len(result) == 8
    assert result[0]['datetime'] == '2023-12-26'
    assert not result[0]['is_daytime']
    expected = IrmKmiForecast(
        datetime='2023-12-27',
        condition=ATTR_CONDITION_PARTLYCLOUDY,
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


@freeze_time(datetime.fromisoformat('2023-12-26T18:30:00+01:00'))
async def test_hourly_forecast() -> None:
    api = get_api_with_data("forecast.json")
    tz = ZoneInfo("Europe/Brussels")
    result = await api.get_hourly_forecast(tz)

    assert isinstance(result, list)
    assert len(result) == 49

    expected = Forecast(
        datetime='2023-12-27T02:00:00+01:00',
        condition=ATTR_CONDITION_RAINY,
        native_precipitation=.98,
        native_temperature=8,
        native_templow=None,
        native_wind_gust_speed=None,
        native_wind_speed=15,
        precipitation_probability=70,
        wind_bearing=180,
        native_pressure=1020,
        is_daytime=False
    )

    assert result[8] == expected


@freeze_time(datetime.fromisoformat('2024-05-31T01:50:00+02:00'))
async def test_hourly_forecast_bis() -> None:
    api = get_api_with_data("no-midnight-bug-31-05-2024T01-55.json")
    tz = ZoneInfo("Europe/Brussels")

    result = await api.get_hourly_forecast(tz)

    assert isinstance(result, list)

    times = ['2024-05-31T01:00:00+02:00', '2024-05-31T02:00:00+02:00', '2024-05-31T03:00:00+02:00',
             '2024-05-31T04:00:00+02:00', '2024-05-31T05:00:00+02:00', '2024-05-31T06:00:00+02:00',
             '2024-05-31T07:00:00+02:00', '2024-05-31T08:00:00+02:00', '2024-05-31T09:00:00+02:00']

    actual = [f['datetime'] for f in result[:9]]

    assert actual == times


@freeze_time(datetime.fromisoformat('2024-05-31T00:10:00+02:00'))
async def test_hourly_forecast_midnight_bug() -> None:
    # Related to https://github.com/jdejaegh/irm-kmi-ha/issues/38
    api = get_api_with_data("midnight-bug-31-05-2024T00-13.json")
    tz = ZoneInfo("Europe/Brussels")

    result = await api.get_hourly_forecast(tz)

    assert isinstance(result, list)

    first = Forecast(
        datetime='2024-05-31T00:00:00+02:00',
        condition=ATTR_CONDITION_CLOUDY,
        native_precipitation=0,
        native_temperature=14,
        native_templow=None,
        native_wind_gust_speed=None,
        native_wind_speed=10,
        precipitation_probability=0,
        wind_bearing=293,
        native_pressure=1010,
        is_daytime=False
    )

    assert result[0] == first

    times = ['2024-05-31T00:00:00+02:00', '2024-05-31T01:00:00+02:00', '2024-05-31T02:00:00+02:00',
             '2024-05-31T03:00:00+02:00', '2024-05-31T04:00:00+02:00', '2024-05-31T05:00:00+02:00',
             '2024-05-31T06:00:00+02:00', '2024-05-31T07:00:00+02:00', '2024-05-31T08:00:00+02:00']

    actual = [f['datetime'] for f in result[:9]]

    assert actual == times

    assert result[24]['datetime'] == '2024-06-01T00:00:00+02:00'


@freeze_time(datetime.fromisoformat('2024-05-31T00:10:00+02:00'))
async def test_daily_forecast_midnight_bug() -> None:
    api = get_api_with_data("midnight-bug-31-05-2024T00-13.json")
    tz = ZoneInfo("Europe/Brussels")

    result = await api.get_daily_forecast(tz, 'en')

    assert result[0]['datetime'] == '2024-05-31'
    assert not result[0]['is_daytime']

    assert result[1]['datetime'] == '2024-05-31'
    assert result[1]['is_daytime']

    assert result[2]['datetime'] == '2024-06-01'
    assert result[2]['is_daytime']

    assert result[3]['datetime'] == '2024-06-02'
    assert result[3]['is_daytime']


def test_radar_forecast() -> None:
    api = get_api_with_data("forecast.json")
    result = api.get_radar_forecast()

    expected = [
        IrmKmiRadarForecast(datetime="2023-12-26T17:00:00+01:00", native_precipitation=0, might_rain=False,
                            rain_forecast_max=0, rain_forecast_min=0, unit='mm/10min'),
        IrmKmiRadarForecast(datetime="2023-12-26T17:10:00+01:00", native_precipitation=0, might_rain=False,
                            rain_forecast_max=0, rain_forecast_min=0, unit='mm/10min'),
        IrmKmiRadarForecast(datetime="2023-12-26T17:20:00+01:00", native_precipitation=0, might_rain=False,
                            rain_forecast_max=0, rain_forecast_min=0, unit='mm/10min'),
        IrmKmiRadarForecast(datetime="2023-12-26T17:30:00+01:00", native_precipitation=0, might_rain=False,
                            rain_forecast_max=0, rain_forecast_min=0, unit='mm/10min'),
        IrmKmiRadarForecast(datetime="2023-12-26T17:40:00+01:00", native_precipitation=0.1, might_rain=False,
                            rain_forecast_max=0, rain_forecast_min=0, unit='mm/10min'),
        IrmKmiRadarForecast(datetime="2023-12-26T17:50:00+01:00", native_precipitation=0.01, might_rain=False,
                            rain_forecast_max=0, rain_forecast_min=0, unit='mm/10min'),
        IrmKmiRadarForecast(datetime="2023-12-26T18:00:00+01:00", native_precipitation=0.12, might_rain=False,
                            rain_forecast_max=0, rain_forecast_min=0, unit='mm/10min'),
        IrmKmiRadarForecast(datetime="2023-12-26T18:10:00+01:00", native_precipitation=1.2, might_rain=False,
                            rain_forecast_max=0, rain_forecast_min=0, unit='mm/10min'),
        IrmKmiRadarForecast(datetime="2023-12-26T18:20:00+01:00", native_precipitation=2, might_rain=False,
                            rain_forecast_max=0, rain_forecast_min=0, unit='mm/10min'),
        IrmKmiRadarForecast(datetime="2023-12-26T18:30:00+01:00", native_precipitation=0, might_rain=False,
                            rain_forecast_max=0, rain_forecast_min=0, unit='mm/10min'),
        IrmKmiRadarForecast(datetime="2023-12-26T18:40:00+01:00", native_precipitation=0, might_rain=False,
                            rain_forecast_max=0, rain_forecast_min=0, unit='mm/10min')
    ]

    assert expected == result


def test_radar_forecast_rain_interval() -> None:
    api = get_api_with_data('forecast_with_rain_on_radar.json')
    result = api.get_radar_forecast()

    _12 = IrmKmiRadarForecast(
        datetime='2024-05-30T18:00:00+02:00',
        native_precipitation=0.89,
        might_rain=True,
        rain_forecast_max=1.12,
        rain_forecast_min=0.50,
        unit='mm/10min'
    )

    _13 = IrmKmiRadarForecast(
        datetime="2024-05-30T18:10:00+02:00",
        native_precipitation=0.83,
        might_rain=True,
        rain_forecast_max=1.09,
        rain_forecast_min=0.64,
        unit='mm/10min'
    )

    assert result[12] == _12
    assert result[13] == _13


@freeze_time("2024-06-09T13:40:00+00:00")
async def test_datetime_daily_forecast_nl() -> None:
    api = get_api_with_data("forecast_ams_no_ww.json")
    tz = ZoneInfo("Europe/Brussels")

    result = await api.get_daily_forecast(tz, 'en')

    assert result[0]['datetime'] == '2024-06-09'
    assert result[0]['is_daytime']

    assert result[1]['datetime'] == '2024-06-10'
    assert not result[1]['is_daytime']

    assert result[2]['datetime'] == '2024-06-10'
    assert result[2]['is_daytime']


@freeze_time("2024-06-09T13:40:00+00:00")
async def test_current_condition_forecast_nl() -> None:
    api = get_api_with_data("forecast_ams_no_ww.json")
    tz = ZoneInfo("Europe/Brussels")

    result = await api.get_current_weather(tz)

    expected = CurrentWeatherData(
        condition=ATTR_CONDITION_PARTLYCLOUDY,
        temperature=15,
        wind_speed=26,
        wind_gust_speed=None,
        wind_bearing=270,
        pressure=1010,
        uv_index=6
    )
    assert result == expected


@freeze_time("2024-06-09T13:40:00+00:00")
async def test_sunrise_sunset_nl() -> None:
    api = get_api_with_data("forecast_ams_no_ww.json")
    tz = ZoneInfo("Europe/Brussels")

    result = await api.get_daily_forecast(tz, 'en')

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

    result = await api.get_daily_forecast(tz, 'en')

    assert result[1]['sunrise'] == '2023-12-27T08:44:00+01:00'
    assert result[1]['sunset'] == '2023-12-27T16:43:00+01:00'

    assert result[2]['sunrise'] == '2023-12-28T08:45:00+01:00'
    assert result[2]['sunset'] == '2023-12-28T16:43:00+01:00'
