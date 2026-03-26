from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional

from models.worksheet_models import (
    APPROVED_PUPIL_ITEM_FAMILIES,
    APPROVED_QUIZ_FORMATS,
    FORBIDDEN_PUPIL_ITEM_TYPES,
    QuizFormat,
    WorksheetItemFamily,
    WorksheetTier,
    validate_item_family,
    validate_quiz_format,
    validate_tier,
)


@dataclass(frozen=True)
class ItemFamilyDefinition:
    family: WorksheetItemFamily
    label: str
    pupil_safe: bool
    mathematical_purpose: str
    description: str
    supports_vocab: bool
    supports_single_product: bool
    supports_three_product: bool
    support_allowed: bool
    core_allowed: bool
    extension_allowed: bool


@dataclass(frozen=True)
class QuizFormatDefinition:
    quiz_format: QuizFormat
    label: str
    pupil_safe: bool
    low_language_load: bool
    supports_single_answer: bool
    supports_multiple_selection: bool
    supports_comparison: bool
    supports_vocab_learning: bool
    typical_instruction: str


@dataclass(frozen=True)
class FamilyFormatRule:
    family: WorksheetItemFamily
    allowed_formats: tuple[QuizFormat, ...]
    preferred_formats_support: tuple[QuizFormat, ...]
    preferred_formats_core: tuple[QuizFormat, ...]
    preferred_formats_extension: tuple[QuizFormat, ...]


@dataclass(frozen=True)
class ExplanationConstraint:
    tier: WorksheetTier
    allowed_formats: tuple[QuizFormat, ...]
    max_expected_response_shape: str
    guidance: str


ITEM_FAMILY_DEFINITIONS: Final[dict[WorksheetItemFamily, ItemFamilyDefinition]] = {
    "product_recognition": ItemFamilyDefinition(
        family="product_recognition",
        label="Product recognition",
        pupil_safe=True,
        mathematical_purpose="Notice or identify the target product through multiplication/division structure.",
        description=(
            "Used when the learner must spot the product, identify which equation makes the product, "
            "or recognise the target product inside a mathematical action."
        ),
        supports_vocab=True,
        supports_single_product=True,
        supports_three_product=True,
        support_allowed=True,
        core_allowed=True,
        extension_allowed=True,
    ),
    "route_in": ItemFamilyDefinition(
        family="route_in",
        label="Route in",
        pupil_safe=True,
        mathematical_purpose="Build the target product through multiplication.",
        description=(
            "Used for multiplication routes into the product. Supports direct route completion, "
            "guided build tasks, and product-entry work."
        ),
        supports_vocab=True,
        supports_single_product=True,
        supports_three_product=True,
        support_allowed=True,
        core_allowed=True,
        extension_allowed=True,
    ),
    "missing_factor": ItemFamilyDefinition(
        family="missing_factor",
        label="Missing factor",
        pupil_safe=True,
        mathematical_purpose="Recover a factor from a partial multiplication route.",
        description=(
            "Used when one factor is hidden and the learner must reconstruct the multiplication relation."
        ),
        supports_vocab=True,
        supports_single_product=True,
        supports_three_product=True,
        support_allowed=True,
        core_allowed=True,
        extension_allowed=True,
    ),
    "another_way": ItemFamilyDefinition(
        family="another_way",
        label="Another way",
        pupil_safe=True,
        mathematical_purpose="Show variation while preserving the same product.",
        description=(
            "Used to surface another valid route to the same product. Best for products with more than one "
            "useful visible route at the current stage."
        ),
        supports_vocab=True,
        supports_single_product=True,
        supports_three_product=True,
        support_allowed=True,
        core_allowed=True,
        extension_allowed=True,
    ),
    "compare_routes": ItemFamilyDefinition(
        family="compare_routes",
        label="Compare routes",
        pupil_safe=True,
        mathematical_purpose="Compare same-product or different-product routes structurally.",
        description=(
            "Used for route comparison, sameness/difference judgment, and same product / different multiplication reasoning."
        ),
        supports_vocab=True,
        supports_single_product=True,
        supports_three_product=True,
        support_allowed=True,
        core_allowed=True,
        extension_allowed=True,
    ),
    "route_out": ItemFamilyDefinition(
        family="route_out",
        label="Route out",
        pupil_safe=True,
        mathematical_purpose="Use the product to divide back and recover a factor.",
        description=(
            "Used for inverse division tasks. This family is mandatory because TMK links multiplication and division."
        ),
        supports_vocab=True,
        supports_single_product=True,
        supports_three_product=True,
        support_allowed=True,
        core_allowed=True,
        extension_allowed=True,
    ),
    "check_match": ItemFamilyDefinition(
        family="check_match",
        label="Check or match",
        pupil_safe=True,
        mathematical_purpose="Match a route, fact, or product correctly to its target.",
        description=(
            "Used for matching a target product, choosing the equation that matches, or selecting the right route."
        ),
        supports_vocab=True,
        supports_single_product=True,
        supports_three_product=True,
        support_allowed=True,
        core_allowed=True,
        extension_allowed=True,
    ),
    "correct_incorrect": ItemFamilyDefinition(
        family="correct_incorrect",
        label="Correct or incorrect",
        pupil_safe=True,
        mathematical_purpose="Judge mathematical correctness of a route or statement.",
        description=(
            "Used for yes/no, tick-correct, and direct truth-check tasks tied to multiplication/division structure."
        ),
        supports_vocab=True,
        supports_single_product=True,
        supports_three_product=True,
        support_allowed=True,
        core_allowed=True,
        extension_allowed=True,
    ),
    "error_repair": ItemFamilyDefinition(
        family="error_repair",
        label="Error repair",
        pupil_safe=True,
        mathematical_purpose="Find and fix a structural mistake.",
        description=(
            "Used when the learner must detect and repair a broken multiplication/division route."
        ),
        supports_vocab=True,
        supports_single_product=True,
        supports_three_product=True,
        support_allowed=True,
        core_allowed=True,
        extension_allowed=True,
    ),
    "structural_grouping": ItemFamilyDefinition(
        family="structural_grouping",
        label="Structural grouping",
        pupil_safe=True,
        mathematical_purpose="Group, sort, or match related equations and products structurally.",
        description=(
            "Used for family grouping, same family / different family sorting, matching multiplication to division, "
            "and related structural classification tied directly to multiplication/division."
        ),
        supports_vocab=True,
        supports_single_product=True,
        supports_three_product=True,
        support_allowed=True,
        core_allowed=True,
        extension_allowed=True,
    ),
    "final_explanation": ItemFamilyDefinition(
        family="final_explanation",
        label="Final explanation",
        pupil_safe=True,
        mathematical_purpose="Give a short explanation of the structure used.",
        description=(
            "Used as the final reasoning item. Language load must be tier-sensitive: heavily scaffolded in Support, "
            "short independent explanation in Core, stronger justification in Extension."
        ),
        supports_vocab=True,
        supports_single_product=True,
        supports_three_product=True,
        support_allowed=True,
        core_allowed=True,
        extension_allowed=True,
    ),
}


