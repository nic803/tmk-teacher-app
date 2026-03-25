from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from products import product_record


@dataclass(frozen=True)
class MultiplicationRoute:
    left: int
    right: int


@dataclass(frozen=True)
class DivisionRoute:
    product: int
    divisor: int
    quotient: int


def multiplication_route(left: int, right: int) -> MultiplicationRoute:
    return MultiplicationRoute(left=left, right=right)


def division_route(product: int, divisor: int, quotient: int) -> DivisionRoute:
    return DivisionRoute(product=product, divisor=divisor, quotient=quotient)


def multiplication_routes_from_tuples(
    routes: Iterable[tuple[int, int]],
) -> tuple[MultiplicationRoute, ...]:
    return tuple(MultiplicationRoute(left=left, right=right) for left, right in routes)


def canonical_route(route: tuple[int, int]) -> tuple[int, int]:
    a, b = route
    return (a, b) if a <= b else (b, a)


def distinct_factor_routes(product: int) -> list[tuple[int, int]]:
    record = product_record(product)
    seen: set[tuple[int, int]] = set()
    routes: list[tuple[int, int]] = []

    intro = canonical_route(record.intro_route)
    seen.add(intro)
    routes.append(intro)

    for route in record.factor_families:
        canonical = canonical_route(route)
        if canonical not in seen:
            seen.add(canonical)
            routes.append(canonical)

    return routes


def entry_routes(product: int) -> list[tuple[int, int]]:
    return distinct_factor_routes(product)


def exit_routes(product: int) -> tuple[DivisionRoute, ...]:
    record = product_record(product)
    return tuple(
        division_route(product=product, divisor=divisor, quotient=quotient)
        for divisor, quotient in record.ways_out
    )


def exit_route_labels(product: int, limit: int | None = None) -> list[str]:
    labels = [f"{route.product}÷{route.divisor}={route.quotient}" for route in exit_routes(product)]
    if limit is None:
        return labels
    return labels[:limit]


def inverse_labels(product: int) -> tuple[str, ...]:
    return tuple(f"{route.product}÷{route.divisor}={route.quotient}" for route in exit_routes(product))


def shared_factors(product_a: int, product_b: int) -> str:
    factors_a = {n for route in distinct_factor_routes(product_a) for n in route}
    factors_b = {n for route in distinct_factor_routes(product_b) for n in route}
    shared = sorted(factors_a.intersection(factors_b))
    return ", ".join(str(n) for n in shared) if shared else "none"
