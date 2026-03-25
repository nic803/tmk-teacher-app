from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domain.routes import distinct_factor_routes
from products import product_record, stage_label


@dataclass(frozen=True)
class WorksheetQuestion:
    id: int
    pupil_prompt: str


@dataclass(frozen=True)
class TeacherKey:
    answers: tuple[str, ...]
    notes: tuple[str, ...]


@dataclass(frozen=True)
class Worksheet:
    product: int
    stage: str
    tier: str
    questions: tuple[WorksheetQuestion, ...]
    teacher_key: TeacherKey


def generate_worksheet(product: int, tier: str) -> Worksheet:
    record = product_record(product)
    stage = stage_label(record.stage)

    intro_route = _coerce_route(record.intro_route)
    routes = _coerce_routes(distinct_factor_routes(product))
    exits = _coerce_exits(getattr(record, "ways_out", ()))

    alt_route = _first_non_intro_route(routes, intro_route)
    third_route = _next_distinct_route(routes, {intro_route, alt_route})
    fourth_route = _next_distinct_route(routes, {intro_route, alt_route, third_route})

    exit_1 = exits[0] if len(exits) > 0 else (intro_route[0], intro_route[1])
    exit_2 = exits[1] if len(exits) > 1 else (alt_route[0], alt_route[1])
    exit_3 = exits[2] if len(exits) > 2 else (intro_route[1], intro_route[0])

    if tier == "Support":
        questions = (
            WorksheetQuestion(1, f"Complete: {intro_route[0]} × {intro_route[1]} = ____"),
            WorksheetQuestion(2, f"Write the product for {intro_route[0]} × {intro_route[1]}."),
            WorksheetQuestion(3, f"Complete: {product} ÷ {intro_route[0]} = ____"),
            WorksheetQuestion(4, f"Complete: {product} ÷ {intro_route[1]} = ____"),
            WorksheetQuestion(5, f"Complete: {intro_route[0]} × ____ = {product}"),
            WorksheetQuestion(6, f"Complete: ____ × {intro_route[1]} = {product}"),
            WorksheetQuestion(7, f"Which stage introduces {product}?"),
            WorksheetQuestion(8, f"Complete: {exit_1[0]} × {exit_1[1]} = ____"),
            WorksheetQuestion(9, f"Complete: {product} ÷ {exit_2[0]} = ____"),
            WorksheetQuestion(10, f"Write the intro route for {product}."),
        )
        answers = (
            str(product),
            str(product),
            str(intro_route[1]),
            str(intro_route[0]),
            str(intro_route[1]),
            str(intro_route[0]),
            stage,
            str(product),
            str(exit_2[1]),
            _format_route(intro_route),
        )
        notes = (
            f"{product} is introduced in {stage} through {_format_route(intro_route)}.",
            "Support tier stays anchored to the pedagogical intro route and linked inverse division facts.",
        )

    elif tier == "Core":
        questions = (
            WorksheetQuestion(1, f"Complete: {intro_route[0]} × {intro_route[1]} = ____"),
            WorksheetQuestion(2, f"Write another valid route for {product}: {alt_route[0]} × ____ = {product}"),
            WorksheetQuestion(3, f"Complete: {product} ÷ {exit_1[0]} = ____"),
            WorksheetQuestion(4, f"What stage introduces {product}?"),
            WorksheetQuestion(5, f"Complete: {alt_route[0]} × {alt_route[1]} = ____"),
            WorksheetQuestion(6, f"Complete: {product} ÷ {exit_2[0]} = ____"),
            WorksheetQuestion(7, f"Write the intro route for {product}."),
            WorksheetQuestion(8, f"Complete: ____ × {alt_route[1]} = {product}"),
            WorksheetQuestion(9, f"Is {_format_route(intro_route)} a valid route for {product}?"),
            WorksheetQuestion(10, f"Complete: {exit_3[0]} × {exit_3[1]} = ____"),
        )
        answers = (
            str(product),
            str(alt_route[1]),
            str(exit_1[1]),
            stage,
            str(product),
            str(exit_2[1]),
            _format_route(intro_route),
            str(alt_route[0]),
            "Yes",
            str(product),
        )
        notes = (
            f"Core tier anchors on intro route {_format_route(intro_route)} plus one additional admissible route.",
            "Division remains linked to the same product.",
        )

    elif tier == "Extension":
        extension_routes = routes if routes else (intro_route,)
        route_answer = ", ".join(_format_route(route) for route in extension_routes)

        questions = (
            WorksheetQuestion(1, f"List the distinct multiplication routes for {product}."),
            WorksheetQuestion(2, f"Which stage introduces {product}?"),
            WorksheetQuestion(3, f"Complete: {product} ÷ {exit_1[0]} = ____"),
            WorksheetQuestion(4, f"Explain why {_format_route(intro_route)} is used as the intro route for {product}."),
            WorksheetQuestion(5, f"Complete: {alt_route[0]} × {alt_route[1]} = ____"),
            WorksheetQuestion(6, f"Complete: {third_route[0]} × {third_route[1]} = ____"),
            WorksheetQuestion(7, f"Complete: {product} ÷ {exit_2[0]} = ____"),
            WorksheetQuestion(8, f"Write one non-intro valid route for {product}."),
            WorksheetQuestion(9, f"Complete: {fourth_route[0]} × {fourth_route[1]} = ____"),
            WorksheetQuestion(10, f"How many distinct multiplication routes does {product} have?"),
        )
        answers = (
            route_answer,
            stage,
            str(exit_1[1]),
            f"It is the pedagogical introduction route for {product}.",
            str(product),
            str(product),
            str(exit_2[1]),
            _format_route(alt_route),
            str(product),
            str(len(routes)),
        )
        notes = (
            "Extension tier can expose the wider admissible route set without breaking product-first structure.",
            f"{product} has {len(routes)} distinct multiplication route(s) and {len(exits)} division exit route(s).",
        )

    else:
        raise ValueError(f"Unsupported worksheet tier: {tier}")

    if len(questions) != 10:
        raise ValueError(f"Worksheet must contain exactly 10 questions, got {len(questions)}")

    return Worksheet(
        product=product,
        stage=stage,
        tier=tier,
        questions=questions,
        teacher_key=TeacherKey(
            answers=answers,
            notes=notes,
        ),
    )


