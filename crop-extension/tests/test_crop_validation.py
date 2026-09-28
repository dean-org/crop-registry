"""Crop domain-service rules. Runs WITHOUT the registry platform: the two core
modules the service imports (errors, services) are replaced by tests/stubs."""
import asyncio
import importlib.util
import pathlib
import sys
import types

import pytest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "stubs"))
SERVICES = HERE.parent / "src/openg2p_registry_crop_extension/register_domain/services"


def _load():
    pkg = types.ModuleType("crop_svc")
    pkg.__path__ = [str(SERVICES)]
    sys.modules["crop_svc"] = pkg
    for name in ("domain_validation_utils", "g2p_register_domain_service_crop"):
        spec = importlib.util.spec_from_file_location(f"crop_svc.{name}", SERVICES / f"{name}.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[f"crop_svc.{name}"] = mod
        spec.loader.exec_module(mod)
    return sys.modules["crop_svc.g2p_register_domain_service_crop"].G2PRegisterDomainServiceCrop()


SVC = _load()
OK = dict(
    farmer_id="FR-1", parcel_id="P-1", crop_code="CROP_COMMODITY:MAIZE", crop_name="Maize",
    season="CROP_SEASON:SEASON_1", production_year=2026, cultivated_area=2.5,
    planting_date="2026-03-10", expected_harvest_date="2026-07-01",
    fertilizer_used=True, fertilizer_type="NPK", fertilizer_quantity=50,
    actual_yield=100, quantity_sold=80,
)


def check(*records):
    asyncio.run(SVC.validate_domain_attributes(list(records)))


def test_valid_record_passes():
    check(OK)


@pytest.mark.parametrize("change,message", [
    ({"farmer_id": ""}, "farmer_id is required"),
    ({"season": None}, "season is required"),
    ({"production_year": None}, "production_year is required"),
    ({"production_year": 202}, "before 1990"),
    ({"expected_harvest_date": "2026-01-01"}, "expected_harvest_date must not be before planting_date"),
    ({"planting_date": "2999-01-01"}, "planting_date must not be in the future"),
    ({"cultivated_area": 0}, "greater than zero"),
    ({"actual_yield": -1}, "must not be negative"),
    ({"fertilizer_used": False}, "must be empty when fertilizer_used is false"),
    ({"quantity_sold": 500}, "must not exceed actual_yield"),
])
def test_rejects(change, message):
    with pytest.raises(Exception, match=message):
        check({**OK, **change})


def test_fertilizer_no_without_details_passes():
    check({**OK, "fertilizer_used": False, "fertilizer_type": None, "fertilizer_quantity": None})


def test_duplicate_cycle_in_batch_rejected():
    with pytest.raises(Exception, match="Duplicate crop cycle"):
        check(OK, dict(OK))


def test_other_parcel_or_season_is_a_different_cycle():
    check(OK, {**OK, "parcel_id": "P-2"}, {**OK, "season": "CROP_SEASON:SEASON_2"})


def test_record_name_drops_code_list_prefix():
    assert SVC.construct_record_name(OK) == "Maize SEASON_1 2026"
