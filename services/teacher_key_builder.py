from __future__ import annotations

from dataclasses import asdict, is_dataclass
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


def _to_plain_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if is_dataclass(value):
        return asdict(value)
    if hasattr(value, "__dict__"):
        return dict(value.__dict__)
    return {}


def _as_tuple(value: Any) -> tuple[Any, ...]:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    if isinstance(value, set):
        return tuple(value)
    return (value,)


def _resolve_product(row: dict[str, Any]) -> int:
    product = _get(
        row,
        "target_product",
        "product",
        default=0,
    )
    try:
        return int(product)
    except (TypeError, ValueError):
        return 0


def _resolve_tier(plan: Any, row: dict[str, Any]) -> str:
    return str(
        _get(
            row,
            "tier",
            default=_get(plan, "tier", default="Core"),
        )
    )


def _resolve_family(row: dict[str, Any]) -> str:
    return str(
        _get(
            row,
            "family",
            "section",
            default="route_in",
        )
    )


def _resolve_quiz_format(row: dict[str, Any]) -> str:
    return str(
        _get(
            row,
            "quiz_format",
            "format",
            default="fill_box",
        )
    )


def _resolve_vocab(plan: Any, row: dict[str, Any]) -> tuple[str, ...]:
    item_vocab = _as_tuple(
        _get(
            row,
            "vocabulary_words",
            "vocab",
            default=(),
        )
    )
    if item_vocab:
        return tuple(str(word) for word in item_vocab)

    required_vocab_focus = _as_tuple(_get(plan, "required_vocab_focus", default=()) or ())
    if required_vocab_focus:
        return tuple(str(word) for word in required_vocab_focus[:2])

    stage_available_vocab = _as_tuple(_get(plan, "stage_available_vocab", default=()) or ())
    return tuple(str(word) for word in stage_available_vocab[:2])


def _resolve_related_products(row: dict[str, Any]) -> tuple[int, ...]:
    related = _as_tuple(_get(row, "related_products", default=()) or ())
    resolved: list[int] = []
    for value in related:
        try:
            resolved.append(int(value))
        except (TypeError, ValueError):
            continue
    return tuple(resolved)


def _load_msvwa_registry() -> Any:
    try:
        from services.msvwa_registry import resolve_item_msvwa
        return resolve_item_msvwa
    except Exception:
        return None


def _fallback_msvwa_tags(
    family: str,
    quiz_format: str,
    tier: str,
) -> tuple[str, ...]:
    family_defaults: dict[str, tuple[str, ...]] = {
        "product_recognition": ("A", "M"),
        "route_in": ("S", "W"),
        "missing_factor": ("S", "W"),
        "another_way": ("V", "W"),
        "compare_routes": ("V", "M", "W"),
        "route_out": ("S", "W"),
        "check_match": ("A", "M"),
        "correct_incorrect": ("M", "W"),
        "error_repair": ("M", "S", "W"),
        "structural_grouping": ("A", "V", "M"),
        "final_explanation": ("W", "M"),
    }

    format_boosts: dict[str, tuple[str, ...]] = {
        "circle": ("A",),
        "tick": ("A",),
        "yes_no": ("M",),
        "tick_all": ("A", "V", "M"),
        "match": ("A", "W"),
        "sort": ("V", "M"),
        "choose": ("A", "M"),
        "fill_box": ("S", "W"),
        "label_from_options": ("A", "W"),
    }

    tier_priority: dict[str, tuple[str, ...]] = {
        "Support": ("A", "S", "W", "M", "V"),
        "Core": ("S", "V", "W", "A", "M"),
        "Extension": ("V", "M", "W", "S", "A"),
    }

    merged: list[str] = []
    for tag in family_defaults.get(family, ("M", "S")) + format_boosts.get(quiz_format, ()):
        if tag not in merged:
            merged.append(tag)

    priority = tier_priority.get(tier, ("S", "V", "W", "A", "M"))
    merged.sort(key=lambda tag: priority.index(tag) if tag in priority else 99)

    return tuple(merged[:3])


