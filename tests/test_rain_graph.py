import base64
import datetime
import json
from datetime import datetime as dt
from datetime import timedelta
from unittest.mock import MagicMock, AsyncMock
from zoneinfo import ZoneInfo

from irm_kmi_api.api import IrmKmiApiClientHa
from irm_kmi_api.data import AnimationFrameData, RadarAnimationData, RadarStyle
from irm_kmi_api.rain_graph import RainGraph
from tests.conftest import load_fixture


def get_radar_animation_data() -> RadarAnimationData:
    with open("tests/fixtures/clouds_be.png", "rb") as file:
        image_data = file.read()
    with open("tests/fixtures/loc_layer_be_n.png", "rb") as file:
        location = file.read()

    sequence = [
        AnimationFrameData(
            time=dt.fromisoformat("2023-12-26T18:30:00+00:00") + timedelta(minutes=10 * i),
            image=image_data,
            value=2,
            position=.5,
            position_lower=.4,
            position_higher=.6
        )
        for i in range(10)
    ]

    return RadarAnimationData(
        sequence=sequence,
        most_recent_image_idx=2,
        hint="Testing SVG camera",
        unit="mm/10min",
        location=location
    )


async def test_svg_frame_setup():
    data = get_radar_animation_data()
    rain_graph = RainGraph(
        animation_data=data,
        country='BE',
        style=RadarStyle.OPTION_STYLE_STD,
    )

    await rain_graph._draw_svg_frame()

    svg_str = rain_graph._get_dwg().tostring()

    with open("irm_kmi_api/resources/roboto_medium.ttf", "rb") as file:
        font_b64 = base64.b64encode(file.read()).decode('utf-8')

    assert '#385E95' in svg_str
    assert 'font-family: "Roboto Medium";' in svg_str
    assert font_b64 in svg_str


def test_svg_hint():
    data = get_radar_animation_data()
    rain_graph = RainGraph(
        animation_data=data,
        country='BE',
        style=RadarStyle.OPTION_STYLE_STD,
    )

    rain_graph._write_hint()

    svg_str = rain_graph._get_dwg().tostring()

    assert "Testing SVG camera" in svg_str


def test_svg_time_bars():
    data = get_radar_animation_data()
    rain_graph = RainGraph(
        tz = datetime.UTC,
        animation_data=data,
        country='BE',
        style=RadarStyle.OPTION_STYLE_STD,
    )

    rain_graph._draw_hour_bars()

    svg_str = rain_graph._get_dwg().tostring()

    assert "19h" in svg_str
    assert "20h" in svg_str

    assert "<line" in svg_str
    assert 'stroke="white"' in svg_str


def test_draw_chances_path():
    data = get_radar_animation_data()
    rain_graph = RainGraph(
        animation_data=data,
        country='BE',
        style=RadarStyle.OPTION_STYLE_STD,
    )

    rain_graph._draw_chances_path()

    svg_str = rain_graph._get_dwg().tostring()

    assert 'fill="#63c8fa"' in svg_str
    assert 'opacity="0.3"' in svg_str
    assert 'stroke="none"' in svg_str
    assert '<path ' in svg_str


def test_draw_data_line():
    data = get_radar_animation_data()
    rain_graph = RainGraph(
        animation_data=data,
        country='BE',
        style=RadarStyle.OPTION_STYLE_STD,
    )

    rain_graph._draw_data_line()

    svg_str = rain_graph._get_dwg().tostring()

    assert 'fill="none"' in svg_str
    assert 'stroke-width="2"' in svg_str
    assert 'stroke="#63c8fa"' in svg_str
    assert '<path ' in svg_str


async def test_insert_background():
    data = get_radar_animation_data()
    rain_graph = RainGraph(
        animation_data=data,
        country='BE',
        style=RadarStyle.OPTION_STYLE_STD,
    )

    await rain_graph._insert_background()

    with open("irm_kmi_api/resources/be_white.png", "rb") as file:
        png_b64 = base64.b64encode(file.read()).decode('utf-8')

    svg_str = rain_graph._get_dwg().tostring()

    assert png_b64 in svg_str
    assert "<image " in svg_str
    assert 'height="490"' in svg_str
    assert 'width="640"' in svg_str
    assert 'x="0"' in svg_str
    assert 'y="0"' in svg_str


def test_draw_current_frame_line_moving():
    data = get_radar_animation_data()
    rain_graph = RainGraph(
        animation_data=data,
        country='BE',
        style=RadarStyle.OPTION_STYLE_STD,
    )

    rain_graph._draw_current_fame_line()

    str_svg = rain_graph._get_dwg().tostring()

    assert '<line' in str_svg
    assert 'id="now"' in str_svg
    assert 'opacity="1"' in str_svg
    assert 'stroke="white"' in str_svg
    assert 'stroke-width="2"' in str_svg
    assert 'x1="50' in str_svg
    assert 'x2="50' in str_svg
    assert 'y1="520' in str_svg
    assert 'y2="670' in str_svg

    assert 'animateTransform' in str_svg
    assert 'attributeName="transform"' in str_svg
    assert 'repeatCount="indefinite"' in str_svg
    assert 'type="translate"' in str_svg