QUIZ_FORMAT_DEFINITIONS: Final[dict[QuizFormat, QuizFormatDefinition]] = {
    "circle": QuizFormatDefinition(
        quiz_format="circle",
        label="Circle",
        pupil_safe=True,
        low_language_load=True,
        supports_single_answer=True,
        supports_multiple_selection=False,
        supports_comparison=False,
        supports_vocab_learning=True,
        typical_instruction="Circle the correct answer.",
    ),
    "tick": QuizFormatDefinition(
        quiz_format="tick",
        label="Tick",
        pupil_safe=True,
        low_language_load=True,
        supports_single_answer=True,
        supports_multiple_selection=False,
        supports_comparison=False,
        supports_vocab_learning=True,
        typical_instruction="Tick the correct answer.",
    ),
    "yes_no": QuizFormatDefinition(
        quiz_format="yes_no",
        label="Yes / no",
        pupil_safe=True,
        low_language_load=True,
        supports_single_answer=True,
        supports_multiple_selection=False,
        supports_comparison=False,
        supports_vocab_learning=True,
        typical_instruction="Yes or no?",
    ),
    "tick_all": QuizFormatDefinition(
        quiz_format="tick_all",
        label="Tick all",
        pupil_safe=True,
        low_language_load=True,
        supports_single_answer=False,
        supports_multiple_selection=True,
        supports_comparison=True,
        supports_vocab_learning=True,
        typical_instruction="Tick all that match.",
    ),
    "match": QuizFormatDefinition(
        quiz_format="match",
        label="Match",
        pupil_safe=True,
        low_language_load=True,
        supports_single_answer=False,
        supports_multiple_selection=True,
        supports_comparison=True,
        supports_vocab_learning=True,
        typical_instruction="Match up.",
    ),
    "sort": QuizFormatDefinition(
        quiz_format="sort",
        label="Sort",
        pupil_safe=True,
        low_language_load=True,
        supports_single_answer=False,
        supports_multiple_selection=True,
        supports_comparison=True,
        supports_vocab_learning=True,
        typical_instruction="Sort into groups.",
    ),
    "choose": QuizFormatDefinition(
        quiz_format="choose",
        label="Choose",
        pupil_safe=True,
        low_language_load=True,
        supports_single_answer=True,
        supports_multiple_selection=False,
        supports_comparison=True,
        supports_vocab_learning=True,
        typical_instruction="Choose from the options.",
    ),
    "fill_box": QuizFormatDefinition(
        quiz_format="fill_box",
        label="Fill one box",
        pupil_safe=True,
        low_language_load=True,
        supports_single_answer=True,
        supports_multiple_selection=False,
        supports_comparison=False,
        supports_vocab_learning=True,
        typical_instruction="Fill the box.",
    ),
    "label_from_options": QuizFormatDefinition(
        quiz_format="label_from_options",
        label="Label from options",
        pupil_safe=True,
        low_language_load=True,
        supports_single_answer=False,
        supports_multiple_selection=True,
        supports_comparison=True,
        supports_vocab_learning=True,
        typical_instruction="Label from the word bank.",
    ),
}


