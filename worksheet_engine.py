from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Final, Literal, Tuple

from memory_cues import MemoryCue, memory_cues_for_product
from patterns import product_pattern_ids
from products import ALL_PRODUCTS, ProductRecord, belongs_to_p10, product_record

Tier = Literal["Support", "Core", "Extension"]
QuestionSection = Literal[
    "product_first",
    "ways_in",
    "ways_out",
    "another_way",
    "belongs",
    "error_repair",
    "final_explanation",
]
AnswerKind = Literal["number", "route", "boolean", "text", "structured"]
ErrorMode = Literal["broken_route", "broken_output", "true_but_outside_world"]

WORKSHEET_QUESTION_COUNT: Final[int] = 10
WORKSHEET_TIER_MODE: Final[str] = "single"
WORKSHEET_OUTPUT_MODE: Final[str] = "python_data_first"
WORKSHEET_MEMORY_CUES: Final[str] = "teacher_key_only"

VALID_TIERS: Final[Tuple[Tier, ...]] = ("Support", "Core", "Extension")


@dataclass(frozen=True)
class WorksheetQuestion:
    id: int
    section: QuestionSection
    prompt_key: str
    answer_kind: AnswerKind
    prompt_data: Dict[str, object]
    answer_data: Dict[str, object]
    pattern_ids: Tuple[str, ...]
    msvwa_tags: Tuple[str, ...]


@dataclass(frozen=True)
class WorksheetTeacherKey:
    answers: Tuple[Dict[str, object], ...]
    pattern_ids: Tuple[str, ...]
    memory_cue_ids: Tuple[str, ...]
    notes: Tuple[str, ...]


@dataclass(frozen=True)
class Worksheet:
    product: int
    stage: str
    tier: Tier
    questions: Tuple[WorksheetQuestion, ...]
    teacher_key: WorksheetTeacherKey


def generate_worksheet(product: int, tier: Tier) -> Worksheet:
    _validate_product(product)
    _validate_tier(tier)

    record = product_record(product)
    attached_patterns = attached_product_pattern_ids(product)
    questions = _build_questions(record, tier, attached_patterns)
    teacher_key = _build_teacher_key(record, tier, questions, attached_patterns)

    return Worksheet(
        product=record.product,
        stage=record.stage,
        tier=tier,
        questions=questions,
        teacher_key=teacher_key,
    )


def generate_worksheet_dict(product: int, tier: Tier) -> Dict[str, object]:
    return asdict(generate_worksheet(product, tier))


def attached_product_pattern_ids(product: int) -> Tuple[str, ...]:
    return product_pattern_ids(product)


def teacher_memory_cues_for_product(product: int) -> Tuple[MemoryCue, ...]:
    return memory_cues_for_product(product)


def _validate_product(product: int) -> None:
    if product not in ALL_PRODUCTS:
        raise ValueError(f"Unknown TMK product: {product}")


def _validate_tier(tier: str) -> None:
    if tier not in VALID_TIERS:
        raise ValueError(f"Unknown worksheet tier: {tier}")


def _build_questions(
    record: ProductRecord,
    tier: Tier,
    attached_patterns: Tuple[str, ...],
) -> Tuple[WorksheetQuestion, ...]:
    questions = (
        _build_product_first_question(record, tier, attached_patterns, 1),
        _build_ways_in_question(record, tier, attached_patterns, 2, variant="intro"),
        _build_ways_in_question(record, tier, attached_patterns, 3, variant="other"),
        _build_ways_out_question(record, tier, attached_patterns, 4, variant="intro"),
        _build_ways_out_question(record, tier, attached_patterns, 5, variant="other"),
        _build_another_way_question(record, tier, attached_patterns, 6),
        _build_belongs_question(record, tier, attached_patterns, 7),
        _build_error_repair_question(record, tier, attached_patterns, 8),
        _build_final_explanation_question(record, tier, attached_patterns, 9, variant="rebuild"),
        _build_final_explanation_question(record, tier, attached_patterns, 10, variant="structure"),
    )

    if len(questions) != WORKSHEET_QUESTION_COUNT:
        raise ValueError("Worksheet question count is not canonical.")

    return questions


