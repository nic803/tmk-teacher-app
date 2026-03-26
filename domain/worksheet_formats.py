from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from domain.worksheet_taxonomy import (
    choose_default_quiz_format,
    explanation_format_allowed_for_tier,
    family_allowed_for_tier,
    format_allowed_for_family,
)
from models.worksheet_models import (
    QuizFormat,
    WorksheetFormatId,
    WorksheetItemFamily,
    WorksheetTier,
    expected_question_count,
    validate_format_id,
    validate_item_family,
    validate_quiz_format,
    validate_tier,
)


@dataclass(frozen=True)
class WorksheetSlotDefinition:
    q_id: int
    family: WorksheetItemFamily
    support_format: QuizFormat
    core_format: QuizFormat
    extension_format: QuizFormat
    vocab_expected: bool
    notes: str = ""


@dataclass(frozen=True)
class WorksheetFormatDefinition:
    format_id: WorksheetFormatId
    label: str
    question_count: int
    product_count: int
    description: str
    slots: tuple[WorksheetSlotDefinition, ...]


ONE_PRODUCT_10: Final[WorksheetFormatDefinition] = WorksheetFormatDefinition(
    format_id="one_product_10",
    label="One-product worksheet (10 questions)",
    question_count=10,
    product_count=1,
    description=(
        "A single-product worksheet built around one selected product as the hub. "
        "It must include at least one route in, at least one route out, vocabulary-bearing work, "
        "and a final explanation."
    ),
    slots=(
        WorksheetSlotDefinition(
            q_id=1,
            family="product_recognition",
            support_format="circle",
            core_format="tick",
            extension_format="choose",
            vocab_expected=True,
            notes="Notice the target product or identify which equation makes it.",
        ),
        WorksheetSlotDefinition(
            q_id=2,
            family="route_in",
            support_format="fill_box",
            core_format="fill_box",
            extension_format="fill_box",
            vocab_expected=False,
            notes="First multiplication route into the product.",
        ),
        WorksheetSlotDefinition(
            q_id=3,
            family="missing_factor",
            support_format="fill_box",
            core_format="fill_box",
            extension_format="match",
            vocab_expected=False,
            notes="Recover a factor from a partial multiplication route.",
        ),
        WorksheetSlotDefinition(
            q_id=4,
            family="another_way",
            support_format="match",
            core_format="match",
            extension_format="label_from_options",
            vocab_expected=False,
            notes="Show another way to make the same product when available.",
        ),
        WorksheetSlotDefinition(
            q_id=5,
            family="route_out",
            support_format="fill_box",
            core_format="fill_box",
            extension_format="fill_box",
            vocab_expected=False,
            notes="First route out using division.",
        ),
        WorksheetSlotDefinition(
            q_id=6,
            family="route_out",
            support_format="fill_box",
            core_format="choose",
            extension_format="match",
            vocab_expected=False,
            notes="Second route out or variation on inverse use.",
        ),
        WorksheetSlotDefinition(
            q_id=7,
            family="check_match",
            support_format="tick",
            core_format="match",
            extension_format="tick_all",
            vocab_expected=True,
            notes="Check which route or fact matches the target product.",
        ),
        WorksheetSlotDefinition(
            q_id=8,
            family="error_repair",
            support_format="fill_box",
            core_format="match",
            extension_format="sort",
            vocab_expected=False,
            notes="Find and fix a broken route or fact.",
        ),
        WorksheetSlotDefinition(
            q_id=9,
            family="structural_grouping",
            support_format="match",
            core_format="sort",
            extension_format="sort",
            vocab_expected=True,
            notes="Group same-family / different-family or structurally related items.",
        ),
        WorksheetSlotDefinition(
            q_id=10,
            family="final_explanation",
            support_format="choose",
            core_format="fill_box",
            extension_format="fill_box",
            vocab_expected=True,
            notes="Tier-sensitive final explanation.",
        ),
    ),
)


