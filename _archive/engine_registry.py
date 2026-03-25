from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from blueprint_rotation import available_variants_for_tier
from validation_engine import (
    validate_prompt_wording,
    validate_teacher_key_answers,
)
from worksheet_blueprint_library import register_all_blueprint_variants
from worksheet_blueprints import validate_all_blueprints
from wording_policy import world_membership_prompt
from worlds import TMK_WORLD


@dataclass(frozen=True)
class EngineRegistryStatus:
    blueprints_registered: bool
    blueprints_validated: bool
    wording_validated: bool
    variants_available: Tuple[str, ...]


_BLUEPRINTS_REGISTERED = False


def initialize_engine_registry() -> EngineRegistryStatus:
    global _BLUEPRINTS_REGISTERED

    if not _BLUEPRINTS_REGISTERED:
        register_all_blueprint_variants()
        _BLUEPRINTS_REGISTERED = True

    validate_all_blueprints()
    _validate_wording_startup()

    variants = _all_registered_variants()

    return EngineRegistryStatus(
        blueprints_registered=True,
        blueprints_validated=True,
        wording_validated=True,
        variants_available=variants,
    )


def engine_registry_status() -> EngineRegistryStatus:
    return initialize_engine_registry()


def _validate_wording_startup() -> None:
    prompt_samples = (
        world_membership_prompt(36),
        world_membership_prompt(77).replace("36", "77") if "36" in world_membership_prompt(36) else f"Does 77 belong in {TMK_WORLD}?",
        f"This route is true, but it is outside {TMK_WORLD}.",
        f"Does 49 belong in {TMK_WORLD}?",
    )

    validate_prompt_wording(prompt_samples)
    validate_teacher_key_answers(({"value": 36}, {"value": True}))


def _all_registered_variants() -> Tuple[str, ...]:
    variants = []
    for tier in ("Support", "Core", "Extension"):
        variants.extend(f"{tier}:{variant}" for variant in available_variants_for_tier(tier))
    return tuple(variants)