def _build_teacher_key(
    record: ProductRecord,
    tier: Tier,
    questions: Tuple[WorksheetQuestion, ...],
    attached_patterns: Tuple[str, ...],
) -> WorksheetTeacherKey:
    cues = teacher_memory_cues_for_product(record.product)

    route_family_count = len(record.factor_families)
    route_note = (
        f"{route_family_count} factor family"
        if route_family_count == 1
        else f"{route_family_count} factor families"
    )

    notes = (
        f"Stage {record.stage} worksheet for product {record.product}.",
        f"Tier: {tier}.",
        f"Intro route: {record.intro_route[0]}×{record.intro_route[1]}.",
        f"Structural role: {record.structural_role}.",
        f"Route structure: {route_note}.",
        "Memory cues are teacher-side only.",
    )

    return WorksheetTeacherKey(
        answers=tuple(question.answer_data for question in questions),
        pattern_ids=attached_patterns,
        memory_cue_ids=tuple(cue.id for cue in cues),
        notes=notes,
    )


def _build_product_first_question(
    record: ProductRecord,
    tier: Tier,
    attached_patterns: Tuple[str, ...],
    question_id: int,
) -> WorksheetQuestion:
    prompt_key = {
        "Support": "notice_product",
        "Core": "find_product",
        "Extension": "notice_product_structure",
    }[tier]

    return WorksheetQuestion(
        id=question_id,
        section="product_first",
        prompt_key=prompt_key,
        answer_kind="number",
        prompt_data={"product": record.product},
        answer_data={"value": record.product},
        pattern_ids=_filter_patterns(attached_patterns, "product_hub", "boundary_belonging"),
        msvwa_tags=("attention",),
    )


def _build_ways_in_question(
    record: ProductRecord,
    tier: Tier,
    attached_patterns: Tuple[str, ...],
    question_id: int,
    variant: Literal["intro", "other"],
) -> WorksheetQuestion:
    if variant == "intro":
        left, right = record.intro_route
        prompt_key = {
            "Support": "complete_way_in",
            "Core": "find_way_in",
            "Extension": "show_way_in",
        }[tier]
        answer_kind: AnswerKind = "structured" if tier == "Extension" else "number"
        return WorksheetQuestion(
            id=question_id,
            section="ways_in",
            prompt_key=prompt_key,
            answer_kind=answer_kind,
            prompt_data={"left": left, "product": record.product},
            answer_data={"value": right, "route": {"left": left, "right": right}},
            pattern_ids=_filter_patterns(attached_patterns, "route_in_route_out", "product_hub"),
            msvwa_tags=("sequence", "working_memory"),
        )

    other_route = _preferred_other_route(record)
    if other_route is None:
        prompt_key = {
            "Support": "single_way_in_notice",
            "Core": "single_way_in_notice",
            "Extension": "single_way_in_explain",
        }[tier]
        return WorksheetQuestion(
            id=question_id,
            section="ways_in",
            prompt_key=prompt_key,
            answer_kind="structured",
            prompt_data={
                "product": record.product,
                "route": {"left": record.intro_route[0], "right": record.intro_route[1]},
            },
            answer_data={
                "has_another_way_in": False,
                "route": {"left": record.intro_route[0], "right": record.intro_route[1]},
            },
            pattern_ids=_filter_patterns(attached_patterns, "route_multiplicity", "product_hub"),
            msvwa_tags=("attention", "variation"),
        )

    left, right = other_route
    prompt_key = {
        "Support": "complete_another_way_in",
        "Core": "find_another_way_in",
        "Extension": "show_another_way_in",
    }[tier]
    answer_kind = "structured" if tier == "Extension" else "number"

    return WorksheetQuestion(
        id=question_id,
        section="ways_in",
        prompt_key=prompt_key,
        answer_kind=answer_kind,
        prompt_data={"left": left, "product": record.product},
        answer_data={"value": right, "route": {"left": left, "right": right}},
        pattern_ids=_filter_patterns(
            attached_patterns,
            "same_product_different_routes",
            "product_family_overlap",
            "route_multiplicity",
        ),
        msvwa_tags=("sequence", "variation"),
    )


