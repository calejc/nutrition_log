import enum


class Day_Range(enum.Enum):
    WEEK_ONE_RANGE = [1,7]
    WEEK_TWO_RANGE = [8, 14]
    WEEK_THREE_RANGE = [15, 21]


FIELDS = (
    'WEIGHT', 
    'CALORIES', 
    'PROTEIN', 
    'CARBS', 
    'STEPS', 
    'CALS_BURNED', 
    'SLEEP'
)
