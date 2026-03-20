from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Final, Literal, Tuple

from memory_cues import memory_cues_for_product
from patterns import product_pattern_ids
from products import ALL_PRODUCTS, ProductRecord, belongs_to_p10, product_record


Tier = Literal["Support", "Core", "Extension"]

QuestionSection = Literal[
    "product_first",
    "ways_in",
    "ways_out",
    "structure",
    "belongs",
    "error_repair",
    "sorting",
    "final_explanation",
]

QuestionForm = Literal[
    "identify",
    "fill_blank",
    "missing_value",
    "division",
    "true_false",
    "compare_routes",
    "belongs_check",
    "error_repair",
    "sort_routes",
    "explanation",
]

AnswerKind = Literal[
    "number",
    "boolean",
    "route",
    "structured",
]

WORKSHEET_QUESTION_COUNT: Final[int] = 10
VALID_TIERS: Final[Tuple[Tier, ...]] = ("Support", "Core", "Extension")


@dataclass(frozen=True)
class WorksheetQuestion:
    id: int
    section: QuestionSection
    question_form: QuestionForm
    prompt_key: str
    answer_kind: AnswerKind
    prompt_data: Dict[str, object]
    answer_data: Dict[str, object]


@dataclass(frozen=True)
class WorksheetTeacherKey:
    answers: Tuple[Dict[str, object], ...]
    pattern_ids: Tuple[str, ...]
    notes: Tuple[str, ...]


@dataclass(frozen=True)
class Worksheet:
    product: int
    stage: str
    tier: Tier
    questions: Tuple[WorksheetQuestion, ...]
    teacher_key: WorksheetTeacherKey


def generate_worksheet(product: int, tier: Tier) -> Worksheet:

    if product not in ALL_PRODUCTS:
        raise ValueError("Invalid TMK product")

    if tier not in VALID_TIERS:
        raise ValueError("Invalid tier")

    record = product_record(product)

    questions = _build_questions(record, tier)

    teacher_key = WorksheetTeacherKey(
        answers=tuple(q.answer_data for q in questions),
        pattern_ids=product_pattern_ids(product),
        notes=(
            f"Product {record.product}",
            f"Stage {record.stage}",
            f"Intro route {record.intro_route[0]}×{record.intro_route[1]}",
        ),
    )

    return Worksheet(
        product=record.product,
        stage=record.stage,
        tier=tier,
        questions=questions,
        teacher_key=teacher_key,
    )


def generate_worksheet_dict(product: int, tier: Tier) -> Dict[str, object]:
    return asdict(generate_worksheet(product, tier))


def _build_questions(record: ProductRecord, tier: Tier) -> Tuple[WorksheetQuestion, ...]:

    p = record.product
    a, b = record.intro_route

    other = _other_route(record)

    questions = [

        WorksheetQuestion(
            1,
            "product_first",
            "identify",
            "identify_product",
            "number",
            {"product": p},
            {"value": p},
        ),

        WorksheetQuestion(
            2,
            "ways_in",
            "fill_blank",
            "complete_way_in",
            "number",
            {"left": a, "product": p},
            {"value": b},
        ),

        WorksheetQuestion(
            3,
            "ways_in",
            "missing_value",
            "missing_factor",
            "number",
            {"right": b, "product": p},
            {"value": a},
        ),

        WorksheetQuestion(
            4,
            "ways_out",
            "division",
            "division_way_out",
            "number",
            {"product": p, "divisor": a},
            {"value": b},
        ),

        WorksheetQuestion(
            5,
            "structure",
            "true_false",
            "check_equation",
            "boolean",
            {"left": a, "right": b, "product": p},
            {"value": True},
        ),

        WorksheetQuestion(
            6,
            "structure",
            "compare_routes",
            "compare_routes",
            "structured",
            {
                "product": p,
                "route_a": {"left": a, "right": b},
                "route_b": other,
            },
            {"comparison": "same_product"},
        ),

        WorksheetQuestion(
            7,
            "belongs",
            "belongs_check",
            "belongs_question",
            "boolean",
            {"candidate": p},
            {"value": True},
        ),

        WorksheetQuestion(
            8,
            "error_repair",
            "error_repair",
            "repair_equation",
            "structured",
            {"left": a, "right": b + 1, "product": p},
            {"correct": {"left": a, "right": b, "product": p}},
        ),

        WorksheetQuestion(
            9,
            "sorting",
            "sort_routes",
            "sort_equations",
            "structured",
            {
                "product": p,
                "routes": _route_examples(record),
            },
            {"valid_routes": record.ways_in},
        ),

        WorksheetQuestion(
            10,
            "final_explanation",
            "explanation",
            "explain_product",
            "structured",
            {"product": p},
            {"accepted_routes": record.ways_in},
        ),

    ]

    return tuple(questions)


def _other_route(record: ProductRecord):

    for r in record.ways_in:
        if r != record.intro_route:
            return {"left": r[0], "right": r[1]}

    return {"left": record.intro_route[1], "right": record.intro_route[0]}


def _route_examples(record: ProductRecord):

    examples = list(record.ways_in)

    if len(examples) < 3:
        examples.append((record.intro_route[0], record.intro_route[1] + 1))

    return examples
