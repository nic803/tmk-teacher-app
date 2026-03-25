from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal, Tuple

from products import ProductRecord, belongs_to_p10
from tier_policy import QuestionForm, Tier, validate_form_for_tier
from worksheet_blueprints import WorksheetPurpose, WorksheetSlot


QuestionSection = Literal[
    "product_first",
    "ways_in",
    "ways_out",
    "structure",
    "belongs",
    "error_repair",
    "sorting",
    "final_explanation",
]


@dataclass(frozen=True)
class QuestionSpec:
    id: int
    tier: Tier
    section: QuestionSection
    purpose: WorksheetPurpose
    question_form: QuestionForm
    prompt_key: str
    prompt_data: Dict[str, object]
    answer_data: Dict[str, object]


def build_question_spec(record: ProductRecord, tier: Tier, slot: WorksheetSlot) -> QuestionSpec:
    form = _select_form_for_slot(tier, slot)

    if slot.purpose == "product_notice":
        return _build_product_notice_question(record, tier, slot.id, form)

    if slot.purpose == "intro_way_in":
        return _build_intro_way_in_question(record, tier, slot.id, form)

    if slot.purpose == "reverse_factor":
        return _build_reverse_factor_question(record, tier, slot.id, form)

    if slot.purpose == "way_out":
        return _build_way_out_question(record, tier, slot.id, form)

    if slot.purpose == "truth_check":
        return _build_truth_check_question(record, tier, slot.id, form)

    if slot.purpose == "compare_routes":
        return _build_compare_routes_question(record, tier, slot.id, form)

    if slot.purpose == "world_membership":
        return _build_world_membership_question(record, tier, slot.id, form)

    if slot.purpose == "error_repair":
        return _build_error_repair_question(record, tier, slot.id, form)

    if slot.purpose == "sorting":
        return _build_sorting_question(record, tier, slot.id, form)

    if slot.purpose == "explanation":
        return _build_explanation_question(record, tier, slot.id, form)

    raise ValueError(f"Unsupported worksheet purpose: {slot.purpose}")


def _select_form_for_slot(tier: Tier, slot: WorksheetSlot) -> QuestionForm:
    if not slot.allowed_forms:
        raise ValueError(f"Worksheet slot {slot.id} has no allowed forms.")

    form = slot.allowed_forms[0]
    validate_form_for_tier(tier, form)
    return form


def _build_product_notice_question(
    record: ProductRecord,
    tier: Tier,
    question_id: int,
    form: QuestionForm,
) -> QuestionSpec:
    section = "product_first"
    prompt_key = "product_notice"

    if form == "circle":
        prompt_key = "circle_product"
    elif form == "find":
        prompt_key = "find_product"
    elif form == "compare_routes":
        prompt_key = "notice_product_structure"

    return QuestionSpec(
        id=question_id,
        tier=tier,
        section=section,
        purpose="product_notice",
        question_form=form,
        prompt_key=prompt_key,
        prompt_data={"product": record.product},
        answer_data={"value": record.product},
    )


def _build_intro_way_in_question(
    record: ProductRecord,
    tier: Tier,
    question_id: int,
    form: QuestionForm,
) -> QuestionSpec:
    left, right = record.intro_route

    if form == "fill_blank":
        prompt_key = "complete_way_in"
    elif form == "complete":
        prompt_key = "complete_way_in"
    elif form == "rebuild_and_explain":
        prompt_key = "rebuild_intro_route"
    else:
        prompt_key = "complete_way_in"

    return QuestionSpec(
        id=question_id,
        tier=tier,
        section="ways_in",
        purpose="intro_way_in",
        question_form=form,
        prompt_key=prompt_key,
        prompt_data={"left": left, "product": record.product},
        answer_data={
            "value": right,
            "route": {"left": left, "right": right},
        },
    )


