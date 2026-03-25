from __future__ import annotations

from domain.products import product_record
from domain.routes import (
    distinct_factor_routes,
    entry_routes,
    exit_route_labels,
    inverse_labels,
)


def get_product_structure(product: int) -> dict:
    record = product_record(product)

    return {
        "product": record.product,
        "stage": record.stage,
        "intro_route": record.intro_route,

        # multiplication routes
        "routes": distinct_factor_routes(product),
        "entry_routes": entry_routes(product),

        # division exits
        "ways_out": tuple(getattr(record, "ways_out", ())),

        # formatted labels
        "exit_labels": exit_route_labels(product),
        "inverse_labels": inverse_labels(product),

        # structural metadata
        "factor_families": tuple(getattr(record, "factor_families", ())),
        "structural_role": getattr(record, "structural_role", None),
    }
