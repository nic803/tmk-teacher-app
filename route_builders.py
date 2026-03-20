from __future__ import annotations

from typing import Iterable, Tuple

from route_models import DivisionRoute, MultiplicationRoute


def multiplication_route(left: int, right: int) -> MultiplicationRoute:
    return MultiplicationRoute(left=left, right=right)


def division_route(product: int, divisor: int, quotient: int) -> DivisionRoute:
    return DivisionRoute(product=product, divisor=divisor, quotient=quotient)


def multiplication_routes_from_tuples(
    routes: Iterable[Tuple[int, int]],
) -> Tuple[MultiplicationRoute, ...]:
    return tuple(MultiplicationRoute(left=left, right=right) for left, right in routes)
