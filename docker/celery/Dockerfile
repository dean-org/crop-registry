# Crop Registry - celery image. Thin layer over the registry-platform base image:
# adds only the crop domain package and selects it via REGISTRY_EXTENSION_MODULE.
# RP_VERSION must match the openg2p-registry chart dependency in
# helm/openg2p-crop-registry/Chart.yaml (enforced by test/test_rp_pin_lockstep.py).
# Build context = repo root.
ARG RP_VERSION=1.2
FROM openg2p/openg2p-registry-celery:${RP_VERSION}

ENV REGISTRY_EXTENSION_MODULE=openg2p_registry_crop_extension

COPY crop-extension/ /app/crop-extension/
RUN pip install --no-cache-dir /app/crop-extension
