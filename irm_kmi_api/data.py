"""Data classes for IRM KMI integration"""
from datetime import datetime
from enum import StrEnum
from typing import List, Required, TypedDict


class Forecast(TypedDict, total=False):
    """Typed weather forecast dict.

    All attributes are in native units and old attributes kept
    for backwards compatibility.

    Data from Home Assistant to avoid to depend on Home Assistant for this
    """

    condition: str | None
    datetime: Required[str]
    humidity: float | None
    precipitation_probability: int | None
    cloud_coverage: int | None
    native_precipitation: float | None
    precipitation: None
    native_pressure: float | None
    pressure: None
    native_temperature: float | None
    temperature: None
    native_templow: float | None
    templow: None
    native_apparent_temperature: float | None
    wind_bearing: float | str | None
    native_wind_gust_speed: float | None
    native_wind_speed: float | None
    wind_speed: None
    native_dew_point: float | None
    uv_index: float | None
    is_daytime: bool | None  # Mandatory to use with forecast_twice_daily


class ConditionEvol(StrEnum):
    """Possible state for evolution between weather conditions"""

    ONE_WAY = 'one_way'
    TWO_WAYS = 'two_ways'
    STABLE = 'stable'


class RadarStyle(StrEnum):
    """Possible style for the rain radar"""

    OPTION_STYLE_STD = 'standard_style'
    OPTION_STYLE_CONTRAST = 'contrast_style'
    OPTION_STYLE_YELLOW_RED = 'yellow_red_style'
    OPTION_STYLE_SATELLITE = 'satellite_style'


class PollenName(StrEnum):
    ALDER = 'alder'
    ASH = 'ash'
    BIRCH = 'birch'
    GRASSES = 'grasses'
    HAZEL = 'hazel'
    MUGWORT = 'mugwort'
    OAK = 'oak'


class PollenLevel(StrEnum):
    """Possible pollen levels"""

    NONE = 'none'
    ACTIVE = 'active'
    GREEN = 'green'
    YELLOW = 'yellow'
    ORANGE = 'orange'
    RED = 'red'
    PURPLE = 'purple'

class WarningType(StrEnum):
    """Possible warning types"""

    COLD = 'cold'
    COLDSPELL = 'coldspell'
    FOG = 'fog'
    ICE_OR_SNOW = 'ice_or_snow'
    RAIN = 'rain'
    STORM_SURGE = 'storm_surge'
    THUNDER = 'thunder'
    THUNDERSTORM_LARGE_RAINFALL = 'thunderstorm_large_rainfall'
    THUNDERSTORM_STRONG_GUSTS = 'thunderstorm_strong_gusts'
    THUNDER_WIND_RAIN = 'thunder_wind_rain'
    WIND = 'wind'
    UNKNOWN = 'unknown'

class ExtendedForecast(Forecast, total=False):
    """Forecast class with additional attributes for IRM KMI"""

    condition_2: str | None
    condition_evol: ConditionEvol | None
    text: str | None
    sunrise: str | None
    sunset: str | None


class CurrentWeatherData(TypedDict, total=False):
    """Class to hold the currently observable weather at a given location"""

    condition: str | None
    temperature: float | None
    wind_speed: float | None
    wind_gust_speed: float | None
    wind_bearing: float | str | None
    uv_index: float | None
    pressure: float | None


class WarningData(TypedDict, total=False):
    """Holds data about a specific warning"""

    slug: WarningType
    id: int
    level: int
    friendly_name: str
    text: str
    starts_at: datetime
    ends_at: datetime


class RadarForecast(Forecast):
    """Forecast class to handle rain forecast from the IRM KMI rain radar"""

    rain_forecast_max: float
    rain_forecast_min: float
    might_rain: bool
    unit: str | None


class AnimationFrameData(TypedDict, total=False):
    """Holds one single frame of the radar camera, along with the timestamp of the frame"""

    time: datetime | None
    image: bytes | str | None
    value: float | None
    position: float | None
    position_higher: float | None
    position_lower: float | None


class RadarAnimationData(TypedDict, total=False):
    """Holds frames and additional data for the animation to be rendered"""

    sequence: List[AnimationFrameData] | None
    most_recent_image_idx: int | None
    hint: str | None
    unit: str | None
    location: bytes | str | None
    svg_still: bytes | None
    svg_animated: bytes | None