def _build_ways_out_question(
    record: ProductRecord,
    tier: Tier,
    attached_patterns: Tuple[str, ...],
    question_id: int,
    variant: Literal["intro", "other"],
) -> WorksheetQuestion:
    if variant == "intro":
        divisor, quotient = record.intro_route
        prompt_key = {
            "Support": "complete_way_out",
            "Core": "complete_way_out",
            "Extension": "show_way_out",
        }[tier]
        return WorksheetQuestion(
            id=question_id,
            section="ways_out",
            prompt_key=prompt_key,
            answer_kind="number" if tier != "Extension" else "structured",
            prompt_data={"product": record.product, "divisor": divisor},
            answer_data={"value": quotient, "division": {"product": record.product, "divisor": divisor, "quotient": quotient}},
            pattern_ids=_filter_patterns(attached_patterns, "route_in_route_out"),
            msvwa_tags=("sequence", "working_memory"),
        )

    other_route = _preferred_other_route(record)
    if other_route is None:
        prompt_key = {
            "Support": "single_way_out_notice",
            "Core": "single_way_out_notice",
            "Extension": "single_way_out_explain",
        }[tier]
        return WorksheetQuestion(
            id=question_id,
            section="ways_out",
            prompt_key=prompt_key,
            answer_kind="structured",
            prompt_data={
                "product": record.product,
                "division": {
                    "product": record.product,
                    "divisor": record.intro_route[0],
                    "quotient": record.intro_route[1],
                },
            },
            answer_data={
                "has_another_way_out": False,
                "division": {
                    "product": record.product,
                    "divisor": record.intro_route[0],
                    "quotient": record.intro_route[1],
                },
            },
            pattern_ids=_filter_patterns(attached_patterns, "route_multiplicity", "route_in_route_out"),
            msvwa_tags=("attention", "variation"),
        )

    divisor, quotient = other_route
    prompt_key = {
        "Support": "complete_another_way_out",
        "Core": "complete_another_way_out",
        "Extension": "show_another_way_out",
    }[tier]

    return WorksheetQuestion(
        id=question_id,
        section="ways_out",
        prompt_key=prompt_key,
        answer_kind="number" if tier != "Extension" else "structured",
        prompt_data={"product": record.product, "divisor": divisor},
        answer_data={"value": quotient, "division": {"product": record.product, "divisor": divisor, "quotient": quotient}},
        pattern_ids=_filter_patterns(
            attached_patterns,
            "same_product_different_routes",
            "product_family_overlap",
            "route_multiplicity",
        ),
        msvwa_tags=("sequence", "variation"),
    )


