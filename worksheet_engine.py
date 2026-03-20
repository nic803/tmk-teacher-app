from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal

from patterns import get_pattern, product_pattern_ids
from products import ALL_PRODUCTS, ProductRecord, product_record

Tier = Literal["Support", "Core", "Extension"]

SUPPORTED_TIERS: Final[tuple[Tier, ...]] = ("Support", "Core", "Extension")
QUESTION_COUNT: Final[int] = 10


@dataclass(frozen=True)
class QuestionSpec:
    id: int
    prompt_key: str
    pupil_prompt: str
    answer: str
    pattern_id: str | None
    memory_cue_id: str | None


@dataclass(frozen=True)
class TeacherKey:
    answers: tuple[str, ...]
    pattern_ids: tuple[str, ...]
    memory_cue_ids: tuple[str, ...]
    notes: tuple[str, ...]


@dataclass(frozen=True)
class WorksheetPackage:
    product: int
    stage: str
    tier: Tier
    questions: tuple[QuestionSpec, ...]
    teacher_key: TeacherKey


def generate_worksheet(product: int, tier: Tier) -> WorksheetPackage:
    _validate_product(product)
    _validate_tier(tier)

    record = product_record(product)
    pattern_ids = product_pattern_ids(product)

    questions = (
        _question_intro_route(record, tier),
        _question_commutative(record, tier),
        _question_route_count(record, tier),
        _question_factor_families(record, tier),
        _question_missing_factor(record, tier),
        _question_division_from_intro(record, tier),
        _question_related_product(record, tier),
        _question_pattern_focus(record, tier, pattern_ids, slot_index=0),
        _question_pattern_focus(record, tier, pattern_ids, slot_index=1),
        _question_structural_role(record, tier),
    )

    worksheet = WorksheetPackage(
        product=record.product,
        stage=record.stage,
        tier=tier,
        questions=questions,
        teacher_key=build_teacher_key(product, questions),
    )

    _validate_worksheet_package(worksheet)
    return worksheet


def build_teacher_key(product: int, questions: tuple[QuestionSpec, ...]) -> TeacherKey:
    _validate_product(product)

    pattern_ids = tuple(
        dict.fromkeys(
            question.pattern_id
            for question in questions
            if question.pattern_id
        )
    )

    memory_cue_ids = tuple(
        dict.fromkeys(
            question.memory_cue_id
            for question in questions
            if question.memory_cue_id
        )
    )

    answers = tuple(question.answer for question in questions)

    notes = tuple(_teacher_notes(product, questions, pattern_ids))

    return TeacherKey(
        answers=answers,
        pattern_ids=pattern_ids,
        memory_cue_ids=memory_cue_ids,
        notes=notes,
    )


def _teacher_notes(
    product: int,
    questions: tuple[QuestionSpec, ...],
    pattern_ids: tuple[str, ...],
) -> list[str]:
    record = product_record(product)
    notes = [
        f"Product {record.product} is in stage {record.stage}.",
        f"Intro route: {record.intro_route[0]} × {record.intro_route[1]}.",
        f"Worksheet tier: {_tier_label_for_note(questions)}.",
        f"Structural role: {record.structural_role}.",
    ]

    if pattern_ids:
        first_pattern = get_pattern(pattern_ids[0])
        notes.append(f"Primary pattern focus: {first_pattern.name}.")
        notes.append(first_pattern.teacher_note)

    if len(pattern_ids) > 1:
        second_pattern = get_pattern(pattern_ids[1])
        notes.append(f"Secondary pattern focus: {second_pattern.name}.")
        notes.append(second_pattern.teacher_note)

    return notes


def _question_intro_route(record: ProductRecord, tier: Tier) -> QuestionSpec:
    a, b = record.intro_route
    return QuestionSpec(
        id=1,
        prompt_key="intro_route",
        pupil_prompt=f"Complete the intro route: {a} × {b} = ___",
        answer=str(record.product),
        pattern_id="product_hub",
        memory_cue_id="intro_route_anchor",
    )


