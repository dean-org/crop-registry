from enum import StrEnum


class AreaUnitEnum(StrEnum):
    HECTARE = "HECTARE"
    ACRE = "ACRE"
    SQUARE_METER = "SQUARE_METER"


class YieldUnitEnum(StrEnum):
    """Unit for expected_yield, actual_yield and quantity_sold."""

    KG = "KG"
    TONNE = "TONNE"


class SeedTypeEnum(StrEnum):
    LOCAL = "LOCAL"
    IMPROVED = "IMPROVED"
    HYBRID = "HYBRID"
