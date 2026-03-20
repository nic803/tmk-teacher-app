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
AnswerKind = Literal["number", "route", "route_list", "boolean", "text", "structured"]
ErrorMode = Literal["broken_route", "broken_output", "true_but_outside_world"]

WORKSHEET_QUESTION_COUNT: Final[int] = 10
WORKSHEET_TIER_MODE: Final[str] = "single"
WORKSHEET_OUTPUT_MODE: Final[str] = "python_data_first"
WORKSHEET_MEMORY_CUES: Final[str] = "teacher_key_only"

SECTION_ORDER: Final[Tuple[QuestionSection, ...]] = (
    "product_first",
    "ways_in",
    "ways_in",
    "ways_out",
    "ways_out",
    "another_way",
    "belongs",
    "error_repair",
    "final_explanation",
    "final_explanation",
)

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
    notes = (
        f"Stage {record.stage} worksheet for product {record.product}.",
        f"Tier: {tier}.",
        f"Intro route: {record.intro_route[0]}×{record.intro_route[1]}.",
        f"Structural role: {record.structural_role}.",
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
        "Core": "identify_product",
        "Extension": "explain_product_notice",
    }[tier]

    return WorksheetQuestion(
        id=question_id,
        section="product_first",
        prompt_key=prompt_key,
        answer_kind="number",
        prompt_data={"product": record.product, "stage": record.stage, "tier": tier},
        answer_data={"value": record.product},
        pattern_ids=_filter_patterns(
            attached_patterns,
            "product_hub",
            "boundary_belonging",
        ),
        msvwa_tags=("attention",),
    )


def _build_ways_in_question(
    record: ProductRecord,
    tier: Tier,
    attached_patterns: Tuple[str, ...],
    question_id: int,
    variant: Literal["intro", "other"],
) -> WorksheetQuestion:
    route = record.intro_route if variant == "intro" else _preferred_other_route(record)
    left, right = route

    prompt_key = {
        ("Support", "intro"): "complete_intro_way_in",
        ("Support", "other"): "complete_other_way_in",
        ("Core", "intro"): "find_intro_way_in",
        ("Core", "other"): "find_other_way_in",
        ("Extension", "intro"): "justify_intro_way_in",
        ("Extension", "other"): "justify_other_way_in",
    }[(tier, variant)]

    if tier == "Support":
        prompt_data = {"left": left, "right": None, "product": record.product}
        answer_data = {"value": right, "route": {"left": left, "right": right}}
        answer_kind: AnswerKind = "number"
    elif tier == "Core":
        prompt_data = {"left": left, "product": record.product}
        answer_data = {"route": {"left": left, "right": right}}
        answer_kind = "route"
    else:
        prompt_data = {
            "left": left,
            "product": record.product,
            "expected_route": {"left": left, "right": right},
        }
        answer_data = {
            "route": {"left": left, "right": right},
            "reason_keys": ("route_in_route_out",),
        }
        answer_kind = "structured"

    return WorksheetQuestion(
        id=question_id,
        section="ways_in",
        prompt_key=prompt_key,
        answer_kind=answer_kind,
        prompt_data=prompt_data,
        answer_data=answer_data,
        pattern_ids=_filter_patterns(
            attached_patterns,
            "route_in_route_out",
            "commutative_switch",
            "same_product_different_routes",
        ),
        msvwa_tags=("sequence", "working_memory"),
    )


