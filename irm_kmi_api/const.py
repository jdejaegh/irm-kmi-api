from typing import Final

from .data import ConditionEvol, RadarStyle, PollenLevels

POLLEN_LEVEL_TO_COLOR = {
    'null': PollenLevels.GREEN,
    'low': PollenLevels.YELLOW,
    'moderate': PollenLevels.ORANGE,
    'high': PollenLevels.RED,
    'very high': PollenLevels.PURPLE,
    'active': PollenLevels.ACTIVE
}

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

STYLE_TO_PARAM_MAP: Final = {
    RadarStyle.OPTION_STYLE_STD: 1,
    RadarStyle.OPTION_STYLE_CONTRAST: 2,
    RadarStyle.OPTION_STYLE_YELLOW_RED: 3,
    RadarStyle.OPTION_STYLE_SATELLITE: 4
}

MAP_WARNING_ID_TO_SLUG: Final = {
    0: 'wind',
    1: 'rain',
    2: 'ice_or_snow',
    3: 'thunder',
    7: 'fog',
    9: 'cold',
    12: 'thunder_wind_rain',
    13: 'thunderstorm_strong_gusts',
    14: 'thunderstorm_large_rainfall',
    15: 'storm_surge',
    17: 'coldspell'}

WWEVOL_TO_ENUM_MAP: Final = {
    None: ConditionEvol.STABLE,
    0: ConditionEvol.ONE_WAY,
    1: ConditionEvol.TWO_WAYS
}