from unittest.mock import AsyncMock

from irm_kmi_api.pollen import PollenParser
from tests.conftest import get_api_with_data, load_fixture


def test_svg_pollen_parsing():
    with open("tests/fixtures/pollen.svg", "r") as file:
        svg_data = file.read()
    data = PollenParser(svg_data).get_pollen_data()
    assert data == {'birch': 'none', 'oak': 'none', 'hazel': 'none', 'mugwort': 'none', 'alder': 'none',
                    'grasses': 'purple', 'ash': 'none'}

def test_svg_two_pollen_parsing():
    with open("tests/fixtures/new_two_pollens.svg", "r") as file:
        svg_data = file.read()
    data = PollenParser(svg_data).get_pollen_data()
    assert data == {'birch': 'none', 'oak': 'none', 'hazel': 'none', 'mugwort': 'active', 'alder': 'none',
                    'grasses': 'red', 'ash': 'none'}

def test_svg_two_pollen_parsing_2025_update():
    with open("tests/fixtures/pollens-2025.svg", "r") as file:
        svg_data = file.read()
    data = PollenParser(svg_data).get_pollen_data()
    assert data == {'birch': 'none', 'oak': 'none', 'hazel': 'active', 'mugwort': 'none', 'alder': 'green',
                    'grasses': 'none', 'ash': 'none'}

def test_pollen_options():
    assert set(PollenParser.get_option_values()) == {'green', 'yellow', 'orange', 'red', 'purple', 'active', 'none'}


def test_pollen_default_values():
    assert PollenParser.get_default_data() == {'birch': 'none', 'oak': 'none', 'hazel': 'none', 'mugwort': 'none',
                                               'alder': 'none', 'grasses': 'none', 'ash': 'none'}


async def test_pollen_data_from_api() -> None:
    api = get_api_with_data("be_forecast_warning.json")

    # Mock get_svg function
    api.get_svg = AsyncMock(return_value=load_fixture("pollen.svg"))

    result = await api.get_pollen()
    expected = {'mugwort': 'none', 'birch': 'none', 'alder': 'none', 'ash': 'none', 'oak': 'none',
                'grasses': 'purple', 'hazel': 'none'}
    assert result == expected

