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
    families = record.factor_families
    intro = record.intro_route
    alternate = _alternate_family(record)
    pattern_ids = product_pattern_ids(product)

    questions = (
        _question_intro_route(record),
        _question_switch(record),
        _question_route_count(record),
        _question_route_listing(record),
        _question_missing_factor_from_intro(record, tier),
        _question_missing_factor_from_alternate(record, tier, alternate),
        _question_division_from_intro_left(record),
        _question_division_from_intro_right(record),
        _question_same_product_another_route(record, alternate),
        _question_square_or_route_focus(record, families, intro, alternate, pattern_ids),
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
) -> tuple[str, ...]:
    record = product_record(product)
    notes = [
        f"Product {record.product} is in stage {record.stage}.",
        f"Intro route: {_format_route(record.intro_route)}.",
        f"Distinct multiplication routes: {len(record.factor_families)}.",
        f"Teacher-side factor families: {_format_routes(record.factor_families)}.",
        f"Structural role: {record.structural_role}.",
    ]

    for pattern_id in pattern_ids[:2]:
        pattern = get_pattern(pattern_id)
        notes.append(f"{pattern.name}: {pattern.teacher_note}")

    return tuple(notes)


def _question_intro_route(record: ProductRecord) -> QuestionSpec:
    a, b = record.intro_route
    return QuestionSpec(
        id=1,
        prompt_key="intro_route",
        pupil_prompt=_inline_equation_prompt(
            "Complete the route:",
            a,
            b,
        ),
        answer=str(record.product),
        pattern_id="product_hub",
        memory_cue_id="intro_route_anchor",
    )


def _question_switch(record: ProductRecord) -> QuestionSpec:
    a, b = record.intro_route

    if a == b:
        prompt = _inline_equation_prompt(
            "Use the same-factor route:",
            a,
            b,
        )
    else:
        prompt = _inline_equation_prompt(
            "Switch the factors:",
            b,
            a,
        )

    return QuestionSpec(
        id=2,
        prompt_key="switch_route",
        pupil_prompt=prompt,
        answer=str(record.product),
        pattern_id="commutative_switch",
        memory_cue_id="switch_same_product",
    )


def _question_route_count(record: ProductRecord) -> QuestionSpec:
    return QuestionSpec(
        id=3,
        prompt_key="route_count",
        pupil_prompt=f"How many different multiplication routes make {record.product}?",
        answer=str(len(record.factor_families)),
        pattern_id="route_multiplicity",
        memory_cue_id="count_routes",
    )


def _question_route_listing(record: ProductRecord) -> QuestionSpec:
    if len(record.factor_families) == 1:
        prompt = f"Write the multiplication route that makes {record.product}."
    else:
        prompt = f"Write the different multiplication routes that make {record.product}."

    return QuestionSpec(
        id=4,
        prompt_key="route_listing",
        pupil_prompt=prompt,
        answer=_format_routes(record.factor_families),
        pattern_id=_route_listing_pattern_id(record),
        memory_cue_id="list_routes",
    )


def _question_missing_factor_from_intro(record: ProductRecord, tier: Tier) -> QuestionSpec:
    a, b = record.intro_route

    if tier == "Support":
        prompt = f"{a} × __ = {record.product}"
        answer = str(b)
    elif tier == "Core":
        prompt = f"__ × {b} = {record.product}"
        answer = str(a)
    else:
        prompt = f"Complete the route: {a} × __ = {record.product}"
        answer = str(b)

    return QuestionSpec(
        id=5,
        prompt_key="missing_factor_intro",
        pupil_prompt=prompt,
        answer=answer,
        pattern_id="route_in_route_out",
        memory_cue_id="missing_factor_from_intro",
    )


def _question_missing_factor_from_alternate(
    record: ProductRecord,
    tier: Tier,
    alternate: tuple[int, int] | None,
) -> QuestionSpec:
    if alternate is None:
        a, b = record.intro_route
        if a == b:
            prompt = f"Complete the route again: __ × {b} = {record.product}"
            answer = str(a)
        else:
            prompt = f"Switch the route again: {b} × __ = {record.product}"
            answer = str(a)
    else:
        x, y = alternate
        if tier == "Support":
            prompt = f"{x} × __ = {record.product}"
            answer = str(y)
        elif tier == "Core":
            prompt = f"__ × {y} = {record.product}"
            answer = str(x)
        else:
            prompt = f"Use another route: {x} × __ = {record.product}"
            answer = str(y)

    return QuestionSpec(
        id=6,
        prompt_key="missing_factor_alternate",
        pupil_prompt=prompt,
        answer=answer,
        pattern_id="same_product_different_routes",
        memory_cue_id="missing_factor_from_another_route",
    )


