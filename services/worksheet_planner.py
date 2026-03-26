from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any

from domain.product_metadata import (
    available_products as metadata_available_products,
    new_products as metadata_new_products,
)

from domain.stage_vocabulary import get_stage_vocabulary


ITEM_FAMILY_SEQUENCE = (
    "product_recognition",
    "route_in",
    "missing_factor",
    "route_out",
    "another_way",
    "compare_routes",
    "correct_incorrect",
    "error_repair",
    "structural_grouping",
    "final_explanation",
)

QUIZ_FORMAT_SEQUENCE = (
    "circle",
    "fill_box",
    "fill_box",
    "fill_box",
    "fill_box",
    "choose",
    "yes_no",
    "fill_box",
    "sort",
    "fill_box",
)


def _as_plain_data(value: Any) -> Any:
    if value is None:
        return None
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, dict):
        return {k: _as_plain_data(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_as_plain_data(v) for v in value]
    return value


def _get(value: Any, *names: str, default: Any = None) -> Any:
    if value is None:
        return default

    for name in names:
        if isinstance(value, dict) and name in value:
            return value[name]
        if hasattr(value, name):
            return getattr(value, name)

    return default


def _question_count(format_id: str) -> int:
    if format_id == "one_product_10":
        return 10
    if format_id == "three_product_12":
        return 12
    raise ValueError(f"Unsupported worksheet format: {format_id}")


def _selected_products(selection: Any) -> tuple[int, ...]:
    selection = _as_plain_data(selection) or {}
    products = _get(selection, "selected_products", "products", default=()) or ()
    return tuple(int(p) for p in products)


def _recap_products(selection: Any) -> tuple[int, ...]:
    selection = _as_plain_data(selection) or {}
    products = _get(selection, "recap_products", default=()) or ()
    return tuple(int(p) for p in products)


def _selection_reasons(selection: Any) -> tuple[str, ...]:
    selection = _as_plain_data(selection) or {}
    reasons = _get(selection, "selection_reasons", "reasons", default=()) or ()
    return tuple(str(r) for r in reasons)


def _structural_tags(selection: Any) -> tuple[str, ...]:
    selection = _as_plain_data(selection) or {}
    tags = _get(selection, "structural_tags", "tags", default=()) or ()
    return tuple(str(t) for t in tags)


def _vocab_supported(selection: Any, stage: str) -> tuple[str, ...]:
    selection = _as_plain_data(selection) or {}

    vocab = _get(selection, "vocab_supported", "supported_vocabulary", default=None)

    if vocab:
        return tuple(str(v) for v in vocab)

    try:
        stage_vocab = get_stage_vocabulary(stage)
        available_vocab = _get(stage_vocab, "available_vocab", default=()) or ()
        return tuple(str(v) for v in available_vocab)
    except Exception:
        return ()


def _build_question_items(
    *,
    stage: str,
    format_id: str,
    tier: str,
    selected_products: tuple[int, ...],
    recap_products: tuple[int, ...],
) -> list[dict[str, Any]]:

    total = _question_count(format_id)

    primary_pool = list(selected_products)
    recap_pool = list(recap_products)

    items: list[dict[str, Any]] = []

    for index in range(total):

        if recap_pool and index >= total - len(recap_pool):
            product = recap_pool[(index - (total - len(recap_pool))) % len(recap_pool)]
            source = "recap"
        else:
            product = primary_pool[index % len(primary_pool)]
            source = "selected"

        family = ITEM_FAMILY_SEQUENCE[index % len(ITEM_FAMILY_SEQUENCE)]
        quiz_format = QUIZ_FORMAT_SEQUENCE[index % len(QUIZ_FORMAT_SEQUENCE)]

        items.append(
            {
                "q_id": index + 1,
                "slot_index": index,
                "family": family,
                "quiz_format": quiz_format,
                "target_product": product,
                "product": product,
                "source": source,
                "stage": stage,
                "tier": tier,
                "format_id": format_id,
                "related_products": selected_products,
            }
        )

    return items


def build_worksheet_plan(request: Any, selection: Any) -> dict[str, Any]:

    request_data = _as_plain_data(request) or {}

    stage = _get(request_data, "stage", default=None)
    format_id = _get(request_data, "format_id", default=None)
    tier = _get(request_data, "tier", default=None)

    if not stage:
        raise ValueError("Worksheet request is missing 'stage'.")
    if not format_id:
        raise ValueError("Worksheet request is missing 'format_id'.")
    if not tier:
        raise ValueError("Worksheet request is missing 'tier'.")

    selected_products = _selected_products(selection)
    recap_products = _recap_products(selection)

    stage_vocab = get_stage_vocabulary(stage)

    plan = {
        "stage": stage,
        "format_id": format_id,
        "tier": tier,
        "selection_scope": _get(request_data, "selection_scope", default=None),
        "selection_mode": _get(request_data, "selection_mode", default=None),
        "include_recap": bool(_get(request_data, "include_recap", default=False)),
        "recap_count": int(_get(request_data, "recap_count", default=0) or 0),
        "selected_products": selected_products,
        "recap_products": recap_products,
        "selection_reasons": _selection_reasons(selection),
        "vocab_supported": _vocab_supported(selection, stage),
        "structural_tags": _structural_tags(selection),
        "available_products": tuple(metadata_available_products(stage)),
        "new_products": tuple(metadata_new_products(stage)),
        "required_vocab_focus": tuple(_get(stage_vocab, "required_vocab_focus", default=()) or ()),
        "preferred_quiz_formats": tuple(_get(stage_vocab, "preferred_quiz_formats", default=()) or ()),
        "preferred_vocab_task_types": tuple(_get(stage_vocab, "preferred_vocab_task_types", default=()) or ()),
        "items": _build_question_items(
            stage=stage,
            format_id=format_id,
            tier=tier,
            selected_products=selected_products,
            recap_products=recap_products,
        ),
    }

    return plan


__all__ = ["build_worksheet_plan"]
