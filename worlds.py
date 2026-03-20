from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Tuple


TMK_WORLD: Final[str] = "TMK World"
BEYOND_10_WORLD: Final[str] = "Beyond-10 World"

FORBIDDEN_WORLD_PHRASES: Final[Tuple[str, ...]] = (
    "the TMK World",
    "the Beyond-10 World",
    "belongs to TMK World",
    "belongs to Beyond-10 World",
)


@dataclass(frozen=True)
class WorldNames:
    tmk: str = TMK_WORLD
    beyond_10: str = BEYOND_10_WORLD


WORLD_NAMES: Final[WorldNames] = WorldNames()


def tmk_world_name() -> str:
    return WORLD_NAMES.tmk


def beyond_10_world_name() -> str:
    return WORLD_NAMES.beyond_10


def forbidden_world_phrases() -> Tuple[str, ...]:
    return FORBIDDEN_WORLD_PHRASES


def validate_world_name_usage(text: str) -> None:
    for phrase in FORBIDDEN_WORLD_PHRASES:
        if phrase in text:
            raise ValueError(
                f"Forbidden world phrasing detected: '{phrase}' in '{text}'"
            )
