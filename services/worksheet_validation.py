from __future__ import annotations

from typing import Final

from domain.stage_vocabulary import available_vocab as stage_available_vocab
from domain.worksheet_taxonomy import (
    family_allowed_for_tier,
    forbidden_pupil_prompt_patterns,
    format_allowed_for_family,
    validate_prompt_text_for_pupil_use,
)
from models.worksheet_models import (
    PlannedWorksheetItem,
    ProductSelectionResult,
    WorksheetPlan,
    WorksheetValidationResult,
    validate_msvwa_tags,
    validate_selection_result,
    validate_worksheet_plan,
)
from services.msvwa_registry import (
    tier_profile_alignment_report,
    validate_item_msvwa_assignment,
    worksheet_matches_tier_profile,
)


def validate_selection(selection: ProductSelectionResult) -> None:
    validate_selection_result(selection)


def validate_plan(plan: WorksheetPlan) -> WorksheetValidationResult:
    """
    Validate the structural worksheet plan before rendering.
    """
    errors: list[str] = []
    warnings: list[str] = []

    try:
        validate_worksheet_plan(plan)
    except Exception as exc:
        errors.append(str(exc))
        return WorksheetValidationResult(
            is_valid=False,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )

    errors.extend(_validate_plan_products(plan))
    errors.extend(_validate_plan_vocabulary(plan))
    errors.extend(_validate_plan_msvwa(plan))
    errors.extend(_validate_plan_routes(plan))
    warnings.extend(_plan_warnings(plan))

    return WorksheetValidationResult(
        is_valid=len(errors) == 0,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )


def validate_student_output(
    plan: WorksheetPlan,
    student_worksheet: dict,
) -> WorksheetValidationResult:
    """
    Validate the student-facing rendered worksheet.
    """
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(student_worksheet, dict):
        errors.append("Student worksheet output must be a dictionary.")
        return WorksheetValidationResult(
            is_valid=False,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )

    expected_question_count = len(plan.items)

    questions = student_worksheet.get("questions")
    if not isinstance(questions, list):
        errors.append("Student worksheet must contain a 'questions' list.")
        return WorksheetValidationResult(
            is_valid=False,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )

    if len(questions) != expected_question_count:
        errors.append(
            f"Student worksheet must contain exactly {expected_question_count} questions. "
            f"Found {len(questions)}."
        )

    actual_ids: list[int] = []
    for index, question in enumerate(questions, start=1):
        if not isinstance(question, dict):
            errors.append(f"Student worksheet question {index} must be a dictionary.")
            continue

        q_id = question.get("q_id")
        prompt = question.get("question")

        if q_id is None:
            errors.append(f"Student worksheet question {index} is missing 'q_id'.")
        elif not isinstance(q_id, int):
            errors.append(f"Student worksheet question {index} has non-integer 'q_id'.")
        else:
            actual_ids.append(q_id)

        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"Student worksheet question {index} is missing prompt text.")
            continue

        try:
            validate_prompt_text_for_pupil_use(prompt)
        except Exception as exc:
            errors.append(f"Question {q_id if isinstance(q_id, int) else index}: {exc}")

    expected_ids = list(range(1, expected_question_count + 1))
    if actual_ids and actual_ids != expected_ids:
        errors.append(
            f"Student worksheet question ids must be sequential {expected_ids}. "
            f"Found {actual_ids}."
        )

    return WorksheetValidationResult(
        is_valid=len(errors) == 0,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )


def validate_teacher_output(
    plan: WorksheetPlan,
    teacher_key: dict,
) -> WorksheetValidationResult:
    """
    Validate the teacher-facing answer key.
    """
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(teacher_key, dict):
        errors.append("Teacher key output must be a dictionary.")
        return WorksheetValidationResult(
            is_valid=False,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )

    answers = teacher_key.get("answers")
    if not isinstance(answers, list):
        errors.append("Teacher key must contain an 'answers' list.")
        return WorksheetValidationResult(
            is_valid=False,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )

    if len(answers) != len(plan.items):
        errors.append(
            f"Teacher key must contain exactly {len(plan.items)} answers. "
            f"Found {len(answers)}."
        )

    actual_ids: list[int] = []
    plan_by_id = {item.q_id: item for item in plan.items}

    for index, entry in enumerate(answers, start=1):
        if not isinstance(entry, dict):
            errors.append(f"Teacher answer {index} must be a dictionary.")
            continue

        q_id = entry.get("q_id")
        answer = entry.get("answer")
        msvwa = entry.get("msvwa")
        teacher_note = entry.get("teacher_note")

        if q_id is None:
            errors.append(f"Teacher answer {index} is missing 'q_id'.")
            continue

        if not isinstance(q_id, int):
            errors.append(f"Teacher answer {index} has non-integer 'q_id'.")
            continue

        actual_ids.append(q_id)

        if q_id not in plan_by_id:
            errors.append(f"Teacher answer references unknown question id {q_id}.")
            continue

        planned_item = plan_by_id[q_id]

        if not isinstance(answer, str) or not answer.strip():
            errors.append(f"Teacher answer {q_id} is missing answer text.")

        if not isinstance(teacher_note, str) or not teacher_note.strip():
            errors.append(f"Teacher answer {q_id} is missing teacher_note.")

        if not isinstance(msvwa, list) and not isinstance(msvwa, tuple):
            errors.append(f"Teacher answer {q_id} must include MSVWA tags as a list/tuple.")
            continue

        try:
            validate_msvwa_tags(tuple(msvwa))
            validate_item_msvwa_assignment(
                family=planned_item.family,
                quiz_format=planned_item.quiz_format,
                tier=plan.tier,
                tags=tuple(msvwa),
            )
        except Exception as exc:
            errors.append(f"Teacher answer {q_id} MSVWA validation failed: {exc}")

    expected_ids = list(range(1, len(plan.items) + 1))
    if actual_ids and actual_ids != expected_ids:
        errors.append(
            f"Teacher answer ids must be sequential {expected_ids}. Found {actual_ids}."
        )

    return WorksheetValidationResult(
        is_valid=len(errors) == 0,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )


