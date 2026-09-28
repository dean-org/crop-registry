# Crop Registry - DB-seed image. Thin layer over the registry-platform db-seed
# base (generic entrypoint + loaders). The base ships the reference registry's
# seed, so clear it and apply only the crop registry's own metadata.
# Build context = repo root.
ARG RP_VERSION=0.0.0-develop.432
FROM openg2p/openg2p-registry-db-seed:${RP_VERSION}

RUN rm -rf /seed/meta_data/* /seed/awe_meta_data/* /seed/templates/* /seed/seed-data/*

COPY crop-extension/src/openg2p_registry_crop_extension/meta_data/     /seed/meta_data/
COPY crop-extension/src/openg2p_registry_crop_extension/awe_meta_data/ /seed/awe_meta_data/
