from __future__ import annotations

from typing import Any


def _get(value: Any, *names: str, default: Any = None) -> Any:
    if value is None:
        return default

    if isinstance(value, dict):
        for name in names:
            if name in value:
                return value[name]
        return default

    for name in names:
        if hasattr(value, name):
            return getattr(value, name)

    return default


def _msvwa_tags(item: dict[str, Any]) -> tuple[str, ...]:
    tier = str(item["tier"])
    source = str(item["source"])

    tags = ["M", "S"]

    if tier in ("Core", "Extension"):
        tags.append("V")
    if tier == "Extension":
        tags.append("A")
    if source == "recap":
        tags.append("W")

    return tuple(tags)


def _answer_text(product: int) -> str:
    return f"Accept any correct multiplication/division fact family for {product}."


def _teacher_note(product: int, tier: str) -> str:
    if tier == "Support":
        return f"Guide pupils toward one clear route into {product}."
    if tier == "Extension":
        return f"Press for explanation, comparison, and inverse linkage for {product}."
    return f"Secure product-first understanding for {product}."


def build_teacher_key(plan: Any) -> dict[str, Any]:
    items = _get(plan, "items", default=()) or ()
    required_vocab_focus = tuple(_get(plan, "required_vocab_focus", default=()) or ())

    answers: list[dict[str, Any]] = []

    for item in items:
        row = item if isinstance(item, dict) else dict(item)
        product = int(row["product"])
        tier = str(row["tier"])

        answers.append(
            {
                "q_id": int(row["q_id"]),
                "answer": _answer_text(product),
                "msvwa_tags": _msvwa_tags(row),
                "teacher_note": _teacher_note(product, tier),
                "vocab": required_vocab_focus[:2],
            }
        )

    return {
        "answers": answers,
    }


__all__ = ["build_teacher_key"]
