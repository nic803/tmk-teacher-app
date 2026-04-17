# File: services/product_lab_service.py

from __future__ import annotations

from typing import Any, Dict, List, Optional

from domain.products import product_record, stage_label
from domain.routes import distinct_factor_routes, exit_route_labels, shared_factors


def _format_multiplication_route(route: Any) -> str:
    if isinstance(route, tuple) and len(route) == 2:
        return f"{route[0]} × {route[1]}"
    return str(route)


def _build_entry_routes(product: int) -> List[Dict[str, Any]]:
    routes: List[Dict[str, Any]] = []

    for route in distinct_factor_routes(product):
        expression = _format_multiplication_route(route)
        factors = list(route) if isinstance(route, tuple) and len(route) == 2 else None

        route_item: Dict[str, Any] = {
            "product": product,
            "type": "canonical",
            "expression": expression,
            "is_canonical": True,
        }

        if factors is not None:
            route_item["factors"] = factors

        routes.append(route_item)

    return routes


def _build_exit_routes(product: int) -> List[Dict[str, Any]]:
    routes: List[Dict[str, Any]] = []

    for label in exit_route_labels(product):
        routes.append(
            {
                "product": product,
                "type": "inverse",
                "expression": str(label),
            }
        )

    return routes


def _build_product_meta(product: int) -> Dict[str, Any]:
    record = product_record(product)

    return {
        "product": record.product,
        "stage": record.stage,
        "stage_label": stage_label(record.stage),
        "intro_route": _format_multiplication_route(record.intro_route),
        "structural_role": record.structural_role,
    }


def _build_compare_meta(selected_product: int, compare_product: int) -> Dict[str, Any]:
    compare_record = product_record(compare_product)

    return {
        "product": compare_record.product,
        "stage": compare_record.stage,
        "stage_label": stage_label(compare_record.stage),
        "shared_factors": list(shared_factors(selected_product, compare_product)),
    }


def get_product_lab_view(
    selected_product: int,
    compare_product: Optional[int] = None,
) -> Dict[str, Any]:
    product_meta = _build_product_meta(selected_product)

    view_model: Dict[str, Any] = {
        "title": "Product Lab",
        "subtitle": "A single hub view with routes in and out.",
        "product_meta": product_meta,
        "entry_routes": _build_entry_routes(selected_product),
        "exit_routes": _build_exit_routes(selected_product),
    }

    if compare_product is not None and compare_product != selected_product:
        view_model["compare_meta"] = _build_compare_meta(
            selected_product=selected_product,
            compare_product=compare_product,
        )

    return view_model
