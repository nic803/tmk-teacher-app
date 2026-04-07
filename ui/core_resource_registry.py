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
    "tmk_matrix": {
        "id": "tmk_matrix",
        "title": "TMK Matrix",
        "stage": "A–G Overview",
        "theme": "Whiteboard Mode",
        "pattern": "Stage-pattern explorer across the bounded 1×1 to 10×10 product field",
        "purpose": (
            "Show the full bounded TMK product matrix so teachers and pupils can inspect "
            "stage patterns, square structure, multi-route products, and product routes "
            "inside one visual field."
        ),
        "asset_path": "tmk_matrix.html",
        "content_path": "tmk-matrix/whiteboard-mode",
        "prompt": "Tap a product and explore its routes and stage pattern.",
        "equations": {
            "format": "a × b = product",
            "examples": (
                "6 × 6 = 36",
                "4 × 6 = 24",
                "8 × 9 = 72",
            ),
            "toggleable_for_prediction_mode": False,
        },
        "controls": (
            "Reset board",
            "Select stage pattern",
            "Tap product",
            "Show routes",
            "Collapse stages",
        ),
        "teacher_panel": {
            "msvwa": {
                "marker": "The pupil notices that products can be grouped by structural pattern, not just read as isolated facts.",
                "sequence": "The pupil scans the bounded matrix, selects a pattern or product, and then explains how the selected product sits inside the wider structure.",
                "variation": "Products vary by stage pattern, route count, and square status while the bounded 1–10 domain stays fixed.",
                "working_memory": "Hold the selected product, its factor routes, and the surrounding stage pattern together while interpreting the matrix.",
                "attention": "Notice the selected product first, then the factor routes, then the wider pattern family shown in the matrix.",
            },
            "diagnostics": {
                "look_for": "Whether the pupil can locate a product, identify at least one lawful route, and explain how it belongs to a visible pattern family or stage group.",
                "secure_if": "The pupil can navigate the matrix confidently, identify routes into a selected product, and explain at least one structural pattern such as squares, doubling, or near-ten logic.",
                "watch_for": "Treating the grid as a random list of answers, missing the bounded 1–10 structure, or failing to connect a selected product to its pattern family.",
                "prompt_if_stuck": "Which product have you chosen? Which factors build it? Which coloured pattern or stage group does it belong to?",
                "if_knowledge_is_missing": "Routes not secure → Rebuild one selected product from its factor pairs before returning to the full matrix view.",
                "next_move": "Pattern not secure → Compare one highlighted product with another in the same family and name what stays the same and what changes.",
            },
        },
        "tags": {
            "access": (
                "Whole class",
                "Teacher-led modelling",
                "EAL",
                "SEND",
            ),
            "use_case": (
                "Pattern noticing",
                "Structural reasoning",
                "Route exploration",
                "Stage overview",
            ),
            "status": "In progress",
        },
    },
}


def get_core_resource(resource_id: str) -> dict[str, Any]:
    return CORE_RESOURCE_REGISTRY[resource_id]
