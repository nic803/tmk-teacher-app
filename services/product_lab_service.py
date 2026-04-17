# File: services/product_lab_service.py

from __future__ import annotations

from typing import Any, Dict, List, Optional

from models.products import get_product
from models.routes import get_routes_for_product
from models.product_metadata import get_product_metadata


def _build_product_meta(product_value: int) -> Dict[str, Any]:
    metadata = get_product_metadata(product_value)

    return {
        "product": product_value,
        "stage": metadata.get("stage"),
        "stage_label": metadata.get("stage_label"),
        "intro_route": metadata.get("intro_route"),
        "structural_role": metadata.get("structural_role"),
    }


def _split_routes(routes: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    entry_routes: List[Dict[str, Any]] = []
    exit_routes: List[Dict[str, Any]] = []

    for route in routes:
        route_type = route.get("type")

        if route_type in ("canonical", "derived"):
            entry_routes.append(route)

        elif route_type == "inverse":
            exit_routes.append(route)

    return {
        "entry_routes": entry_routes,
        "exit_routes": exit_routes,
    }


def _build_compare_meta(
    selected_product: int,
    compare_product: int,
) -> Dict[str, Any]:
    selected = get_product(selected_product)
    compare = get_product(compare_product)

    selected_factors = set(selected.get("factors", []))
    compare_factors = set(compare.get("factors", []))

    shared_factors = sorted(selected_factors.intersection(compare_factors))

    compare_metadata = get_product_metadata(compare_product)

    return {
        "product": compare_product,
        "stage": compare_metadata.get("stage"),
        "stage_label": compare_metadata.get("stage_label"),
        "shared_factors": shared_factors,
    }


def get_product_lab_view(
    selected_product: int,
    compare_product: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Service for Product Lab page.

    This function:
    - retrieves product metadata
    - retrieves routes
    - separates entry and exit routes
    - optionally builds comparison metadata

    It does NOT:
    - generate structure
    - generate teaching content
    - duplicate route representations
    """

    product_meta = _build_product_meta(selected_product)

    routes = get_routes_for_product(selected_product)

    route_groups = _split_routes(routes)

    view_model: Dict[str, Any] = {
        "title": "Product Lab",
        "subtitle": "A single hub view with routes in and out.",
        "product_meta": product_meta,
        "entry_routes": route_groups["entry_routes"],
        "exit_routes": route_groups["exit_routes"],
    }

    if compare_product is not None and compare_product != selected_product:
        view_model["compare_meta"] = _build_compare_meta(
            selected_product,
            compare_product,
        )

    return view_model
