from typing import Final

from irm_kmi_api.data import IrmKmiConditionEvol, IrmKmiRadarStyle

# TODO enum as well for those three values?
POLLEN_NAMES: Final = {'Alder', 'Ash', 'Birch', 'Grasses', 'Hazel', 'Mugwort', 'Oak'}
POLLEN_LEVEL_TO_COLOR = {'null': 'green', 'low': 'yellow', 'moderate': 'orange', 'high': 'red', 'very high': 'purple',
                         'active': 'active'}
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

STYLE_TO_PARAM_MAP: Final = {
    IrmKmiRadarStyle.OPTION_STYLE_STD: 1,
    IrmKmiRadarStyle.OPTION_STYLE_CONTRAST: 2,
    IrmKmiRadarStyle.OPTION_STYLE_YELLOW_RED: 3,
    IrmKmiRadarStyle.OPTION_STYLE_SATELLITE: 4
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
    None: IrmKmiConditionEvol.STABLE,
    0: IrmKmiConditionEvol.ONE_WAY,
    1: IrmKmiConditionEvol.TWO_WAYS
}