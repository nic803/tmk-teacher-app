from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Final, Literal, Tuple

from tier_policy import QuestionForm, Tier, form_allowed_for_tier


WorksheetPurpose = Literal[
    "product_notice",
    "intro_way_in",
    "reverse_factor",
    "way_out",
    "truth_check",
    "compare_routes",
    "world_membership",
    "error_repair",
    "sorting",
    "explanation",
]


@dataclass(frozen=True)
class WorksheetSlot:
    id: int
    purpose: WorksheetPurpose
    allowed_forms: Tuple[QuestionForm, ...]


@dataclass(frozen=True)
class WorksheetBlueprint:
    tier: Tier
    slots: Tuple[WorksheetSlot, ...]


SUPPORT_BLUEPRINT: Final[WorksheetBlueprint] = WorksheetBlueprint(
    tier="Support",
    slots=(
        WorksheetSlot(1, "product_notice", ("circle",)),
        WorksheetSlot(2, "intro_way_in", ("fill_blank",)),
        WorksheetSlot(3, "reverse_factor", ("match",)),
        WorksheetSlot(4, "way_out", ("fill_blank",)),
        WorksheetSlot(5, "truth_check", ("tick_yes_no",)),
        WorksheetSlot(6, "compare_routes", ("match",)),
        WorksheetSlot(7, "world_membership", ("tick_yes_no",)),
        WorksheetSlot(8, "error_repair", ("fill_blank",)),
        WorksheetSlot(9, "sorting", ("match",)),
        WorksheetSlot(10, "explanation", ("fill_blank",)),
    ),
)

CORE_BLUEPRINT: Final[WorksheetBlueprint] = WorksheetBlueprint(
    tier="Core",
    slots=(
        WorksheetSlot(1, "product_notice", ("find",)),
        WorksheetSlot(2, "intro_way_in", ("complete",)),
        WorksheetSlot(3, "reverse_factor", ("find",)),
        WorksheetSlot(4, "way_out", ("complete",)),
        WorksheetSlot(5, "truth_check", ("true_false",)),
        WorksheetSlot(6, "compare_routes", ("compare",)),
        WorksheetSlot(7, "world_membership", ("choose_one", "true_false")),
        WorksheetSlot(8, "error_repair", ("complete",)),
        WorksheetSlot(9, "sorting", ("simple_sort",)),
        WorksheetSlot(10, "explanation", ("compare", "find")),
    ),
)

EXTENSION_BLUEPRINT: Final[WorksheetBlueprint] = WorksheetBlueprint(
    tier="Extension",
    slots=(
        WorksheetSlot(1, "product_notice", ("compare_routes",)),
        WorksheetSlot(2, "intro_way_in", ("rebuild_and_explain",)),
        WorksheetSlot(3, "reverse_factor", ("odd_one_out",)),
        WorksheetSlot(4, "way_out", ("compare_routes",)),
        WorksheetSlot(5, "truth_check", ("true_outside_false",)),
        WorksheetSlot(6, "compare_routes", ("compare_routes",)),
        WorksheetSlot(7, "world_membership", ("true_outside_false",)),
        WorksheetSlot(8, "error_repair", ("sort_and_justify",)),
        WorksheetSlot(9, "sorting", ("sort_and_justify",)),
        WorksheetSlot(10, "explanation", ("one_sentence_explain",)),
    ),
)

BLUEPRINTS: Final[Dict[Tier, WorksheetBlueprint]] = {
    "Support": SUPPORT_BLUEPRINT,
    "Core": CORE_BLUEPRINT,
    "Extension": EXTENSION_BLUEPRINT,
}


def blueprint_for_tier(tier: Tier) -> WorksheetBlueprint:
    return BLUEPRINTS[tier]


def blueprint_slots_for_tier(tier: Tier) -> Tuple[WorksheetSlot, ...]:
    return BLUEPRINTS[tier].slots


def validate_blueprint(blueprint: WorksheetBlueprint) -> None:
    if len(blueprint.slots) != 10:
        raise ValueError(
            f"Worksheet blueprint for tier '{blueprint.tier}' must contain exactly 10 slots."
        )

    expected_ids = tuple(range(1, 11))
    actual_ids = tuple(slot.id for slot in blueprint.slots)

    if actual_ids != expected_ids:
        raise ValueError(
            f"Worksheet blueprint for tier '{blueprint.tier}' must use slot ids 1..10 in order. "
            f"Found {actual_ids}."
        )

    for slot in blueprint.slots:
        if not slot.allowed_forms:
            raise ValueError(
                f"Worksheet slot {slot.id} in tier '{blueprint.tier}' has no allowed forms."
            )

        for form in slot.allowed_forms:
            if not form_allowed_for_tier(blueprint.tier, form):
                raise ValueError(
                    f"Worksheet slot {slot.id} in tier '{blueprint.tier}' uses form '{form}', "
                    f"which is not allowed for that tier."
                )


def validate_all_blueprints() -> None:
    for blueprint in BLUEPRINTS.values():
        validate_blueprint(blueprint)