FAMILY_FORMAT_RULES: Final[dict[WorksheetItemFamily, FamilyFormatRule]] = {
    "product_recognition": FamilyFormatRule(
        family="product_recognition",
        allowed_formats=("circle", "tick", "choose", "tick_all"),
        preferred_formats_support=("circle", "tick"),
        preferred_formats_core=("tick", "choose", "tick_all"),
        preferred_formats_extension=("choose", "tick_all"),
    ),
    "route_in": FamilyFormatRule(
        family="route_in",
        allowed_formats=("fill_box", "choose", "match"),
        preferred_formats_support=("fill_box",),
        preferred_formats_core=("fill_box", "choose"),
        preferred_formats_extension=("fill_box", "match"),
    ),
    "missing_factor": FamilyFormatRule(
        family="missing_factor",
        allowed_formats=("fill_box", "choose", "match"),
        preferred_formats_support=("fill_box",),
        preferred_formats_core=("fill_box", "choose"),
        preferred_formats_extension=("fill_box", "match"),
    ),
    "another_way": FamilyFormatRule(
        family="another_way",
        allowed_formats=("match", "choose", "fill_box", "label_from_options"),
        preferred_formats_support=("match", "choose"),
        preferred_formats_core=("match", "fill_box", "choose"),
        preferred_formats_extension=("match", "label_from_options", "fill_box"),
    ),
    "compare_routes": FamilyFormatRule(
        family="compare_routes",
        allowed_formats=("match", "sort", "choose", "tick_all"),
        preferred_formats_support=("match", "choose"),
        preferred_formats_core=("match", "sort", "choose"),
        preferred_formats_extension=("sort", "match", "tick_all"),
    ),
    "route_out": FamilyFormatRule(
        family="route_out",
        allowed_formats=("fill_box", "choose", "match"),
        preferred_formats_support=("fill_box",),
        preferred_formats_core=("fill_box", "choose"),
        preferred_formats_extension=("fill_box", "match"),
    ),
    "check_match": FamilyFormatRule(
        family="check_match",
        allowed_formats=("circle", "tick", "choose", "tick_all", "match"),
        preferred_formats_support=("circle", "tick"),
        preferred_formats_core=("tick", "choose", "match"),
        preferred_formats_extension=("choose", "tick_all", "match"),
    ),
    "correct_incorrect": FamilyFormatRule(
        family="correct_incorrect",
        allowed_formats=("yes_no", "tick", "choose"),
        preferred_formats_support=("yes_no", "tick"),
        preferred_formats_core=("yes_no", "tick", "choose"),
        preferred_formats_extension=("yes_no", "choose"),
    ),
    "error_repair": FamilyFormatRule(
        family="error_repair",
        allowed_formats=("fill_box", "choose", "match", "sort"),
        preferred_formats_support=("fill_box", "choose"),
        preferred_formats_core=("fill_box", "choose", "match"),
        preferred_formats_extension=("sort", "match", "fill_box"),
    ),
    "structural_grouping": FamilyFormatRule(
        family="structural_grouping",
        allowed_formats=("match", "sort", "tick_all", "label_from_options"),
        preferred_formats_support=("match", "sort"),
        preferred_formats_core=("match", "sort", "tick_all"),
        preferred_formats_extension=("sort", "match", "label_from_options"),
    ),
    "final_explanation": FamilyFormatRule(
        family="final_explanation",
        allowed_formats=("choose", "label_from_options", "fill_box"),
        preferred_formats_support=("choose", "label_from_options", "fill_box"),
        preferred_formats_core=("fill_box", "label_from_options", "choose"),
        preferred_formats_extension=("fill_box", "label_from_options", "choose"),
    ),
}