def _build_reverse_factor_question(
    record: ProductRecord,
    tier: Tier,
    question_id: int,
    form: QuestionForm,
) -> QuestionSpec:
    left, right = record.intro_route
    other_route = _other_route(record)

    if form == "match":
        prompt_key = "match_route"
        prompt_data = {
            "product": record.product,
            "route": {"left": left, "right": right},
        }
        answer_data = {"route": {"left": left, "right": right}}
    elif form == "find":
        prompt_key = "reverse_factor"
        prompt_data = {"right": right, "product": record.product}
        answer_data = {"value": left}
    elif form == "odd_one_out":
        options = _odd_one_out_options(record)
        prompt_key = "odd_one_out"
        prompt_data = {"product": record.product, "options": options}
        answer_data = {"odd_one_out": options[-1]}
    else:
        prompt_key = "reverse_factor"
        prompt_data = {"right": right, "product": record.product}
        answer_data = {"value": left}

    return QuestionSpec(
        id=question_id,
        tier=tier,
        section="ways_in",
        purpose="reverse_factor",
        question_form=form,
        prompt_key=prompt_key,
        prompt_data=prompt_data,
        answer_data=answer_data,
    )


def _build_way_out_question(
    record: ProductRecord,
    tier: Tier,
    question_id: int,
    form: QuestionForm,
) -> QuestionSpec:
    divisor, quotient = record.intro_route

    if form == "fill_blank":
        prompt_key = "way_out"
    elif form == "complete":
        prompt_key = "way_out"
    elif form == "compare_routes":
        prompt_key = "way_out_compare"
    else:
        prompt_key = "way_out"

    return QuestionSpec(
        id=question_id,
        tier=tier,
        section="ways_out",
        purpose="way_out",
        question_form=form,
        prompt_key=prompt_key,
        prompt_data={"product": record.product, "divisor": divisor},
        answer_data={
            "value": quotient,
            "division": {
                "product": record.product,
                "divisor": divisor,
                "quotient": quotient,
            },
        },
    )


def _build_truth_check_question(
    record: ProductRecord,
    tier: Tier,
    question_id: int,
    form: QuestionForm,
) -> QuestionSpec:
    left, right = record.intro_route

    if form == "tick_yes_no":
        prompt_key = "is_route"
        prompt_data = {"left": left, "right": right, "product": record.product}
        answer_data = {"value": True}
    elif form == "true_false":
        prompt_key = "truth_check"
        prompt_data = {"left": left, "right": right, "product": record.product}
        answer_data = {"value": True}
    elif form == "true_outside_false":
        outside_route = _true_outside_route(record)
        prompt_key = "true_outside_false"
        prompt_data = {
            "left": outside_route[0],
            "right": outside_route[1],
            "product": outside_route[0] * outside_route[1],
        }
        answer_data = {"classification": "true_but_outside"}
    else:
        prompt_key = "truth_check"
        prompt_data = {"left": left, "right": right, "product": record.product}
        answer_data = {"value": True}

    return QuestionSpec(
        id=question_id,
        tier=tier,
        section="structure",
        purpose="truth_check",
        question_form=form,
        prompt_key=prompt_key,
        prompt_data=prompt_data,
        answer_data=answer_data,
    )


def _build_compare_routes_question(
    record: ProductRecord,
    tier: Tier,
    question_id: int,
    form: QuestionForm,
) -> QuestionSpec:
    intro_left, intro_right = record.intro_route
    other = _other_route(record)

    if form == "match":
        prompt_key = "match_way_in_out"
        prompt_data = {"product": record.product}
        answer_data = {"route": {"left": intro_left, "right": intro_right}}
    elif form == "compare":
        prompt_key = "compare_routes"
        prompt_data = {
            "product": record.product,
            "route_a": {"left": intro_left, "right": intro_right},
            "route_b": {"left": other[0], "right": other[1]},
        }
        answer_data = {"comparison": "same_product"}
    elif form == "compare_routes":
        prompt_key = "compare_routes_family"
        prompt_data = {
            "product": record.product,
            "routes": tuple(
                {"left": left, "right": right}
                for left, right in _display_routes(record)
            ),
        }
        answer_data = {
            "routes": tuple(_display_routes(record)),
            "route_family_count": len(record.factor_families),
        }
    else:
        prompt_key = "compare_routes"
        prompt_data = {
            "product": record.product,
            "route_a": {"left": intro_left, "right": intro_right},
            "route_b": {"left": other[0], "right": other[1]},
        }
        answer_data = {"comparison": "same_product"}

    return QuestionSpec(
        id=question_id,
        tier=tier,
        section="structure",
        purpose="compare_routes",
        question_form=form,
        prompt_key=prompt_key,
        prompt_data=prompt_data,
        answer_data=answer_data,
    )