def _question_commutative(record: ProductRecord, tier: Tier) -> QuestionSpec:
    a, b = record.intro_route
    return QuestionSpec(
        id=2,
        prompt_key="commutative_switch",
        pupil_prompt=f"Switch the factors and complete: {b} × {a} = ___",
        answer=str(record.product),
        pattern_id="commutative_switch",
        memory_cue_id="switch_same_product",
    )


def _question_route_count(record: ProductRecord, tier: Tier) -> QuestionSpec:
    family_count = len(record.factor_families)
    wording = {
        "Support": "How many route families does this product have?",
        "Core": f"How many factor families does {record.product} have?",
        "Extension": f"State the number of distinct factor families for {record.product}.",
    }[tier]

    return QuestionSpec(
        id=3,
        prompt_key="route_count",
        pupil_prompt=wording,
        answer=str(family_count),
        pattern_id="route_multiplicity",
        memory_cue_id="count_route_families",
    )


def _question_factor_families(record: ProductRecord, tier: Tier) -> QuestionSpec:
    prompt = {
        "Support": f"List the factor families for {record.product}.",
        "Core": f"Write all factor families that make {record.product}.",
        "Extension": f"Enumerate all distinct factor families for {record.product}.",
    }[tier]

    answer = ", ".join(_format_route(route) for route in record.factor_families)

    pattern_id = "same_product_different_routes"
    if len(record.factor_families) == 1:
        pattern_id = "route_multiplicity"

    return QuestionSpec(
        id=4,
        prompt_key="factor_families",
        pupil_prompt=prompt,
        answer=answer,
        pattern_id=pattern_id,
        memory_cue_id="list_factor_families",
    )


def _question_missing_factor(record: ProductRecord, tier: Tier) -> QuestionSpec:
    a, b = record.intro_route
    if tier == "Support":
        prompt = f"Fill the missing factor: {a} × ___ = {record.product}"
        answer = str(b)
    elif tier == "Core":
        prompt = f"Fill the missing factor: ___ × {b} = {record.product}"
        answer = str(a)
    else:
        if len(record.factor_families) > 1:
            x, y = record.factor_families[-1]
            prompt = f"Use a different route: {x} × ___ = {record.product}"
            answer = str(y)
        else:
            prompt = f"Use the route you know: {a} × ___ = {record.product}"
            answer = str(b)

    return QuestionSpec(
        id=5,
        prompt_key="missing_factor",
        pupil_prompt=prompt,
        answer=answer,
        pattern_id="route_in_route_out",
        memory_cue_id="product_fixes_missing_factor",
    )


def _question_division_from_intro(record: ProductRecord, tier: Tier) -> QuestionSpec:
    a, b = record.intro_route
    if tier == "Support":
        prompt = f"Complete: {record.product} ÷ {a} = ___"
        answer = str(b)
    elif tier == "Core":
        prompt = f"Complete: {record.product} ÷ {b} = ___"
        answer = str(a)
    else:
        prompt = f"Use division to recover a factor: {record.product} ÷ {a} = ___"
        answer = str(b)

    return QuestionSpec(
        id=6,
        prompt_key="division_partner",
        pupil_prompt=prompt,
        answer=answer,
        pattern_id="route_in_route_out",
        memory_cue_id="division_recovers_factor",
    )


def _question_related_product(record: ProductRecord, tier: Tier) -> QuestionSpec:
    related = _best_related_product(record)
    if related is None:
        prompt = f"State the stage for {record.product}."
        answer = record.stage
        pattern_id = "product_hub"
        memory_cue_id = "product_stage_anchor"
    else:
        prompt = {
            "Support": f"Name one related product that shares a factor with {record.product}.",
            "Core": f"Give one related product that overlaps with {record.product} through a shared factor.",
            "Extension": f"State one related product structurally linked to {record.product} by a shared factor.",
        }[tier]
        answer = str(related)
        pattern_id = "product_family_overlap"
        memory_cue_id = "shared_factor_overlap"

    return QuestionSpec(
        id=7,
        prompt_key="related_product",
        pupil_prompt=prompt,
        answer=answer,
        pattern_id=pattern_id,
        memory_cue_id=memory_cue_id,
    )