def _build_another_way_question(
    record: ProductRecord,
    tier: Tier,
    attached_patterns: Tuple[str, ...],
    question_id: int,
) -> WorksheetQuestion:
    other_route = _preferred_other_route(record)

    if other_route is None:
        prompt_key = {
            "Support": "one_way_in_only",
            "Core": "one_way_in_only",
            "Extension": "explain_one_way_in_only",
        }[tier]
        return WorksheetQuestion(
            id=question_id,
            section="another_way",
            prompt_key=prompt_key,
            answer_kind="structured",
            prompt_data={
                "product": record.product,
                "route": {"left": record.intro_route[0], "right": record.intro_route[1]},
            },
            answer_data={
                "has_another_way_in": False,
                "route": {"left": record.intro_route[0], "right": record.intro_route[1]},
            },
            pattern_ids=_filter_patterns(attached_patterns, "route_multiplicity"),
            msvwa_tags=("variation", "attention"),
        )

    return WorksheetQuestion(
        id=question_id,
        section="another_way",
        prompt_key={
            "Support": "find_another_way",
            "Core": "find_another_way",
            "Extension": "compare_two_ways",
        }[tier],
        answer_kind="structured",
        prompt_data={
            "product": record.product,
            "intro_route": {"left": record.intro_route[0], "right": record.intro_route[1]},
            "other_route": {"left": other_route[0], "right": other_route[1]},
        },
        answer_data={
            "route": {"left": other_route[0], "right": other_route[1]},
            "comparison_keys": _comparison_keys(record, record.intro_route, other_route),
        },
        pattern_ids=_filter_patterns(
            attached_patterns,
            "same_product_different_routes",
            "product_family_overlap",
            "route_multiplicity",
        ),
        msvwa_tags=("variation", "attention"),
    )


def _build_belongs_question(
    record: ProductRecord,
    tier: Tier,
    attached_patterns: Tuple[str, ...],
    question_id: int,
) -> WorksheetQuestion:
    contrast = _outside_world_contrast(record.product)

    if tier == "Support":
        return WorksheetQuestion(
            id=question_id,
            section="belongs",
            prompt_key="belongs_yes_no",
            answer_kind="boolean",
            prompt_data={"candidate": record.product},
            answer_data={"belongs": True},
            pattern_ids=_filter_patterns(attached_patterns, "boundary_belonging"),
            msvwa_tags=("magnitude", "attention"),
        )

    if tier == "Core":
        return WorksheetQuestion(
            id=question_id,
            section="belongs",
            prompt_key="belongs_yes_no",
            answer_kind="boolean",
            prompt_data={"candidate": record.product},
            answer_data={"belongs": True},
            pattern_ids=_filter_patterns(attached_patterns, "boundary_belonging"),
            msvwa_tags=("magnitude", "attention"),
        )

    return WorksheetQuestion(
        id=question_id,
        section="belongs",
        prompt_key="belongs_explain_outside",
        answer_kind="structured",
        prompt_data={"candidate": contrast},
        answer_data={
            "belongs": False,
            "reason_key": "true_but_outside_or_no_valid_tmk_route",
        },
        pattern_ids=_filter_patterns(attached_patterns, "boundary_belonging"),
        msvwa_tags=("magnitude", "attention"),
    )


def _build_error_repair_question(
    record: ProductRecord,
    tier: Tier,
    attached_patterns: Tuple[str, ...],
    question_id: int,
) -> WorksheetQuestion:
    if tier == "Support":
        left, right = record.intro_route
        wrong_product = _wrong_product(record.product)
        return WorksheetQuestion(
            id=question_id,
            section="error_repair",
            prompt_key="repair_broken_output",
            answer_kind="structured",
            prompt_data={"left": left, "right": right, "product": wrong_product},
            answer_data={
                "error_mode": "broken_output",
                "correct_equation": {"left": left, "right": right, "product": record.product},
            },
            pattern_ids=_filter_patterns(attached_patterns, "route_in_route_out"),
            msvwa_tags=("attention", "working_memory"),
        )

    if tier == "Core":
        outside_left = max(record.intro_route)
        outside_right = 11
        outside_product = outside_left * outside_right
        return WorksheetQuestion(
            id=question_id,
            section="error_repair",
            prompt_key="check_true_but_outside_world",
            answer_kind="structured",
            prompt_data={"left": outside_left, "right": outside_right, "product": outside_product},
            answer_data={
                "error_mode": "true_but_outside_world",
                "classification": "true_but_outside_tmk_world",
                "reason_key": "factor_above_10",
            },
            pattern_ids=_filter_patterns(attached_patterns, "boundary_belonging"),
            msvwa_tags=("attention", "working_memory"),
        )

    wrong_left, wrong_right = _broken_route(record)
    return WorksheetQuestion(
        id=question_id,
        section="error_repair",
        prompt_key="repair_broken_route",
        answer_kind="structured",
        prompt_data={"left": wrong_left, "right": wrong_right, "product": record.product},
        answer_data={
            "error_mode": "broken_route",
            "correct_equation": {
                "left": record.intro_route[0],
                "right": record.intro_route[1],
                "product": record.product,
            },
        },
        pattern_ids=_filter_patterns(attached_patterns, "route_in_route_out", "boundary_belonging"),
        msvwa_tags=("attention", "working_memory"),
    )