def _build_world_membership_question(
    record: ProductRecord,
    tier: Tier,
    question_id: int,
    form: QuestionForm,
) -> QuestionSpec:
    if form == "tick_yes_no":
        prompt_key = "belongs_yes_no"
        prompt_data = {"candidate": record.product}
        answer_data = {"value": True}
    elif form == "choose_one":
        outside_number = _outside_number(record.product)
        prompt_key = "choose_world_member"
        prompt_data = {"candidates": (record.product, outside_number)}
        answer_data = {"value": record.product}
    elif form == "true_false":
        prompt_key = "belongs_yes_no"
        prompt_data = {"candidate": record.product}
        answer_data = {"value": True}
    elif form == "true_outside_false":
        outside_route = _true_outside_route(record)
        prompt_key = "world_membership_classify"
        prompt_data = {
            "left": outside_route[0],
            "right": outside_route[1],
            "product": outside_route[0] * outside_route[1],
        }
        answer_data = {"classification": "true_but_outside"}
    else:
        prompt_key = "belongs_yes_no"
        prompt_data = {"candidate": record.product}
        answer_data = {"value": True}

    return QuestionSpec(
        id=question_id,
        tier=tier,
        section="belongs",
        purpose="world_membership",
        question_form=form,
        prompt_key=prompt_key,
        prompt_data=prompt_data,
        answer_data=answer_data,
    )


def _build_error_repair_question(
    record: ProductRecord,
    tier: Tier,
    question_id: int,
    form: QuestionForm,
) -> QuestionSpec:
    left, right = record.intro_route
    wrong_right = right + 1 if right < 10 else right - 1

    if form == "fill_blank":
        prompt_key = "repair_equation"
        prompt_data = {"left": left, "product": record.product}
        answer_data = {"value": right}
    elif form == "complete":
        prompt_key = "repair_equation"
        prompt_data = {"left": left, "product": record.product}
        answer_data = {"value": right}
    elif form == "sort_and_justify":
        options = _repair_sort_options(record)
        prompt_key = "sort_and_justify"
        prompt_data = {"product": record.product, "options": options}
        answer_data = {
            "valid": tuple(option for option in options if option["classification"] == "inside"),
            "outside": tuple(option for option in options if option["classification"] == "outside"),
            "false": tuple(option for option in options if option["classification"] == "false"),
        }
    else:
        prompt_key = "repair_broken_route"
        prompt_data = {"left": left, "right": wrong_right, "product": record.product}
        answer_data = {
            "correct_equation": {"left": left, "right": right, "product": record.product}
        }

    return QuestionSpec(
        id=question_id,
        tier=tier,
        section="error_repair",
        purpose="error_repair",
        question_form=form,
        prompt_key=prompt_key,
        prompt_data=prompt_data,
        answer_data=answer_data,
    )


def _build_sorting_question(
    record: ProductRecord,
    tier: Tier,
    question_id: int,
    form: QuestionForm,
) -> QuestionSpec:
    route_options = _sorting_options(record)

    if form == "match":
        prompt_key = "choose_route"
        prompt_data = {"product": record.product, "options": route_options}
        answer_data = {"route": {"left": record.intro_route[0], "right": record.intro_route[1]}}
    elif form == "simple_sort":
        prompt_key = "sort_routes"
        prompt_data = {"product": record.product, "options": route_options}
        answer_data = {
            "valid_routes": tuple(
                option["route"]
                for option in route_options
                if option["classification"] == "inside"
            )
        }
    elif form == "sort_and_justify":
        prompt_key = "sort_and_justify"
        prompt_data = {"product": record.product, "options": route_options}
        answer_data = {
            "valid": tuple(option for option in route_options if option["classification"] == "inside"),
            "outside": tuple(option for option in route_options if option["classification"] == "outside"),
            "false": tuple(option for option in route_options if option["classification"] == "false"),
        }
    else:
        prompt_key = "sort_routes"
        prompt_data = {"product": record.product, "options": route_options}
        answer_data = {
            "valid_routes": tuple(
                option["route"]
                for option in route_options
                if option["classification"] == "inside"
            )
        }

    return QuestionSpec(
        id=question_id,
        tier=tier,
        section="sorting",
        purpose="sorting",
        question_form=form,
        prompt_key=prompt_key,
        prompt_data=prompt_data,
        answer_data=answer_data,
    )


