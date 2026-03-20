from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Tuple, Literal, Final

from products import product_record, ALL_PRODUCTS
from patterns import product_pattern_ids
from memory_cues import memory_cues_for_product

Tier = Literal["Support", "Core", "Extension"]

QuestionForm = Literal[
    "circle",
    "fill_blank",
    "match",
    "yes_no",
    "complete",
    "find",
    "true_false",
    "compare",
    "simple_sort",
    "compare_routes",
    "odd_one_out",
    "true_outside_false",
    "sort_and_justify",
    "rebuild_and_explain",
]

VALID_TIERS: Final[Tuple[Tier, ...]] = ("Support", "Core", "Extension")


@dataclass(frozen=True)
class WorksheetQuestion:
    id: int
    question_form: QuestionForm
    prompt_key: str
    prompt_data: Dict[str, object]
    answer_data: Dict[str, object]


@dataclass(frozen=True)
class WorksheetTeacherKey:
    answers: Tuple[Dict[str, object], ...]
    pattern_ids: Tuple[str, ...]
    memory_cues: Tuple[str, ...]


@dataclass(frozen=True)
class Worksheet:
    product: int
    stage: str
    tier: Tier
    questions: Tuple[WorksheetQuestion, ...]
    teacher_key: WorksheetTeacherKey


def generate_worksheet(product: int, tier: Tier) -> Worksheet:

    if product not in ALL_PRODUCTS:
        raise ValueError("Invalid product")

    if tier not in VALID_TIERS:
        raise ValueError("Invalid tier")

    record = product_record(product)

    questions = _build_questions(record, tier)

    teacher_key = WorksheetTeacherKey(
        answers=tuple(q.answer_data for q in questions),
        pattern_ids=product_pattern_ids(product),
        memory_cues=tuple(c.id for c in memory_cues_for_product(product)),
    )

    return Worksheet(
        product=record.product,
        stage=record.stage,
        tier=tier,
        questions=questions,
        teacher_key=teacher_key,
    )


def generate_worksheet_dict(product: int, tier: Tier):
    return asdict(generate_worksheet(product, tier))


def _build_questions(record, tier):

    if tier == "Support":
        return _support_questions(record)

    if tier == "Core":
        return _core_questions(record)

    return _extension_questions(record)


# ---------------- SUPPORT ----------------


def _support_questions(record):

    p = record.product
    a, b = record.intro_route

    return (
        WorksheetQuestion(
            1,
            "circle",
            "circle_product",
            {"product": p},
            {"value": p},
        ),
        WorksheetQuestion(
            2,
            "fill_blank",
            "complete_way_in",
            {"left": a, "product": p},
            {"value": b},
        ),
        WorksheetQuestion(
            3,
            "match",
            "match_route",
            {"product": p, "route": (a, b)},
            {"route": (a, b)},
        ),
        WorksheetQuestion(
            4,
            "fill_blank",
            "division",
            {"product": p, "divisor": a},
            {"value": b},
        ),
        WorksheetQuestion(
            5,
            "yes_no",
            "belongs_yes_no",
            {"candidate": p},
            {"value": True},
        ),
        WorksheetQuestion(
            6,
            "match",
            "match_way_in_out",
            {"product": p},
            {"route": (a, b)},
        ),
        WorksheetQuestion(
            7,
            "yes_no",
            "is_route",
            {"left": a, "right": b},
            {"value": True},
        ),
        WorksheetQuestion(
            8,
            "fill_blank",
            "repair_equation",
            {"left": a, "product": p},
            {"value": b},
        ),
        WorksheetQuestion(
            9,
            "match",
            "choose_route",
            {"product": p},
            {"route": (a, b)},
        ),
        WorksheetQuestion(
            10,
            "fill_blank",
            "belongs_reason",
            {"product": p},
            {"route": (a, b)},
        ),
    )


# ---------------- CORE ----------------


def _core_questions(record):

    p = record.product
    a, b = record.intro_route

    return (
        WorksheetQuestion(
            1,
            "find",
            "find_product",
            {"product": p},
            {"value": p},
        ),
        WorksheetQuestion(
            2,
            "complete",
            "complete_way_in",
            {"left": a, "product": p},
            {"value": b},
        ),
        WorksheetQuestion(
            3,
            "find",
            "find_other_way",
            {"product": p},
            {"route": record.ways_in[0]},
        ),
        WorksheetQuestion(
            4,
            "complete",
            "division",
            {"product": p, "divisor": a},
            {"value": b},
        ),
        WorksheetQuestion(
            5,
            "true_false",
            "check_equation",
            {"left": a, "right": b, "product": p},
            {"value": True},
        ),
        WorksheetQuestion(
            6,
            "compare",
            "compare_routes",
            {"product": p},
            {"routes": record.ways_in},
        ),
        WorksheetQuestion(
            7,
            "find",
            "belongs_check",
            {"candidate": p},
            {"value": True},
        ),
        WorksheetQuestion(
            8,
            "complete",
            "repair_equation",
            {"left": a, "product": p},
            {"value": b},
        ),
        WorksheetQuestion(
            9,
            "simple_sort",
            "sort_routes",
            {"routes": record.ways_in},
            {"routes": record.ways_in},
        ),
        WorksheetQuestion(
            10,
            "compare",
            "rebuild_product",
            {"product": p},
            {"routes": record.ways_in},
        ),
    )


# ---------------- EXTENSION ----------------


def _extension_questions(record):

    p = record.product
    routes = record.ways_in

    return (
        WorksheetQuestion(
            1,
            "compare_routes",
            "compare_routes",
            {"product": p, "routes": routes},
            {"routes": routes},
        ),
        WorksheetQuestion(
            2,
            "true_outside_false",
            "true_outside_false",
            {"product": p},
            {"value": True},
        ),
        WorksheetQuestion(
            3,
            "odd_one_out",
            "odd_one_out",
            {"routes": routes},
            {"route": routes[0]},
        ),
        WorksheetQuestion(
            4,
            "compare_routes",
            "compare_routes",
            {"product": p},
            {"routes": routes},
        ),
        WorksheetQuestion(
            5,
            "sort_and_justify",
            "sort_routes",
            {"routes": routes},
            {"routes": routes},
        ),
        WorksheetQuestion(
            6,
            "compare_routes",
            "compare_routes",
            {"product": p},
            {"routes": routes},
        ),
        WorksheetQuestion(
            7,
            "true_outside_false",
            "boundary_check",
            {"product": p},
            {"value": True},
        ),
        WorksheetQuestion(
            8,
            "rebuild_and_explain",
            "rebuild_product",
            {"product": p},
            {"routes": routes},
        ),
        WorksheetQuestion(
            9,
            "sort_and_justify",
            "sort_routes",
            {"routes": routes},
            {"routes": routes},
        ),
        WorksheetQuestion(
            10,
            "rebuild_and_explain",
            "explain_product",
            {"product": p},
            {"routes": routes},
        ),
    )