def _build_ways_out_question(
    record: ProductRecord,
    tier: Tier,
    attached_patterns: Tuple[str, ...],
    question_id: int,
    variant: Literal["intro", "other"],
) -> WorksheetQuestion:
    route = record.intro_route if variant == "intro" else _preferred_other_route(record)
    divisor, quotient = route

    prompt_key = {
        ("Support", "intro"): "complete_intro_way_out",
        ("Support", "other"): "complete_other_way_out",
        ("Core", "intro"): "find_intro_way_out",
        ("Core", "other"): "find_other_way_out",
        ("Extension", "intro"): "justify_intro_way_out",
        ("Extension", "other"): "justify_other_way_out",
    }[(tier, variant)]

    if tier == "Support":
        prompt_data = {"product": record.product, "divisor": divisor, "quotient": None}
        answer_data = {"value": quotient, "division": {"product": record.product, "divisor": divisor, "quotient": quotient}}
        answer_kind: AnswerKind = "number"
    elif tier == "Core":
        prompt_data = {"product": record.product, "divisor": divisor}
        answer_data = {"division": {"product": record.product, "divisor": divisor, "quotient": quotient}}
        answer_kind = "structured"
    else:
        prompt_data = {
            "product": record.product,
            "divisor": divisor,
            "expected_division": {"product": record.product, "divisor": divisor, "quotient": quotient},
        }
        answer_data = {
            "division": {"product": record.product, "divisor": divisor, "quotient": quotient},
            "reason_keys": ("route_in_route_out",),
        }
        answer_kind = "structured"

    return WorksheetQuestion(
        id=question_id,
        section="ways_out",
        prompt_key=prompt_key,
        answer_kind=answer_kind,
        prompt_data=prompt_data,
        answer_data=answer_data,
        pattern_ids=_filter_patterns(
            attached_patterns,
            "route_in_route_out",
            "product_hub",
        ),
        msvwa_tags=("sequence", "working_memory"),
    )


