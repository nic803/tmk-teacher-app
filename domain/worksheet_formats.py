# domain/worksheet_formats.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

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


# Example only; keep your existing banks/order.
ONE_PRODUCT_10: Sequence[WorksheetSlotDefinition] = [
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
]

ALL_WORKSHEET_FORMATS: Sequence[Sequence[WorksheetSlotDefinition]] = [
    ONE_PRODUCT_10,
]


def validate_slot_definition(slot: WorksheetSlotDefinition) -> None:
    # Temporary diagnostic: this identifies the exact first failing slot.
    print(
        "DEBUG SLOT",
        slot.q_id,
        slot.family,
        slot.support_format,
        slot.core_format,
        slot.extension_format,
    )

    if not family_allowed_for_tier(slot.family, "Support"):
        raise ValueError(f"Family '{slot.family}' is not allowed for tier 'Support'")

    if not family_allowed_for_tier(slot.family, "Core"):
        raise ValueError(f"Family '{slot.family}' is not allowed for tier 'Core'")

    if not family_allowed_for_tier(slot.family, "Extension"):
        raise ValueError(f"Family '{slot.family}' is not allowed for tier 'Extension'")

    if not format_allowed_for_family(slot.family, slot.support_format, "Support"):
        raise ValueError(
            f"Support format '{slot.support_format}' is not allowed for family '{slot.family}'"
        )

    if not format_allowed_for_family(slot.family, slot.core_format, "Core"):
        raise ValueError(
            f"Core format '{slot.core_format}' is not allowed for family '{slot.family}'"
        )

    if not format_allowed_for_family(slot.family, slot.extension_format, "Extension"):
        raise ValueError(
            f"Extension format '{slot.extension_format}' is not allowed for family '{slot.family}'"
        )

    if slot.family == "final_explanation":
        if not explanation_format_allowed_for_tier("Support", slot.support_format):
            raise ValueError(
                f"Support explanation format '{slot.support_format}' is not allowed"
            )
        if not explanation_format_allowed_for_tier("Core", slot.core_format):
            raise ValueError(
                f"Core explanation format '{slot.core_format}' is not allowed"
            )
        if not explanation_format_allowed_for_tier("Extension", slot.extension_format):
            raise ValueError(
                f"Extension explanation format '{slot.extension_format}' is not allowed"
            )


def validate_worksheet_format_system() -> None:
    for worksheet in ALL_WORKSHEET_FORMATS:
        for slot in worksheet:
            validate_slot_definition(slot)


validate_worksheet_format_system()