def _build_explanation_question(
    record: ProductRecord,
    tier: Tier,
    question_id: int,
    form: QuestionForm,
) -> QuestionSpec:
    if form == "fill_blank":
        prompt_key = "belongs_reason"
        prompt_data = {"product": record.product}
        answer_data = {"route": {"left": record.intro_route[0], "right": record.intro_route[1]}}
    elif form == "find":
        prompt_key = "rebuild_product"
        prompt_data = {"product": record.product}
        answer_data = {"accepted_routes": tuple(_display_routes(record))}
    elif form == "compare":
        prompt_key = "rebuild_product"
        prompt_data = {"product": record.product}
        answer_data = {"accepted_routes": tuple(_display_routes(record))}
    elif form == "one_sentence_explain":
        prompt_key = "one_sentence_explain"
        prompt_data = {"product": record.product}
        answer_data = {
            "accepted_pattern_ids": ("product_hub", "route_in_route_out"),
            "accepted_routes": tuple(_display_routes(record)),
        }
    else:
        prompt_key = "explain_product"
        prompt_data = {"product": record.product}
        answer_data = {"accepted_routes": tuple(_display_routes(record))}

    return QuestionSpec(
        id=question_id,
        tier=tier,
        section="final_explanation",
        purpose="explanation",
        question_form=form,
        prompt_key=prompt_key,
        prompt_data=prompt_data,
        answer_data=answer_data,
    )


def _display_routes(record: ProductRecord) -> Tuple[Tuple[int, int], ...]:
    if len(record.factor_families) > 1:
        return record.factor_families
    if record.intro_route[0] == record.intro_route[1]:
        return (record.intro_route,)
    return (record.intro_route,)


def _other_route(record: ProductRecord) -> Tuple[int, int]:
    intro_family = tuple(sorted(record.intro_route))
    for route in record.factor_families:
        if route != intro_family:
            return route
    return record.intro_route


def _outside_number(product: int) -> int:
    preferred = (77, 121, 33, 22)
    for candidate in preferred:
        if candidate != product and not belongs_to_p10(candidate):
            return candidate

    candidate = product + 1
    while belongs_to_p10(candidate):
        candidate += 1
    return candidate


def _true_outside_route(record: ProductRecord) -> Tuple[int, int]:
    left = max(record.intro_route)
    right = 11
    return (left, right)


def _odd_one_out_options(record: ProductRecord) -> Tuple[Dict[str, object], ...]:
    valid_routes = _display_routes(record)
    options = [
        {"route": {"left": left, "right": right}, "classification": "inside"}
        for left, right in valid_routes[:2]
    ]

    false_route = {
        "route": {
            "left": record.intro_route[0],
            "right": record.intro_route[1] + 1 if record.intro_route[1] < 10 else record.intro_route[1] - 1,
        },
        "classification": "false",
    }

    while len(options) < 2:
        options.append({"route": {"left": record.intro_route[0], "right": record.intro_route[1]}, "classification": "inside"})

    options.append(false_route)
    return tuple(options)


def _sorting_options(record: ProductRecord) -> Tuple[Dict[str, object], ...]:
    valid_routes = [
        {
            "route": {"left": left, "right": right},
            "classification": "inside",
        }
        for left, right in _display_routes(record)
    ]

    outside_left, outside_right = _true_outside_route(record)
    outside_option = {
        "route": {"left": outside_left, "right": outside_right},
        "classification": "outside",
    }

    false_option = {
        "route": {
            "left": record.intro_route[0],
            "right": record.intro_route[1] + 1 if record.intro_route[1] < 10 else record.intro_route[1] - 1,
        },
        "classification": "false",
    }

    options = valid_routes + [outside_option, false_option]
    return tuple(options)


def _repair_sort_options(record: ProductRecord) -> Tuple[Dict[str, object], ...]:
    return _sorting_options(record)
