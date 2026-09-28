# Crop Registry

An installable **Crop Registry** built as a thin extension of the OpenG2P
[registry platform](https://github.com/OpenG2P/registry-platform), modelled on
`farmer-registry`. It holds **one record per crop cycle**: which crop a farmer
grew, on which parcel, in which season, with the cultivation, input and market
details of that cycle.

It is a *separate register*, not a `crop_name` on the farmer. In the farmer
extension `Crop` is a child table of `Land`; here it is a top-level `REGISTER`
with its own ID (`CR-…`), search, dedup, change-request and intake flow.

```
NIN -> Farmer ID -> Parcel ID -> Crop Record ID
                 \____________/
      the Crop register keeps BOTH farmer_id and parcel_id
```

`farmer_id` and `parcel_id` are **references by functional ID** to records in the
Farmer and Land registers (no database foreign key: they are separate registry
deployments). Their existence is not checked at write time.

## Layout

| Path | Purpose |
|---|---|
| `crop-extension/` | The crop domain package: model, schema, domain service, ID generator, seed metadata |
| `docker/` | Thin Dockerfiles (`FROM openg2p/openg2p-registry-*` + `pip install crop-extension`) |
| `helm/openg2p-crop-registry/` | Wrapper chart: pins `openg2p-registry`, supplies the crop values overlay |
| `translation/domain.json` | UI labels for the crop forms (also embedded in `registry_languages.sql`) |
| `test/` | Guard that the platform pin is identical in every Dockerfile and the chart |

## Deploy

```bash
helm repo add openg2p https://openg2p.github.io/openg2p-helm
helm dependency build ./helm/openg2p-crop-registry
helm install crop-registry ./helm/openg2p-crop-registry \
  --set global.registryHostname=crop-registry.example.org
```

