from datetime import datetime

import pytest
from freezegun import freeze_time

from irm_kmi_api import WarningType
from tests.conftest import get_api_with_data, is_serializable


@freeze_time(datetime.fromisoformat('2024-01-12T07:10:00+00:00'))
async def test_warning_data() -> None:
    api = get_api_with_data("be_forecast_warning.json")

    result = api.get_warnings(lang='en')

    assert isinstance(result, list)
    assert len(result) == 2

    first = result[0]
    assert first.get('starts_at').replace(tzinfo=None) < datetime.now()
    assert first.get('ends_at').replace(tzinfo=None) > datetime.now()

    assert first.get('slug') == WarningType.FOG
    assert first.get('friendly_name') == 'Fog'
    assert first.get('id') == 7
    assert first.get('level') == 1

async def test_warning_heat() -> None:
    api = get_api_with_data("antwerp_with_heat_warning.json")

    result = api.get_warnings(lang='en')

    assert isinstance(result, list)
    assert len(result) == 1

    first = result[0]

    assert first.get('slug') == WarningType.HEAT
    assert first.get('friendly_name') == 'Heat'
    assert first.get('id') == 10
    assert first.get('level') == 1


@pytest.mark.parametrize("warning_level", ['high', ''])
async def test_warning_with_invalid_level(warning_level) -> None:
    api = get_api_with_data("be_forecast_warning.json")
    api._api_data['for']['warning'][0]['warningLevel'] = warning_level

    result = api.get_warnings(lang='en')

    assert len(result) == 2
    assert result[0].get('level') is None


@pytest.mark.parametrize("warning_type", ['7', ['7'], None, 7])
async def test_warning_with_invalid_type_is_skipped(warning_type) -> None:
    api = get_api_with_data("be_forecast_warning.json")
    api._api_data['for']['warning'][0]['warningType'] = warning_type

    result = api.get_warnings(lang='en')

    assert len(result) == 1
    assert result[0].get('id') == 2


@pytest.mark.parametrize("name,text", [(None, {}), ({}, 'Fog')])
async def test_warning_with_invalid_name_or_text(name, text) -> None:
    api = get_api_with_data("be_forecast_warning.json")
    api._api_data['for']['warning'][0]['warningType']['name'] = name
    api._api_data['for']['warning'][0]['text'] = text

    result = api.get_warnings(lang='en')

    assert result[0].get('friendly_name') == ''
    assert result[0].get('text') == ''


@pytest.mark.parametrize("forecast", [None, ['x'], 'x'])
async def test_warning_when_for_is_invalid(forecast) -> None:
    api = get_api_with_data("be_forecast_warning.json")
    api._api_data['for'] = forecast

    assert api.get_warnings(lang='en') == []


async def test_warning_data_is_serializable() -> None:
    api = get_api_with_data("be_forecast_warning.json")

    result = api.get_warnings(lang='en')
    for r in result:
        del r["starts_at"]
        del r["ends_at"]
        assert is_serializable(r)