def test_draw_current_frame_line_index():
    data = get_radar_animation_data()
    rain_graph = RainGraph(
        animation_data=data,
        country='BE',
        style=RadarStyle.OPTION_STYLE_STD,
    )

    rain_graph._draw_current_fame_line(0)

    str_svg = rain_graph._get_dwg().tostring()

    assert '<line' in str_svg
    assert 'id="now"' in str_svg
    assert 'opacity="1"' in str_svg
    assert 'stroke="white"' in str_svg
    assert 'stroke-width="2"' in str_svg
    assert 'x1="50' in str_svg
    assert 'x2="50' in str_svg
    assert 'y1="520' in str_svg
    assert 'y2="670' in str_svg

    assert 'animateTransform' not in str_svg
    assert 'attributeName="transform"' not in str_svg
    assert 'repeatCount="indefinite"' not in str_svg
    assert 'type="translate"' not in str_svg


def test_draw_description_text():
    data = get_radar_animation_data()
    rain_graph = RainGraph(
        tz=datetime.UTC,
        animation_data=data,
        country='BE',
        style=RadarStyle.OPTION_STYLE_STD,
    )

    rain_graph._draw_description_text()

    str_svg = rain_graph._get_dwg().tostring()

    assert "18:30" in str_svg
    assert "18:40" in str_svg
    assert "18:50" in str_svg
    assert "19:00" in str_svg
    assert "19:10" in str_svg
    assert "19:20" in str_svg
    assert "19:30" in str_svg
    assert "19:40" in str_svg
    assert "19:50" in str_svg
    assert "20:00" in str_svg

    assert str_svg.count("2mm/10") == 10
    assert 'class="roboto"' in str_svg


def test_draw_cloud_layer():
    data = get_radar_animation_data()
    rain_graph = RainGraph(
        animation_data=data,
        country='BE',
        style=RadarStyle.OPTION_STYLE_STD,
    )

    rain_graph._insert_cloud_layer()

    str_svg = rain_graph._get_dwg().tostring()

    with open("tests/fixtures/clouds_be.png", "rb") as file:
        png_b64 = base64.b64encode(file.read()).decode('utf-8')

    assert str_svg.count(png_b64) == 10
    assert str_svg.count('height="490"') == 10
    assert str_svg.count('width="640"') == 11  # Is also the width of the SVG itself


async def test_draw_location_layer():
    data = get_radar_animation_data()
    rain_graph = RainGraph(
        animation_data=data,
        country='BE',
        style=RadarStyle.OPTION_STYLE_STD,
    )

    await rain_graph._draw_location()

    str_svg = rain_graph._get_dwg().tostring()

    with open("tests/fixtures/loc_layer_be_n.png", "rb") as file:
        png_b64 = base64.b64encode(file.read()).decode('utf-8')

    assert png_b64 in str_svg


def test_get_animation_data():
    api = IrmKmiApiClientHa(session=MagicMock(), user_agent='testing', cdt_map={})

    tz = ZoneInfo('Europe/Brussels')
    lang = 'en'
    style = RadarStyle.OPTION_STYLE_SATELLITE
    dark_mode = False

    api._api_data = json.loads(load_fixture("forecast.json"))

    data = api.get_animation_data(tz, lang, style, dark_mode)
    print(data)

    assert list(map(lambda x: x.get('value'), data['sequence'])) == [0, 0, 0, 0, 0.1, 0.01, 0.12, 1.2, 2, 0, 0]
    assert list(map(lambda x: x.get('position'), data['sequence'])) == [0, 0, 0, 8, 4, 12, 0, 0, 0, 0, 0]
    assert list(map(lambda x: x.get('position_lower'), data['sequence'])) == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert list(map(lambda x: x.get('position_higher'), data['sequence'])) == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for element in data['sequence']:
        assert 'rs=4' in element['image']


async def test_download_single_cloud():
    data = get_radar_animation_data()
    for i, item in enumerate(data['sequence']):
        item['image'] = f'image-url-{i}'

    rain_graph = RainGraph(
        animation_data=data,
        country='BE',
        style=RadarStyle.OPTION_STYLE_STD,
    )

    rain_graph._api_client = MagicMock()
    rain_graph._api_client.get_image = AsyncMock()

    await rain_graph._download_clouds(2)

    rain_graph._api_client.get_image.assert_called_once_with('image-url-2')

async def test_download_many_clouds():
    data = get_radar_animation_data()
    for i, item in enumerate(data['sequence']):
        item['image'] = f'image-url-{i}'

    rain_graph = RainGraph(
        animation_data=data,
        country='BE',
        style=RadarStyle.OPTION_STYLE_STD,
    )

    rain_graph._api_client = MagicMock()
    rain_graph._api_client.get_image = AsyncMock()

    await rain_graph._download_clouds()

    for i in range(10):
        rain_graph._api_client.get_image.assert_any_call(f'image-url-{i}')

def test_can_build_rain_graph_with_empty_sequence():

    RainGraph(
        RadarAnimationData(sequence=None),
        'BE', RadarStyle.OPTION_STYLE_STD
    )

    RainGraph(
        RadarAnimationData(sequence=[]),
        'BE', RadarStyle.OPTION_STYLE_STD
    )

