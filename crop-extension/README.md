# OpenG2P Registry Crop Extension

Domain package for a standalone **Crop Registry** (one record per crop cycle).

| Mnemonic | Table | Purpose |
|---|---|---|
| `Crop` | `g2p_register_crops` | Top-level register (`REGISTER`) |
| | `g2p_register_history_crops` | Version snapshots |
| | `g2p_intake_form_crops` | Ingestion intake form |

## Specification -> column mapping

`crop_record_id` is the core `functional_record_id` (generated as `CR-` + digits).
All other spec fields are columns of the same name.

| Spec section | Columns |
|---|---|
| A. Crop record | `farmer_id`, `parcel_id`, `crop_code`, `crop_name`, `variety_code`, `season`, `production_year` |
| B. Cultivation | `cultivated_area`, `area_unit`*, `planting_date`, `expected_harvest_date`, `actual_harvest_date`, `seed_type`, `seed_quantity`, `expected_yield`, `actual_yield`, `yield_unit`* |
| C. Inputs | `fertilizer_used`, `fertilizer_type`, `fertilizer_quantity`, `pesticide_used`, `pesticide_quantity`, `improved_seed_used`, `machinery_used` |
| D. Market | `buyer_id`, `market_id`, `cooperative_id`, `storage_facility_id`, `expected_market_price`, `actual_sale_price`, `quantity_sold` |

\* **Added beyond the spec**: `area_unit` (HECTARE/ACRE/SQUARE_METER) and
`yield_unit` (KG/TONNE, applies to `expected_yield`, `actual_yield`,
`quantity_sold`). Without them the numbers are ambiguous.

Unit conventions that have **no column** (assumptions - change if wrong):
`seed_quantity` and `fertilizer_quantity` in kg, `pesticide_quantity` in litres,
prices in UGX per `yield_unit`.

## Rules (domain service)

Required: `farmer_id`, `crop_code` or `crop_name`, `season`, `production_year`.
`parcel_id` is optional (the Land register may lag). Also enforced: harvest dates
not before planting, no future planting/actual harvest, area > 0, quantities and
prices >= 0, `quantity_sold <= actual_yield`, no fertilizer type/quantity when
`fertilizer_used` is false, and no duplicate cycle (same farmer + parcel + crop +
season + year) within one request.

Duplicates against records **already stored** are handled by the register's dedup
configuration (exact match on those five fields, threshold 100), not by code.

## Code lists

`crop_code` -> `CROP_COMMODITY`, `season` -> `CROP_SEASON`, `fertilizer_type` ->
`FERTILIZER_TYPE`. Defaults are in `meta_data/lookup-data/`; a Uganda agriculture
pack loaded from Master Data replaces any list with the same attribute id. Stored
values are code-list value ids (e.g. `CROP_COMMODITY:MAIZE`), as in the farmer
extension.

## Open decisions

* **`variety_code`** is free text: no national variety list was provided.
* **Crop-record ID format** is `CR-<digits>`; the spec's example `CR-2026-001`
  (year in the ID) is not supported by the platform's prefix/suffix generator.
* **Seed approvers** (`alex.carter`, `nina.patel`) in `awe_meta_data/` are the
  platform demo users, as in farmer-registry. Replace with real approver rules.
* `registry_themes*.sql`, `g2p_registry_configuration.sql` (logo) are copied from
  the farmer registry; only the registry name and domain translations changed.

## Tests

```bash
cd crop-extension && python -m pytest tests -q   # no platform needed
```
