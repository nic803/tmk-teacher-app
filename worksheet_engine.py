from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple

from memory_cues import memory_cues_for_product
from patterns import product_pattern_ids
from products import ALL_PRODUCTS, product_record
from question_form_engine import QuestionSpec, build_question_spec
from tier_policy import Tier
from worksheet_blueprints import blueprint_for_tier
from worksheet_policy import (
    validate_question_count,
    validate_supported_tier,
    worksheet_memory_cue_mode,
)


@dataclass(frozen=True)
class TeacherKey:
    answers: Tuple[Dict[str, object], ...]
    pattern_ids: Tuple[str, ...]
    memory_cue_ids: Tuple[str, ...]
    notes: Tuple[str, ...]


@dataclass(frozen=True)
class WorksheetPackage:
    product: int
    stage: str
    tier: Tier
    questions: Tuple[QuestionSpec, ...]
    teacher_key: TeacherKey


def generate_worksheet(product: int, tier: Tier) -> WorksheetPackage:
    _validate_product(product)
    validate_supported_tier(tier)

    record = product_record(product)
    blueprint = blueprint_for_tier(tier)

    questions = tuple(
        build_question_spec(record, tier, slot)
        for slot in blueprint.slots
    )

    validate_question_count(len(questions))

    teacher_key = _build_teacher_key(product, questions)

    worksheet = WorksheetPackage(
        product=record.product,
        stage=record.stage,
        tier=tier,
        questions=questions,
        teacher_key=teacher_key,
    )

    _validate_worksheet_package(worksheet)

    return worksheet


def generate_worksheet_dict(product: int, tier: Tier) -> Dict[str, object]:
    return asdict(generate_worksheet(product, tier))


def _build_teacher_key(
    product: int,
    questions: Tuple[QuestionSpec, ...],
) -> TeacherKey:
    record = product_record(product)
    memory_cues = memory_cues_for_product(product)
    memory_cue_ids = _teacher_memory_cue_ids(memory_cues)

    return TeacherKey(
        answers=tuple(question.answer_data for question in questions),
        pattern_ids=product_pattern_ids(product),
        memory_cue_ids=memory_cue_ids,
        notes=(
            f"Product: {record.product}",
            f"Stage: {record.stage}",
            f"Intro route: {record.intro_route[0]} × {record.intro_route[1]}",
            f"Structural role: {record.structural_role}",
            f"Factor families: {len(record.factor_families)}",
        ),
    )


def _teacher_memory_cue_ids(memory_cues: Tuple[object, ...]) -> Tuple[str, ...]:
    mode = worksheet_memory_cue_mode()
    if mode != "teacher_key_only":
        return ()
    return tuple(cue.id for cue in memory_cues)


def _validate_product(product: int) -> None:
    if product not in ALL_PRODUCTS:
        raise ValueError(f"Unknown TMK product: {product}")


def _validate_worksheet_package(worksheet: WorksheetPackage) -> None:
    validate_question_count(len(worksheet.questions))

    if worksheet.product not in ALL_PRODUCTS:
        raise ValueError(f"Worksheet contains invalid product: {worksheet.product}")

    if worksheet.tier not in ("Support", "Core", "Extension"):
        raise ValueError(f"Worksheet contains invalid tier: {worksheet.tier}")

    question_ids = tuple(question.id for question in worksheet.questions)
    expected_ids = tuple(range(1, len(worksheet.questions) + 1))

    if question_ids != expected_ids:
        raise ValueError(
            f"Worksheet question ids must be sequential. "
            f"Expected {expected_ids}, found {question_ids}."
        )

    question_forms = tuple(question.question_form for question in worksheet.questions)
    if len(question_forms) != len(worksheet.questions):
        raise ValueError("Worksheet question forms are inconsistent.")

    prompt_keys = tuple(question.prompt_key for question in worksheet.questions)
    if any(not prompt_key for prompt_key in prompt_keys):
        raise ValueError("Worksheet contains an empty prompt key.")


def attached_pattern_ids(product: int) -> Tuple[str, ...]:
    return product_pattern_ids(product)
