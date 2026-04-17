# File: services/product_lab_service.py

from __future__ import annotations

from importlib import import_module
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence


def _safe_import(module_name: str):
    try:
        return import_module(module_name)
    except Exception:
        return None


_PRODUCTS_MODULE = _safe_import("models.products")
_ROUTES_MODULE = _safe_import("models.routes")
_METADATA_MODULE = _safe_import("models.product_metadata")


def _call_first(module: Any, names: Sequence[str], *args: Any, **kwargs: Any) -> Any:
    if module is None:
        return None

    for name in names:
        fn = getattr(module, name, None)
        if callable(fn):
            return fn(*args, **kwargs)

    return None


def _get_attr_first(module: Any, names: Sequence[str]) -> Any:
    if module is None:
        return None

    for name in names:
        if hasattr(module, name):
            return getattr(module, name)

    return None


def _coerce_int(value: Any) -> Optional[int]:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        cleaned = value.strip()
        if cleaned.isdigit():
            return int(cleaned)
    return None


def _normalise_factor_list(raw_factors: Any) -> List[int]:
    if raw_factors is None:
        return []

    if isinstance(raw_factors, (list, tuple, set)):
        values: List[int] = []
        for item in raw_factors:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                for part in item:
                    part_int = _coerce_int(part)
                    if part_int is not None:
                        values.append(part_int)
            else:
                item_int = _coerce_int(item)
                if item_int is not None:
                    values.append(item_int)

        return sorted(set(values))

    return []


def _extract_product_value(product_record: Any, fallback: Optional[int] = None) -> Optional[int]:
    if isinstance(product_record, Mapping):
        for key in ("value", "product", "product_value"):
            value = _coerce_int(product_record.get(key))
            if value is not None:
                return value

    return fallback


def _extract_factors(product_record: Any) -> List[int]:
    if not isinstance(product_record, Mapping):
        return []

    raw_factors = product_record.get("factors")
    if raw_factors is None:
        raw_factors = product_record.get("factor_values")

    return _normalise_factor_list(raw_factors)


def _build_expression_from_route(route: Mapping[str, Any]) -> str:
    expression = route.get("expression")
    if expression:
        return str(expression)

    factors = route.get("factors")
    product = route.get("product")

    if isinstance(factors, (list, tuple)) and len(factors) == 2 and product is not None:
        return f"{factors[0]} × {factors[1]} = {product}"

    dividend = route.get("dividend")
    divisor = route.get("divisor")
    quotient = route.get("quotient")
    if dividend is not None and divisor is not None and quotient is not None:
        return f"{dividend} ÷ {divisor} = {quotient}"

    return str(route)


def _normalise_route(route: Any, selected_product: int) -> Optional[Dict[str, Any]]:
    if not isinstance(route, Mapping):
        if isinstance(route, str) and route.strip():
            return {
                "product": selected_product,
                "type": "canonical",
                "expression": route.strip(),
                "is_canonical": True,
            }
        return None

    route_type = str(route.get("type") or "").strip().lower()
    is_canonical = bool(route.get("is_canonical", route_type == "canonical"))

    factors = route.get("factors")
    normalised_factors: List[int] = []
    if isinstance(factors, (list, tuple)) and len(factors) == 2:
        left = _coerce_int(factors[0])
        right = _coerce_int(factors[1])
        if left is not None and right is not None:
            normalised_factors = [left, right]

    product_value = _coerce_int(route.get("product")) or selected_product
    stage_available = route.get("stage_available")
    source_product = _coerce_int(route.get("source_product"))

    dividend = _coerce_int(route.get("dividend"))
    divisor = _coerce_int(route.get("divisor"))
    quotient = _coerce_int(route.get("quotient"))

    normalised: Dict[str, Any] = {
        "product": product_value,
        "type": route_type or "canonical",
        "expression": _build_expression_from_route(route),
        "is_canonical": is_canonical,
    }

    if normalised_factors:
        normalised["factors"] = normalised_factors

    if stage_available is not None:
        normalised["stage_available"] = stage_available

    if source_product is not None:
        normalised["source_product"] = source_product

    if dividend is not None and divisor is not None and quotient is not None:
        normalised["dividend"] = dividend
        normalised["divisor"] = divisor
        normalised["quotient"] = quotient

    return normalised