def _build_another_way_question(
    record: ProductRecord,
    tier: Tier,
    attached_patterns: Tuple[str, ...],
    question_id: int,
) -> WorksheetQuestion:
    intro_route = record.intro_route
    other_route = _preferred_other_route(record)

    prompt_key = {
        "Support": "match_another_way",
        "Core": "find_another_way",
        "Extension": "compare_another_way",
    }[tier]

    if tier == "Support":
        prompt_data = {
            "product": record.product,
            "intro_route": {"left": intro_route[0], "right": intro_route[1]},
            "other_route": {"left": other_route[0], "right": other_route[1]},
        }
        answer_data = {"route": {"left": other_route[0], "right": other_route[1]}}
        answer_kind: AnswerKind = "route"
    elif tier == "Core":
        prompt_data = {"product": record.product, "intro_route": {"left": intro_route[0], "right": intro_route[1]}}
        answer_data = {"route": {"left": other_route[0], "right": other_route[1]}}
        answer_kind = "route"
    else:
        prompt_data = {
            "product": record.product,
            "intro_route": {"left": intro_route[0], "right": intro_route[1]},
            "other_route": {"left": other_route[0], "right": other_route[1]},
        }
        answer_data = {
            "route": {"left": other_route[0], "right": other_route[1]},
            "comparison_keys": _comparison_keys(record, intro_route, other_route),
        }
        answer_kind = "structured"

    return WorksheetQuestion(
        id=question_id,
        section="another_way",
        prompt_key=prompt_key,
        answer_kind=answer_kind,
        prompt_data=prompt_data,
        answer_data=answer_data,
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
    candidate = _nearest_non_belonging_number(record.product)

    if tier == "Support":
        prompt_key = "choose_belongs_number"
        prompt_data = {"candidates": (record.product, candidate)}
        answer_data = {"value": record.product}
        answer_kind: AnswerKind = "number"
    elif tier == "Core":
        prompt_key = "does_number_belong"
        prompt_data = {"candidate": candidate}
        answer_data = {"belongs": False}
        answer_kind = "boolean"
    else:
        prompt_key = "explain_belongs_decision"
        prompt_data = {"candidate": candidate}
        answer_data = {
            "belongs": False,
            "reason_key": "no_factor_pair_with_both_factors_at_most_10",
        }
        answer_kind = "structured"

    return WorksheetQuestion(
        id=question_id,
        section="belongs",
        prompt_key=prompt_key,
        answer_kind=answer_kind,
        prompt_data=prompt_data,
        answer_data=answer_data,
        pattern_ids=_filter_patterns(
            attached_patterns,
            "boundary_belonging",
        ),
        msvwa_tags=("magnitude", "attention"),
    )


def _build_error_repair_question(
    record: ProductRecord,
    tier: Tier,
    attached_patterns: Tuple[str, ...],
    question_id: int,
) -> WorksheetQuestion:
    mode = {
        "Support": "broken_output",
        "Core": "broken_route",
        "Extension": "true_but_outside_world",
    }[tier]

    if mode == "broken_output":
        left, right = record.intro_route
        wrong_product = _wrong_product(record.product)
        prompt_key = "repair_broken_output"
        prompt_data = {"left": left, "right": right, "product": wrong_product}
        answer_data = {
            "error_mode": mode,
            "correct_equation": {"left": left, "right": right, "product": record.product},
        }
    elif mode == "broken_route":
        wrong_left, wrong_right = _broken_route(record)
        prompt_key = "repair_broken_route"
        prompt_data = {"left": wrong_left, "right": wrong_right, "product": record.product}
        answer_data = {
            "error_mode": mode,
            "correct_equation": {
                "left": record.intro_route[0],
                "right": record.intro_route[1],
                "product": record.product,
            },
        }
    else:
        left = _outside_world_factor(record)
        right = 11
        prompt_key = "classify_true_but_outside_world"
        prompt_data = {"left": left, "right": right, "product": left * right}
        answer_data = {
            "error_mode": mode,
            "classification": "true_but_outside_tmk_world",
            "reason_key": "factor_above_10",
        }

    return WorksheetQuestion(
        id=question_id,
        section="error_repair",
        prompt_key=prompt_key,
        answer_kind="structured",
        prompt_data=prompt_data,
        answer_data=answer_data,
        pattern_ids=_filter_patterns(
            attached_patterns,
            "boundary_belonging",
            "route_in_route_out",
        ),
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

    prompt_key = {
        ("Support", "rebuild"): "say_how_to_rebuild",
        ("Support", "structure"): "choose_product_fact",
        ("Core", "rebuild"): "explain_how_to_rebuild",
        ("Core", "structure"): "explain_product_structure",
        ("Extension", "rebuild"): "justify_rebuild_strategy",
        ("Extension", "structure"): "generalise_product_structure",
    }[(tier, variant)]

    if variant == "rebuild":
        answer_data = {
            "accepted_routes": (
                {"left": record.intro_route[0], "right": record.intro_route[1]},
                {"left": other_route[0], "right": other_route[1]},
            ),
            "reason_keys": ("use_one_product_for_another", "route_in_route_out"),
        }
        prompt_data = {"product": record.product}
    else:
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
        prompt_data = {"product": record.product, "stage": record.stage}

    return WorksheetQuestion(
        id=question_id,
        section="final_explanation",
        prompt_key=prompt_key,
        answer_kind="structured",
        prompt_data=prompt_data,
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


def _preferred_other_route(record: ProductRecord) -> Tuple[int, int]:
    intro_family = tuple(sorted(record.intro_route))
    alternate_families = [route for route in record.factor_families if route != intro_family]

    if alternate_families:
        return alternate_families[0]

    intro_left, intro_right = record.intro_route
    if intro_left != intro_right:
        return (intro_right, intro_left)

    return record.intro_route


def _comparison_keys(
    record: ProductRecord,
    intro_route: Tuple[int, int],
    other_route: Tuple[int, int],
) -> Tuple[str, ...]:
    keys = ["same_product"]
    if tuple(sorted(intro_route)) != tuple(sorted(other_route)):
        keys.append("different_route_family")
    else:
        keys.append("same_family")
    if intro_route != other_route:
        keys.append("different_order_or_structure")
    if record.structural_role == "compression_hub":
        keys.append("compression_hub")
    return tuple(keys)


def _nearest_non_belonging_number(product: int) -> int:
    offsets = (1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6)
    for offset in offsets:
        candidate = product + offset
        if candidate > 0 and not belongs_to_p10(candidate):
            return candidate
    candidate = product + 11
    while belongs_to_p10(candidate):
        candidate += 1
    return candidate


def _wrong_product(product: int) -> int:
    candidate = product + 1
    if candidate != product:
        return candidate
    return product + 2


def _broken_route(record: ProductRecord) -> Tuple[int, int]:
    left, right = record.intro_route
    candidate_right = right + 1 if right < 10 else right - 1
    if left * candidate_right != record.product:
        return (left, candidate_right)
    candidate_left = left + 1 if left < 10 else left - 1
    return (candidate_left, right)


def _outside_world_factor(record: ProductRecord) -> int:
    return max(record.intro_route)


def _filter_patterns(attached_patterns: Tuple[str, ...], *pattern_ids: str) -> Tuple[str, ...]:
    pattern_set = set(pattern_ids)
    return tuple(pattern_id for pattern_id in attached_patterns if pattern_id in pattern_set)
