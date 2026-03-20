from __future__ import annotations

from typing import Dict, Iterable, Tuple


def render_teacher_answer(answer_data: Dict[str, object]) -> str:
    if "value" in answer_data and len(answer_data) == 1:
        return str(answer_data["value"])

    if "value" in answer_data and "route" in answer_data:
        route = answer_data["route"]
        return f"{answer_data['value']} ({route['left']} × {route['right']})"

    if "value" in answer_data and "division" in answer_data:
        division = answer_data["division"]
        return (
            f"{answer_data['value']} "
            f"({division['product']} ÷ {division['divisor']} = {division['quotient']})"
        )

    if "route" in answer_data and isinstance(answer_data["route"], dict):
        route = answer_data["route"]
        return f"{route['left']} × {route['right']}"

    if "division" in answer_data and isinstance(answer_data["division"], dict):
        division = answer_data["division"]
        return f"{division['product']} ÷ {division['divisor']} = {division['quotient']}"

    if "comparison" in answer_data:
        return str(answer_data["comparison"])

    if "classification" in answer_data:
        return str(answer_data["classification"])

    if "odd_one_out" in answer_data:
        route = answer_data["odd_one_out"]["route"]
        return f"{route['left']} × {route['right']}"

    if "accepted_routes" in answer_data:
        return "; ".join(_format_route_item(route) for route in answer_data["accepted_routes"])

    if "valid_routes" in answer_data:
        return "; ".join(_format_route_item(route) for route in answer_data["valid_routes"])

    if "valid" in answer_data and "outside" in answer_data and "false" in answer_data:
        valid = ", ".join(_format_classified_option(item) for item in answer_data["valid"])
        outside = ", ".join(_format_classified_option(item) for item in answer_data["outside"])
        false = ", ".join(_format_classified_option(item) for item in answer_data["false"])
        return f"Inside: {valid} | Outside: {outside} | False: {false}"

    if "correct_equation" in answer_data:
        eq = answer_data["correct_equation"]
        return f"{eq['left']} × {eq['right']} = {eq['product']}"

    if "value" in answer_data and isinstance(answer_data["value"], bool):
        return "Yes" if answer_data["value"] else "No"

    return str(answer_data)


def render_teacher_answers(answer_payloads: Iterable[Dict[str, object]]) -> Tuple[str, ...]:
    return tuple(render_teacher_answer(answer_data) for answer_data in answer_payloads)


def _format_route_item(route: object) -> str:
    if isinstance(route, dict):
        if "left" in route and "right" in route:
            return f"{route['left']} × {route['right']}"
        if "route" in route:
            inner = route["route"]
            return f"{inner['left']} × {inner['right']}"
    if isinstance(route, (tuple, list)) and len(route) == 2:
        return f"{route[0]} × {route[1]}"
    return str(route)


def _format_classified_option(option: Dict[str, object]) -> str:
    route = option["route"]
    return f"{route['left']} × {route['right']}"