def _question_pattern_focus(
    record: ProductRecord,
    tier: Tier,
    pattern_ids: tuple[str, ...],
    slot_index: int,
) -> QuestionSpec:
    question_id = 8 + slot_index
    pattern_id = _pattern_for_slot(pattern_ids, slot_index)
    pattern = get_pattern(pattern_id)

    if tier == "Support":
        prompt = f"Pattern focus: {pattern.short_prompt} for {record.product}."
    elif tier == "Core":
        prompt = f"Use this pattern idea for {record.product}: {pattern.learner_label}"
    else:
        prompt = f"Explain the pattern link for {record.product}: {pattern.name}"

    return QuestionSpec(
        id=question_id,
        prompt_key=f"pattern_focus_{slot_index + 1}",
        pupil_prompt=prompt,
        answer=pattern.child_text,
        pattern_id=pattern.id,
        memory_cue_id=_memory_cue_id_for_pattern(pattern.id),
    )


def _question_structural_role(record: ProductRecord, tier: Tier) -> QuestionSpec:
    prompt = {
        "Support": f"What structural role does {record.product} have?",
        "Core": f"State the structural role label for {record.product}.",
        "Extension": f"Classify {record.product} by structural role.",
    }[tier]

    return QuestionSpec(
        id=10,
        prompt_key="structural_role",
        pupil_prompt=prompt,
        answer=record.structural_role,
        pattern_id="product_hub",
        memory_cue_id="structural_role_name",
    )


def _pattern_for_slot(pattern_ids: tuple[str, ...], slot_index: int) -> str:
    if not pattern_ids:
        return "product_hub"
    if slot_index < len(pattern_ids):
        return pattern_ids[slot_index]
    return pattern_ids[-1]


def _best_related_product(record: ProductRecord) -> int | None:
    for related in record.related_products:
        if related != record.product:
            return related
    return None


def _memory_cue_id_for_pattern(pattern_id: str) -> str:
    return f"pattern::{pattern_id}"


def _tier_label_for_note(questions: tuple[QuestionSpec, ...]) -> str:
    support_signals = sum("Support" in question.pupil_prompt for question in questions)
    extension_signals = sum("Explain" in question.pupil_prompt for question in questions)

    if extension_signals:
        return "Extension"
    if support_signals:
        return "Support"
    return "Core"


def _format_route(route: tuple[int, int]) -> str:
    return f"{route[0]} × {route[1]}"


def _validate_product(product: int) -> None:
    if product not in ALL_PRODUCTS:
        raise ValueError(f"Unknown TMK product: {product}")


def _validate_tier(tier: str) -> None:
    if tier not in SUPPORTED_TIERS:
        raise ValueError(
            f"Unsupported tier: {tier}. Expected one of {SUPPORTED_TIERS}."
        )


def _validate_worksheet_package(worksheet: WorksheetPackage) -> None:
    if worksheet.product not in ALL_PRODUCTS:
        raise ValueError(
            f"Worksheet contains invalid product: {worksheet.product}"
        )

    if worksheet.tier not in SUPPORTED_TIERS:
        raise ValueError(
            f"Worksheet contains invalid tier: {worksheet.tier}"
        )

    if len(worksheet.questions) != QUESTION_COUNT:
        raise ValueError(
            f"Worksheet must contain exactly {QUESTION_COUNT} questions."
        )

    expected_ids = tuple(range(1, QUESTION_COUNT + 1))
    actual_ids = tuple(question.id for question in worksheet.questions)

    if actual_ids != expected_ids:
        raise ValueError("Worksheet question IDs must be sequential from 1 to 10.")

    for question in worksheet.questions:
        if not question.prompt_key:
            raise ValueError(f"Question {question.id} has an empty prompt key.")
        if not question.pupil_prompt:
            raise ValueError(f"Question {question.id} has an empty pupil prompt.")
        if question.answer in ("", None):
            raise ValueError(f"Question {question.id} has an empty answer.")

    if len(worksheet.teacher_key.answers) != QUESTION_COUNT:
        raise ValueError("Teacher key must contain exactly 10 answers.")
