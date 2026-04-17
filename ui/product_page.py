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
            <div class="tmk-note" style="margin-top:0.35rem;">{escape(str(stage_label))}</div>
            <div class="tmk-note" style="margin-top:0.35rem;">Intro route: {escape(str(intro_route))}</div>
            <div class="tmk-note" style="margin-top:0.35rem;">Structural role: {escape(str(structural_role))}</div>
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
            return f"{factors[0]} × {factors[1]}"

    return str(route)


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


def _render_hub_visual(
    *,
    product_label: Any,
    entry_routes: list[Any],
    exit_routes: list[Any],
) -> None:
    top_items = [_route_text(route) for route in entry_routes]
    bottom_items = [_route_text(route) for route in exit_routes]

    if not top_items:
        top_items = ["No entry routes"]
    if not bottom_items:
        bottom_items = ["No exit routes"]

    top_html = "".join(
        f'<span class="tmk-hub-chip">{escape(item)}</span>'
        for item in top_items
    )
    bottom_html = "".join(
        f'<span class="tmk-hub-chip">{escape(item)}</span>'
        for item in bottom_items
    )

    arrow_count = max(len(top_items), len(bottom_items), 3)
    arrows_html = "".join("<span>↓</span>" for _ in range(min(arrow_count, 6)))

    st.markdown("### Hub view")
    st.caption("Entry routes move inward to the product. Exit routes move outward from it.")

    st.markdown(
        f"""
        <div class="tmk-hub-visual">
            <div class="tmk-hub-top">{top_html}</div>
            <div class="tmk-hub-arrows">{arrows_html}</div>
            <div class="tmk-hub-center-wrap">
                <div class="tmk-hub-center">{escape(str(product_label))}</div>
            </div>
            <div class="tmk-hub-arrows">{arrows_html}</div>
            <div class="tmk-hub-bottom">{bottom_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _apply_product_hub_styles() -> None:
    st.markdown(
        """
        <style>
            .tmk-hub-visual {
                background: linear-gradient(180deg, #232A54 0%, #22284E 100%);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 24px;
                padding: 1.1rem 1rem 1rem 1rem;
                margin-bottom: 1rem;
                color: #FFFFFF;
                box-shadow: 0 10px 26px rgba(34, 40, 78, 0.18);
                min-height: 360px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }

            .tmk-hub-top,
            .tmk-hub-bottom {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-wrap: wrap;
                gap: 0.5rem;
                margin-top: 0.4rem;
                margin-bottom: 0.4rem;
            }

            .tmk-hub-chip {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-width: 64px;
                padding: 0.48rem 0.78rem;
                border-radius: 12px;
                background: rgba(255,255,255,0.96);
                color: #232A54;
                font-weight: 800;
                font-size: 0.92rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.12);
            }

            .tmk-hub-arrows {
                display: flex;
                justify-content: center;
                gap: 0.7rem;
                margin: 0.45rem 0 0.2rem 0;
                color: rgba(255,255,255,0.92);
                font-size: 1.15rem;
                letter-spacing: 0.12em;
            }

            .tmk-hub-center-wrap {
                display: flex;
                justify-content: center;
                margin: 0.25rem 0 0.35rem 0;
            }

            .tmk-hub-center {
                width: 132px;
                height: 132px;
                border-radius: 999px;
                border: 6px solid rgba(255,255,255,0.92);
                background: linear-gradient(180deg, #7390B0 0%, #6B87A6 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: #FFFFFF;
                font-size: 2.1rem;
                font-weight: 800;
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.12);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_product_page(view_model: ViewModel) -> None:
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

    _apply_product_hub_styles()

    page_header(title, subtitle)
    _render_product_identity(product_meta)
    _render_hub_visual(
        product_label=product_meta["product"],
        entry_routes=entry_routes,
        exit_routes=exit_routes,
    )

    if compare_meta is not None:
        _render_compare_bar(compare_meta)
