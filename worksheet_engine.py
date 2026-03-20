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
    alternate = _alternate_family(record)

    questions = (
        _question_1_intro_route(record, tier),
        _question_2_switch(record, tier),
        _question_3_route_count(record, tier),
        _question_4_route_listing(record, tier),
        _question_5_missing_factor_intro(record, tier),
        _question_6_missing_factor_other_route(record, tier, alternate),
        _question_7_division_left(record, tier),
        _question_8_division_right_or_other(record, tier, alternate),
        _question_9_rebuild_product(record, tier, alternate),
        _question_10_true_structural_sentence(record, tier, alternate),
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
    notes = _teacher_notes(product, questions, pattern_ids)

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
        f"Teacher-side factor families: {_format_routes(record.factor_families)}.",
        f"Distinct multiplication routes: {len(record.factor_families)}.",
        f"Structural role: {record.structural_role}.",
        "Pupil prompts should use route language, not factor-family language.",
        "Q9 rebuilds the product.",
        "Q10 states one short true structural sentence.",
    ]

    for pattern_id in pattern_ids[:2]:
        pattern = get_pattern(pattern_id)
        notes.append(f"{pattern.name}: {pattern.teacher_note}")

    return tuple(notes)


def _question_1_intro_route(record: ProductRecord, tier: Tier) -> QuestionSpec:
    a, b = record.intro_route

    if tier == "Support":
        prompt = f"Complete the route: {a} × {b} = __"
    elif tier == "Core":
        prompt = f"Use the route: {a} × {b} = __"
    else:
        prompt = f"Complete this multiplication route for {record.product}: {a} × {b} = __"

    return QuestionSpec(
        id=1,
        prompt_key="intro_route",
        pupil_prompt=prompt,
        answer=str(record.product),
        pattern_id="product_hub",
        memory_cue_id="intro_route_anchor",
    )


def _question_2_switch(record: ProductRecord, tier: Tier) -> QuestionSpec:
    a, b = record.intro_route

    if a == b:
        if tier == "Support":
            prompt = f"Complete the square route: {a} × {b} = __"
        elif tier == "Core":
            prompt = f"Use the same route: {a} × {b} = __"
        else:
            prompt = f"Complete the square route for {record.product}: {a} × {b} = __"
    else:
        if tier == "Support":
            prompt = f"Switch the factors: {b} × {a} = __"
        elif tier == "Core":
            prompt = f"Use the switched route: {b} × {a} = __"
        else:
            prompt = f"Show the switched route for {record.product}: {b} × {a} = __"

    return QuestionSpec(
        id=2,
        prompt_key="switch_route",
        pupil_prompt=prompt,
        answer=str(record.product),
        pattern_id="commutative_switch",
        memory_cue_id="switch_same_product",
    )


def _question_3_route_count(record: ProductRecord, tier: Tier) -> QuestionSpec:
    if tier == "Support":
        prompt = f"How many different multiplication routes make {record.product}?"
    elif tier == "Core":
        prompt = f"How many different routes make {record.product}?"
    else:
        prompt = f"How many multiplication routes can you use to make {record.product} in TMK World?"

    return QuestionSpec(
        id=3,
        prompt_key="route_count",
        pupil_prompt=prompt,
        answer=str(len(record.factor_families)),
        pattern_id="route_multiplicity",
        memory_cue_id="count_routes",
    )


def _question_4_route_listing(record: ProductRecord, tier: Tier) -> QuestionSpec:
    route_count = len(record.factor_families)

    if route_count == 1:
        if tier == "Support":
            prompt = f"Write the multiplication route that makes {record.product}."
        elif tier == "Core":
            prompt = f"Show the route that makes {record.product}."
        else:
            prompt = f"Write the route you would use to make {record.product}."
    else:
        if tier == "Support":
            prompt = f"Write the different multiplication routes that make {record.product}."
        elif tier == "Core":
            prompt = f"Show the different ways to make {record.product}."
        else:
            prompt = f"Write the multiplication routes you can use to make {record.product}."

    return QuestionSpec(
        id=4,
        prompt_key="route_listing",
        pupil_prompt=prompt,
        answer=_format_routes(record.factor_families),
        pattern_id=_route_listing_pattern_id(record),
        memory_cue_id="list_routes",
    )


def _question_5_missing_factor_intro(record: ProductRecord, tier: Tier) -> QuestionSpec:
    a, b = record.intro_route

    if tier == "Support":
        prompt = f"{a} × __ = {record.product}"
        answer = str(b)
    elif tier == "Core":
        prompt = f"__ × {b} = {record.product}"
        answer = str(a)
    else:
        prompt = f"Complete this route to make {record.product}: {a} × __ = {record.product}"
        answer = str(b)

    return QuestionSpec(
        id=5,
        prompt_key="missing_factor_intro",
        pupil_prompt=prompt,
        answer=answer,
        pattern_id="route_in_route_out",
        memory_cue_id="missing_factor_from_intro",
    )