def _normalise_routes(raw_routes: Any, selected_product: int) -> List[Dict[str, Any]]:
    if raw_routes is None:
        return []

    routes: List[Dict[str, Any]] = []

    if isinstance(raw_routes, Mapping):
        for key in ("routes", "items", "values"):
            nested = raw_routes.get(key)
            if isinstance(nested, (list, tuple)):
                raw_routes = nested
                break

    if not isinstance(raw_routes, (list, tuple)):
        return []

    for raw_route in raw_routes:
        normalised = _normalise_route(raw_route, selected_product)
        if normalised is not None:
            routes.append(normalised)

    return routes


def _split_routes(routes: Sequence[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    entry_routes: List[Dict[str, Any]] = []
    exit_routes: List[Dict[str, Any]] = []

    for route in routes:
        route_type = str(route.get("type") or "").lower()

        if route_type == "inverse":
            exit_routes.append(route)
            continue

        if {"dividend", "divisor", "quotient"}.issubset(route.keys()):
            exit_routes.append(route)
            continue

        entry_routes.append(route)

    return {
        "entry_routes": entry_routes,
        "exit_routes": exit_routes,
    }


def _load_product_record(product_value: int) -> Dict[str, Any]:
    record = _call_first(
        _PRODUCTS_MODULE,
        (
            "get_product",
            "get_product_by_value",
            "build_product",
            "product_by_value",
        ),
        product_value,
    )

    if isinstance(record, Mapping):
        return dict(record)

    all_products = _get_attr_first(
        _PRODUCTS_MODULE,
        (
            "PRODUCTS",
            "PRODUCT_MAP",
            "PRODUCTS_BY_VALUE",
            "PRODUCT_REGISTRY",
        ),
    )

    if isinstance(all_products, Mapping):
        candidate = all_products.get(product_value) or all_products.get(str(product_value))
        if isinstance(candidate, Mapping):
            return dict(candidate)

    if isinstance(all_products, (list, tuple)):
        for item in all_products:
            if isinstance(item, Mapping):
                value = _extract_product_value(item)
                if value == product_value:
                    return dict(item)

    return {"value": product_value, "factors": []}


def _load_product_metadata(product_value: int) -> Dict[str, Any]:
    metadata = _call_first(
        _METADATA_MODULE,
        (
            "get_product_metadata",
            "get_metadata_for_product",
            "build_product_metadata",
            "product_metadata_for_value",
        ),
        product_value,
    )

    if isinstance(metadata, Mapping):
        return dict(metadata)

    registry = _get_attr_first(
        _METADATA_MODULE,
        (
            "PRODUCT_METADATA",
            "PRODUCT_METADATA_MAP",
            "PRODUCTS_METADATA",
            "METADATA_BY_PRODUCT",
        ),
    )

    if isinstance(registry, Mapping):
        candidate = registry.get(product_value) or registry.get(str(product_value))
        if isinstance(candidate, Mapping):
            return dict(candidate)

    return {}


def _load_product_routes(product_value: int) -> List[Dict[str, Any]]:
    raw_routes = _call_first(
        _ROUTES_MODULE,
        (
            "get_routes_for_product",
            "get_product_routes",
            "build_routes_for_product",
            "routes_for_product",
        ),
        product_value,
    )

    if raw_routes is None:
        registry = _get_attr_first(
            _ROUTES_MODULE,
            (
                "ROUTES_BY_PRODUCT",
                "PRODUCT_ROUTES",
                "ROUTE_MAP",
                "ROUTES",
            ),
        )
        if isinstance(registry, Mapping):
            raw_routes = registry.get(product_value) or registry.get(str(product_value))

    return _normalise_routes(raw_routes, product_value)


def _derive_intro_route(
    product_value: int,
    metadata: Mapping[str, Any],
    entry_routes: Sequence[Dict[str, Any]],
) -> str:
    intro_route = metadata.get("intro_route")
    if intro_route:
        return str(intro_route)

    intro_factors = metadata.get("intro_factors")
    if isinstance(intro_factors, (list, tuple)) and len(intro_factors) == 2:
        return f"{intro_factors[0]} × {intro_factors[1]}"

    for route in entry_routes:
        if route.get("is_canonical"):
            factors = route.get("factors")
            if isinstance(factors, list) and len(factors) == 2:
                return f"{factors[0]} × {factors[1]}"
            return str(route.get("expression") or product_value)

    for route in entry_routes:
        expression = route.get("expression")
        if expression:
            return str(expression)

    return str(product_value)


def _derive_structural_role(metadata: Mapping[str, Any]) -> str:
    for key in ("structural_role", "role", "family_role", "pattern_label"):
        value = metadata.get(key)
        if value:
            return str(value)
    return "product object"


def _derive_stage(metadata: Mapping[str, Any], product_record: Mapping[str, Any]) -> Optional[str]:
    for key in ("stage", "stage_id", "introduced_stage"):
        value = metadata.get(key)
        if value:
            return str(value)

    for key in ("stage", "introduced_stage"):
        value = product_record.get(key)
        if value:
            return str(value)

    return None


def _derive_stage_label(
    stage: Optional[str],
    metadata: Mapping[str, Any],
    product_record: Mapping[str, Any],
) -> Optional[str]:
    for key in ("stage_label", "stage_name", "introduced_stage_label"):
        value = metadata.get(key)
        if value:
            return str(value)

    for key in ("stage_label", "stage_name"):
        value = product_record.get(key)
        if value:
            return str(value)

    return stage


def _build_product_meta(product_value: int) -> Dict[str, Any]:
    product_record = _load_product_record(product_value)
    metadata = _load_product_metadata(product_value)
    routes = _load_product_routes(product_value)
    route_groups = _split_routes(routes)

    stage = _derive_stage(metadata, product_record)
    stage_label = _derive_stage_label(stage, metadata, product_record)

    return {
        "product": product_value,
        "stage": stage,
        "stage_label": stage_label,
        "intro_route": _derive_intro_route(
            product_value=product_value,
            metadata=metadata,
            entry_routes=route_groups["entry_routes"],
        ),
        "structural_role": _derive_structural_role(metadata),
        "factors": _extract_factors(product_record),
    }


def _build_compare_meta(selected_product: int, compare_product: int) -> Dict[str, Any]:
    selected_meta = _build_product_meta(selected_product)
    compare_meta = _build_product_meta(compare_product)

    selected_factors = set(selected_meta.get("factors") or [])
    compare_factors = set(compare_meta.get("factors") or [])
    shared_factors = sorted(selected_factors.intersection(compare_factors))

    return {
        "product": compare_product,
        "stage": compare_meta.get("stage"),
        "stage_label": compare_meta.get("stage_label"),
        "shared_factors": shared_factors,
    }


def get_product_lab_view(
    selected_product: int,
    compare_product: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Build the Product Lab view model.

    Product Lab is product-level only.
    It returns:
    - one selected product identity
    - one set of entry routes
    - one set of exit routes
    - one optional compare block

    It does not return:
    - representations
    - inverse link duplicates
    - structure explorer data
    - teaching activity content
    """
    selected_value = _coerce_int(selected_product)
    if selected_value is None:
        raise ValueError("selected_product must be an integer product value")

    routes = _load_product_routes(selected_value)
    route_groups = _split_routes(routes)
    product_meta = _build_product_meta(selected_value)

    view_model: Dict[str, Any] = {
        "title": "Product Lab",
        "subtitle": "A single hub view with routes in and out.",
        "product_meta": {
            "product": product_meta["product"],
            "stage": product_meta.get("stage"),
            "stage_label": product_meta.get("stage_label"),
            "intro_route": product_meta.get("intro_route"),
            "structural_role": product_meta.get("structural_role"),
        },
        "entry_routes": route_groups["entry_routes"],
        "exit_routes": route_groups["exit_routes"],
    }

    compare_value = _coerce_int(compare_product)
    if compare_value is not None and compare_value != selected_value:
        view_model["compare_meta"] = _build_compare_meta(
            selected_product=selected_value,
            compare_product=compare_value,
        )

    return view_model