THREE_PRODUCT_12: Final[WorksheetFormatDefinition] = WorksheetFormatDefinition(
    format_id="three_product_12",
    label="Three-product worksheet (12 questions)",
    question_count=12,
    product_count=3,
    description=(
        "A three-product comparative worksheet. It must establish each selected product, "
        "use route-in and route-out tasks, include comparison/grouping, support recap when present, "
        "and end with a final explanation."
    ),
    slots=(
        WorksheetSlotDefinition(
            q_id=1,
            family="product_recognition",
            support_format="circle",
            core_format="tick",
            extension_format="choose",
            vocab_expected=True,
            notes="Recognise product A.",
        ),
        WorksheetSlotDefinition(
            q_id=2,
            family="product_recognition",
            support_format="circle",
            core_format="tick",
            extension_format="choose",
            vocab_expected=False,
            notes="Recognise product B.",
        ),
        WorksheetSlotDefinition(
            q_id=3,
            family="product_recognition",
            support_format="circle",
            core_format="tick",
            extension_format="choose",
            vocab_expected=False,
            notes="Recognise product C.",
        ),
        WorksheetSlotDefinition(
            q_id=4,
            family="route_in",
            support_format="fill_box",
            core_format="fill_box",
            extension_format="fill_box",
            vocab_expected=False,
            notes="Route in for one selected product.",
        ),
        WorksheetSlotDefinition(
            q_id=5,
            family="missing_factor",
            support_format="fill_box",
            core_format="fill_box",
            extension_format="match",
            vocab_expected=False,
            notes="Recover a factor for another selected product.",
        ),
        WorksheetSlotDefinition(
            q_id=6,
            family="route_out",
            support_format="fill_box",
            core_format="fill_box",
            extension_format="fill_box",
            vocab_expected=False,
            notes="Route out for one selected product.",
        ),
        WorksheetSlotDefinition(
            q_id=7,
            family="another_way",
            support_format="match",
            core_format="match",
            extension_format="label_from_options",
            vocab_expected=False,
            notes="Another way for a multi-route or recap-aware product.",
        ),
        WorksheetSlotDefinition(
            q_id=8,
            family="compare_routes",
            support_format="choose",
            core_format="match",
            extension_format="sort",
            vocab_expected=True,
            notes="Compare same product / different multiplication or structurally related routes.",
        ),
        WorksheetSlotDefinition(
            q_id=9,
            family="structural_grouping",
            support_format="match",
            core_format="sort",
            extension_format="sort",
            vocab_expected=True,
            notes="Group the three-product set by shared structure or fact family.",
        ),
        WorksheetSlotDefinition(
            q_id=10,
            family="check_match",
            support_format="tick",
            core_format="choose",
            extension_format="tick_all",
            vocab_expected=False,
            notes="Check which fact, route, or product matches correctly.",
        ),
        WorksheetSlotDefinition(
            q_id=11,
            family="error_repair",
            support_format="fill_box",
            core_format="match",
            extension_format="sort",
            vocab_expected=False,
            notes="Repair a broken structural relation from the set.",
        ),
        WorksheetSlotDefinition(
            q_id=12,
            family="final_explanation",
            support_format="choose",
            core_format="fill_box",
            extension_format="fill_box",
            vocab_expected=True,
            notes="Final comparison or justification across the set.",
        ),
    ),
)


WORKSHEET_FORMAT_DEFINITIONS: Final[dict[WorksheetFormatId, WorksheetFormatDefinition]] = {
    "one_product_10": ONE_PRODUCT_10,
    "three_product_12": THREE_PRODUCT_12,
}


def get_worksheet_format_definition(
    format_id: WorksheetFormatId,
) -> WorksheetFormatDefinition:
    validate_format_id(format_id)
    return WORKSHEET_FORMAT_DEFINITIONS[format_id]


def worksheet_slots_for_format(
    format_id: WorksheetFormatId,
) -> tuple[WorksheetSlotDefinition, ...]:
    return get_worksheet_format_definition(format_id).slots


def product_count_for_format(format_id: WorksheetFormatId) -> int:
    return get_worksheet_format_definition(format_id).product_count


def question_count_for_format(format_id: WorksheetFormatId) -> int:
    return get_worksheet_format_definition(format_id).question_count


def slot_format_for_tier(
    slot: WorksheetSlotDefinition,
    tier: WorksheetTier,
) -> QuizFormat:
    validate_tier(tier)

    if tier == "Support":
        return slot.support_format
    if tier == "Core":
        return slot.core_format
    if tier == "Extension":
        return slot.extension_format

    raise ValueError(f"Unsupported tier '{tier}'.")


