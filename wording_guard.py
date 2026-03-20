from __future__ import annotations

from typing import Iterable

FORBIDDEN_WORLD_PHRASES = (
    "the TMK World",
    "the Beyond-10 World",
    "belongs to TMK World",
    "belongs to Beyond-10 World",
)


def assert_no_forbidden_world_phrasing(texts: Iterable[str]) -> None:
    violations = []

    for text in texts:
        for phrase in FORBIDDEN_WORLD_PHRASES:
            if phrase in text:
                violations.append((phrase, text))

    if violations:
        formatted = "; ".join(
            f"forbidden='{phrase}' in text='{text}'"
            for phrase, text in violations
        )
        raise ValueError(f"Forbidden TMK world phrasing detected: {formatted}")
