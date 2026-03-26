from __future__ import annotations

from typing import Final

from models.worksheet_models import WorksheetPlan
from services.msvwa_registry import (
    resolve_item_msvwa,
    resolve_item_msvwa_reason,
)


def build_teacher_key(plan: WorksheetPlan) -> dict:
    """
    Build the teacher-facing answer key.

    Output includes, for every item:
    - correct answer
    - MSVWA tags
    - short teacher note
    - optional vocabulary target
    """

    answers = []

    for item in plan.items:
        contextual_secondary_tag = _contextual_secondary_tag(item)

        msvwa_tags = resolve_item_msvwa(
            family=item.family,
            quiz_format=item.quiz_format,
            tier=plan.tier,
            contextual_secondary_tag=contextual_secondary_tag,
        )

        answer_text = _teacher_answer(item)
        teacher_note = _teacher_note(
            item=item,
            plan=plan,
            msvwa_tags=msvwa_tags,
            contextual_secondary_tag=contextual_secondary_tag,
        )

        entry = {
            "q_id": item.question_id,
            "answer": answer_text,
            "msvwa": list(msvwa_tags),
            "teacher_note": teacher_note,
        }

        if item.vocab_target:
            entry["vocab"] = item.vocab_target

        answers.append(entry)

    return {
        "stage": plan.stage,
        "format_id": plan.format_id,
        "tier": plan.tier,
        "selected_products": list(plan.selected_products),
        "recap_products": list(plan.recap_products),
        "answers": answers,
    }


def _teacher_answer(item) -> str:
    """
    Return the correct teacher-facing answer string for a planned item.
    """

    if item.family == "product_recognition":
        return str(item.product)

    if item.family == "route_in":
        a, b = item.route
        return str(a * b)

    if item.family == "missing_factor":
        a, b = item.route
        return str(a)

    if item.family == "another_way":
        a, b = item.route
        return f"{a} × {b} = {item.product}"

    if item.family == "compare_routes":
        return "Teacher checks whether both routes make the same product."

    if item.family == "route_out":
        a, b = item.route
        return str(b)

    if item.family == "check_match":
        return str(item.product)

    if item.family == "correct_incorrect":
        return "Teacher checks correctness."

    if item.family == "error_repair":
        a, b = item.route
        return f"{a} × {b} = {a * b}"

    if item.family == "structural_grouping":
        return "Teacher checks grouping accuracy."

    if item.family == "final_explanation":
        return "Teacher judges explanation against the product-route structure."

    raise ValueError(f"Unknown worksheet item family: {item.family}")


def _teacher_note(
    item,
    plan: WorksheetPlan,
    msvwa_tags: tuple[str, ...],
    contextual_secondary_tag: str | None,
) -> str:
    """
    Produce a brief practical teacher note.
    """

    base = resolve_item_msvwa_reason(
        family=item.family,
        quiz_format=item.quiz_format,
        tier=plan.tier,
        contextual_secondary_tag=contextual_secondary_tag,
    )

    structural = _structural_note(item)

    if item.vocab_target:
        return f"{structural} Vocabulary focus: {item.vocab_target}. {base}"

    return f"{structural} {base}"


def _structural_note(item) -> str:
    """
    Brief structural explanation of what the item is doing mathematically.
    """

    if item.family == "product_recognition":
        return (
            f"Target product is {item.product}. "
            f"The learner identifies the correct product signal."
        )

    if item.family == "route_in":
        a, b = item.route
        return (
            f"Uses a multiplication route into {item.product}: {a} × {b}."
        )

    if item.family == "missing_factor":
        a, b = item.route
        return (
            f"Recovers the missing factor from the route {a} × {b} = {item.product}."
        )

    if item.family == "another_way":
        a, b = item.route
        return (
            f"Shows another route to the same product: {a} × {b} = {item.product}."
        )

    if item.family == "compare_routes":
        return (
            f"Compares routes linked to product {item.product}."
        )

    if item.family == "route_out":
        a, b = item.route
        return (
            f"Uses inverse division from {item.product}: {item.product} ÷ {a} = {b}."
        )

    if item.family == "check_match":
        return (
            f"Checks which route or equation matches product {item.product}."
        )

    if item.family == "correct_incorrect":
        return (
            "Checks mathematical status against the known product-route structure."
        )

    if item.family == "error_repair":
        a, b = item.route
        return (
            f"Repairs the route so it matches {a} × {b} = {a * b}."
        )

    if item.family == "structural_grouping":
        return (
            "Groups routes or facts by shared family or product structure."
        )

    if item.family == "final_explanation":
        return (
            f"Final explanation anchored in product {item.product}."
        )

    raise ValueError(f"Unknown worksheet item family: {item.family}")


def _contextual_secondary_tag(item) -> str | None:
    """
    Optional contextual tag for final explanation items.
    """

    if item.family != "final_explanation":
        return None

    if item.vocab_target in {"square", "squared", "square number"}:
        return "M"

    if item.route is not None:
        return "V"

    return "M"
