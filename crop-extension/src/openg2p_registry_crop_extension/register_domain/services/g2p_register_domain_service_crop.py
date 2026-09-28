import logging
from datetime import date

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_validation_utils import (
    as_bool,
    as_float,
    as_int,
    is_blank,
    parse_date,
    validation_error,
)

_logger = logging.getLogger("g2p-register-domain-service")

# Guards against typos such as 202 rather than encoding any policy.
_MIN_PRODUCTION_YEAR = 1990


class G2PRegisterDomainServiceCrop(G2PRegisterDomainService):
    """Validation and naming rules for the Crop register.

    One record is one crop cycle: a farmer growing a crop on a parcel in a
    season. Cross-record duplicates already in the database are caught by the
    register's dedup configuration (see g2p_register_schemas.sql), not here;
    this service only sees the records of the current request.
    """

    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            self._validate_required_references(record)
            self._validate_production_year(record)
            self._validate_dates(record)
            self._validate_quantities(record)
            self._validate_inputs(record)
            self._validate_sales(record)
        self._validate_no_duplicate_cycle(records)

    # -- per-record rules --------------------------------------------------

    def _validate_required_references(self, record: dict) -> None:
        # A crop cycle is "what, by whom, in which season": without a farmer,
        # a crop, a season and a year the record cannot be told apart from
        # another cycle. parcel_id stays optional because not every farmer has
        # a registered parcel yet (the Land register may lag the Crop register).
        if is_blank(record.get("farmer_id")):
            validation_error("farmer_id is required")
        if is_blank(record.get("crop_code")) and is_blank(record.get("crop_name")):
            validation_error("crop_code or crop_name is required")
        if is_blank(record.get("season")):
            validation_error("season is required")
        if as_int(record.get("production_year")) is None:
            validation_error("production_year is required")

    def _validate_production_year(self, record: dict) -> None:
        year = as_int(record.get("production_year"))
        if year is None:
            return
        if year < _MIN_PRODUCTION_YEAR:
            validation_error(f"production_year must not be before {_MIN_PRODUCTION_YEAR}")
        if year > date.today().year + 1:
            validation_error("production_year must not be more than one year in the future")

    def _validate_dates(self, record: dict) -> None:
        planting = parse_date(record.get("planting_date"))
        expected = parse_date(record.get("expected_harvest_date"))
        actual = parse_date(record.get("actual_harvest_date"))

        if planting is not None and planting > date.today():
            validation_error("planting_date must not be in the future")
        if actual is not None and actual > date.today():
            validation_error("actual_harvest_date must not be in the future")
        if planting is not None and expected is not None and expected < planting:
            validation_error("expected_harvest_date must not be before planting_date")
        if planting is not None and actual is not None and actual < planting:
            validation_error("actual_harvest_date must not be before planting_date")

    def _validate_quantities(self, record: dict) -> None:
        area = as_float(record.get("cultivated_area"))
        if area is not None and area <= 0:
            validation_error("cultivated_area must be greater than zero when provided")

        for field in (
            "seed_quantity",
            "expected_yield",
            "actual_yield",
            "fertilizer_quantity",
            "pesticide_quantity",
            "expected_market_price",
            "actual_sale_price",
            "quantity_sold",
        ):
            value = as_float(record.get(field))
            if value is not None and value < 0:
                validation_error(f"{field} must not be negative")

    def _validate_inputs(self, record: dict) -> None:
        # A "no" answer must not carry details, otherwise the register would
        # report a fertilizer type for a farmer who used none.
        if as_bool(record.get("fertilizer_used")) is False:
            if not is_blank(record.get("fertilizer_type")) or as_float(record.get("fertilizer_quantity")):
                validation_error(
                    "fertilizer_type and fertilizer_quantity must be empty when fertilizer_used is false"
                )
        if as_bool(record.get("pesticide_used")) is False and as_float(record.get("pesticide_quantity")):
            validation_error("pesticide_quantity must be empty when pesticide_used is false")

    def _validate_sales(self, record: dict) -> None:
        sold = as_float(record.get("quantity_sold"))
        actual_yield = as_float(record.get("actual_yield"))
        if sold is not None and actual_yield is not None and sold > actual_yield:
            validation_error("quantity_sold must not exceed actual_yield")

    # -- batch rules -------------------------------------------------------

    def _validate_no_duplicate_cycle(self, records: list[dict]) -> None:
        """The same farmer cannot plant the same crop on the same parcel twice
        in one season of one year."""
        seen: set[tuple] = set()
        for record in records:
            key = (
                str(record.get("farmer_id") or "").strip(),
                str(record.get("parcel_id") or "").strip(),
                str(record.get("crop_code") or record.get("crop_name") or "").strip().upper(),
                str(record.get("season") or "").strip(),
                as_int(record.get("production_year")),
            )
            if not key[0]:
                continue
            if key in seen:
                validation_error(
                    "Duplicate crop cycle: same farmer, parcel, crop, season and production year"
                )
            seen.add(key)

    # -- naming ------------------------------------------------------------

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for crop")

        keys = [
            "farmer_id",
            "parcel_id",
            "crop_code",
            "crop_name",
            "variety_code",
            "season",
            "production_year",
            "cooperative_id",
            "buyer_id",
        ]
        search_text = []
        if extra:
            search_text.extend(str(item).strip() for item in extra if str(item).strip())
        search_text.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )
        return " ".join(search_text).strip()

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for crop")

        # e.g. "Maize SEASON_1 2026". season is stored as a code-list value id
        # ("CROP_SEASON:SEASON_1"); keep only the code part for display.
        keys = ["crop_name", "season", "production_year"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        for key in keys:
            value = str(payload.get(key) or "").strip()
            if key == "season":
                value = value.rsplit(":", 1)[-1]
            if value:
                record_name.append(value)
        return " ".join(record_name).strip()
