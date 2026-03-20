from __future__ import annotations

from typing import Iterable, Tuple

from route_models import DivisionRoute, MultiplicationRoute
from route_render import render_division_route, render_multiplication_route


def render_teacher_answer(answer_data: dict) -> str:
    if "value" in answer_data and len(answer_data) == 1:
        return str(answer_data["value"])

    if "value" in answer_data and "route" in answer_data:
        route = _route_from_data(answer_data["route"])
        return f"{answer_data['value']} ({render_multiplication_route(route)})"

    if "division" in answer_data:
        division = _division_from_data(answer_data["division"])
        return render_division_route(division)

    if "route" in answer_data:
        route = _route_from_data(answer_data["route"])
        return render_multiplication_route(route)

    if "accepted_routes" in answer_data:
        routes = _routes_from_iterable(answer_data["accepted_routes"])
        return "; ".join(render_multiplication_route(r) for r in routes)

    if "valid_routes" in answer_data:
        routes = _routes_from_iterable(answer_data["valid_routes"])
        return "; ".join(render_multiplication_route(r) for r in routes)

    if "correct_equation" in answer_data:
        route = _route_from_data(answer_data["correct_equation"])
        return f"{render_multiplication_route(route)} = {route.product}"

    if "classification" in answer_data:
        return str(answer_data["classification"])

    if "comparison" in answer_data:
        return str(answer_data["comparison"])

    if "value" in answer_data and isinstance(answer_data["value"], bool):
        return "Yes" if answer_data["value"] else "No"

    return str(answer_data)


def render_teacher_answers(answer_payloads: Iterable[dict]) -> Tuple[str, ...]:
    return tuple(render_teacher_answer(answer) for answer in answer_payloads)


def _route_from_data(data) -> MultiplicationRoute:
    if isinstance(data, MultiplicationRoute):
        return data

    if isinstance(data, dict):
        return MultiplicationRoute(left=data["left"], right=data["right"])

    if isinstance(data, (tuple, list)) and len(data) == 2:
        return MultiplicationRoute(left=data[0], right=data[1])

    raise ValueError(f"Cannot interpret route data: {data}")


def _routes_from_iterable(routes) -> Tuple[MultiplicationRoute, ...]:
    return tuple(_route_from_data(route) for route in routes)


def _division_from_data(data) -> DivisionRoute:
    if isinstance(data, DivisionRoute):
        return data

    if isinstance(data, dict):
        return DivisionRoute(
            product=data["product"],
            divisor=data["divisor"],
            quotient=data["quotient"],
        )

    raise ValueError(f"Cannot interpret division data: {data}")
