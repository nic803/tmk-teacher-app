# domain/worksheet_taxonomy.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, FrozenSet, Iterable, Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ItemFamilyDefinition:
    family: str
    label: str
    allowed_tiers: FrozenSet[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class QuizFormatDefinition:
    format_id: str
    label: str


@dataclass(frozen=True)
class FamilyFormatRule:
    family: str
    allowed_support_formats: FrozenSet[str] = field(default_factory=frozenset)
    allowed_core_formats: FrozenSet[str] = field(default_factory=frozenset)
    allowed_extension_formats: FrozenSet[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class TierExplanationConstraint:
    tier: str
    allowed_formats: FrozenSet[str] = field(default_factory=frozenset)


# ---------------------------------------------------------------------------
# Canonical definitions
# ---------------------------------------------------------------------------

ALL_TIERS = frozenset({"Support", "Core", "Extension"})

ITEM_FAMILY_DEFINITIONS: Dict[str, ItemFamilyDefinition] = {
    "product_recognition": ItemFamilyDefinition(
        family="product_recognition",
        label="Recognise the product / representation",
        allowed_tiers=ALL_TIERS,
    ),
    "missing_factor": ItemFamilyDefinition(
        family="missing_factor",
        label="Find a missing factor",
        allowed_tiers=ALL_TIERS,
    ),
    "another_way": ItemFamilyDefinition(
        family="another_way",
        label="Represent or solve in another way",
        allowed_tiers=ALL_TIERS,
    ),
    "error_repair": ItemFamilyDefinition(
        family="error_repair",
        label="Repair an incorrect method or statement",
        allowed_tiers=ALL_TIERS,
    ),
    "final_explanation": ItemFamilyDefinition(
        family="final_explanation",
        label="Final explanation / justification",
        allowed_tiers=ALL_TIERS,
    ),
}

QUIZ_FORMAT_DEFINITIONS: Dict[str, QuizFormatDefinition] = {
    "choose": QuizFormatDefinition("choose", "Multiple choice"),
    "match": QuizFormatDefinition("match", "Matching"),
    "sort": QuizFormatDefinition("sort", "Sorting / ordering"),
    "label_from_options": QuizFormatDefinition("label_from_options", "Label from options"),
    "fill_box": QuizFormatDefinition("fill_box", "Fill in box"),
    "short_answer": QuizFormatDefinition("short_answer", "Short answer"),
    "write_expression": QuizFormatDefinition("write_expression", "Write an expression"),
    "number_entry": QuizFormatDefinition("number_entry", "Numeric entry"),
}

# These rules are the contract used by worksheet_formats.py.
FAMILY_FORMAT_RULES: Dict[str, FamilyFormatRule] = {
    "product_recognition": FamilyFormatRule(
        family="product_recognition",
        allowed_support_formats=frozenset({"choose", "match"}),
        allowed_core_formats=frozenset({"choose", "match", "label_from_options"}),
        allowed_extension_formats=frozenset({"choose", "match", "label_from_options"}),
    ),
    "missing_factor": FamilyFormatRule(
        family="missing_factor",
        allowed_support_formats=frozenset({"choose", "fill_box", "number_entry"}),
        allowed_core_formats=frozenset({"choose", "match", "fill_box", "number_entry"}),
        allowed_extension_formats=frozenset({"choose", "match", "fill_box", "number_entry"}),
    ),
    "another_way": FamilyFormatRule(
        family="another_way",
        allowed_support_formats=frozenset({"choose", "label_from_options"}),
        allowed_core_formats=frozenset({"choose", "label_from_options", "short_answer"}),
        allowed_extension_formats=frozenset({"choose", "label_from_options", "short_answer", "write_expression"}),
    ),
    "error_repair": FamilyFormatRule(
        family="error_repair",
        allowed_support_formats=frozenset({"choose", "match"}),
        allowed_core_formats=frozenset({"choose", "match", "sort"}),
        allowed_extension_formats=frozenset({"choose", "match", "sort", "short_answer"}),
    ),
    "final_explanation": FamilyFormatRule(
        family="final_explanation",
        allowed_support_formats=frozenset({"choose", "short_answer"}),
        allowed_core_formats=frozenset({"short_answer", "fill_box"}),
        allowed_extension_formats=frozenset({"fill_box", "short_answer", "write_expression"}),
    ),
}

TIER_EXPLANATION_CONSTRAINTS: Dict[str, TierExplanationConstraint] = {
    "Support": TierExplanationConstraint(
        tier="Support",
        allowed_formats=frozenset({"choose", "short_answer"}),
    ),
    "Core": TierExplanationConstraint(
        tier="Core",
        allowed_formats=frozenset({"short_answer", "fill_box"}),
    ),
    "Extension": TierExplanationConstraint(
        tier="Extension",
        allowed_formats=frozenset({"fill_box", "short_answer", "write_expression"}),
    ),
}


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def validate_taxonomy_consistency() -> None:
    for family, item_def in ITEM_FAMILY_DEFINITIONS.items():
        if family not in FAMILY_FORMAT_RULES:
            raise ValueError(f"Missing FAMILY_FORMAT_RULES entry for family '{family}'")
        unknown_tiers = set(item_def.allowed_tiers) - set(ALL_TIERS)
        if unknown_tiers:
            raise ValueError(
                f"Family '{family}' references unknown tiers: {sorted(unknown_tiers)}"
            )

    for family, rule in FAMILY_FORMAT_RULES.items():
        if family not in ITEM_FAMILY_DEFINITIONS:
            raise ValueError(f"FAMILY_FORMAT_RULES references unknown family '{family}'")

        for fmt in (
            set(rule.allowed_support_formats)
            | set(rule.allowed_core_formats)
            | set(rule.allowed_extension_formats)
        ):
            if fmt not in QUIZ_FORMAT_DEFINITIONS:
                raise ValueError(
                    f"Family '{family}' references unknown quiz format '{fmt}'"
                )

    for tier, constraint in TIER_EXPLANATION_CONSTRAINTS.items():
        if tier not in ALL_TIERS:
            raise ValueError(f"Unknown explanation tier '{tier}'")
        for fmt in constraint.allowed_formats:
            if fmt not in QUIZ_FORMAT_DEFINITIONS:
                raise ValueError(
                    f"Tier '{tier}' explanation constraint uses unknown format '{fmt}'"
                )


def family_allowed_for_tier(family: str, tier: str) -> bool:
    item_def = ITEM_FAMILY_DEFINITIONS.get(family)
    if item_def is None:
        return False
    return tier in item_def.allowed_tiers


def format_allowed_for_family(family: str, fmt: str, tier: Optional[str] = None) -> bool:
    rule = FAMILY_FORMAT_RULES.get(family)
    if rule is None:
        return False

    if tier == "Support":
        return fmt in rule.allowed_support_formats
    if tier == "Core":
        return fmt in rule.allowed_core_formats
    if tier == "Extension":
        return fmt in rule.allowed_extension_formats

    return (
        fmt in rule.allowed_support_formats
        or fmt in rule.allowed_core_formats
        or fmt in rule.allowed_extension_formats
    )


def explanation_format_allowed_for_tier(tier: str, fmt: str) -> bool:
    constraint = TIER_EXPLANATION_CONSTRAINTS.get(tier)
    if constraint is None:
        return False
    return fmt in constraint.allowed_formats


def choose_default_quiz_format(family: str, tier: str) -> str:
    rule = FAMILY_FORMAT_RULES[family]
    if tier == "Support":
        allowed = tuple(rule.allowed_support_formats)
    elif tier == "Core":
        allowed = tuple(rule.allowed_core_formats)
    elif tier == "Extension":
        allowed = tuple(rule.allowed_extension_formats)
    else:
        raise ValueError(f"Unknown tier '{tier}'")

    if family == "final_explanation":
        allowed = tuple(
            fmt for fmt in allowed if explanation_format_allowed_for_tier(tier, fmt)
        )

    if not allowed:
        raise ValueError(
            f"No default quiz format available for family '{family}' at tier '{tier}'"
        )
    return allowed[0]


validate_taxonomy_consistency()
