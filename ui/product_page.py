# File: ui/product_page.py

from __future__ import annotations

from html import escape
from typing import Any, Mapping

import streamlit as st

from ui.components import page_header


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


def _render_empty_state() -> None:
    page_header("Product Lab", "A single hub view with routes in and out.")
    st.info("No product is available for Product Lab.")


def _render_product_identity(product_meta: Mapping[str, Any]) -> None:
    product = product_meta.get("product", "—")
    intro_route = product_meta.get("intro_route", "—")
    structural_role = product_meta.get("structural_role", "—")
    stage_label = product_meta.get("stage_label") or product_meta.get("stage") or "—"

    st.markdown(
        f"""
        <div class="tmk-card" style="margin-bottom:1rem;">
            <div class="tmk-small-label">Selected product</div>
            <div class="tmk-section-title">{escape(str(product))}</div>
            <div class="tmk-note" style="margin-top:0.35rem;">
                {escape(str(stage_label))}
            </div>
            <div class="tmk-note" style="margin-top:0.35rem;">
                Intro route: {escape(str(intro_route))}
            </div>
            <div class="tmk-note" style="margin-top:0.35rem;">
                Structural role: {escape(str(structural_role))}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _route_text(route: Any) -> str:
    if isinstance(route, str):
        return route

    if isinstance(route, Mapping):
        expression = route.get("expression")
        if expression:
            return str(expression)

        dividend = route.get("dividend")
        divisor = route.get("divisor")
        quotient = route.get("quotient")
        if dividend is not None and divisor is not None and quotient is not None:
            return f"{dividend} ÷ {divisor} = {quotient}"

        factors = route.get("factors")
        product = route.get("product")
        if isinstance(factors, (list, tuple)) and len(factors) == 2 and product is not None:
            return f"{factors[0]} × {factors[1]} = {product}"

    return str(route)


def _render_route_column(title: str, routes: list[Any], empty_text: str) -> None:
    st.markdown(
        f"""
        <div class="tmk-card" style="height:100%;">
            <div class="tmk-small-label">{escape(title)}</div>
        """,
        unsafe_allow_html=True,
    )

    if routes:
        for route in routes:
            st.markdown(
                f'<div class="tmk-answer-box">{escape(_route_text(route))}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            f'<div class="tmk-note">{escape(empty_text)}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def _render_product_hub(
    *,
    product_label: Any,
    entry_routes: list[Any],
    exit_routes: list[Any],
) -> None:
    st.markdown("### Hub view")
    st.caption("Entry routes move inward to the product. Exit routes move outward from it.")

    left_col, middle_col, right_col = st.columns([1.35, 0.8, 1.35])

    with left_col:
        _render_route_column(
            "Entry routes",
            entry_routes,
            "No entry routes provided.",
        )

    with middle_col:
        st.markdown(
            f"""
            <div class="tmk-card" style="text-align:center;height:100%;display:flex;flex-direction:column;justify-content:center;">
                <div class="tmk-small-label">Product hub</div>
                <div class="tmk-section-title" style="margin-top:0.35rem;">{escape(str(product_label))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right_col:
        _render_route_column(
            "Exit routes",
            exit_routes,
            "No exit routes provided.",
        )


def _render_compare_bar(compare_meta: Mapping[str, Any]) -> None:
    compare_product = compare_meta.get("product", "—")
    compare_stage = compare_meta.get("stage_label") or compare_meta.get("stage") or "—"
    shared_factors = _as_sequence(compare_meta.get("shared_factors"))

    shared_text = ""
    if shared_factors:
        shared_text = f" · Shared factors: {', '.join(str(value) for value in shared_factors)}"

    st.markdown(
        f"""
        <div class="tmk-card" style="margin-top:1rem;">
            <div class="tmk-small-label">Compare product</div>
            <div class="tmk-note">
                {escape(str(compare_product))} · {escape(str(compare_stage))}{escape(shared_text)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_product_lab_page(view_model: ViewModel) -> None:
    """
    Product Lab is a product-level surface.

    It renders:
    - one page header
    - one product identity block
    - one product hub
    - one optional compare bar

    It must not render:
    - representation cards
    - inverse link cards
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
    _render_product_identity(product_meta)
    _render_product_hub(
        product_label=product_meta["product"],
        entry_routes=entry_routes,
        exit_routes=exit_routes,
    )

    if compare_meta is not None:
        _render_compare_bar(compare_meta)