TIER_EXPLANATION_CONSTRAINTS: Final[dict[WorksheetTier, ExplanationConstraint]] = {
    "Support": ExplanationConstraint(
        tier="Support",
        allowed_formats=("choose", "label_from_options", "fill_box"),
        max_expected_response_shape="sentence_stem_or_one_clause",
        guidance=(
            "Support explanation must be tightly scaffolded. Use a sentence stem, a short label, "
            "a choice from options, or one-clause completion only."
        ),
    ),
    "Core": ExplanationConstraint(
        tier="Core",
        allowed_formats=("fill_box", "label_from_options", "choose"),
        max_expected_response_shape="short_independent_explanation",
        guidance=(
            "Core explanation may ask for a short written reason or short comparison, but must stay concise."
        ),
    ),
    "Extension": ExplanationConstraint(
        tier="Extension",
        allowed_formats=("fill_box", "label_from_options", "choose"),
        max_expected_response_shape="brief_justification",
        guidance=(
            "Extension explanation may require stronger comparison, classification, or justification, "
            "but should still remain worksheet-sized."
        ),
    ),
}


FORBIDDEN_PUPIL_PROMPT_PATTERNS: Final[tuple[str, ...]] = (
    "What stage introduces",
    "Which stage is this",
    "Does this belong in the TMK world",
    "Is this inside the TMK world",
    "What does identity mean",
    "What is the product",
    "What does double mean",
    "What is a fact family",
    "What does squared mean",
)


def get_item_family_definition(family: WorksheetItemFamily) -> ItemFamilyDefinition:
    validate_item_family(family)
    return ITEM_FAMILY_DEFINITIONS[family]


def get_quiz_format_definition(quiz_format: QuizFormat) -> QuizFormatDefinition:
    validate_quiz_format(quiz_format)
    return QUIZ_FORMAT_DEFINITIONS[quiz_format]


def get_family_format_rule(family: WorksheetItemFamily) -> FamilyFormatRule:
    validate_item_family(family)
    return FAMILY_FORMAT_RULES[family]


def get_explanation_constraint(tier: WorksheetTier) -> ExplanationConstraint:
    validate_tier(tier)
    return TIER_EXPLANATION_CONSTRAINTS[tier]


def allowed_formats_for_family(family: WorksheetItemFamily) -> tuple[QuizFormat, ...]:
    return get_family_format_rule(family).allowed_formats


def preferred_formats_for_tier(
    family: WorksheetItemFamily,
    tier: WorksheetTier,
) -> tuple[QuizFormat, ...]:
    rule = get_family_format_rule(family)
    validate_tier(tier)

    if tier == "Support":
        return rule.preferred_formats_support
    if tier == "Core":
        return rule.preferred_formats_core
    if tier == "Extension":
        return rule.preferred_formats_extension

    raise ValueError(f"Unsupported tier '{tier}'.")


def family_allowed_for_tier(
    family: WorksheetItemFamily,
    tier: WorksheetTier,
) -> bool:
    definition = get_item_family_definition(family)
    validate_tier(tier)

    if tier == "Support":
        return definition.support_allowed
    if tier == "Core":
        return definition.core_allowed
    if tier == "Extension":
        return definition.extension_allowed

    raise ValueError(f"Unsupported tier '{tier}'.")


def format_allowed_for_family(
    family: WorksheetItemFamily,
    quiz_format: QuizFormat,
) -> bool:
    validate_item_family(family)
    validate_quiz_format(quiz_format)
    return quiz_format in FAMILY_FORMAT_RULES[family].allowed_formats


def is_vocab_friendly_family(family: WorksheetItemFamily) -> bool:
    return get_item_family_definition(family).supports_vocab


def is_low_language_format(quiz_format: QuizFormat) -> bool:
    return get_quiz_format_definition(quiz_format).low_language_load


def explanation_format_allowed_for_tier(
    quiz_format: QuizFormat,
    tier: WorksheetTier,
) -> bool:
    validate_quiz_format(quiz_format)
    constraint = get_explanation_constraint(tier)
    return quiz_format in constraint.allowed_formats


def approved_item_families() -> tuple[WorksheetItemFamily, ...]:
    return APPROVED_PUPIL_ITEM_FAMILIES


def approved_quiz_formats() -> tuple[QuizFormat, ...]:
    return APPROVED_QUIZ_FORMATS


def forbidden_pupil_item_types() -> tuple[str, ...]:
    return FORBIDDEN_PUPIL_ITEM_TYPES


def forbidden_pupil_prompt_patterns() -> tuple[str, ...]:
    return FORBIDDEN_PUPIL_PROMPT_PATTERNS


