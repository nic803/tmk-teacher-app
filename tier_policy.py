from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal, Tuple


Tier = Literal["Support", "Core", "Extension"]


QuestionForm = Literal[
    "circle",
    "tick_yes_no",
    "match",
    "fill_blank",
    "complete",
    "find",
    "choose_one",
    "true_false",
    "compare",
    "simple_sort",
    "odd_one_out",
    "one_sentence_explain",
    "sort_and_justify",
    "true_outside_false",
    "rebuild_and_explain",
    "compare_routes",
]


@dataclass(frozen=True)
class TierFormPolicy:
    tier: Tier
    preferred_forms: Tuple[QuestionForm, ...]


TIER_FORM_POLICY: Dict[Tier, TierFormPolicy] = {
    "Support": TierFormPolicy(
        tier="Support",
        preferred_forms=(
            "circle",
            "tick_yes_no",
            "match",
            "fill_blank",
        ),
    ),
    "Core": TierFormPolicy(
        tier="Core",
        preferred_forms=(
            "complete",
            "find",
            "choose_one",
            "true_false",
            "compare",
            "simple_sort",
        ),
    ),
    "Extension": TierFormPolicy(
        tier="Extension",
        preferred_forms=(
            "odd_one_out",
            "one_sentence_explain",
            "sort_and_justify",
            "true_outside_false",
            "rebuild_and_explain",
            "compare_routes",
        ),
    ),
}


def preferred_forms_for_tier(tier: Tier) -> Tuple[QuestionForm, ...]:
    return TIER_FORM_POLICY[tier].preferred_forms


def form_allowed_for_tier(tier: Tier, form: QuestionForm) -> bool:
    return form in TIER_FORM_POLICY[tier].preferred_forms


def validate_form_for_tier(tier: Tier, form: QuestionForm) -> None:
    if not form_allowed_for_tier(tier, form):
        raise ValueError(
            f"Question form '{form}' is not allowed for tier '{tier}'. "
            f"Allowed forms: {preferred_forms_for_tier(tier)}"
        )
