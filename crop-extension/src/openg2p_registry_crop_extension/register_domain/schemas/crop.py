from datetime import date
from typing import Optional

from openg2p_registry_core.schemas import G2PRegisterBaseSchema, G2PRegisterHistorySchema, G2PIntakeFormSchemaBase
from ..models.enums import AreaUnitEnum, SeedTypeEnum, YieldUnitEnum


class G2PSchemaCrop:
    # A. Crop record
    farmer_id: Optional[str] = None
    parcel_id: Optional[str] = None
    crop_code: Optional[str] = None
    crop_name: Optional[str] = None
    variety_code: Optional[str] = None
    season: Optional[str] = None
    production_year: Optional[int] = None

    # B. Cultivation
    cultivated_area: Optional[float] = None
    area_unit: Optional[AreaUnitEnum] = None
    planting_date: Optional[date] = None
    expected_harvest_date: Optional[date] = None
    actual_harvest_date: Optional[date] = None
    seed_type: Optional[SeedTypeEnum] = None
    seed_quantity: Optional[float] = None
    expected_yield: Optional[float] = None
    actual_yield: Optional[float] = None
    yield_unit: Optional[YieldUnitEnum] = None

    # C. Inputs
    fertilizer_used: Optional[bool] = None
    fertilizer_type: Optional[str] = None
    fertilizer_quantity: Optional[float] = None
    pesticide_used: Optional[bool] = None
    pesticide_quantity: Optional[float] = None
    improved_seed_used: Optional[bool] = None
    machinery_used: Optional[bool] = None

    # D. Market information
    buyer_id: Optional[str] = None
    market_id: Optional[str] = None
    cooperative_id: Optional[str] = None
    storage_facility_id: Optional[str] = None
    expected_market_price: Optional[float] = None
    actual_sale_price: Optional[float] = None
    quantity_sold: Optional[float] = None


class G2PRegisterSchemaCrop(G2PRegisterBaseSchema, G2PSchemaCrop):
    """Schema for the Crop register."""


class G2PRegisterHistorySchemaCrop(G2PRegisterHistorySchema):
    """Schema for Crop history."""


class G2PIntakeFormSchemaCrop(G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaCrop):
    """Schema for the Crop intake form."""
