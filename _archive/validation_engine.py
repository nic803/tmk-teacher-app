from __future__ import annotations

from typing import Iterable, Tuple

from products import ALL_PRODUCTS
from question_form_engine import QuestionSpec
from tier_policy import Tier, form_allowed_for_tier
from worksheet_policy import (
    validate_question_count,
    validate_supported_tier,
)
from worlds import forbidden_world_phrases


def validate_worksheet_structure(
    product: int,
    tier: Tier,
    questions: Tuple[QuestionSpec, ...],
) -> None:
    _validate_product(product)
    validate_supported_tier(tier)
    validate_question_count(len(questions))

    _validate_question_ids(questions)
    _validate_question_forms(tier, questions)
    _validate_prompt_keys(questions)


def validate_prompt_wording(prompts: Iterable[str]) -> None:
    forbidden = forbidden_world_phrases()

    for prompt in prompts:
        for phrase in forbidden:
            if phrase in prompt:
                raise ValueError(
                    f"Forbidden wording detected: '{phrase}' in '{prompt}'"
                )


def _validate_product(product: int) -> None:
    if product not in ALL_PRODUCTS:
        raise ValueError(f"Invalid TMK product: {product}")


def _validate_question_ids(questions: Tuple[QuestionSpec, ...]) -> None:
    expected = tuple(range(1, len(questions) + 1))
    actual = tuple(question.id for question in questions)

    if actual != expected:
        raise ValueError(
            f"Question IDs must be sequential. Expected {expected}, found {actual}"
        )


def _validate_question_forms(
    tier: Tier,
    questions: Tuple[QuestionSpec, ...],
) -> None:
    for question in questions:
        if not form_allowed_for_tier(tier, question.question_form):
            raise ValueError(
                f"Form '{question.question_form}' not allowed for tier '{tier}'."
            )


def _validate_prompt_keys(questions: Tuple[QuestionSpec, ...]) -> None:
    for question in questions:
        if not question.prompt_key:
            raise ValueError(f"Question {question.id} has empty prompt key.")


def validate_teacher_key_answers(
    answers: Tuple[dict, ...],
) -> None:
    for index, answer in enumerate(answers, start=1):
        if not isinstance(answer, dict):
            raise ValueError(
                f"Teacher answer {index} must be a dictionary."
            )
