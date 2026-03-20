from __future__ import annotations

from route_models import DivisionRoute, MultiplicationRoute


def render_multiplication_route(route: MultiplicationRoute) -> str:
    return f"{route.left} × {route.right}"


def render_division_route(route: DivisionRoute) -> str:
    return f"{route.product} ÷ {route.divisor} = {route.quotient}"
