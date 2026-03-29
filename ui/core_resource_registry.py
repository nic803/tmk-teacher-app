from __future__ import annotations

from typing import Any


CORE_RESOURCE_REGISTRY: dict[str, dict[str, Any]] = {
    "number_line_doubler": {
        "id": "number_line_doubler",
        "title": "Number Line Doubler",
        "stage": "Stage E — Doubling Chain (2× → 4× → 8×)",
        "theme": "Meadow Stage",
        "pattern": "Fixed factor, doubled multiplier, doubled product",
        "purpose": (
            "Show that 2×, 4×, and 8× are connected by doubling with one factor "
            "held fixed, so pupils move from skip-counting to structural comparison."
        ),
        "asset_path": "number_line_doubler.html",
        "content_path": "stage-e/number-line-doubler",
        "prompt": "Double it, then double it again!",
        "equations": {
            "format": "X × Y = Z",
            "examples": (
                "2 × 6 = 12",
                "4 × 6 = 24",
                "8 × 6 = 48",
            ),
            "toggleable_for_prediction_mode": True,
        },
        "controls": (
            "Select factor",
            "Show 2× jump",
            "Show 4× jump",
            "Show 8× jump",
            "Sync jumps",
            "Slow motion",
            "Show equations",
            "Show structure",
            "Full screen",
            "Reset",
        ),
        "teacher_panel": {
            "msvwa": {
                "marker": "The fixed factor stays the same across the chain.",
                "sequence": "The pupil follows the order 2×, 4×, 8× and links each step to a doubled product.",
                "variation": "The multiplier and product change; the factor stays fixed.",
                "working_memory": "Hold the fixed factor, jump sequence, and matching equations together.",
                "attention": "Notice the fixed factor first, then the doubling in the multiplier and product.",
            },
            "diagnostics": {
                "look_for": "Whether the pupil can identify the fixed factor and explain how the products grow as the multiplier doubles.",
                "secure_if": "The pupil can explain one fixed-factor family clearly and track how doubling the multiplier doubles the product.",
                "watch_for": "Missing the fixed factor, treating each fact as unrelated, or losing the doubling relationship across the chain.",
                "prompt_if_stuck": "What stays the same? Which number doubles? What happens to the product when the multiplier doubles?",
                "if_knowledge_is_missing": "Fixed factor not seen → Rebuild one factor family. Example: 2 × 7 = 14, 4 × 7 = 28, 8 × 7 = 56",
                "next_move": "Change/stay confusion → Name the fixed factor and changing multiplier. Example: 7 stays fixed; 2, 4, 8 change",
                "cues": (
                    {
                        "title": "Fixed factor not seen",
                        "instruction": "Rebuild one factor family",
                        "example": "2 × 7 = 14, 4 × 7 = 28, 8 × 7 = 56",
                    },
                    {
                        "title": "Doubling not secure",
                        "instruction": "Rebuild the doubling chain",
                        "example": "14 → 28 → 56",
                    },
                    {
                        "title": "Equation link weak",
                        "instruction": "Match each product to its equation",
                        "example": "28 = 4 × 7",
                    },
                    {
                        "title": "Change/stay confusion",
                        "instruction": "Name the fixed factor and changing multiplier",
                        "example": "7 stays fixed; 2, 4, 8 change",
                    },
                    {
                        "title": "Factor family not secure",
                        "instruction": "Rehearse one family side by side",
                        "example": "2 × 7 = 14, 4 × 7 = 28, 8 × 7 = 56",
                    },
                ),
            },
        },
        "tags": {
            "access": (
                "SEND",
                "EAL",
                "Intervention",
                "Teacher-led modelling",
            ),
            "use_case": (
                "Catch-up",
                "Pattern noticing",
                "Linked-family comparison",
                "Structural reasoning",
            ),
            "status": "In progress",
        },
    },
}


def get_core_resource(resource_id: str) -> dict[str, Any]:
    return CORE_RESOURCE_REGISTRY[resource_id]
