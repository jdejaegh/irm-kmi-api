import pytest

from irm_kmi_api.data import IrmKmiRadarForecast
from tests.conftest import get_api_with_data


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