def slot_definitions_for_tier(
    format_id: WorksheetFormatId,
    tier: WorksheetTier,
) -> tuple[tuple[WorksheetSlotDefinition, QuizFormat], ...]:
    validate_format_id(format_id)
    validate_tier(tier)

    slots = worksheet_slots_for_format(format_id)
    return tuple((slot, slot_format_for_tier(slot, tier)) for slot in slots)


def vocabulary_slot_ids_for_format(
    format_id: WorksheetFormatId,
) -> tuple[int, ...]:
    validate_format_id(format_id)
    return tuple(
        slot.q_id
        for slot in worksheet_slots_for_format(format_id)
        if slot.vocab_expected
    )


def final_explanation_slot_id(
    format_id: WorksheetFormatId,
) -> int:
    validate_format_id(format_id)
    for slot in worksheet_slots_for_format(format_id):
        if slot.family == "final_explanation":
            return slot.q_id
    raise ValueError(f"Format '{format_id}' does not define a final_explanation slot.")


def has_family_in_format(
    format_id: WorksheetFormatId,
    family: WorksheetItemFamily,
) -> bool:
    validate_format_id(format_id)
    validate_item_family(family)
    return any(slot.family == family for slot in worksheet_slots_for_format(format_id))


def family_count_in_format(
    format_id: WorksheetFormatId,
    family: WorksheetItemFamily,
) -> int:
    validate_format_id(format_id)
    validate_item_family(family)
    return sum(1 for slot in worksheet_slots_for_format(format_id) if slot.family == family)


def required_family_counts_for_format(
    format_id: WorksheetFormatId,
) -> dict[WorksheetItemFamily, int]:
    validate_format_id(format_id)
    counts: dict[WorksheetItemFamily, int] = {}
    for slot in worksheet_slots_for_format(format_id):
        counts[slot.family] = counts.get(slot.family, 0) + 1
    return counts


def required_route_in_count(format_id: WorksheetFormatId) -> int:
    return family_count_in_format(format_id, "route_in")


def required_route_out_count(format_id: WorksheetFormatId) -> int:
    return family_count_in_format(format_id, "route_out")


def required_compare_capacity(format_id: WorksheetFormatId) -> bool:
    validate_format_id(format_id)
    return has_family_in_format(format_id, "compare_routes") or has_family_in_format(
        format_id,
        "another_way",
    )


def format_supports_multi_product_comparison(format_id: WorksheetFormatId) -> bool:
    validate_format_id(format_id)
    return format_id == "three_product_12"


def default_quiz_format_map_for_tier(
    format_id: WorksheetFormatId,
    tier: WorksheetTier,
) -> dict[int, QuizFormat]:
    validate_format_id(format_id)
    validate_tier(tier)
    return {
        slot.q_id: slot_format_for_tier(slot, tier)
        for slot in worksheet_slots_for_format(format_id)
    }


def validate_slot_definition(slot: WorksheetSlotDefinition) -> None:
    if slot.q_id < 1:
        raise ValueError("Worksheet slot ids must start at 1.")

    validate_item_family(slot.family)
    validate_quiz_format(slot.support_format)
    validate_quiz_format(slot.core_format)
    validate_quiz_format(slot.extension_format)

    if not family_allowed_for_tier(slot.family, "Support"):
        raise ValueError(
            f"Family '{slot.family}' is not allowed for Support but is used in slot {slot.q_id}."
        )
    if not family_allowed_for_tier(slot.family, "Core"):
        raise ValueError(
            f"Family '{slot.family}' is not allowed for Core but is used in slot {slot.q_id}."
        )
    if not family_allowed_for_tier(slot.family, "Extension"):
        raise ValueError(
            f"Family '{slot.family}' is not allowed for Extension but is used in slot {slot.q_id}."
        )

    if not format_allowed_for_family(slot.family, slot.support_format):
        raise ValueError(
            f"Support format '{slot.support_format}' is not allowed for family '{slot.family}'."
        )
    if not format_allowed_for_family(slot.family, slot.core_format):
        raise ValueError(
            f"Core format '{slot.core_format}' is not allowed for family '{slot.family}'."
        )
    if not format_allowed_for_family(slot.family, slot.extension_format):
        raise ValueError(
            f"Extension format '{slot.extension_format}' is not allowed for family '{slot.family}'."
        )

    if slot.family == "final_explanation":
        if not explanation_format_allowed_for_tier(slot.support_format, "Support"):
            raise ValueError(
                f"Support format '{slot.support_format}' is not valid for final_explanation."
            )
        if not explanation_format_allowed_for_tier(slot.core_format, "Core"):
            raise ValueError(
                f"Core format '{slot.core_format}' is not valid for final_explanation."
            )
        if not explanation_format_allowed_for_tier(slot.extension_format, "Extension"):
            raise ValueError(
                f"Extension format '{slot.extension_format}' is not valid for final_explanation."
            )