def _format_route(route: tuple[int, int]) -> str:
    return f"{route[0]}×{route[1]}"


def _coerce_route(value: Any) -> tuple[int, int]:
    if isinstance(value, (tuple, list)) and len(value) == 2:
        return (int(value[0]), int(value[1]))
    raise ValueError(f"Invalid intro route: {value!r}")


def _coerce_routes(value: Any) -> tuple[tuple[int, int], ...]:
    if value is None:
        return ()

    routes: list[tuple[int, int]] = []
    for item in value:
        if isinstance(item, (tuple, list)) and len(item) == 2:
            routes.append((int(item[0]), int(item[1])))
        else:
            raise ValueError(f"Invalid route entry: {item!r}")

    return tuple(routes)


def _coerce_exits(value: Any) -> tuple[tuple[int, int], ...]:
    if value is None:
        return ()

    exits: list[tuple[int, int]] = []
    for item in value:
        if isinstance(item, (tuple, list)) and len(item) == 2:
            exits.append((int(item[0]), int(item[1])))
        else:
            raise ValueError(f"Invalid exit entry: {item!r}")

    return tuple(exits)


def _first_non_intro_route(
    routes: tuple[tuple[int, int], ...],
    intro_route: tuple[int, int],
) -> tuple[int, int]:
    for route in routes:
        if route != intro_route:
            return route
    return intro_route


def _next_distinct_route(
    routes: tuple[tuple[int, int], ...],
    used: set[tuple[int, int]],
) -> tuple[int, int]:
    for route in routes:
        if route not in used:
            return route
    return next(iter(used))
