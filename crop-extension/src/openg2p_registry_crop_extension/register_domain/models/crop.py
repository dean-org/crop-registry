from sqlalchemy import Boolean, Date, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from openg2p_registry_core.models import G2PRegister, G2PRegisterHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm

from ..services import G2PRegisterDomainServiceCrop
from .enums import AreaUnitEnum, SeedTypeEnum, YieldUnitEnum


class G2PCrop:
    """One crop cycle: a crop grown by a farmer on a parcel in a season.

    ``crop_record_id`` in the specification is the core ``functional_record_id``.
    ``farmer_id`` / ``parcel_id`` are the functional IDs of records held in the
    Farmer and Land registers. They are plain references (no foreign key),
    because those records live in a different registry deployment.
    """

    # -- A. Crop record ----------------------------------------------------
    farmer_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    parcel_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    crop_code: Mapped[str] = mapped_column(String, nullable=True, index=True)     # Attribute lookup CROP_CODE
    crop_name: Mapped[str] = mapped_column(String, nullable=True)
    variety_code: Mapped[str] = mapped_column(String, nullable=True)
    season: Mapped[str] = mapped_column(String, nullable=True, index=True)        # Attribute lookup CROP_SEASON
    production_year: Mapped[int] = mapped_column(Integer, nullable=True, index=True)

    # -- B. Cultivation ----------------------------------------------------
    cultivated_area: Mapped[float] = mapped_column(Float, nullable=True)
    area_unit: Mapped[AreaUnitEnum] = mapped_column(String, nullable=True)        # AreaUnitEnum
    planting_date: Mapped[str] = mapped_column(Date, nullable=True)
    expected_harvest_date: Mapped[str] = mapped_column(Date, nullable=True)
    actual_harvest_date: Mapped[str] = mapped_column(Date, nullable=True)
    seed_type: Mapped[SeedTypeEnum] = mapped_column(String, nullable=True)        # SeedTypeEnum
    seed_quantity: Mapped[float] = mapped_column(Float, nullable=True)            # kg
    expected_yield: Mapped[float] = mapped_column(Float, nullable=True)           # in yield_unit
    actual_yield: Mapped[float] = mapped_column(Float, nullable=True)             # in yield_unit
    yield_unit: Mapped[YieldUnitEnum] = mapped_column(String, nullable=True)      # YieldUnitEnum

    # -- C. Inputs ---------------------------------------------------------
    fertilizer_used: Mapped[bool] = mapped_column(Boolean, nullable=True)
    fertilizer_type: Mapped[str] = mapped_column(String, nullable=True)           # Attribute lookup FERTILIZER_TYPE
    fertilizer_quantity: Mapped[float] = mapped_column(Float, nullable=True)      # kg
    pesticide_used: Mapped[bool] = mapped_column(Boolean, nullable=True)
    pesticide_quantity: Mapped[float] = mapped_column(Float, nullable=True)       # litres
    improved_seed_used: Mapped[bool] = mapped_column(Boolean, nullable=True)
    machinery_used: Mapped[bool] = mapped_column(Boolean, nullable=True)

    # -- D. Market information --------------------------------------------
    buyer_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    market_id: Mapped[str] = mapped_column(String, nullable=True)
    cooperative_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    storage_facility_id: Mapped[str] = mapped_column(String, nullable=True)
    expected_market_price: Mapped[float] = mapped_column(Float, nullable=True)    # UGX per yield_unit
    actual_sale_price: Mapped[float] = mapped_column(Float, nullable=True)        # UGX per yield_unit
    quantity_sold: Mapped[float] = mapped_column(Float, nullable=True)            # in yield_unit


# All Register classes should have the prefix G2PRegister
class G2PRegisterCrop(G2PRegister, G2PCrop):
    __tablename__ = "g2p_register_crops"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceCrop().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceCrop().construct_record_name(self.to_dict())


# All Register History classes should have the prefix G2PRegisterHistory
class G2PRegisterHistoryCrop(G2PRegisterHistory, G2PCrop):
    __tablename__ = "g2p_register_history_crops"


# All Intake Form classes should have the prefix G2PIntakeForm
class G2PIntakeFormCrop(G2PIntakeForm, G2PRegister, G2PCrop):
    __tablename__ = "g2p_intake_form_crops"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceCrop().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceCrop().construct_record_name(self.to_dict())
