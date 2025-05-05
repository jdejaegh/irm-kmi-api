import logging
from unittest.mock import AsyncMock

from irm_kmi_api.data import IrmKmiPollenNames, IrmKmiPollenLevels
from irm_kmi_api.pollen import PollenParser
from tests.conftest import get_api_with_data, load_fixture


def test_svg_pollen_parsing():
    with open("tests/fixtures/pollen.svg", "r") as file:
        svg_data = file.read()
    data = PollenParser(svg_data).get_pollen_data()
    assert data == {IrmKmiPollenNames.BIRCH: IrmKmiPollenLevels.NONE, 
                    IrmKmiPollenNames.OAK: IrmKmiPollenLevels.NONE,
                    IrmKmiPollenNames.HAZEL: IrmKmiPollenLevels.NONE,
                    IrmKmiPollenNames.MUGWORT: IrmKmiPollenLevels.NONE,
                    IrmKmiPollenNames.ALDER: IrmKmiPollenLevels.NONE,
                    IrmKmiPollenNames.GRASSES: IrmKmiPollenLevels.PURPLE, 
                    IrmKmiPollenNames.ASH: IrmKmiPollenLevels.NONE}

def test_svg_two_pollen_parsing():
    with open("tests/fixtures/new_two_pollens.svg", "r") as file:
        svg_data = file.read()
    data = PollenParser(svg_data).get_pollen_data()
    assert data == {IrmKmiPollenNames.BIRCH: IrmKmiPollenLevels.NONE,
                    IrmKmiPollenNames.OAK: IrmKmiPollenLevels.NONE,
                    IrmKmiPollenNames.HAZEL: IrmKmiPollenLevels.NONE,
                    IrmKmiPollenNames.MUGWORT: IrmKmiPollenLevels.ACTIVE,
                    IrmKmiPollenNames.ALDER: IrmKmiPollenLevels.NONE,
                    IrmKmiPollenNames.GRASSES: IrmKmiPollenLevels.RED,
                    IrmKmiPollenNames.ASH: IrmKmiPollenLevels.NONE}

def test_svg_two_pollen_parsing_2025_update():
    with open("tests/fixtures/pollens-2025.svg", "r") as file:
        svg_data = file.read()
    data = PollenParser(svg_data).get_pollen_data()
    assert data == {IrmKmiPollenNames.BIRCH: IrmKmiPollenLevels.NONE,
                    IrmKmiPollenNames.OAK: IrmKmiPollenLevels.NONE,
                    IrmKmiPollenNames.HAZEL: IrmKmiPollenLevels.ACTIVE,
                    IrmKmiPollenNames.MUGWORT: IrmKmiPollenLevels.NONE,
                    IrmKmiPollenNames.ALDER: IrmKmiPollenLevels.GREEN,
                    IrmKmiPollenNames.GRASSES: IrmKmiPollenLevels.NONE,
                    IrmKmiPollenNames.ASH: IrmKmiPollenLevels.NONE}

def test_pollen_options():
    assert set(PollenParser.get_option_values()) == {IrmKmiPollenLevels.GREEN,
                                                     IrmKmiPollenLevels.YELLOW,
                                                     IrmKmiPollenLevels.ORANGE,
                                                     IrmKmiPollenLevels.RED,
                                                     IrmKmiPollenLevels.PURPLE,
                                                     IrmKmiPollenLevels.ACTIVE,
                                                     IrmKmiPollenLevels.NONE}


def test_pollen_default_values():
    assert PollenParser.get_default_data() == {IrmKmiPollenNames.BIRCH: IrmKmiPollenLevels.NONE,
                                               IrmKmiPollenNames.OAK: IrmKmiPollenLevels.NONE,
                                               IrmKmiPollenNames.HAZEL: IrmKmiPollenLevels.NONE,
                                               IrmKmiPollenNames.MUGWORT: IrmKmiPollenLevels.NONE,
                                               IrmKmiPollenNames.ALDER: IrmKmiPollenLevels.NONE,
                                               IrmKmiPollenNames.GRASSES: IrmKmiPollenLevels.NONE,
                                               IrmKmiPollenNames.ASH: IrmKmiPollenLevels.NONE}


async def test_pollen_data_from_api() -> None:
    api = get_api_with_data("be_forecast_warning.json")

    # Mock get_svg function
    api.get_svg = AsyncMock(return_value=load_fixture("pollen.svg"))

    result = await api.get_pollen()
    expected = {IrmKmiPollenNames.MUGWORT: IrmKmiPollenLevels.NONE,
                IrmKmiPollenNames.BIRCH: IrmKmiPollenLevels.NONE,
                IrmKmiPollenNames.ALDER: IrmKmiPollenLevels.NONE,
                IrmKmiPollenNames.ASH: IrmKmiPollenLevels.NONE,
                IrmKmiPollenNames.OAK: IrmKmiPollenLevels.NONE,
                IrmKmiPollenNames.GRASSES: IrmKmiPollenLevels.PURPLE,
                IrmKmiPollenNames.HAZEL: IrmKmiPollenLevels.NONE}
    assert result == expected

