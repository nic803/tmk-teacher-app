from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Final, Literal, Tuple

from tier_policy import Tier
from worksheet_blueprints import WorksheetBlueprint


BlueprintVariant = Literal["A", "B", "C"]


@dataclass(frozen=True)
class TierBlueprintSet:
    tier: Tier
    variants: Dict[BlueprintVariant, WorksheetBlueprint]


BLUEPRINT_ROTATION: Final[Dict[Tier, TierBlueprintSet]] = {}


def register_blueprint_set(
    tier: Tier,
    variant_a: WorksheetBlueprint,
    variant_b: WorksheetBlueprint | None = None,
    variant_c: WorksheetBlueprint | None = None,
) -> None:
    variants: Dict[BlueprintVariant, WorksheetBlueprint] = {"A": variant_a}

    if variant_b is not None:
        variants["B"] = variant_b

    if variant_c is not None:
        variants["C"] = variant_c

    BLUEPRINT_ROTATION[tier] = TierBlueprintSet(
        tier=tier,
        variants=variants,
    )


def blueprint_variant_for_tier(
    tier: Tier,
    variant: BlueprintVariant = "A",
) -> WorksheetBlueprint:
    if tier not in BLUEPRINT_ROTATION:
        raise ValueError(f"No blueprint rotation registered for tier '{tier}'.")

    blueprint_set = BLUEPRINT_ROTATION[tier]

    if variant not in blueprint_set.variants:
        available = tuple(blueprint_set.variants.keys())
        raise ValueError(
            f"Blueprint variant '{variant}' not registered for tier '{tier}'. "
            f"Available variants: {available}"
        )

    return blueprint_set.variants[variant]


def available_variants_for_tier(tier: Tier) -> Tuple[BlueprintVariant, ...]:
    if tier not in BLUEPRINT_ROTATION:
        return ()
    return tuple(BLUEPRINT_ROTATION[tier].variants.keys())


def default_variant_for_tier(tier: Tier) -> BlueprintVariant:
    variants = available_variants_for_tier(tier)
    if not variants:
        raise ValueError(f"No blueprint variants registered for tier '{tier}'.")
    return variants[0]