def _question_division_from_intro_left(record: ProductRecord) -> QuestionSpec:
    a, b = record.intro_route
    return QuestionSpec(
        id=7,
        prompt_key="division_left",
        pupil_prompt=f"{record.product} ÷ {a} = __",
        answer=str(b),
        pattern_id="route_in_route_out",
        memory_cue_id="division_recovers_factor_left",
    )


def _question_division_from_intro_right(record: ProductRecord) -> QuestionSpec:
    a, b = record.intro_route
    return QuestionSpec(
        id=8,
        prompt_key="division_right",
        pupil_prompt=f"{record.product} ÷ {b} = __",
        answer=str(a),
        pattern_id="route_in_route_out",
        memory_cue_id="division_recovers_factor_right",
    )


def _question_same_product_another_route(
    record: ProductRecord,
    alternate: tuple[int, int] | None,
) -> QuestionSpec:
    if alternate is None:
        a, b = record.intro_route
        prompt = f"Does {a} × {b} make {record.product}? Write yes or no."
        answer = "yes"
        pattern_id = "product_hub"
        memory_cue_id = "same_route_same_product"
    else:
        x, y = alternate
        prompt = _inline_equation_prompt(
            f"Another route makes the same product {record.product}:",
            x,
            y,
        )
        answer = str(record.product)
        pattern_id = "same_product_different_routes"
        memory_cue_id = "another_route_same_product"

    return QuestionSpec(
        id=9,
        prompt_key="same_product_another_route",
        pupil_prompt=prompt,
        answer=answer,
        pattern_id=pattern_id,
        memory_cue_id=memory_cue_id,
    )


def _question_square_or_route_focus(
    record: ProductRecord,
    families: tuple[tuple[int, int], ...],
    intro: tuple[int, int],
    alternate: tuple[int, int] | None,
    pattern_ids: tuple[str, ...],
) -> QuestionSpec:
    square_route = _square_route(families)

    if square_route is not None:
        a, b = square_route
        prompt = _inline_equation_prompt(
            "Complete the square route:",
            a,
            b,
        )
        answer = str(record.product)
        pattern_id = "square_pattern"
        memory_cue_id = "square_route_anchor"
    elif alternate is not None and alternate != intro:
        x, y = alternate
        prompt = f"Give another way to make {record.product}."
        answer = _format_route((x, y))
        pattern_id = "same_product_different_routes"
        memory_cue_id = "give_another_route"
    else:
        chosen_pattern_id = _best_pattern_for_final_question(pattern_ids)
        pattern = get_pattern(chosen_pattern_id)
        prompt = f"What does this product show? {pattern.learner_label}"
        answer = pattern.child_text
        pattern_id = pattern.id
        memory_cue_id = f"pattern::{pattern.id}"

    return QuestionSpec(
        id=10,
        prompt_key="square_or_route_focus",
        pupil_prompt=prompt,
        answer=answer,
        pattern_id=pattern_id,
        memory_cue_id=memory_cue_id,
    )


def _best_pattern_for_final_question(pattern_ids: tuple[str, ...]) -> str:
    preferred = (
        "closure_with_7x7",
        "nine_quantifier_build",
        "doubling_chain",
        "ten_times_benchmark",
        "five_half_ten",
        "product_hub",
    )

    for pattern_id in preferred:
        if pattern_id in pattern_ids:
            return pattern_id

    if pattern_ids:
        return pattern_ids[0]

    return "product_hub"


def _route_listing_pattern_id(record: ProductRecord) -> str:
    if len(record.factor_families) > 1:
        return "same_product_different_routes"
    return "product_hub"


def _alternate_family(record: ProductRecord) -> tuple[int, int] | None:
    for family in record.factor_families:
        if family != tuple(sorted(record.intro_route)):
            return family
    return None


def _square_route(
    families: tuple[tuple[int, int], ...],
) -> tuple[int, int] | None:
    for a, b in families:
        if a == b:
            return (a, b)
    return None


def _inline_equation_prompt(prefix: str, a: int, b: int) -> str:
    return f"{prefix} {a} × {b} = __"


def _format_route(route: tuple[int, int]) -> str:
    return f"{route[0]} × {route[1]}"


def _format_routes(routes: tuple[tuple[int, int], ...]) -> str:
    return ", ".join(_format_route(route) for route in routes)


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
