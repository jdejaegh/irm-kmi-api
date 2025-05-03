from datetime import datetime
from zoneinfo import ZoneInfo

from freezegun import freeze_time

from irm_kmi_api.data import Forecast
from tests.conftest import get_api_with_data
from tests.const import ATTR_CONDITION_CLOUDY, ATTR_CONDITION_RAINY


@freeze_time(datetime.fromisoformat('2023-12-26T18:30:00+01:00'))
def test_hourly_forecast() -> None:
    api = get_api_with_data("forecast.json")
    tz = ZoneInfo("Europe/Brussels")
    result = api.get_hourly_forecast(tz)

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
def test_hourly_forecast_bis() -> None:
    api = get_api_with_data("no-midnight-bug-31-05-2024T01-55.json")
    tz = ZoneInfo("Europe/Brussels")

    result = api.get_hourly_forecast(tz)

    assert isinstance(result, list)

    times = ['2024-05-31T01:00:00+02:00', '2024-05-31T02:00:00+02:00', '2024-05-31T03:00:00+02:00',
             '2024-05-31T04:00:00+02:00', '2024-05-31T05:00:00+02:00', '2024-05-31T06:00:00+02:00',
             '2024-05-31T07:00:00+02:00', '2024-05-31T08:00:00+02:00', '2024-05-31T09:00:00+02:00']

    actual = [f['datetime'] for f in result[:9]]

    assert actual == times


@freeze_time(datetime.fromisoformat('2024-05-31T00:10:00+02:00'))
def test_hourly_forecast_midnight_bug() -> None:
    # Related to https://github.com/jdejaegh/irm-kmi-ha/issues/38
    api = get_api_with_data("midnight-bug-31-05-2024T00-13.json")
    tz = ZoneInfo("Europe/Brussels")

    result = api.get_hourly_forecast(tz)

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


