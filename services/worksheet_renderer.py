from __future__ import annotations

from typing import Final

from models.worksheet_models import (
    PlannedWorksheetItem,
    WorksheetPlan,
)


def render_student_worksheet(plan: WorksheetPlan) -> dict:
    """
    Convert a worksheet plan into student-facing questions.

    This layer:
    - produces only pupil-facing text
    - obeys quiz-format vocabulary rules
    - never exposes structural metadata
    """

    questions = []

    for item in plan.items:
        question_text = _render_question(item)

        questions.append(
            {
                "q_id": item.question_id,
                "question": question_text,
            }
        )

    return {
        "stage": plan.stage,
        "format_id": plan.format_id,
        "tier": plan.tier,
        "selected_products": plan.selected_products,
        "questions": questions,
    }


def render_teacher_key(plan: WorksheetPlan) -> dict:
    """
    Teacher-facing output.

    Includes:
    - correct answers
    - short notes explaining the structure
    """

    answers = []

    for item in plan.items:
        answers.append(
            {
                "q_id": item.question_id,
                "answer": _render_answer(item),
                "notes": item.notes,
            }
        )

    return {
        "answers": answers
    }


def _render_question(item: PlannedWorksheetItem) -> str:
    """
    Dispatch question rendering based on family.
    """

    if item.family == "product_recognition":
        return _product_recognition(item)

    if item.family == "route_in":
        return _route_in(item)

    if item.family == "missing_factor":
        return _missing_factor(item)

    if item.family == "another_way":
        return _another_way(item)

    if item.family == "compare_routes":
        return _compare_routes(item)

    if item.family == "route_out":
        return _route_out(item)

    if item.family == "check_match":
        return _check_match(item)

    if item.family == "error_repair":
        return _error_repair(item)

    if item.family == "structural_grouping":
        return _structural_group(item)

    if item.family == "final_explanation":
        return _final_explanation(item)

    raise ValueError(f"Unknown worksheet item family: {item.family}")


def _product_recognition(item: PlannedWorksheetItem) -> str:
    product = item.product
    return f"Circle the multiplication that makes {product}."


def _route_in(item: PlannedWorksheetItem) -> str:
    a, b = item.route
    return f"Fill the box: {a} × {b} = □"


def _missing_factor(item: PlannedWorksheetItem) -> str:
    a, b = item.route
    return f"Fill the box: □ × {b} = {item.product}"


def _another_way(item: PlannedWorksheetItem) -> str:
    product = item.product
    return f"Find another multiplication that makes {product}."


def _compare_routes(item: PlannedWorksheetItem) -> str:
    product = item.product
    return f"Do these make the same product {product}? Tick yes or no."


def _route_out(item: PlannedWorksheetItem) -> str:
    a, b = item.route
    return f"Fill the box: {item.product} ÷ {a} = □"


def _check_match(item: PlannedWorksheetItem) -> str:
    product = item.product
    return f"Tick the equation that makes {product}."


def _error_repair(item: PlannedWorksheetItem) -> str:
    a, b = item.route
    wrong = a * b + 1
    return f"This is wrong: {a} × {b} = {wrong}. Fix it."


def _structural_group(item: PlannedWorksheetItem) -> str:
    return "Sort these into the same family or different family."


def _final_explanation(item: PlannedWorksheetItem) -> str:
    return "Explain how you know your answer."


def _render_answer(item: PlannedWorksheetItem) -> str:
    if item.family in ("route_in", "missing_factor"):
        a, b = item.route
        return str(a * b)

    if item.family == "route_out":
        a, b = item.route
        return str(b)

    if item.family == "error_repair":
        a, b = item.route
        return f"{a} × {b} = {a*b}"

    if item.family == "product_recognition":
        return str(item.product)

    if item.family == "another_way":
        a, b = item.route
        return f"{a} × {b} = {item.product}"

    if item.family == "compare_routes":
        return "Yes"

    return "Teacher judgement"
