from __future__ import annotations

from typing import Tuple


TMK_WORLD: str = "TMK World"
BEYOND_10_WORLD: str = "Beyond-10 World"


def forbidden_world_phrases() -> Tuple[str, ...]:
    """
    Phrases that must never appear in prompts or UI text.
    """
    return (
        "the TMK World",
        "the Beyond-10 World",
        "belongs to TMK World",
        "belongs to Beyond-10 World",
    )


def validate_world_name_usage(text: str) -> None:
    """
    Ensure forbidden world wording never appears.
    """
    for phrase in forbidden_world_phrases():
        if phrase in text:
            raise ValueError(
                f"Forbidden world wording detected: '{phrase}' in '{text}'"
            )


def world_names() -> Tuple[str, str]:
    """
    Canonical world names used by the system.
    """
    return (TMK_WORLD, BEYOND_10_WORLD)
