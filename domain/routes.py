from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from domain.products import (
    ALL_PRODUCTS,
    PRODUCT_STAGE,
    STAGE_ORDER,
    available_products,
    factors_for_product,
    product_record,
)


@dataclass(frozen=True)
class Route:
    product: int
    type: str
    source_product: int | None
    factors: tuple[int, int]
    operations: tuple[str, ...]
    is_canonical: bool
    stage_available: str


_STAGE_INDEX: Final[dict[str, int]] = {
    stage_id: index for index, stage_id in enumerate(STAGE_ORDER)
}


def _stage_at_or_before(stage_a: str, stage_b: str) -> bool:
    return _STAGE_INDEX[stage_a] <= _STAGE_INDEX[stage_b]


def _route_stage(*stage_ids: str) -> str:
    return max(stage_ids, key=lambda stage_id: _STAGE_INDEX[stage_id])


def _canonical_routes(product: int) -> tuple[Route, ...]:
    record = product_record(product)

    return tuple(
        Route(
            product=product,
            type="canonical",
            source_product=None,
            factors=(a, b),
            operations=("multiply",),
            is_canonical=True,
            stage_available=record.stage,
        )
        for a, b in record.factors
    )


def _doubling_source(product: int) -> int | None:
    if product % 2 != 0:
        return None

    source = product // 2
    if source not in ALL_PRODUCTS:
        return None

    if PRODUCT_STAGE[product] != "E":
        return None

    return source


def _near_ten_source(product: int) -> int | None:
    if PRODUCT_STAGE[product] != "D":
        return None

    source = product + (product // 9)
    if source not in ALL_PRODUCTS:
        return None

    return source


def _half_of_ten_source(product: int) -> int | None:
    if PRODUCT_STAGE[product] != "C":
        return None

    source = product * 2
    if source not in ALL_PRODUCTS:
        return None

    return source


def _interleaving_source(product: int) -> int | None:
    if PRODUCT_STAGE[product] != "F":
        return None

    if product == 21:
        return None

    if product == 42:
        return 21

    return None


def _square_closure_source(product: int) -> int | None:
    if PRODUCT_STAGE[product] != "G":
        return None

    source = 42
    if source not in ALL_PRODUCTS:
        return None

    return source


def _derived_routes(product: int) -> tuple[Route, ...]:
    stage = PRODUCT_STAGE[product]
    routes: list[Route] = []

    if stage == "C":
        source = _half_of_ten_source(product)
        if source is not None:
            routes.append(
                Route(
                    product=product,
                    type="derived",
                    source_product=source,
                    factors=(5, product // 5),
                    operations=("scale_from_10", "halve"),
                    is_canonical=False,
                    stage_available="C",
                )
            )

    elif stage == "D":
        source = _near_ten_source(product)
        if source is not None:
            routes.append(
                Route(
                    product=product,
                    type="derived",
                    source_product=source,
                    factors=(9, product // 9),
                    operations=("scale_from_10", "subtract_1_group"),
                    is_canonical=False,
                    stage_available="D",
                )
            )

    elif stage == "E":
        source = _doubling_source(product)
        if source is not None:
            routes.append(
                Route(
                    product=product,
                    type="derived",
                    source_product=source,
                    factors=factors_for_product(product)[0],
                    operations=("double",),
                    is_canonical=False,
                    stage_available="E",
                )
            )

    elif stage == "F":
        source = _interleaving_source(product)
        if source is not None:
            routes.append(
                Route(
                    product=product,
                    type="derived",
                    source_product=source,
                    factors=factors_for_product(product)[0],
                    operations=("interleave_from_known_product",),
                    is_canonical=False,
                    stage_available="F",
                )
            )

    elif stage == "G":
        source = _square_closure_source(product)
        if source is not None:
            routes.append(
                Route(
                    product=product,
                    type="derived",
                    source_product=source,
                    factors=(7, 7),
                    operations=("square_closure",),
                    is_canonical=False,
                    stage_available="G",
                )
            )

    return tuple(routes)


def routes_for_product(product: int) -> tuple[Route, ...]:
    if product not in ALL_PRODUCTS:
        raise ValueError(f"Unknown TMK product: {product}")

    return _canonical_routes(product) + _derived_routes(product)


def distinct_factor_routes(product: int) -> tuple[dict[str, object], ...]:
    return tuple(
        {
            "product": route.product,
            "type": route.type,
            "source_product": route.source_product,
            "factors": route.factors,
            "operations": route.operations,
            "is_canonical": route.is_canonical,
            "stage_available": route.stage_available,
        }
        for route in routes_for_product(product)
    )


def entry_routes(product: int) -> tuple[dict[str, object], ...]:
    if product not in ALL_PRODUCTS:
        raise ValueError(f"Unknown TMK product: {product}")

    return tuple(
        route
        for route in distinct_factor_routes(product)
        if route["source_product"] is not None
    )


def exit_route_labels(product: int) -> tuple[str, ...]:
    if product not in ALL_PRODUCTS:
        raise ValueError(f"Unknown TMK product: {product}")

    labels: list[str] = []

    for candidate in ALL_PRODUCTS:
        for route in routes_for_product(candidate):
            if route.source_product == product:
                labels.append(f"{product} -> {candidate} ({route.operations[0]})")

    return tuple(labels)


def inverse_labels(product: int) -> tuple[str, ...]:
    record = product_record(product)
    return tuple(
        f"{dividend} ÷ {divisor} = {quotient}"
        for dividend, divisor, quotient in record.inverse_pairs
    )


def shared_factors(a: int, b: int) -> tuple[int, ...]:
    if a not in ALL_PRODUCTS:
        raise ValueError(f"Unknown TMK product: {a}")
    if b not in ALL_PRODUCTS:
        raise ValueError(f"Unknown TMK product: {b}")

    factors_a = {factor for pair in factors_for_product(a) for factor in pair}
    factors_b = {factor for pair in factors_for_product(b) for factor in pair}

    return tuple(sorted(factors_a & factors_b))


def routes_available_at_stage(stage_id: str) -> tuple[Route, ...]:
    products = available_products(stage_id)
    routes: list[Route] = []

    for product in products:
        for route in routes_for_product(product):
            if _stage_at_or_before(route.stage_available, stage_id):
                routes.append(route)

    return tuple(routes)


__all__ = [
    "Route",
    "routes_for_product",
    "routes_available_at_stage",
    "distinct_factor_routes",
    "entry_routes",
    "exit_route_labels",
    "inverse_labels",
    "shared_factors",
]
