from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from products import ALL_PRODUCTS, product_record
from question_form_engine import QuestionSpec, build_question_spec
from teacher_key_engine import TeacherKey, build_teacher_key
from tier_policy import Tier
from validation_engine import validate_worksheet_structure
from worksheet_blueprints import blueprint_for_tier
from worksheet_policy import validate_supported_tier


@dataclass(frozen=True)
class WorksheetPackage:
    product: int
    stage: str
    tier: Tier
    questions: Tuple[QuestionSpec, ...]
    teacher_key: TeacherKey


def generate_worksheet(
    product: int,
    tier: Tier,
) -> WorksheetPackage:
    _validate_product(product)
    validate_supported_tier(tier)

    record = product_record(product)
    blueprint = blueprint_for_tier(tier)

    questions = tuple(
        build_question_spec(record, tier, slot)
        for slot in blueprint.slots
    )

    validate_worksheet_structure(product, tier, questions)

    teacher_key = build_teacher_key(product, questions)

    worksheet = WorksheetPackage(
        product=record.product,
        stage=record.stage,
        tier=tier,
        questions=questions,
        teacher_key=teacher_key,
    )

    _validate_worksheet_package(worksheet)

    return worksheet


def _validate_product(product: int) -> None:
    if product not in ALL_PRODUCTS:
        raise ValueError(f"Unknown TMK product: {product}")


def _validate_worksheet_package(worksheet: WorksheetPackage) -> None:
    if worksheet.product not in ALL_PRODUCTS:
        raise ValueError(
            f"Worksheet contains invalid product: {worksheet.product}"
        )

    if worksheet.tier not in ("Support", "Core", "Extension"):
        raise ValueError(
            f"Worksheet contains invalid tier: {worksheet.tier}"
        )

    question_ids = tuple(question.id for question in worksheet.questions)
    expected_ids = tuple(range(1, len(worksheet.questions) + 1))

    if question_ids != expected_ids:
        raise ValueError(
            "Worksheet question IDs must be sequential."
        )

    for question in worksheet.questions:
        if not question.prompt_key:
            raise ValueError(
                f"Question {question.id} has empty prompt key."
            )
