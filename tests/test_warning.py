from datetime import datetime

from freezegun import freeze_time

from irm_kmi_api.data import WarningType
from tests.conftest import get_api_with_data


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
