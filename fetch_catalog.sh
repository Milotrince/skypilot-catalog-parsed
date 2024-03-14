#!/bin/bash
# SkyPilot Catalog Fetch Script
# Downloads https://github.com/skypilot-org/skypilot-catalog/tree/master/catalogs/v5

curl https://codeload.github.com/skypilot-org/skypilot-catalog/tar.gz/master \
    | tar -xz --strip=2 skypilot-catalog-master/catalogs/v5 \
    && mv v5 catalog