def _question_6_missing_factor_other_route(
    record: ProductRecord,
    tier: Tier,
    alternate: tuple[int, int] | None,
) -> QuestionSpec:
    if alternate is None:
        a, b = record.intro_route

        if tier == "Support":
            prompt = f"Complete again: __ × {b} = {record.product}"
            answer = str(a)
        elif tier == "Core":
            prompt = f"Use the same route again: {a} × __ = {record.product}"
            answer = str(b)
        else:
            prompt = f"Rebuild {record.product} using the known route: __ × {b} = {record.product}"
            answer = str(a)

        pattern_id = "product_hub"
        memory_cue_id = "repeat_known_route"
    else:
        x, y = alternate

        if tier == "Support":
            prompt = f"{x} × __ = {record.product}"
            answer = str(y)
        elif tier == "Core":
            prompt = f"Use another route: __ × {y} = {record.product}"
            answer = str(x)
        else:
            prompt = f"Complete another route for {record.product}: {x} × __ = {record.product}"
            answer = str(y)

        pattern_id = "same_product_different_routes"
        memory_cue_id = "missing_factor_other_route"

    return QuestionSpec(
        id=6,
        prompt_key="missing_factor_other_route",
        pupil_prompt=prompt,
        answer=answer,
        pattern_id=pattern_id,
        memory_cue_id=memory_cue_id,
    )


def _question_7_division_left(record: ProductRecord, tier: Tier) -> QuestionSpec:
    a, b = record.intro_route

    if tier == "Support":
        prompt = f"{record.product} ÷ {a} = __"
    elif tier == "Core":
        prompt = f"Complete: {record.product} ÷ {a} = __"
    else:
        prompt = f"Use division to rebuild the route: {record.product} ÷ {a} = __"

    return QuestionSpec(
        id=7,
        prompt_key="division_left",
        pupil_prompt=prompt,
        answer=str(b),
        pattern_id="route_in_route_out",
        memory_cue_id="division_left",
    )


def _question_8_division_right_or_other(
    record: ProductRecord,
    tier: Tier,
    alternate: tuple[int, int] | None,
) -> QuestionSpec:
    a, b = record.intro_route

    if alternate is None:
        if tier == "Support":
            prompt = f"{record.product} ÷ {b} = __"
        elif tier == "Core":
            prompt = f"Complete: {record.product} ÷ {b} = __"
        else:
            prompt = f"Use division again: {record.product} ÷ {b} = __"

        answer = str(a)
        pattern_id = "route_in_route_out"
        memory_cue_id = "division_right"
    else:
        x, y = alternate

        if tier == "Support":
            prompt = f"{record.product} ÷ {x} = __"
            answer = str(y)
        elif tier == "Core":
            prompt = f"Use another route with division: {record.product} ÷ {y} = __"
            answer = str(x)
        else:
            prompt = f"Use division with another route for {record.product}: {record.product} ÷ {x} = __"
            answer = str(y)

        pattern_id = "same_product_different_routes"
        memory_cue_id = "division_other_route"

    return QuestionSpec(
        id=8,
        prompt_key="division_right_or_other",
        pupil_prompt=prompt,
        answer=answer,
        pattern_id=pattern_id,
        memory_cue_id=memory_cue_id,
    )


def _question_9_rebuild_product(
    record: ProductRecord,
    tier: Tier,
    alternate: tuple[int, int] | None,
) -> QuestionSpec:
    route = alternate if alternate is not None else record.intro_route
    x, y = route

    if tier == "Support":
        prompt = f"Complete: I can rebuild {record.product} by using __ × __."
        answer = f"{x} × {y}"
    elif tier == "Core":
        prompt = f"Show one way to rebuild {record.product}."
        answer = f"{x} × {y}"
    else:
        prompt = f"Write one short sentence to show how you could rebuild {record.product}."
        answer = f"I can rebuild {record.product} by using {x} × {y}."

    return QuestionSpec(
        id=9,
        prompt_key="rebuild_product",
        pupil_prompt=prompt,
        answer=answer,
        pattern_id="product_hub",
        memory_cue_id="rebuild_product",
    )


def _question_10_true_structural_sentence(
    record: ProductRecord,
    tier: Tier,
    alternate: tuple[int, int] | None,
) -> QuestionSpec:
    truth = _true_structural_sentence(record, alternate)

    if tier == "Support":
        prompt = f"Complete: One true thing about {record.product} is __."
    elif tier == "Core":
        prompt = f"Tell one true thing about {record.product}."
    else:
        prompt = f"Write one short sentence to explain {record.product}."

    return QuestionSpec(
        id=10,
        prompt_key="true_structural_sentence",
        pupil_prompt=prompt,
        answer=truth,
        pattern_id="product_hub",
        memory_cue_id="true_structural_sentence",
    )


def _true_structural_sentence(
    record: ProductRecord,
    alternate: tuple[int, int] | None,
) -> str:
    square = _square_route(record.factor_families)

    if len(record.factor_families) > 1:
        return f"{record.product} has more than one way in."

    if square is not None:
        a, b = square
        return f"{record.product} is a square product because {a} × {b} = {record.product}."

    a, b = record.intro_route
    return f"{record.product} belongs in TMK World because {a} × {b} = {record.product}."


def _route_listing_pattern_id(record: ProductRecord) -> str:
    if len(record.factor_families) > 1:
        return "same_product_different_routes"
    return "product_hub"


def _alternate_family(record: ProductRecord) -> tuple[int, int] | None:
    intro = tuple(sorted(record.intro_route))

    for family in record.factor_families:
        if family != intro:
            return family

    return None


def _square_route(
    families: tuple[tuple[int, int], ...],
) -> tuple[int, int] | None:
    for a, b in families:
        if a == b:
            return (a, b)
    return None


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
