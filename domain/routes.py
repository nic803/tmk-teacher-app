from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from domain.products import product_record

@dataclass(frozen=True)
class MultiplicationRoute:
    left: int
    right: int

    @property
    def product(self) -> int:
        return self.left * self.right

    def as_tuple(self) -> tuple[int, int]:
        return (self.left, self.right)

    def as_dict(self) -> dict[str, int]:
        return {"left": self.left, "right": self.right}


@dataclass(frozen=True)
class DivisionRoute:
    product: int
    divisor: int
    quotient: int

    def as_dict(self) -> dict[str, int]:
        return {
            "product": self.product,
            "divisor": self.divisor,
            "quotient": self.quotient,
        }


def multiplication_route(left: int, right: int) -> MultiplicationRoute:
    return MultiplicationRoute(left=left, right=right)


def division_route(product: int, divisor: int, quotient: int) -> DivisionRoute:
    return DivisionRoute(product=product, divisor=divisor, quotient=quotient)


def multiplication_routes_from_tuples(
    routes: Iterable[tuple[int, int]],
) -> tuple[MultiplicationRoute, ...]:
    return tuple(MultiplicationRoute(left=left, right=right) for left, right in routes)


def canonical_route(route: tuple[int, int]) -> tuple[int, int]:
    left, right = route
    return (left, right) if left <= right else (right, left)


def canonical_multiplication_route(route: MultiplicationRoute) -> MultiplicationRoute:
    left, right = canonical_route(route.as_tuple())
    return MultiplicationRoute(left=left, right=right)


def distinct_factor_routes(product: int) -> list[tuple[int, int]]:
    record = product_record(product)
    seen: set[tuple[int, int]] = set()
    routes: list[tuple[int, int]] = []

    intro = canonical_route(tuple(record.intro_route))
    seen.add(intro)
    routes.append(intro)

    for route in record.factor_families:
        canonical = canonical_route(tuple(route))
        if canonical not in seen:
            seen.add(canonical)
            routes.append(canonical)

    return routes


def distinct_multiplication_routes(product: int) -> tuple[MultiplicationRoute, ...]:
    return tuple(
        MultiplicationRoute(left=left, right=right)
        for left, right in distinct_factor_routes(product)
    )


def entry_routes(product: int) -> list[tuple[int, int]]:
    return distinct_factor_routes(product)


def entry_multiplication_routes(product: int) -> tuple[MultiplicationRoute, ...]:
    return distinct_multiplication_routes(product)


def exit_routes(product: int) -> tuple[DivisionRoute, ...]:
    record = product_record(product)
    return tuple(
        DivisionRoute(product=product, divisor=divisor, quotient=quotient)
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
    factors_a = {factor for route in distinct_factor_routes(product_a) for factor in route}
    factors_b = {factor for route in distinct_factor_routes(product_b) for factor in route}
    shared = sorted(factors_a.intersection(factors_b))
    return ", ".join(str(value) for value in shared) if shared else "none"

def render_multiplication_route(route: MultiplicationRoute) -> str:
    return f"{route.left} × {route.right}"


def render_division_route(route: DivisionRoute) -> str:
    return f"{route.product} ÷ {route.divisor} = {route.quotient}"
