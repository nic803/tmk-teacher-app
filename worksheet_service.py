from __future__ import annotations

from dataclasses import asdict
from typing import Dict, Optional

from blueprint_rotation import BlueprintVariant, blueprint_variant_for_tier, default_variant_for_tier
from question_form_engine import build_question_spec
from validation_engine import validate_worksheet_structure
from worksheet_blueprint_library import register_all_blueprint_variants
from worksheet_engine import TeacherKey, WorksheetPackage, _build_teacher_key
from worksheet_policy import validate_supported_tier
from products import ALL_PRODUCTS, product_record
from tier_policy import Tier


_BLUEPRINTS_REGISTERED = False


def generate_worksheet_package(
    product: int,
    tier: Tier,
    variant: Optional[BlueprintVariant] = None,
) -> WorksheetPackage:
    _ensure_blueprints_registered()
    _validate_product(product)
    validate_supported_tier(tier)

    resolved_variant = variant or default_variant_for_tier(tier)
    blueprint = blueprint_variant_for_tier(tier, resolved_variant)
    record = product_record(product)

    questions = tuple(
        build_question_spec(record, tier, slot)
        for slot in blueprint.slots
    )

    validate_worksheet_structure(product, tier, questions)

    teacher_key = _build_teacher_key(product, questions)

    return WorksheetPackage(
        product=record.product,
        stage=record.stage,
        tier=tier,
        questions=questions,
        teacher_key=teacher_key,
    )


def generate_worksheet_package_dict(
    product: int,
    tier: Tier,
    variant: Optional[BlueprintVariant] = None,
) -> Dict[str, object]:
    return asdict(generate_worksheet_package(product, tier, variant))


def available_blueprint_variants(tier: Tier) -> tuple[str, ...]:
    _ensure_blueprints_registered()
    validate_supported_tier(tier)

    variants = []
    for candidate in ("A", "B", "C"):
        try:
            blueprint_variant_for_tier(tier, candidate)
            variants.append(candidate)
        except ValueError:
            continue

    return tuple(variants)


def _ensure_blueprints_registered() -> None:
    global _BLUEPRINTS_REGISTERED

    if not _BLUEPRINTS_REGISTERED:
        register_all_blueprint_variants()
        _BLUEPRINTS_REGISTERED = True


def _validate_product(product: int) -> None:
    if product not in ALL_PRODUCTS:
        raise ValueError(f"Unknown TMK product: {product}")