def validate_bundle(
    selection: ProductSelectionResult,
    plan: WorksheetPlan,
    student_worksheet: dict,
    teacher_key: dict,
) -> WorksheetValidationResult:
    """
    Validate the full worksheet generation bundle.
    """
    errors: list[str] = []
    warnings: list[str] = []

    try:
        validate_selection(selection)
    except Exception as exc:
        errors.append(str(exc))

    plan_result = validate_plan(plan)
    errors.extend(plan_result.errors)
    warnings.extend(plan_result.warnings)

    student_result = validate_student_output(plan, student_worksheet)
    errors.extend(student_result.errors)
    warnings.extend(student_result.warnings)

    teacher_result = validate_teacher_output(plan, teacher_key)
    errors.extend(teacher_result.errors)
    warnings.extend(teacher_result.warnings)

    return WorksheetValidationResult(
        is_valid=len(errors) == 0,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )


def _validate_plan_products(plan: WorksheetPlan) -> list[str]:
    errors: list[str] = []

    selected = tuple(plan.selected_products)
    recap = tuple(plan.recap_products)
    valid_products = set(selected + recap)

    for item in plan.items:
        if item.target_product not in valid_products:
            errors.append(
                f"Planned item {item.q_id} uses product {item.target_product}, "
                f"which is not in selected_products or recap_products."
            )

        if plan.format_id == "one_product_10" and item.target_product not in set(selected):
            errors.append(
                f"one_product_10 plan item {item.q_id} must use the selected hub product."
            )

    return errors


def _validate_plan_vocabulary(plan: WorksheetPlan) -> list[str]:
    errors: list[str] = []

    allowed_vocab = {word.lower() for word in stage_available_vocab(plan.stage)}
    required_vocab = {word.lower() for word in plan.required_vocab_focus}

    vocab_seen: set[str] = set()
    required_seen: set[str] = set()

    for item in plan.items:
        for word in item.vocabulary_words:
            normalized = word.strip().lower()
            vocab_seen.add(normalized)

            if normalized not in allowed_vocab:
                errors.append(
                    f"Planned item {item.q_id} uses vocabulary '{word}' not available at stage {plan.stage}."
                )

            if normalized in required_vocab:
                required_seen.add(normalized)

    if not vocab_seen:
        errors.append("Every worksheet must contain at least one vocabulary-bearing item.")

    if not required_seen:
        errors.append(
            f"Worksheet must use at least one word from required_vocab_focus for stage {plan.stage}."
        )

    return errors


def _validate_plan_msvwa(plan: WorksheetPlan) -> list[str]:
    errors: list[str] = []

    tags_by_item = tuple(item.msvwa_tags for item in plan.items)

    for item in plan.items:
        try:
            validate_msvwa_tags(item.msvwa_tags)
            validate_item_msvwa_assignment(
                family=item.family,
                quiz_format=item.quiz_format,
                tier=plan.tier,
                tags=item.msvwa_tags,
            )
        except Exception as exc:
            errors.append(f"Planned item {item.q_id} MSVWA validation failed: {exc}")

    try:
        if not worksheet_matches_tier_profile(tags_by_item, plan.tier):
            report = tier_profile_alignment_report(tags_by_item, plan.tier)
            errors.append(
                f"Worksheet MSVWA distribution does not align with tier '{plan.tier}'. "
                f"Report: {report}"
            )
    except Exception as exc:
        errors.append(f"Worksheet MSVWA distribution check failed: {exc}")

    return errors


def _validate_plan_routes(plan: WorksheetPlan) -> list[str]:
    errors: list[str] = []

    route_in_count = 0
    route_out_count = 0

    for item in plan.items:
        if item.family == "route_in":
            route_in_count += 1
            if item.metadata and not _metadata_has_route(item):
                errors.append(f"route_in item {item.q_id} is missing route metadata.")
        elif item.family == "route_out":
            route_out_count += 1
            if item.metadata and not _metadata_has_route(item):
                errors.append(f"route_out item {item.q_id} is missing route metadata.")

    if route_in_count < 1:
        errors.append("Every worksheet must contain at least one route_in item.")

    if route_out_count < 1:
        errors.append("Every worksheet must contain at least one route_out item.")

    return errors


def _plan_warnings(plan: WorksheetPlan) -> list[str]:
    warnings: list[str] = []

    if plan.format_id == "three_product_12" and len(plan.recap_products) == 0:
        warnings.append(
            "three_product_12 worksheet contains no recap products; this is valid but may reduce cumulative review."
        )

    if len(plan.recap_products) > 0 and not any(
        item.target_product in set(plan.recap_products) for item in plan.items
    ):
        warnings.append(
            "Recap products were selected but do not appear in any planned items."
        )

    if not any(item.family == "compare_routes" for item in plan.items) and not any(
        item.family == "another_way" for item in plan.items
    ):
        warnings.append(
            "Worksheet contains no compare_routes or another_way item."
        )

    return warnings


def _metadata_has_route(item: PlannedWorksheetItem) -> bool:
    for key, _value in item.metadata:
        if key in {"route", "route_a", "route_b"}:
            return True
    return False
