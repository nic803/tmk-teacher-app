from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from models.worksheet_models import (
    APPROVED_PUPIL_ITEM_FAMILIES,
    APPROVED_QUIZ_FORMATS,
    FORBIDDEN_PUPIL_ITEM_TYPES,
    QuizFormat,
    WorksheetItemFamily,
    WorksheetTier,
    validate_item_family,
    validate_quiz_format,
    validate_tier,
)


@dataclass(frozen=True)
class WorksheetTaxonomyPolicy:
    approved_item_families: Tuple[WorksheetItemFamily, ...]
    approved_quiz_formats: Tuple[QuizFormat, ...]
    forbidden_pupil_item_types: Tuple[str, ...]


_CANONICAL_POLICY = WorksheetTaxonomyPolicy(
    approved_item_families=APPROVED_PUPIL_ITEM_FAMILIES,
    approved_quiz_formats=APPROVED_QUIZ_FORMATS,
    forbidden_pupil_item_types=FORBIDDEN_PUPIL_ITEM_TYPES,
)


def taxonomy_policy() -> WorksheetTaxonomyPolicy:
    return _CANONICAL_POLICY


def approved_item_families() -> Tuple[WorksheetItemFamily, ...]:
    return APPROVED_PUPIL_ITEM_FAMILIES


def approved_quiz_formats() -> Tuple[QuizFormat, ...]:
    return APPROVED_QUIZ_FORMATS


def forbidden_pupil_item_types() -> Tuple[str, ...]:
    return FORBIDDEN_PUPIL_ITEM_TYPES


def validate_taxonomy_item_family(item_family: WorksheetItemFamily) -> None:
    validate_item_family(item_family)


def validate_taxonomy_quiz_format(quiz_format: QuizFormat) -> None:
    validate_quiz_format(quiz_format)


def validate_taxonomy_tier(tier: WorksheetTier) -> None:
    validate_tier(tier)


def item_family_explanations() -> Dict[WorksheetItemFamily, str]:
    return {
        "product_recognition": "Find or identify the product.",
        "route_in": "Build the product through a multiplication route.",
        "missing_factor": "Complete a multiplication with one value missing.",
        "another_way": "Find a different route to the same product.",
        "compare_routes": "Compare two or more ways that make the same product.",
        "route_out": "Leave the product through a division route.",
        "check_match": "Check whether a route matches the product.",
        "correct_incorrect": "Decide whether a route is correct or not.",
        "error_repair": "Fix a broken route or explain why it is outside TMK World.",
        "structural_grouping": "Sort, group, or classify items structurally.",
        "final_explanation": "Give one short final explanation.",
    }


def recommended_quiz_formats_by_family() -> Dict[WorksheetItemFamily, Tuple[QuizFormat, ...]]:
    return {
        "product_recognition": ("circle", "tick", "choose"),
        "route_in": ("fill_box", "write_equation", "match"),
        "missing_factor": ("fill_box", "write_number"),
        "another_way": ("write_equation", "label_route", "choose"),
        "compare_routes": ("sort", "match", "route_sort"),
        "route_out": ("fill_box", "write_number", "match"),
        "check_match": ("yes_no", "tick", "choose"),
        "correct_incorrect": ("yes_no", "tick", "choose"),
        "error_repair": ("open_response", "write_word", "choose"),
        "structural_grouping": ("sort", "route_sort", "match"),
        "final_explanation": ("write_word", "open_response"),
    }


def permitted_quiz_formats_for_family(
    item_family: WorksheetItemFamily,
) -> Tuple[QuizFormat, ...]:
    validate_item_family(item_family)
    result = recommended_quiz_formats_by_family()[item_family]
    for fmt in result:
        validate_quiz_format(fmt)
    return result


def item_family_allowed_for_pupils(item_family: str) -> bool:
    return item_family in APPROVED_PUPIL_ITEM_FAMILIES


def item_type_forbidden_for_pupils(item_type: str) -> bool:
    return item_type in FORBIDDEN_PUPIL_ITEM_TYPES
