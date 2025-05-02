from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest
from freezegun import freeze_time

from tests.conftest import get_api_data, get_api_with_data


@pytest.mark.parametrize("sensor,expected,filename",
                         [
                             ('temperature', -2, 'be_forecast_warning.json'),
                             ('temperature', 7, 'forecast.json'),
                             ('temperature', 15, 'forecast_ams_no_ww.json'),
                             ('temperature', 9, 'forecast_out_of_benelux.json'),
                             ('temperature', 13, 'forecast_with_rain_on_radar.json'),
                             ('temperature', 4, 'high_low_temp.json'),
                             ('temperature', 14, 'midnight-bug-31-05-2024T00-13.json'),
                             ('temperature', 13, 'no-midnight-bug-31-05-2024T01-55.json'),

                             ('wind_speed', 10, 'be_forecast_warning.json'),
                             ('wind_speed', 5, 'forecast.json'),
                             ('wind_speed', 26, 'forecast_ams_no_ww.json'),
                             ('wind_speed', 25, 'forecast_out_of_benelux.json'),
                             ('wind_speed', 15, 'forecast_with_rain_on_radar.json'),
                             ('wind_speed', 30, 'high_low_temp.json'),
                             ('wind_speed', 10, 'midnight-bug-31-05-2024T00-13.json'),
                             ('wind_speed', 15, 'no-midnight-bug-31-05-2024T01-55.json'),

                             ('wind_gust_speed', None, 'be_forecast_warning.json'),
                             ('wind_gust_speed', None, 'forecast.json'),
                             ('wind_gust_speed', None, 'forecast_ams_no_ww.json'),
                             ('wind_gust_speed', None, 'forecast_out_of_benelux.json'),
                             ('wind_gust_speed', None, 'forecast_with_rain_on_radar.json'),
                             ('wind_gust_speed', 50, 'high_low_temp.json'),
                             ('wind_gust_speed', None, 'midnight-bug-31-05-2024T00-13.json'),
                             ('wind_gust_speed', None, 'no-midnight-bug-31-05-2024T01-55.json'),

                             ('wind_bearing', 23, 'be_forecast_warning.json'),
                             ('wind_bearing', 248, 'forecast.json'),
                             ('wind_bearing', 270, 'forecast_ams_no_ww.json'),
                             ('wind_bearing', 180, 'forecast_out_of_benelux.json'),
                             ('wind_bearing', 293, 'forecast_with_rain_on_radar.json'),
                             ('wind_bearing', 180, 'high_low_temp.json'),
                             ('wind_bearing', 293, 'midnight-bug-31-05-2024T00-13.json'),
                             ('wind_bearing', 270, 'no-midnight-bug-31-05-2024T01-55.json'),

                             ('uv_index', 0.7, 'be_forecast_warning.json'),
                             ('uv_index', 0.7, 'forecast.json'),
                             ('uv_index', 6, 'forecast_ams_no_ww.json'),
                             ('uv_index', 0.6, 'forecast_out_of_benelux.json'),
                             ('uv_index', None, 'forecast_with_rain_on_radar.json'),
                             ('uv_index', 0.7, 'high_low_temp.json'),
                             ('uv_index', 5.6, 'midnight-bug-31-05-2024T00-13.json'),
                             ('uv_index', 5.6, 'no-midnight-bug-31-05-2024T01-55.json'),

                             ('pressure', 1034, 'be_forecast_warning.json'),
                             ('pressure', 1020, 'forecast.json'),
                             ('pressure', 1010, 'forecast_ams_no_ww.json'),
                             ('pressure', 1013, 'forecast_out_of_benelux.json'),
                             ('pressure', 1006, 'forecast_with_rain_on_radar.json'),
                             ('pressure', 1022, 'high_low_temp.json'),
                             ('pressure', 1010, 'midnight-bug-31-05-2024T00-13.json'),
                             ('pressure', 1010, 'no-midnight-bug-31-05-2024T01-55.json')
                         ])
async def test_current_weather_sensors(
        sensor: str,
        expected: int | float | None,
        filename: str
) -> None:
    api_data = get_api_data(filename)
    time = api_data.get('obs').get('timestamp')
    api = get_api_with_data(filename)
    tz = ZoneInfo("Europe/Brussels")

    @freeze_time(datetime.fromisoformat(time) + timedelta(seconds=45, minutes=1))
    async def run(sensor_: str, expected_: int | float | None):

        current_weather = await api.get_current_weather(tz)
        r = current_weather.get(sensor_, None)
        assert r == expected_

    await run(sensor, expected)


@pytest.mark.parametrize("expected,filename",
                         [
                             ('mm/h', 'forecast_ams_no_ww.json'),
                             ('mm/10min', 'forecast_out_of_benelux.json'),
                             ('mm/10min', 'forecast_with_rain_on_radar.json'),
                         ])
async def test_current_rainfall_unit(
        expected,
        filename
) -> None:
    api = get_api_with_data(filename)

    radar_forecast=api.get_radar_forecast()

    for r in radar_forecast:
        assert r.get('unit') == expected
