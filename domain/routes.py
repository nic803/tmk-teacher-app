from __future__ import annotations

from typing import Final

from domain.products import ALL_PRODUCTS, PRODUCT_STAGE, STAGE_ORDER, factors_for_product


_STAGE_INDEX: Final[dict[str, int]] = {
    stage_id: index for index, stage_id in enumerate(STAGE_ORDER)
}


def _stage_at_or_before(stage_a: str, stage_b: str) -> bool:
    return _STAGE_INDEX[stage_a] <= _STAGE_INDEX[stage_b]


def _canonical_routes(product: int) -> tuple[tuple[int, int], ...]:
    if product not in ALL_PRODUCTS:
        raise ValueError(f"Unknown TMK product: {product}")
    return factors_for_product(product)


def _derived_entry_routes(product: int) -> tuple[tuple[int, int], ...]:
    if product not in ALL_PRODUCTS:
        raise ValueError(f"Unknown TMK product: {product}")

    stage = PRODUCT_STAGE[product]
    routes: list[tuple[int, int]] = []

    if stage == "C":
        routes.append((5, product // 5))
    elif stage == "D":
        routes.append((9, product // 9))
    elif stage == "E":
        factors = factors_for_product(product)
        preferred = next(
            ((a, b) for a, b in factors if a in (2, 4, 8) or b in (2, 4, 8)),
            None,
        )
        if preferred is not None:
            routes.append(preferred)
    elif stage == "F":
        factors = factors_for_product(product)
        preferred = next(
            ((a, b) for a, b in factors if a in (3, 6) or b in (3, 6)),
            None,
        )
        if preferred is not None:
            routes.append(preferred)
    elif stage == "G":
        routes.append((7, 7))

    deduped: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    for route in routes:
        if route not in seen:
            deduped.append(route)
            seen.add(route)

    return tuple(deduped)


def routes_for_product(product: int) -> tuple[tuple[int, int], ...]:
    canonical = list(_canonical_routes(product))
    seen = set(canonical)

    for route in _derived_entry_routes(product):
        if route not in seen:
            canonical.append(route)
            seen.add(route)

    return tuple(canonical)


def distinct_factor_routes(product: int) -> tuple[tuple[int, int], ...]:
    return routes_for_product(product)


def entry_routes(product: int) -> tuple[tuple[int, int], ...]:
    return routes_for_product(product)


def exit_route_labels(product: int) -> tuple[str, ...]:
    if product not in ALL_PRODUCTS:
        raise ValueError(f"Unknown TMK product: {product}")

    labels: list[str] = []
    for divisor, quotient in factors_for_product(product):
        labels.append(f"{product} ÷ {divisor} = {quotient}")
        if divisor != quotient:
            labels.append(f"{product} ÷ {quotient} = {divisor}")

    return tuple(labels)


def inverse_labels(product: int) -> tuple[str, ...]:
    return exit_route_labels(product)


def shared_factors(a: int, b: int) -> tuple[int, ...]:
    if a not in ALL_PRODUCTS:
        raise ValueError(f"Unknown TMK product: {a}")
    if b not in ALL_PRODUCTS:
        raise ValueError(f"Unknown TMK product: {b}")

    factors_a = {factor for pair in factors_for_product(a) for factor in pair}
    factors_b = {factor for pair in factors_for_product(b) for factor in pair}

    return tuple(sorted(factors_a & factors_b))


def routes_available_at_stage(stage_id: str) -> tuple[tuple[int, int], ...]:
    if stage_id not in STAGE_ORDER:
        raise ValueError(f"Unknown TMK stage: {stage_id}")

    routes: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()

    for product in ALL_PRODUCTS:
        product_stage = PRODUCT_STAGE[product]
        if _stage_at_or_before(product_stage, stage_id):
            for route in routes_for_product(product):
                if route not in seen:
                    routes.append(route)
                    seen.add(route)

    return tuple(routes)


__all__ = [
    "routes_for_product",
    "routes_available_at_stage",
    "distinct_factor_routes",
    "entry_routes",
    "exit_route_labels",
    "inverse_labels",
    "shared_factors",
]
