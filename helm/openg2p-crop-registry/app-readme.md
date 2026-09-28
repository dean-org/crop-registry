# OpenG2P Crop Registry

A ready-to-install **Crop Registry** built on the OpenG2P registry platform.
One record per crop cycle - a farmer growing a crop on a parcel in a season -
with cultivation, input and market information.

A thin overlay over the shared **openg2p-registry** chart: it adds the crop
domain (register, schema, seed metadata) via the crop-built images and reuses the
platform's service templates, IAM/Keycloak wiring and db-seed machinery.

Set the ingress host (`global.registryHostname`) and, for a real environment, the
shared commons endpoints via the inherited `global.*` values.
