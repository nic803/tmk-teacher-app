from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Sequence

from domain.worksheet_taxonomy import (
    explanation_format_allowed_for_tier,
    family_allowed_for_tier,
    format_allowed_for_family,
)


@dataclass(frozen=True)
class WorksheetSlotDefinition:
    q_id: str
    family: str
    support_format: str
    core_format: str
    extension_format: str


# ---------------------------------------------------------------------------
# Replace these sample slot lists with your real worksheet slots.
# Keep the format ids exactly: one_product_10 and three_product_12
# ---------------------------------------------------------------------------

ONE_PRODUCT_10: Sequence[WorksheetSlotDefinition] = (
    WorksheetSlotDefinition(
        q_id="q1",
        family="product_recognition",
        support_format="choose",
        core_format="choose",
        extension_format="choose",
    ),
    WorksheetSlotDefinition(
        q_id="q2",
        family="missing_factor",
        support_format="fill_box",
        core_format="match",
        extension_format="match",
    ),
    WorksheetSlotDefinition(
        q_id="q3",
        family="another_way",
        support_format="choose",
        core_format="label_from_options",
        extension_format="label_from_options",
    ),
    WorksheetSlotDefinition(
        q_id="q4",
        family="error_repair",
        support_format="choose",
        core_format="sort",
        extension_format="sort",
    ),
    WorksheetSlotDefinition(
        q_id="q5",
        family="final_explanation",
        support_format="short_answer",
        core_format="fill_box",
        extension_format="fill_box",
    ),
)

THREE_PRODUCT_12: Sequence[WorksheetSlotDefinition] = (
    WorksheetSlotDefinition(
        q_id="q1",
        family="product_recognition",
        support_format="choose",
        core_format="choose",
        extension_format="choose",
    ),
    WorksheetSlotDefinition(
        q_id="q2",
        family="missing_factor",
        support_format="fill_box",
        core_format="match",
        extension_format="match",
    ),
    WorksheetSlotDefinition(
        q_id="q3",
        family="another_way",
        support_format="choose",
        core_format="label_from_options",
        extension_format="label_from_options",
    ),
    WorksheetSlotDefinition(
        q_id="q4",
        family="error_repair",
        support_format="choose",
        core_format="sort",
        extension_format="sort",
    ),
    WorksheetSlotDefinition(
        q_id="q5",
        family="product_recognition",
        support_format="match",
        core_format="label_from_options",
        extension_format="label_from_options",
    ),
    WorksheetSlotDefinition(
        q_id="q6",
        family="missing_factor",
        support_format="choose",
        core_format="fill_box",
        extension_format="number_entry",
    ),
    WorksheetSlotDefinition(
        q_id="q7",
        family="another_way",
        support_format="label_from_options",
        core_format="short_answer",
        extension_format="write_expression",
    ),
    WorksheetSlotDefinition(
        q_id="q8",
        family="error_repair",
        support_format="match",
        core_format="sort",
        extension_format="short_answer",
    ),
    WorksheetSlotDefinition(
        q_id="q9",
        family="product_recognition",
        support_format="choose",
        core_format="match",
        extension_format="label_from_options",
    ),
    WorksheetSlotDefinition(
        q_id="q10",
        family="missing_factor",
        support_format="fill_box",
        core_format="number_entry",
        extension_format="match",
    ),
    WorksheetSlotDefinition(
        q_id="q11",
        family="another_way",
        support_format="choose",
        core_format="short_answer",
        extension_format="write_expression",
    ),
    WorksheetSlotDefinition(
        q_id="q12",
        family="final_explanation",
        support_format="short_answer",
        core_format="fill_box",
        extension_format="fill_box",
    ),
)


_WORKSHEET_FORMATS: Final[dict[str, Sequence[WorksheetSlotDefinition]]] = {
    "one_product_10": ONE_PRODUCT_10,
    "three_product_12": THREE_PRODUCT_12,
}

_PRODUCT_COUNT_BY_FORMAT: Final[dict[str, int]] = {
    "one_product_10": 1,
    "three_product_12": 3,
}


def product_count_for_format(format_id: str) -> int:
    try:
        return _PRODUCT_COUNT_BY_FORMAT[format_id]
    except KeyError as exc:
        raise ValueError(f"Unknown worksheet format '{format_id}'.") from exc


def worksheet_slots_for_format(format_id: str) -> Sequence[WorksheetSlotDefinition]:
    try:
        return _WORKSHEET_FORMATS[format_id]
    except KeyError as exc:
        raise ValueError(f"Unknown worksheet format '{format_id}'.") from exc


def validate_slot_definition(slot: WorksheetSlotDefinition) -> None:
    print(
        "DEBUG SLOT",
        slot.q_id,
        slot.family,
        slot.support_format,
        slot.core_format,
        slot.extension_format,
    )

    if not family_allowed_for_tier(slot.family, "Support"):
        raise ValueError(f"Family '{slot.family}' is not allowed for tier 'Support'.")

    if not family_allowed_for_tier(slot.family, "Core"):
        raise ValueError(f"Family '{slot.family}' is not allowed for tier 'Core'.")

    if not family_allowed_for_tier(slot.family, "Extension"):
        raise ValueError(f"Family '{slot.family}' is not allowed for tier 'Extension'.")

    if not format_allowed_for_family(slot.family, slot.support_format, "Support"):
        raise ValueError(
            f"Support format '{slot.support_format}' is not allowed for family '{slot.family}'."
        )

    if not format_allowed_for_family(slot.family, slot.core_format, "Core"):
        raise ValueError(
            f"Core format '{slot.core_format}' is not allowed for family '{slot.family}'."
        )

    if not format_allowed_for_family(slot.family, slot.extension_format, "Extension"):
        raise ValueError(
            f"Extension format '{slot.extension_format}' is not allowed for family '{slot.family}'."
        )

    if slot.family == "final_explanation":
        if not explanation_format_allowed_for_tier("Support", slot.support_format):
            raise ValueError(
                f"Support explanation format '{slot.support_format}' is not allowed."
            )

        if not explanation_format_allowed_for_tier("Core", slot.core_format):
            raise ValueError(
                f"Core explanation format '{slot.core_format}' is not allowed."
            )

        if not explanation_format_allowed_for_tier("Extension", slot.extension_format):
            raise ValueError(
                f"Extension explanation format '{slot.extension_format}' is not allowed."
            )


def validate_worksheet_format_system() -> None:
    for format_id, slots in _WORKSHEET_FORMATS.items():
        expected_count = product_count_for_format(format_id)
        if expected_count not in (1, 3):
            raise ValueError(
                f"Unsupported product count '{expected_count}' for format '{format_id}'."
            )

        for slot in slots:
            validate_slot_definition(slot)


validate_worksheet_format_system()
