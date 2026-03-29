from __future__ import annotations

from typing import Any


EXTENSION_ANIMATIONS_REGISTRY: dict[str, dict[str, Any]] = {
    "extension_number_line_doubler": {
        "id": "extension_number_line_doubler",
        "title": "Number Line Doubler",
        "family": "both",
        "pattern": "Fixed factor, doubled multiplier, doubled product",
        "purpose": (
            "Show how doubling links related products through repeated scaling, "
            "with one factor held fixed so pupils can compare 2×, 4×, and 8× forms."
        ),
        "asset_path": "number_line_doubler.html",
        "content_path": "extension/animations/number-line-doubler",
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
        "teacher_support_level": "full",
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
            },
        },
        "tags": {
            "status": "In progress",
            "use_case": (
                "Catch-up",
                "Pattern noticing",
                "Linked-family comparison",
                "Structural reasoning",
            ),
        },
    },
    "extension_11x_ten_plus_one_builder": {
        "id": "extension_11x_ten_plus_one_builder",
        "title": "11× Ten-Plus-One Builder",
        "family": "11x",
        "pattern": "ten-plus-one",
        "purpose": (
            "Show 11× products as 10n + n so pupils can build extension products "
            "from a secure ten-times benchmark."
        ),
        "asset_path": "extension_11x_ten_plus_one_builder.html",
        "content_path": "extension/animations/11x-ten-plus-one-builder",
        "prompt": "Build it from ten lots and one more lot.",
        "equations": {
            "format": "11 × n = 10 × n + 1 × n",
            "examples": (
                "11 × 4 = 10 × 4 + 1 × 4",
                "11 × 7 = 10 × 7 + 1 × 7",
            ),
            "toggleable_for_prediction_mode": True,
        },
        "controls": (
            "Select product",
            "Show build",
            "Show equations",
            "Show structure",
            "Full screen",
            "Reset",
        ),
        "teacher_support_level": "reduced",
        "tags": {
            "status": "Draft",
            "use_case": (
                "Extension bridge",
                "Benchmark reasoning",
                "Teacher-led modelling",
            ),
        },
    },
    "extension_12x_ten_plus_two_builder": {
        "id": "extension_12x_ten_plus_two_builder",
        "title": "12× Ten-Plus-Two Builder",
        "family": "12x",
        "pattern": "ten-plus-two",
        "purpose": (
            "Show 12× products as 10n + 2n so pupils can connect extension facts "
            "to benchmark structure and doubling."
        ),
        "asset_path": "extension_12x_ten_plus_two_builder.html",
        "content_path": "extension/animations/12x-ten-plus-two-builder",
        "prompt": "Build it from ten lots and two more lots.",
        "equations": {
            "format": "12 × n = 10 × n + 2 × n",
            "examples": (
                "12 × 4 = 10 × 4 + 2 × 4",
                "12 × 6 = 10 × 6 + 2 × 6",
            ),
            "toggleable_for_prediction_mode": True,
        },
        "controls": (
            "Select product",
            "Show build",
            "Show equations",
            "Show structure",
            "Full screen",
            "Reset",
        ),
        "teacher_support_level": "reduced",
        "tags": {
            "status": "Draft",
            "use_case": (
                "Extension bridge",
                "Benchmark reasoning",
                "Doubling support",
            ),
        },
    },
    "extension_12x_double_six_compare": {
        "id": "extension_12x_double_six_compare",
        "title": "12× Double-Six Compare",
        "family": "12x",
        "pattern": "double-six",
        "purpose": (
            "Show that 12× can also be built as 2 × 6× so pupils compare lawful "
            "extension builds for the same product."
        ),
        "asset_path": "extension_12x_double_six_compare.html",
        "content_path": "extension/animations/12x-double-six-compare",
        "prompt": "Compare two lawful ways to build the same product.",
        "equations": {
            "format": "12 × n = 2 × (6 × n)",
            "examples": (
                "12 × 4 = 2 × (6 × 4)",
                "12 × 8 = 2 × (6 × 8)",
            ),
            "toggleable_for_prediction_mode": False,
        },
        "controls": (
            "Select product",
            "Compare builds",
            "Show equations",
            "Show structure",
            "Full screen",
            "Reset",
        ),
        "teacher_support_level": "reduced",
        "tags": {
            "status": "Draft",
            "use_case": (
                "Compare forms",
                "Structural reasoning",
                "Teacher-led modelling",
            ),
        },
    },
}


def get_extension_animation(animation_id: str) -> dict[str, Any]:
    return EXTENSION_ANIMATIONS_REGISTRY[animation_id]
