# File: ui/product_page.py

from __future__ import annotations

from typing import Any, Mapping

import streamlit as st

from ui.components import (
    page_header,
    render_product_hub,
    render_product_identity,
)


ViewModel = Mapping[str, Any]


def _as_sequence(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return []


def _normalise_product_meta(view_model: ViewModel) -> dict[str, Any]:
    product_meta = dict(view_model.get("product_meta") or {})

    product_value = product_meta.get("product")
    if product_value is None:
        product_value = view_model.get("product")

    if product_value is not None:
        product_meta["product"] = product_value

    return product_meta


def _normalise_compare_meta(view_model: ViewModel) -> dict[str, Any] | None:
    compare_meta = view_model.get("compare_meta")
    if not compare_meta:
        return None
    return dict(compare_meta)


def _render_compare_bar(compare_meta: Mapping[str, Any]) -> None:
    compare_product = compare_meta.get("product", "—")
    compare_stage = compare_meta.get("stage_label") or compare_meta.get("stage") or "—"
    shared_factors = _as_sequence(compare_meta.get("shared_factors"))

    st.markdown("### Compare product")

    if shared_factors:
        shared_factors_text = ", ".join(str(value) for value in shared_factors)
        st.caption(
            f"{compare_product} · {compare_stage} · Shared factors: {shared_factors_text}"
        )
    else:
        st.caption(f"{compare_product} · {compare_stage}")


def _render_empty_state() -> None:
    page_header("Product Lab", "A single hub view with routes in and out.")
    st.info("No product is available for Product Lab.")


def render_product_lab_page(view_model: ViewModel) -> None:
    """
    Product Lab is a product-level surface.

    It renders:
    - one page header
    - one product identity block
    - one product hub
    - one optional compare bar

    It must not render:
    - duplicated route lists
    - inverse relationship cards
    - representation cards
    - structure explorer content
    - teaching activity content
    """
    if not view_model:
        _render_empty_state()
        return

    title = view_model.get("title") or "Product Lab"
    subtitle = view_model.get("subtitle") or "A single hub view with routes in and out."

    product_meta = _normalise_product_meta(view_model)
    entry_routes = _as_sequence(view_model.get("entry_routes"))
    exit_routes = _as_sequence(view_model.get("exit_routes"))
    compare_meta = _normalise_compare_meta(view_model)

    if not product_meta.get("product"):
        _render_empty_state()
        return

    page_header(title, subtitle)

    render_product_identity(product_meta)

    render_product_hub(
        product_label=product_meta["product"],
        entry_routes=entry_routes,
        exit_routes=exit_routes,
    )

    if compare_meta is not None:
        _render_compare_bar(compare_meta)
