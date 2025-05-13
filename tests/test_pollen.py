from unittest.mock import AsyncMock

from irm_kmi_api import PollenLevel, PollenName, PollenParser
from tests.conftest import get_api_with_data, load_fixture, is_serializable


def test_svg_pollen_parsing():
    with open("tests/fixtures/pollen.svg", "r") as file:
        svg_data = file.read()
    data = PollenParser(svg_data).get_pollen_data()
    assert data == {PollenName.BIRCH: PollenLevel.NONE,
                    PollenName.OAK: PollenLevel.NONE,
                    PollenName.HAZEL: PollenLevel.NONE,
                    PollenName.MUGWORT: PollenLevel.NONE,
                    PollenName.ALDER: PollenLevel.NONE,
                    PollenName.GRASSES: PollenLevel.PURPLE,
                    PollenName.ASH: PollenLevel.NONE}

def test_svg_two_pollen_parsing():
    with open("tests/fixtures/new_two_pollens.svg", "r") as file:
        svg_data = file.read()
    data = PollenParser(svg_data).get_pollen_data()
    assert data == {PollenName.BIRCH: PollenLevel.NONE,
                    PollenName.OAK: PollenLevel.NONE,
                    PollenName.HAZEL: PollenLevel.NONE,
                    PollenName.MUGWORT: PollenLevel.ACTIVE,
                    PollenName.ALDER: PollenLevel.NONE,
                    PollenName.GRASSES: PollenLevel.RED,
                    PollenName.ASH: PollenLevel.NONE}

def test_svg_two_pollen_parsing_2025_update():
    with open("tests/fixtures/pollens-2025.svg", "r") as file:
        svg_data = file.read()
    data = PollenParser(svg_data).get_pollen_data()
    assert data == {PollenName.BIRCH: PollenLevel.NONE,
                    PollenName.OAK: PollenLevel.NONE,
                    PollenName.HAZEL: PollenLevel.ACTIVE,
                    PollenName.MUGWORT: PollenLevel.NONE,
                    PollenName.ALDER: PollenLevel.GREEN,
                    PollenName.GRASSES: PollenLevel.NONE,
                    PollenName.ASH: PollenLevel.NONE}

def test_pollen_options():
    assert set(PollenParser.get_option_values()) == {PollenLevel.GREEN,
                                                     PollenLevel.YELLOW,
                                                     PollenLevel.ORANGE,
                                                     PollenLevel.RED,
                                                     PollenLevel.PURPLE,
                                                     PollenLevel.ACTIVE,
                                                     PollenLevel.NONE}


def test_pollen_default_values():
    assert PollenParser.get_default_data() == {PollenName.BIRCH: PollenLevel.NONE,
                                               PollenName.OAK: PollenLevel.NONE,
                                               PollenName.HAZEL: PollenLevel.NONE,
                                               PollenName.MUGWORT: PollenLevel.NONE,
                                               PollenName.ALDER: PollenLevel.NONE,
                                               PollenName.GRASSES: PollenLevel.NONE,
                                               PollenName.ASH: PollenLevel.NONE}


async def test_pollen_data_from_api() -> None:
    api = get_api_with_data("be_forecast_warning.json")

    # Mock get_svg function
    api.get_svg = AsyncMock(return_value=load_fixture("pollen.svg"))

    result = await api.get_pollen()
    expected = {PollenName.MUGWORT: PollenLevel.NONE,
                PollenName.BIRCH: PollenLevel.NONE,
                PollenName.ALDER: PollenLevel.NONE,
                PollenName.ASH: PollenLevel.NONE,
                PollenName.OAK: PollenLevel.NONE,
                PollenName.GRASSES: PollenLevel.PURPLE,
                PollenName.HAZEL: PollenLevel.NONE}
    assert result == expected

def test_pollen_is_serializable():
    with open("tests/fixtures/pollens-2025.svg", "r") as file:
        svg_data = file.read()
    data = PollenParser(svg_data).get_pollen_data()

    assert is_serializable(data)