def validate_format_definition(definition: WorksheetFormatDefinition) -> None:
    validate_format_id(definition.format_id)

    expected_count = expected_question_count(definition.format_id)
    if definition.question_count != expected_count:
        raise ValueError(
            f"Format '{definition.format_id}' must declare question_count={expected_count}. "
            f"Found {definition.question_count}."
        )

    if definition.product_count not in (1, 3):
        raise ValueError(
            f"Format '{definition.format_id}' must use product_count 1 or 3. "
            f"Found {definition.product_count}."
        )

    if len(definition.slots) != definition.question_count:
        raise ValueError(
            f"Format '{definition.format_id}' must define exactly {definition.question_count} slots. "
            f"Found {len(definition.slots)}."
        )

    actual_ids = tuple(slot.q_id for slot in definition.slots)
    expected_ids = tuple(range(1, definition.question_count + 1))
    if actual_ids != expected_ids:
        raise ValueError(
            f"Format '{definition.format_id}' slot ids must be sequential {expected_ids}. "
            f"Found {actual_ids}."
        )

    for slot in definition.slots:
        validate_slot_definition(slot)

    if family_count_in_format(definition.format_id, "route_in") < 1:
        raise ValueError(
            f"Format '{definition.format_id}' must contain at least one route_in slot."
        )

    if family_count_in_format(definition.format_id, "route_out") < 1:
        raise ValueError(
            f"Format '{definition.format_id}' must contain at least one route_out slot."
        )

    if family_count_in_format(definition.format_id, "final_explanation") != 1:
        raise ValueError(
            f"Format '{definition.format_id}' must contain exactly one final_explanation slot."
        )

    vocab_slots = vocabulary_slot_ids_for_format(definition.format_id)
    if len(vocab_slots) < 1:
        raise ValueError(
            f"Format '{definition.format_id}' must contain at least one vocabulary-bearing slot."
        )

    if definition.format_id == "one_product_10" and definition.product_count != 1:
        raise ValueError("one_product_10 must use product_count=1.")

    if definition.format_id == "three_product_12" and definition.product_count != 3:
        raise ValueError("three_product_12 must use product_count=3.")


def validate_worksheet_format_system() -> None:
    expected_ids = {"one_product_10", "three_product_12"}
    actual_ids = set(WORKSHEET_FORMAT_DEFINITIONS.keys())
    if actual_ids != expected_ids:
        raise ValueError(
            f"Worksheet format registry must contain exactly {expected_ids}. "
            f"Found {actual_ids}."
        )

    for definition in WORKSHEET_FORMAT_DEFINITIONS.values():
        validate_format_definition(definition)


def choose_fallback_format_for_family_and_tier(
    family: WorksheetItemFamily,
    tier: WorksheetTier,
) -> QuizFormat:
    validate_item_family(family)
    validate_tier(tier)
    return choose_default_quiz_format(family, tier)


def slot_note(
    format_id: WorksheetFormatId,
    q_id: int,
) -> str:
    validate_format_id(format_id)
    for slot in worksheet_slots_for_format(format_id):
        if slot.q_id == q_id:
            return slot.notes
    raise ValueError(f"Format '{format_id}' does not define slot id {q_id}.")


def format_label(format_id: WorksheetFormatId) -> str:
    return get_worksheet_format_definition(format_id).label


def format_description(format_id: WorksheetFormatId) -> str:
    return get_worksheet_format_definition(format_id).description


def format_overview(
    format_id: WorksheetFormatId,
) -> tuple[tuple[int, WorksheetItemFamily, str], ...]:
    validate_format_id(format_id)
    definition = get_worksheet_format_definition(format_id)
    return tuple(
        (slot.q_id, slot.family, slot.notes)
        for slot in definition.slots
    )


validate_worksheet_format_system()
