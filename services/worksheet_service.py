from __future__ import annotations

from dataclasses import dataclass
from typing import Any

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

    routes = _coerce_routes(getattr(record, "ways_in", ()))
    exits = _coerce_exits(getattr(record, "ways_out", ()))
    intro_route = tuple(record.intro_route)

    if tier == "Support":
        questions = (
            WorksheetQuestion(1, f"Complete: {intro_route[0]} × {intro_route[1]} = {product}"),
            WorksheetQuestion(2, f"Write the product for {intro_route[0]} × {intro_route[1]}."),
            WorksheetQuestion(3, f"Complete: {product} ÷ {intro_route[0]} = ____"),
            WorksheetQuestion(4, f"Complete: {product} ÷ {intro_route[1]} = ____"),
        )
        answers = (
            str(product),
            str(product),
            str(intro_route[1]),
            str(intro_route[0]),
        )
        notes = (
            f"{product} is introduced in {stage} through {_format_route(intro_route)}.",
            "Support tier stays close to the pedagogical intro route and linked inverse division facts.",
        )

    elif tier == "Extension":
        distinct_routes = routes[:4] if routes else (intro_route,)
        q1 = ", ".join(_format_route(route) for route in distinct_routes)
        q2_divisor, q2_quotient = exits[0] if exits else (intro_route[0], intro_route[1])

        questions = (
            WorksheetQuestion(1, f"List all distinct multiplication routes you know for {product}."),
            WorksheetQuestion(2, f"Which stage introduces {product}?"),
            WorksheetQuestion(3, f"Complete: {product} ÷ {q2_divisor} = ____"),
            WorksheetQuestion(4, f"Explain why {_format_route(intro_route)} is an intro route for {product}."),
        )
        answers = (
            q1,
            stage,
            str(q2_quotient),
            f"It is the pedagogical introduction route for {product}.",
        )
        notes = (
            "Extension tier can include multiple admissible routes, but must preserve the product-first structure.",
            f"{product} has {len(routes)} distinct multiplication route(s) and {len(exits)} division exit route(s).",
        )

    else:  # Core
        q1_divisor, q1_quotient = exits[0] if exits else (intro_route[0], intro_route[1])
        alt_route = routes[1] if len(routes) > 1 else intro_route

        questions = (
            WorksheetQuestion(1, f"Complete: {intro_route[0]} × {intro_route[1]} = ____"),
            WorksheetQuestion(2, f"Write another route for {product}: {alt_route[0]} × ____ = {product}"),
            WorksheetQuestion(3, f"Complete: {product} ÷ {q1_divisor} = ____"),
            WorksheetQuestion(4, f"What stage introduces {product}?"),
        )
        answers = (
            str(product),
            str(alt_route[1]),
            str(q1_quotient),
            stage,
        )
        notes = (
            f"Core tier anchors on intro route {_format_route(intro_route)} and one additional valid route.",
            "Division questions must stay linked to the same product.",
        )

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


def _coerce_routes(value: Any) -> tuple[tuple[int, int], ...]:
    if value is None:
        return ()

    routes: list[tuple[int, int]] = []
    for item in value:
        if isinstance(item, tuple) and len(item) == 2:
            routes.append((int(item[0]), int(item[1])))
        elif isinstance(item, list) and len(item) == 2:
            routes.append((int(item[0]), int(item[1])))

    return tuple(routes)


def _coerce_exits(value: Any) -> tuple[tuple[int, int], ...]:
    if value is None:
        return ()

    exits: list[tuple[int, int]] = []
    for item in value:
        if isinstance(item, tuple) and len(item) == 2:
            exits.append((int(item[0]), int(item[1])))
        elif isinstance(item, list) and len(item) == 2:
            exits.append((int(item[0]), int(item[1])))

    return tuple(exits)