def _build_final_explanation_question(
    record: ProductRecord,
    tier: Tier,
    attached_patterns: Tuple[str, ...],
    question_id: int,
    variant: Literal["rebuild", "structure"],
) -> WorksheetQuestion:
    other_route = _preferred_other_route(record)
    accepted_routes = [{"left": record.intro_route[0], "right": record.intro_route[1]}]
    if other_route is not None:
        accepted_routes.append({"left": other_route[0], "right": other_route[1]})

    if variant == "rebuild":
        prompt_key = {
            "Support": "complete_rebuild",
            "Core": "explain_rebuild",
            "Extension": "justify_rebuild",
        }[tier]
        answer_data = {
            "accepted_routes": tuple(accepted_routes),
            "reason_keys": ("use_one_product_for_another", "route_in_route_out"),
        }
    else:
        prompt_key = {
            "Support": "complete_belongs_reason",
            "Core": "tell_one_true_thing",
            "Extension": "explain_structure",
        }[tier]
        answer_data = {
            "accepted_pattern_ids": _filter_patterns(
                attached_patterns,
                "product_hub",
                "route_multiplicity",
                "product_family_overlap",
                "square_pattern",
                "closure_with_7x7",
            ),
            "structural_role": record.structural_role,
        }

    return WorksheetQuestion(
        id=question_id,
        section="final_explanation",
        prompt_key=prompt_key,
        answer_kind="structured",
        prompt_data={"product": record.product, "stage": record.stage},
        answer_data=answer_data,
        pattern_ids=_filter_patterns(
            attached_patterns,
            "use_one_product_for_another",
            "product_hub",
            "route_multiplicity",
            "product_family_overlap",
            "square_pattern",
            "closure_with_7x7",
        ),
        msvwa_tags=("working_memory", "attention", "variation"),
    )


def _preferred_other_route(record: ProductRecord) -> Tuple[int, int] | None:
    intro_family = tuple(sorted(record.intro_route))
    alternate_families = [route for route in record.factor_families if route != intro_family]
    if alternate_families:
        return alternate_families[0]
    return None


def _comparison_keys(
    record: ProductRecord,
    intro_route: Tuple[int, int],
    other_route: Tuple[int, int],
) -> Tuple[str, ...]:
    keys = ["same_product", "different_route_family"]
    if record.structural_role == "compression_hub":
        keys.append("compression_hub")
    return tuple(keys)


def _outside_world_contrast(product: int) -> int:
    preferred = (77, 121, 33, 22)
    for candidate in preferred:
        if candidate != product:
            return candidate
    candidate = product + 11
    while belongs_to_p10(candidate):
        candidate += 1
    return candidate


def _wrong_product(product: int) -> int:
    candidate = product + 1
    while candidate == product:
        candidate += 1
    return candidate


def _broken_route(record: ProductRecord) -> Tuple[int, int]:
    left, right = record.intro_route
    candidate_right = right + 1 if right < 10 else right - 1
    if left * candidate_right != record.product:
        return (left, candidate_right)
    candidate_left = left + 1 if left < 10 else left - 1
    return (candidate_left, right)


def _filter_patterns(attached_patterns: Tuple[str, ...], *pattern_ids: str) -> Tuple[str, ...]:
    allowed = set(pattern_ids)
    return tuple(pattern_id for pattern_id in attached_patterns if pattern_id in allowed)
