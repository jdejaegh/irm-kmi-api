from typing import Final

from .data import ConditionEvol, PollenLevel, RadarStyle, WarningType

POLLEN_LEVEL_TO_COLOR = {
    'null': PollenLevel.GREEN,
    'low': PollenLevel.YELLOW,
    'moderate': PollenLevel.ORANGE,
    'high': PollenLevel.RED,
    'very high': PollenLevel.PURPLE,
    'active': PollenLevel.ACTIVE
}

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

STYLE_TO_PARAM_MAP: Final = {
    RadarStyle.OPTION_STYLE_STD: 1,
    RadarStyle.OPTION_STYLE_CONTRAST: 2,
    RadarStyle.OPTION_STYLE_YELLOW_RED: 3,
    RadarStyle.OPTION_STYLE_SATELLITE: 4
}

MAP_WARNING_ID_TO_SLUG: Final = {
    0: WarningType.WIND,
    1: WarningType.RAIN,
    2: WarningType.ICE_OR_SNOW,
    3: WarningType.THUNDER,
    7: WarningType.FOG,
    9: WarningType.COLD,
    12: WarningType.THUNDER_WIND_RAIN,
    13: WarningType.THUNDERSTORM_STRONG_GUSTS,
    14: WarningType.THUNDERSTORM_LARGE_RAINFALL,
    15: WarningType.STORM_SURGE,
    17: WarningType.COLDSPELL
}

WWEVOL_TO_ENUM_MAP: Final = {
    None: ConditionEvol.STABLE,
    0: ConditionEvol.ONE_WAY,
    1: ConditionEvol.TWO_WAYS
}