def validate_taxonomy_consistency() -> None:
    for family in APPROVED_PUPIL_ITEM_FAMILIES:
        if family not in ITEM_FAMILY_DEFINITIONS:
            raise ValueError(
                f"Approved item family '{family}' is missing from ITEM_FAMILY_DEFINITIONS."
            )
        if family not in FAMILY_FORMAT_RULES:
            raise ValueError(
                f"Approved item family '{family}' is missing from FAMILY_FORMAT_RULES."
            )

    for quiz_format in APPROVED_QUIZ_FORMATS:
        if quiz_format not in QUIZ_FORMAT_DEFINITIONS:
            raise ValueError(
                f"Approved quiz format '{quiz_format}' is missing from QUIZ_FORMAT_DEFINITIONS."
            )

    for family, rule in FAMILY_FORMAT_RULES.items():
        validate_item_family(family)

        if not rule.allowed_formats:
            raise ValueError(f"Family '{family}' has no allowed formats.")

        for quiz_format in rule.allowed_formats:
            validate_quiz_format(quiz_format)

        for quiz_format in rule.preferred_formats_support:
            if quiz_format not in rule.allowed_formats:
                raise ValueError(
                    f"Support preferred format '{quiz_format}' is not allowed for family '{family}'."
                )

        for quiz_format in rule.preferred_formats_core:
            if quiz_format not in rule.allowed_formats:
                raise ValueError(
                    f"Core preferred format '{quiz_format}' is not allowed for family '{family}'."
                )

        for quiz_format in rule.preferred_formats_extension:
            if quiz_format not in rule.allowed_formats:
                raise ValueError(
                    f"Extension preferred format '{quiz_format}' is not allowed for family '{family}'."
                )

    for tier, constraint in TIER_EXPLANATION_CONSTRAINTS.items():
        validate_tier(tier)
        if not constraint.allowed_formats:
            raise ValueError(f"Tier '{tier}' explanation constraint has no allowed formats.")

        for quiz_format in constraint.allowed_formats:
            validate_quiz_format(quiz_format)


def prompt_violates_forbidden_patterns(prompt: str) -> bool:
    prompt_normalized = prompt.strip().lower()
    return any(pattern.lower() in prompt_normalized for pattern in FORBIDDEN_PUPIL_PROMPT_PATTERNS)


def validate_prompt_text_for_pupil_use(prompt: str) -> None:
    if not prompt.strip():
        raise ValueError("Pupil prompt text may not be empty.")

    if prompt_violates_forbidden_patterns(prompt):
        raise ValueError(
            "Pupil prompt violates a forbidden worksheet pattern "
            "(curriculum placement, TMK-world membership, or dictionary-style definition)."
        )


def choose_default_quiz_format(
    family: WorksheetItemFamily,
    tier: WorksheetTier,
) -> QuizFormat:
    preferred = preferred_formats_for_tier(family, tier)
    if not preferred:
        raise ValueError(
            f"No preferred quiz formats found for family '{family}' and tier '{tier}'."
        )
    return preferred[0]


def choose_vocab_friendly_quiz_format(
    family: WorksheetItemFamily,
    tier: WorksheetTier,
) -> QuizFormat:
    preferred = preferred_formats_for_tier(family, tier)
    for quiz_format in preferred:
        definition = get_quiz_format_definition(quiz_format)
        if definition.supports_vocab_learning:
            return quiz_format

    allowed = allowed_formats_for_family(family)
    for quiz_format in allowed:
        definition = get_quiz_format_definition(quiz_format)
        if definition.supports_vocab_learning:
            return quiz_format

    raise ValueError(
        f"No vocabulary-friendly quiz format available for family '{family}' and tier '{tier}'."
    )


def family_supports_format_and_tier(
    family: WorksheetItemFamily,
    quiz_format: QuizFormat,
    tier: WorksheetTier,
) -> bool:
    return family_allowed_for_tier(family, tier) and format_allowed_for_family(family, quiz_format)


def explanation_guidance_for_tier(tier: WorksheetTier) -> str:
    return get_explanation_constraint(tier).guidance


def all_family_labels() -> tuple[tuple[WorksheetItemFamily, str], ...]:
    return tuple((family, definition.label) for family, definition in ITEM_FAMILY_DEFINITIONS.items())


def all_quiz_format_labels() -> tuple[tuple[QuizFormat, str], ...]:
    return tuple(
        (quiz_format, definition.label)
        for quiz_format, definition in QUIZ_FORMAT_DEFINITIONS.items()
    )


validate_taxonomy_consistency()
