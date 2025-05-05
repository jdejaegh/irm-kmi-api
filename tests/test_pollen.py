import logging
from unittest.mock import AsyncMock

from irm_kmi_api.data import PollenNames, PollenLevels
from irm_kmi_api.pollen import PollenParser
from tests.conftest import get_api_with_data, load_fixture


def test_svg_pollen_parsing():
    with open("tests/fixtures/pollen.svg", "r") as file:
        svg_data = file.read()
    data = PollenParser(svg_data).get_pollen_data()
    assert data == {PollenNames.BIRCH: PollenLevels.NONE,
                    PollenNames.OAK: PollenLevels.NONE,
                    PollenNames.HAZEL: PollenLevels.NONE,
                    PollenNames.MUGWORT: PollenLevels.NONE,
                    PollenNames.ALDER: PollenLevels.NONE,
                    PollenNames.GRASSES: PollenLevels.PURPLE,
                    PollenNames.ASH: PollenLevels.NONE}

def test_svg_two_pollen_parsing():
    with open("tests/fixtures/new_two_pollens.svg", "r") as file:
        svg_data = file.read()
    data = PollenParser(svg_data).get_pollen_data()
    assert data == {PollenNames.BIRCH: PollenLevels.NONE,
                    PollenNames.OAK: PollenLevels.NONE,
                    PollenNames.HAZEL: PollenLevels.NONE,
                    PollenNames.MUGWORT: PollenLevels.ACTIVE,
                    PollenNames.ALDER: PollenLevels.NONE,
                    PollenNames.GRASSES: PollenLevels.RED,
                    PollenNames.ASH: PollenLevels.NONE}

def test_svg_two_pollen_parsing_2025_update():
    with open("tests/fixtures/pollens-2025.svg", "r") as file:
        svg_data = file.read()
    data = PollenParser(svg_data).get_pollen_data()
    assert data == {PollenNames.BIRCH: PollenLevels.NONE,
                    PollenNames.OAK: PollenLevels.NONE,
                    PollenNames.HAZEL: PollenLevels.ACTIVE,
                    PollenNames.MUGWORT: PollenLevels.NONE,
                    PollenNames.ALDER: PollenLevels.GREEN,
                    PollenNames.GRASSES: PollenLevels.NONE,
                    PollenNames.ASH: PollenLevels.NONE}

def test_pollen_options():
    assert set(PollenParser.get_option_values()) == {PollenLevels.GREEN,
                                                     PollenLevels.YELLOW,
                                                     PollenLevels.ORANGE,
                                                     PollenLevels.RED,
                                                     PollenLevels.PURPLE,
                                                     PollenLevels.ACTIVE,
                                                     PollenLevels.NONE}


def test_pollen_default_values():
    assert PollenParser.get_default_data() == {PollenNames.BIRCH: PollenLevels.NONE,
                                               PollenNames.OAK: PollenLevels.NONE,
                                               PollenNames.HAZEL: PollenLevels.NONE,
                                               PollenNames.MUGWORT: PollenLevels.NONE,
                                               PollenNames.ALDER: PollenLevels.NONE,
                                               PollenNames.GRASSES: PollenLevels.NONE,
                                               PollenNames.ASH: PollenLevels.NONE}


async def test_pollen_data_from_api() -> None:
    api = get_api_with_data("be_forecast_warning.json")

    # Mock get_svg function
    api.get_svg = AsyncMock(return_value=load_fixture("pollen.svg"))

    result = await api.get_pollen()
    expected = {PollenNames.MUGWORT: PollenLevels.NONE,
                PollenNames.BIRCH: PollenLevels.NONE,
                PollenNames.ALDER: PollenLevels.NONE,
                PollenNames.ASH: PollenLevels.NONE,
                PollenNames.OAK: PollenLevels.NONE,
                PollenNames.GRASSES: PollenLevels.PURPLE,
                PollenNames.HAZEL: PollenLevels.NONE}
    assert result == expected