def _msvwa_tags(row: dict[str, Any], tier: str) -> tuple[str, ...]:
    family = _resolve_family(row)
    quiz_format = _resolve_quiz_format(row)

    resolver = _load_msvwa_registry()
    if resolver is not None:
        try:
            tags = resolver(
                family=family,
                quiz_format=quiz_format,
                tier=tier,
            )
            if tags:
                return tuple(str(tag) for tag in tags)
        except Exception:
            pass

    return _fallback_msvwa_tags(
        family=family,
        quiz_format=quiz_format,
        tier=tier,
    )


def _answer_text(row: dict[str, Any], product: int) -> str:
    explicit_answer = _get(row, "answer", default="")
    if explicit_answer not in ("", None):
        return str(explicit_answer)

    family = _resolve_family(row)
    related_products = _resolve_related_products(row)

    if family == "product_recognition":
        return str(product)

    if family == "route_in":
        return f"Accept a correct route into {product}."

    if family == "missing_factor":
        return f"Accept the missing factor that completes the route to {product}."

    if family == "another_way":
        if related_products:
            return f"Accept another correct route to {product}, possibly using comparison with {', '.join(str(p) for p in related_products)}."
        return f"Accept another correct way to make {product}."

    if family == "compare_routes":
        return f"Accept a valid comparison between two routes that make {product}."

    if family == "route_out":
        return f"Accept a correct inverse division fact from {product}."

    if family == "check_match":
        return f"Accept the correct matching route, fact, or representation for {product}."

    if family == "correct_incorrect":
        return f"Accept a correct judgement with correction if needed for {product}."

    if family == "error_repair":
        return f"Accept the repaired statement that correctly makes or uses {product}."

    if family == "structural_grouping":
        return f"Accept correct grouping/classification based on the structure of {product}."

    if family == "final_explanation":
        return f"Accept a clear product-first explanation for {product}."

    return f"Accept any correct multiplication/division fact family for {product}."


def _teacher_note(row: dict[str, Any], product: int, tier: str) -> str:
    explicit_note = _get(row, "teacher_note", "note", default="")
    if explicit_note not in ("", None):
        return str(explicit_note)

    family = _resolve_family(row)

    family_notes: dict[str, str] = {
        "product_recognition": f"Secure recognition of {product} as the target product.",
        "route_in": f"Guide pupils into {product} through a valid multiplication route.",
        "missing_factor": f"Focus on the factor-product relationship inside {product}.",
        "another_way": f"Press for another lawful route to the same product {product}.",
        "compare_routes": f"Compare routes while keeping the product {product} fixed.",
        "route_out": f"Link {product} to inverse division without leaving the product-first frame.",
        "check_match": f"Check whether pupils can identify the representation that belongs to {product}.",
        "correct_incorrect": f"Use correctness checking to secure structural understanding of {product}.",
        "error_repair": f"Repair the route while keeping attention on product {product}.",
        "structural_grouping": f"Classify {product} by structure, family, or route behaviour.",
        "final_explanation": f"Press for a spoken or written explanation of how {product} is built.",
    }

    note = family_notes.get(family, f"Secure product-first understanding for {product}.")

    if tier == "Support":
        return note
    if tier == "Extension":
        return note + " Push for fuller explanation, comparison, and inverse linkage."
    return note


def build_teacher_key(plan: Any) -> dict[str, Any]:
    items = _as_tuple(_get(plan, "items", default=()) or ())
    answers: list[dict[str, Any]] = []

    for raw_item in items:
        row = _to_plain_dict(raw_item)
        product = _resolve_product(row)
        tier = _resolve_tier(plan, row)
        vocab = _resolve_vocab(plan, row)

        q_id = _get(row, "q_id", "id", default=len(answers) + 1)
        try:
            q_id = int(q_id)
        except (TypeError, ValueError):
            q_id = len(answers) + 1

        answers.append(
            {
                "q_id": q_id,
                "answer": _answer_text(row, product),
                "msvwa_tags": _msvwa_tags(row, tier),
                "teacher_note": _teacher_note(row, product, tier),
                "vocab": vocab,
            }
        )

    return {
        "answers": answers,
    }


__all__ = ["build_teacher_key"]
