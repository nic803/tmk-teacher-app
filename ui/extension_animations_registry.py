from __future__ import annotations

from typing import Any


EXTENSION_ANIMATIONS_REGISTRY: dict[str, dict[str, Any]] = {
    "extension_11x_ten_plus_one_builder": {
        "id": "extension_11x_ten_plus_one_builder",
        "title": "11× Rabbit and Carrot Builder",
        "family": "11x",
        "pattern": "ten-plus-one",
        "purpose": (
            "Show 11× products as 10n + n through a rabbit-and-carrot build so pupils "
            "can see the ten-plus-one structure in one clear visual model."
        ),
        "asset_path": "11x_rabbit_and _carrot_builder.html",
        "content_path": "extension/animations/11x-rabbit-and-carrot-builder",
        "prompt": (
            "Build 11× by making 10 groups of carrots, then adding 1 group of rabbits. "
            "Do 10 times, then add one more group."
        ),
        "equations": {
            "format": "11 × n = 10 × n + 1 × n",
            "examples": (
                "11 × n = ten groups of n + one group of n",
                "11 × n = 10 × n + 1 × n",
                "One group of n = n",
                "Total = carrots + rabbits",
                "The chosen value changes, but the structure stays 10 groups plus 1 group.",
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
        "title": "12× Rabbit & Carrot Builder",
        "family": "12x",
        "pattern": "ten-plus-two",
        "purpose": (
            "Show 12× products as 10n + 2n through a rabbit-and-carrot build so pupils "
            "can connect extension facts to benchmark structure and doubling."
        ),
        "asset_path": "12x_rabbit_carrot_builder.html",
        "content_path": "extension/animations/12x-rabbit-carrot-builder",
        "prompt": (
            "Build 12× by making 10 groups of carrots, then adding 2 groups of rabbits. "
            "Do 10 times, then add double."
        ),
        "equations": {
            "format": "12 × n = 10 × n + 2 × n",
            "examples": (
                "12 × n = ten groups of n + two groups of n",
                "12 × n = 10 × n + 2 × n",
                "Two groups of n = double n",
                "Total = carrots + rabbits",
                "The chosen value changes, but the structure stays 10 groups plus 2 groups.",
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
        "title": "12× Time Builder",
        "family": "12x",
        "pattern": "time-pattern",
        "purpose": (
            "Show the 12× time pattern by building 12 groups of 5 minutes into "
            "60 minutes, then doubling the group size to connect 12 × 10 with 120 minutes."
        ),
        "asset_path": "extension_12x_double_six_compare.html",
        "content_path": "extension/animations/12x-time-builder",
        "prompt": (
            "Build 12 groups of 5 minutes, convert 60 minutes to 1 hour, then double "
            "the group size to reach 120 minutes."
        ),
        "equations": {
            "format": "12 × 5 minutes = 60 minutes = 1 hour",
            "examples": (
                "12 × 5 minutes = 60 minutes",
                "60 minutes = 1 hour",
                "12 × 10 minutes = 120 minutes",
                "120 minutes = 2 hours",
                "Double 5 minutes to 10 minutes, so the total doubles too.",
            ),
            "toggleable_for_prediction_mode": False,
        },
        "controls": (
            "Check each step",
            "Unlock next step",
            "Show recap",
            "Restart",
        ),
        "teacher_support_level": "reduced",
        "tags": {
            "status": "Draft",
            "use_case": (
                "Time pattern",
                "Structural reasoning",
                "Teacher-led modelling",
            ),
        },
    },
}


def get_extension_animation(animation_id: str) -> dict[str, Any]:
    return EXTENSION_ANIMATIONS_REGISTRY[animation_id]
