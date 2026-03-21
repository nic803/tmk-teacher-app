from __future__ import annotations

from html import escape
from math import cos, pi, sin
from typing import Iterable

import streamlit as st
import streamlit.components.v1 as components

from products import (
    ALL_PRODUCTS,
    STAGE_ORDER,
    STAGES,
    product_record,
    stage_color,
    stage_label,
    visible_products,
)
from worksheet_engine import generate_worksheet

try:
    from patterns import get_pattern, product_pattern_ids
except Exception:
    get_pattern = None
    product_pattern_ids = None


APP_TITLE = "TMK Teacher App"
SURFACES = ("Structural Planner", "Product Lab", "Worksheet Studio")
TIERS = ("Support", "Core", "Extension")
PLANNER_LINK_MODES = ("Selected links", "All links", "No links")
PLANNER_ZOOM_MODES = ("Whole world", "Selected stage lane only")
ROUTE_VIEW_MODES = ("Entry routes", "Exit routes")


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="✳️",
    layout="wide",
)


def main() -> None:
    _ensure_state()
    _sync_surface_from_query_params()
    _apply_styles()

    st.markdown('<div class="tmk-shell">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="tmk-header">
            <div>
                <div class="tmk-kicker">Teacher App</div>
                <h1>TMK Teacher App</h1>
                <p>Structural planner first. Product hubs visible. Worksheets kept in their own studio.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _render_nav()
    _render_sidebar()

    surface = st.session_state.surface
    product = st.session_state.selected_product
    tier = st.session_state.selected_tier

    if surface == "Structural Planner":
        _render_structural_planner(product)
    elif surface == "Product Lab":
        _render_product_lab(product)
    else:
        _render_worksheet_studio(product, tier)

    st.markdown("</div>", unsafe_allow_html=True)


def _ensure_state() -> None:
    if "surface" not in st.session_state:
        st.session_state.surface = "Structural Planner"

    if "selected_product" not in st.session_state:
        st.session_state.selected_product = 36 if 36 in ALL_PRODUCTS else ALL_PRODUCTS[0]

    if "selected_tier" not in st.session_state:
        st.session_state.selected_tier = "Core"

    if "compare_product" not in st.session_state:
        default_compare = 24 if 24 in ALL_PRODUCTS else ALL_PRODUCTS[0]
        if default_compare == st.session_state.selected_product and len(ALL_PRODUCTS) > 1:
            default_compare = ALL_PRODUCTS[1]
        st.session_state.compare_product = default_compare

    if "planner_link_mode" not in st.session_state:
        st.session_state.planner_link_mode = "Selected links"

    if "planner_zoom_mode" not in st.session_state:
        st.session_state.planner_zoom_mode = "Whole world"

    if "route_view_mode" not in st.session_state:
        st.session_state.route_view_mode = "Entry routes"

    if "selected_route_index" not in st.session_state:
        st.session_state.selected_route_index = 0


def _sync_surface_from_query_params() -> None:
    params = st.query_params
    requested_surface = params.get("surface")

    if isinstance(requested_surface, list):
        requested_surface = requested_surface[0] if requested_surface else None

    if requested_surface in SURFACES and requested_surface != st.session_state.surface:
        st.session_state.surface = requested_surface


def _set_surface(surface: str) -> None:
    if surface in SURFACES:
        st.session_state.surface = surface
        st.query_params["surface"] = surface


def _apply_styles() -> None:
    st.markdown(
        """
        <style>
            :root {
                --tmk-bg: #f5f3ef;
                --tmk-surface: rgba(255, 255, 255, 0.74);
                --tmk-surface-strong: #fffaf2;
                --tmk-border: #eadfd0;
                --tmk-text: #1f2a44;
                --tmk-text-soft: #59667f;
                --tmk-accent: #c8ab7a;
                --tmk-accent-soft: #f2e3c8;
                --tmk-pill: #f3ede4;
                --tmk-pill-border: #e4d6c2;
                --tmk-dark-card: #08172f;
                --tmk-dark-border: #243b5e;
                --tmk-dark-text: #eef4ff;
                --tmk-dark-muted: #c4d2e6;
            }

            @media (prefers-color-scheme: dark) {
                :root {
                    --tmk-bg: #10161f;
                    --tmk-surface: rgba(25, 34, 47, 0.88);
                    --tmk-surface-strong: #172130;
                    --tmk-border: #2d4058;
                    --tmk-text: #eef4ff;
                    --tmk-text-soft: #c4d2e6;
                    --tmk-accent: #d8b77b;
                    --tmk-accent-soft: #3a2f1f;
                    --tmk-pill: #1b2738;
                    --tmk-pill-border: #334860;
                    --tmk-dark-card: #08172f;
                    --tmk-dark-border: #36527b;
                    --tmk-dark-text: #eef4ff;
                    --tmk-dark-muted: #c4d2e6;
                }
            }

            .stApp {
                background: var(--tmk-bg);
                color: var(--tmk-text);
            }

            .block-container {
                padding-top: 1rem;
                padding-bottom: 2rem;
            }

            .tmk-shell {
                max-width: 1240px;
                margin: 0 auto;
                padding-bottom: 2rem;
            }

            .tmk-header {
                background: linear-gradient(180deg, var(--tmk-surface-strong) 0%, var(--tmk-surface) 100%);
                border: 1px solid var(--tmk-border);
                border-radius: 24px;
                padding: 1.35rem 1.4rem 1.1rem 1.4rem;
                box-shadow: 0 8px 24px rgba(34, 46, 75, 0.06);
                margin-bottom: 1rem;
            }

            .tmk-kicker {
                font-size: 0.78rem;
                font-weight: 800;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                color: var(--tmk-accent);
                margin-bottom: 0.25rem;
            }

            .tmk-header h1 {
                margin: 0;
                font-size: 2rem;
                line-height: 1.08;
                color: var(--tmk-text);
            }

            .tmk-header p {
                margin: 0.45rem 0 0 0;
                color: var(--tmk-text-soft);
                font-size: 1rem;
                line-height: 1.45;
            }

            .tmk-nav-strip {
                display: flex;
                gap: 0.6rem;
                flex-wrap: wrap;
                margin-bottom: 1rem;
            }

            .tmk-nav-link {
                display: inline-flex;
                align-items: center;
                padding: 0.6rem 0.95rem;
                border-radius: 999px;
                border: 1px solid var(--tmk-accent);
                background: var(--tmk-surface-strong);
                color: var(--tmk-text);
                font-weight: 800;
                font-size: 0.95rem;
                text-decoration: none;
            }

            .tmk-nav-link:hover {
                border-color: var(--tmk-accent);
                color: var(--tmk-text);
            }

            .tmk-nav-link-active {
                background: var(--tmk-accent-soft);
            }

            .tmk-panel {
                background: var(--tmk-surface);
                border: 1px solid var(--tmk-border);
                border-radius: 24px;
                padding: 1rem;
                box-shadow: 0 10px 30px rgba(34, 46, 75, 0.05);
                margin-bottom: 1rem;
            }

            .tmk-section-title {
                font-size: 2rem;
                line-height: 1.1;
                font-weight: 800;
                color: var(--tmk-text);
                margin-bottom: 0.2rem;
            }

            .tmk-section-subtitle {
                color: var(--tmk-text-soft);
                margin-bottom: 0.8rem;
                font-size: 1rem;
                line-height: 1.45;
            }

            .tmk-card {
                background: linear-gradient(180deg, var(--tmk-surface-strong) 0%, var(--tmk-surface) 100%);
                border: 1px solid var(--tmk-border);
                border-radius: 18px;
                padding: 0.95rem 1rem;
                height: 100%;
                margin-bottom: 0.75rem;
            }

            .tmk-card-dark {
                background: var(--tmk-dark-card);
                border: 1px solid var(--tmk-dark-border);
                border-radius: 24px;
                padding: 0.75rem;
                height: 100%;
                margin-bottom: 0.75rem;
            }

            .tmk-small-label {
                font-size: 0.74rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: var(--tmk-text-soft);
                margin-bottom: 0.3rem;
            }

            .tmk-value {
                font-size: 1.35rem;
                font-weight: 800;
                color: var(--tmk-text);
                line-height: 1.2;
                word-break: break-word;
            }

            .tmk-soft-list {
                display: flex;
                flex-wrap: wrap;
                gap: 0.45rem;
                margin-top: 0.5rem;
            }

            .tmk-pill {
                display: inline-flex;
                align-items: center;
                padding: 0.46rem 0.72rem;
                border-radius: 999px;
                background: var(--tmk-pill);
                border: 1px solid var(--tmk-pill-border);
                color: var(--tmk-text);
                font-size: 0.95rem;
                font-weight: 700;
                line-height: 1.2;
            }

            .tmk-pill-accent {
                background: var(--tmk-accent-soft);
                border-color: var(--tmk-accent);
            }

            .tmk-note {
                color: var(--tmk-text-soft);
                font-size: 0.98rem;
                line-height: 1.55;
            }

            .tmk-subhead {
                font-size: 1.18rem;
                font-weight: 800;
                color: var(--tmk-text);
                margin-bottom: 0.5rem;
            }

            .tmk-stage-card {
                border-radius: 20px;
                border: 1px solid var(--tmk-border);
                padding: 0.9rem;
                margin-bottom: 0.8rem;
                background: var(--tmk-surface);
            }

            .tmk-stage-title {
                font-size: 1.05rem;
                font-weight: 800;
                color: var(--tmk-text);
                margin-bottom: 0.55rem;
            }

            .tmk-map-wrap {
                overflow-x: auto;
                overflow-y: hidden;
                -webkit-overflow-scrolling: touch;
                border-radius: 20px;
                margin-top: 0.8rem;
            }

            .tmk-legend-box {
                background: var(--tmk-surface-strong);
                border: 1px solid var(--tmk-border);
                border-radius: 16px;
                padding: 0.8rem 0.95rem;
                margin-top: 0.8rem;
            }

            .tmk-legend-row {
                display: flex;
                flex-wrap: wrap;
                gap: 0.9rem;
                align-items: center;
            }

            .tmk-legend-item {
                display: inline-flex;
                align-items: center;
                gap: 0.45rem;
                color: var(--tmk-text-soft);
                font-size: 0.94rem;
                font-weight: 700;
            }

            .tmk-line-swatch {
                width: 36px;
                height: 0;
                border-top: 4px solid #ff9f43;
                position: relative;
            }

            .tmk-line-swatch-purple {
                width: 36px;
                height: 0;
                border-top: 2px dashed #7c3aed;
                position: relative;
            }

            .tmk-line-swatch-grey {
                width: 36px;
                height: 0;
                border-top: 3px solid rgba(125, 139, 162, 0.95);
                position: relative;
            }

            .tmk-worksheet-frame {
                background: linear-gradient(180deg, var(--tmk-surface-strong) 0%, var(--tmk-surface) 100%);
                border: 1px solid var(--tmk-border);
                border-radius: 22px;
                padding: 1rem;
                margin-bottom: 0.9rem;
            }

            .tmk-answer-box {
                background: rgba(255,255,255,0.08);
                border: 1px solid var(--tmk-border);
                border-radius: 16px;
                padding: 0.9rem 0.95rem;
                margin-bottom: 0.7rem;
                color: var(--tmk-text);
            }

            .tmk-control-caption {
                font-size: 0.92rem;
                color: var(--tmk-text-soft);
                line-height: 1.45;
                margin-top: 0.25rem;
            }

            .tmk-route-button-row {
                display: flex;
                flex-wrap: wrap;
                gap: 0.55rem;
                margin-top: 0.75rem;
            }

            .tmk-mobile-note {
                color: var(--tmk-text-soft);
                font-size: 0.9rem;
                margin-top: 0.25rem;
            }

            .stButton > button {
                border-radius: 999px;
                border: 1px solid var(--tmk-border);
                background: var(--tmk-surface-strong);
                color: var(--tmk-text);
                font-weight: 800;
                min-height: 2.9rem;
                box-shadow: none;
                font-size: 0.98rem;
                line-height: 1.2;
                white-space: normal;
            }

            .stButton > button:hover {
                border-color: var(--tmk-accent);
                color: var(--tmk-text);
            }

            [data-testid="stSidebar"] {
                background: var(--tmk-surface-strong);
                border-left: 1px solid var(--tmk-border);
            }

            [data-testid="stSidebar"] * {
                color: var(--tmk-text);
            }

            .stSelectbox label,
            .stRadio label,
            .stCheckbox label,
            .stMarkdown,
            .stCaption,
            .stText {
                color: var(--tmk-text);
            }

            @media (max-width: 900px) {
                .tmk-shell {
                    max-width: 100%;
                }

                .tmk-header {
                    border-radius: 18px;
                    padding: 1rem 0.95rem 0.9rem 0.95rem;
                }

                .tmk-header h1 {
                    font-size: 1.6rem;
                }

                .tmk-panel {
                    border-radius: 18px;
                    padding: 0.85rem;
                }

                .tmk-section-title {
                    font-size: 1.55rem;
                }

                .tmk-value {
                    font-size: 1.18rem;
                }
            }

            @media (max-width: 640px) {
                .block-container {
                    padding-left: 0.65rem;
                    padding-right: 0.65rem;
                }

                .tmk-header {
                    padding: 0.9rem 0.85rem 0.85rem 0.85rem;
                    margin-bottom: 0.8rem;
                }

                .tmk-kicker {
                    font-size: 0.68rem;
                }

                .tmk-header h1 {
                    font-size: 1.36rem;
                }

                .tmk-header p {
                    font-size: 0.93rem;
                    line-height: 1.45;
                }

                .tmk-panel {
                    padding: 0.75rem;
                    border-radius: 16px;
                }

                .tmk-section-title {
                    font-size: 1.3rem;
                }

                .tmk-section-subtitle,
                .tmk-note,
                .tmk-control-caption,
                .tmk-mobile-note {
                    font-size: 0.92rem;
                    line-height: 1.5;
                }

                .tmk-subhead {
                    font-size: 1.02rem;
                }

                .tmk-small-label {
                    font-size: 0.66rem;
                }

                .tmk-value {
                    font-size: 1.06rem;
                    line-height: 1.25;
                }

                .tmk-pill {
                    font-size: 0.88rem;
                    padding: 0.38rem 0.58rem;
                }

                .stButton > button {
                    min-height: 2.8rem;
                    font-size: 0.94rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_nav() -> None:
    links: list[str] = []
    for surface in SURFACES:
        active_class = " tmk-nav-link-active" if surface == st.session_state.surface else ""
        href = f"?surface={surface.replace(' ', '%20')}"
        links.append(f'<a class="tmk-nav-link{active_class}" href="{href}">{escape(surface)}</a>')

    st.markdown(f'<div class="tmk-nav-strip">{"".join(links)}</div>', unsafe_allow_html=True)


def _on_planner_product_change() -> None:
    st.session_state.selected_product = st.session_state.planner_product_select_v4
    st.rerun()


def _on_planner_link_mode_change() -> None:
    st.session_state.planner_link_mode = st.session_state.planner_link_mode_select_v4


def _on_planner_zoom_mode_change() -> None:
    st.session_state.planner_zoom_mode = st.session_state.planner_zoom_mode_select_v4


def _on_lab_product_change() -> None:
    st.session_state.selected_product = st.session_state.lab_product_select_v4
    if st.session_state.compare_product == st.session_state.selected_product and len(ALL_PRODUCTS) > 1:
        st.session_state.compare_product = next(
            product for product in ALL_PRODUCTS if product != st.session_state.selected_product
        )
    st.session_state.selected_route_index = 0
    st.rerun()


def _on_lab_compare_change() -> None:
    st.session_state.compare_product = st.session_state.lab_compare_select_v4


def _on_lab_route_view_mode_change() -> None:
    st.session_state.route_view_mode = st.session_state.lab_route_view_mode_v4
    st.session_state.selected_route_index = 0


def _on_worksheet_product_change() -> None:
    st.session_state.selected_product = st.session_state.worksheet_product_select_v4
    st.rerun()


def _on_worksheet_tier_change() -> None:
    st.session_state.selected_tier = st.session_state.worksheet_tier_radio_v4


def _render_sidebar() -> None:
    record = product_record(st.session_state.selected_product)

    with st.sidebar:
        st.markdown("## Current selection")
        st.write(f"**Product:** {record.product}")
        st.write(f"**Stage:** {stage_label(record.stage)}")
        st.write(f"**Intro route:** {_format_route(record.intro_route)}")

        st.markdown("---")
        st.markdown("### Current surface")

        if st.session_state.surface == "Structural Planner":
            st.write(f"**Link mode:** {st.session_state.planner_link_mode}")
            st.write(f"**Zoom:** {st.session_state.planner_zoom_mode}")

        elif st.session_state.surface == "Product Lab":
            compare = product_record(st.session_state.compare_product)
            st.write(f"**Compare with:** {compare.product}")
            st.write(f"**Route view:** {st.session_state.route_view_mode}")

        else:
            st.write(f"**Tier:** {st.session_state.selected_tier}")

        st.markdown("---")
        st.markdown("### Hub summary")
        st.write(f"**Routes:** {len(record.factor_families)}")
        st.write(f"**Role:** {record.structural_role}")


def _render_structural_planner(product: int) -> None:
    record = product_record(product)
    focus_stage_only = st.session_state.planner_zoom_mode == "Selected stage lane only"
    _, map_height = _world_map_dimensions(focus_stage_only, record.stage)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Structural Planner</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">See how the selected product is linked to the world through its intro route.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Planner controls")
    control_col1, control_col2, control_col3 = st.columns(3)

    with control_col1:
        st.selectbox(
            "Selected product",
            options=ALL_PRODUCTS,
            index=ALL_PRODUCTS.index(st.session_state.selected_product),
            format_func=_product_option_label,
            key="planner_product_select_v4",
            on_change=_on_planner_product_change,
        )

    with control_col2:
        st.selectbox(
            "Link mode",
            options=PLANNER_LINK_MODES,
            index=PLANNER_LINK_MODES.index(st.session_state.planner_link_mode),
            key="planner_link_mode_select_v4",
            on_change=_on_planner_link_mode_change,
        )

    with control_col3:
        st.selectbox(
            "Planner zoom",
            options=PLANNER_ZOOM_MODES,
            index=PLANNER_ZOOM_MODES.index(st.session_state.planner_zoom_mode),
            key="planner_zoom_mode_select_v4",
            on_change=_on_planner_zoom_mode_change,
        )

    st.markdown(
        """
        <div class="tmk-control-caption">
            Selected links shows only the selected product’s intro route.
            All links shows the wider world network in grey behind the highlighted route.
            No links shows stage layout only.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    explainer_left, explainer_right = st.columns(2)

    with explainer_left:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-subhead">What is happening</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="tmk-note">
                <strong>{record.product}</strong> is selected.<br>
                It belongs to <strong>{stage_label(record.stage)}</strong>.<br>
                Its intro route is <strong>{_format_route(record.intro_route)}</strong>.<br>
                The planner highlights links from <strong>{record.intro_route[0]}</strong> and <strong>{record.intro_route[1]}</strong> into <strong>{record.product}</strong>.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with explainer_right:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-subhead">Selected route reading</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="tmk-note">
                <strong>{record.intro_route[0]}</strong> × <strong>{record.intro_route[1]}</strong> = <strong>{record.product}</strong><br>
                So the selected product is read through the intro route <strong>{_format_route(record.intro_route)}</strong>.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    _render_stage_cards(product)

    st.markdown('<div class="tmk-map-wrap">', unsafe_allow_html=True)
    components.html(
        _world_map_html(
            selected_product=product,
            link_mode=st.session_state.planner_link_mode,
            focus_stage_only=focus_stage_only,
        ),
        height=map_height + 36,
        scrolling=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="tmk-legend-box">
            <div class="tmk-legend-row">
                <div class="tmk-legend-item"><span class="tmk-line-swatch"></span> selected intro link</div>
                <div class="tmk-legend-item"><span class="tmk-line-swatch-purple"></span> selected intro link overlay</div>
                <div class="tmk-legend-item"><span class="tmk-line-swatch-grey"></span> wider world links</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Visible products</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tmk-section-subtitle">{stage_label(record.stage)} unlocks {len(visible_products(record.stage))} visible products.</div>',
        unsafe_allow_html=True,
    )
    _render_visible_products_grid(product)
    st.markdown("</div>", unsafe_allow_html=True)


def _render_stage_cards(selected_product: int) -> None:
    for stage in [stage for stage in STAGE_ORDER if stage in STAGES]:
        stage_record = STAGES[stage]
        products = stage_record.products

        pills: list[str] = []
        for product in products:
            pill_class = "tmk-pill tmk-pill-accent" if product == selected_product else "tmk-pill"
            pills.append(f'<span class="{pill_class}">{product}</span>')

        st.markdown(
            f"""
            <div class="tmk-stage-card" style="background:{_hex_to_rgba(stage_record.color, 0.10)}; border-color:{_hex_to_rgba(stage_record.color, 0.28)};">
                <div class="tmk-stage-title">{escape(stage_record.label)}</div>
                <div class="tmk-soft-list">{''.join(pills)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_product_lab(product: int) -> None:
    record = product_record(product)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Product Lab</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Hub overview, readable radial map, route lists, inverse field, pattern links, and comparisons.</div>',
        unsafe_allow_html=True,
    )

    control_col1, control_col2, control_col3 = st.columns(3)

    with control_col1:
        st.selectbox(
            "Selected product",
            options=ALL_PRODUCTS,
            index=ALL_PRODUCTS.index(st.session_state.selected_product),
            format_func=_product_option_label,
            key="lab_product_select_v4",
            on_change=_on_lab_product_change,
        )

    compare_options = [item for item in ALL_PRODUCTS if item != st.session_state.selected_product]
    if st.session_state.compare_product not in compare_options:
        st.session_state.compare_product = compare_options[0]

    with control_col2:
        st.selectbox(
            "Compare with",
            options=compare_options,
            index=compare_options.index(st.session_state.compare_product),
            format_func=_product_option_label,
            key="lab_compare_select_v4",
            on_change=_on_lab_compare_change,
        )

    with control_col3:
        st.radio(
            "Route view",
            options=ROUTE_VIEW_MODES,
            index=ROUTE_VIEW_MODES.index(st.session_state.route_view_mode),
            horizontal=True,
            key="lab_route_view_mode_v4",
            on_change=_on_lab_route_view_mode_change,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    record = product_record(st.session_state.selected_product)
    compare = product_record(st.session_state.compare_product)

    _metric_card_row(
        [
            ("Product", str(record.product)),
            ("Stage", stage_label(record.stage)),
            ("Routes", str(len(record.factor_families))),
            ("Role", record.structural_role),
        ]
    )

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Radial hub view</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="tmk-note">
            Entry routes sit above the hub. Exit routes sit below the hub. A compact mobile layout is included automatically.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="tmk-card-dark">', unsafe_allow_html=True)
    components.html(_radial_hub_html(record.product), height=660, scrolling=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="tmk-mobile-note">Mobile layout switches to stacked route cards below 720px width.</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    _render_route_inspector(record)

    radial_col1, radial_col2 = st.columns(2)

    with radial_col1:
        st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-subhead">Entry routes</div>', unsafe_allow_html=True)
        for route in _entry_routes_for_radial(record):
            st.markdown(f'<div class="tmk-note">{escape(_format_route(route))}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with radial_col2:
        st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-subhead">Exit routes</div>', unsafe_allow_html=True)
        for label in _exit_routes_for_radial(record):
            st.markdown(f'<div class="tmk-note">{escape(label)}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Hub explanation</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="tmk-note">
            The centre circle is <strong>{record.product}</strong>.<br>
            The inward routes are multiplication routes that make the product.<br>
            The outward routes are division routes that recover factors from the product.<br>
            The intro route stays fixed as <strong>{_format_route(record.intro_route)}</strong>.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Truth set</div>', unsafe_allow_html=True)
    st.markdown(_pill_cloud(record.ways_in, accent=True), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Inverse field</div>', unsafe_allow_html=True)
    st.markdown(_pill_cloud(_inverse_labels(record.product), accent=False), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Pattern links</div>', unsafe_allow_html=True)
    _render_pattern_links(record.product)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Stage relations</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="tmk-note">Current stage: {stage_label(record.stage)}</div>
        <div class="tmk-note">Visible products up to this stage: {len(visible_products(record.stage))}</div>
        <div class="tmk-note">Related products sharing factors: {len(record.related_products)}</div>
        <div class="tmk-note">Intro-route rule stays fixed: {record.product} enters through {_format_route(record.intro_route)}.</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Compare products</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="tmk-note"><strong>{record.product}</strong> · {stage_label(record.stage)} · {_format_route(record.intro_route)}</div>
        <div class="tmk-note"><strong>{compare.product}</strong> · {stage_label(compare.stage)} · {_format_route(compare.intro_route)}</div>
        <div class="tmk-note">Shared factors: {_shared_factors(record.product, compare.product)}</div>
        <div class="tmk-note">Route counts: {len(record.factor_families)} vs {len(compare.factor_families)}</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def _render_route_inspector(record) -> None:
    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Route inspector</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tmk-note">Use the route buttons to inspect the currently selected {st.session_state.route_view_mode.lower()} for {record.product}.</div>',
        unsafe_allow_html=True,
    )

    items = _route_inspector_items(record, st.session_state.route_view_mode)
    if not items:
        st.markdown('<div class="tmk-note">No routes available.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    if st.session_state.selected_route_index >= len(items):
        st.session_state.selected_route_index = 0

    button_cols = st.columns(min(len(items), 4))
    for index, item in enumerate(items):
        col = button_cols[index % len(button_cols)]
        button_type = "primary" if index == st.session_state.selected_route_index else "secondary"
        if col.button(
            item["label"],
            key=f"route_inspector_button_v4_{st.session_state.route_view_mode}_{index}",
            use_container_width=True,
            type=button_type,
        ):
            st.session_state.selected_route_index = index
            st.rerun()

    selected_item = items[st.session_state.selected_route_index]

    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="tmk-small-label">{escape(st.session_state.route_view_mode[:-1]) if st.session_state.route_view_mode.endswith("s") else escape(st.session_state.route_view_mode)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tmk-value">{escape(selected_item["headline"])}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tmk-note" style="margin-top:0.55rem;">{escape(selected_item["explanation"])}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def _route_inspector_items(record, mode: str) -> list[dict[str, str]]:
    if mode == "Entry routes":
        items: list[dict[str, str]] = []
        for a, b in _entry_routes_for_radial(record):
            items.append(
                {
                    "label": _format_route((a, b)),
                    "headline": f"{a} × {b} = {record.product}",
                    "explanation": f"This entry route makes {record.product} by combining {a} and {b}.",
                }
            )
        return items

    items = []
    for divisor, quotient in record.ways_out[:4]:
        items.append(
            {
                "label": f"{record.product}÷{divisor}={quotient}",
                "headline": f"{record.product} ÷ {divisor} = {quotient}",
                "explanation": f"This exit route recovers the factor {quotient} from {record.product} using divisor {divisor}.",
            }
        )
    return items


def _render_worksheet_studio(product: int, tier: str) -> None:
    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Worksheet Studio</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Choose product, choose Support/Core/Extension, generate worksheet, review teacher key.</div>',
        unsafe_allow_html=True,
    )

    control_col1, control_col2 = st.columns(2)

    with control_col1:
        st.selectbox(
            "Selected product",
            options=ALL_PRODUCTS,
            index=ALL_PRODUCTS.index(st.session_state.selected_product),
            format_func=_product_option_label,
            key="worksheet_product_select_v4",
            on_change=_on_worksheet_product_change,
        )

    with control_col2:
        st.radio(
            "Worksheet tier",
            options=TIERS,
            index=TIERS.index(st.session_state.selected_tier),
            horizontal=True,
            key="worksheet_tier_radio_v4",
            on_change=_on_worksheet_tier_change,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    worksheet = generate_worksheet(st.session_state.selected_product, st.session_state.selected_tier)

    _metric_card_row(
        [
            ("Product", str(worksheet.product)),
            ("Stage", str(worksheet.stage)),
            ("Tier", str(worksheet.tier)),
            ("Questions", str(len(worksheet.questions))),
        ]
    )

    st.markdown('<div class="tmk-worksheet-frame">', unsafe_allow_html=True)
    st.markdown("### Pupil worksheet")
    for index, question in enumerate(worksheet.questions, start=1):
        st.markdown(
            f"""
            <div class="tmk-answer-box">
                <div class="tmk-small-label">Q{_question_number(question, index)}</div>
                <div style="font-size:1.02rem;font-weight:700;color:inherit;line-height:1.5;">{escape(_render_question_text(question))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-worksheet-frame">', unsafe_allow_html=True)
    st.markdown("### Teacher key")
    answers = _coerce_sequence(getattr(worksheet.teacher_key, "answers", ()))
    notes = _coerce_sequence(getattr(worksheet.teacher_key, "notes", ()))

    st.markdown("#### Answers")
    for index, answer in enumerate(answers, start=1):
        st.markdown(
            f"""
            <div class="tmk-answer-box">
                <strong>Q{index}.</strong> {escape(_stringify(answer))}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### Notes")
    for note in notes:
        st.markdown(
            f"""
            <div class="tmk-answer-box">
                {escape(_stringify(note))}
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def _metric_card_row(items: list[tuple[str, str]]) -> None:
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        with col:
            _metric_card(label, value)


def _metric_card(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="tmk-card">
            <div class="tmk-small-label">{escape(label)}</div>
            <div class="tmk-value">{escape(value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_visible_products_grid(product: int) -> None:
    record = product_record(product)
    products = visible_products(record.stage)
    cols_per_row = 4

    for row_start in range(0, len(products), cols_per_row):
        cols = st.columns(cols_per_row)
        for offset, visible_product in enumerate(products[row_start : row_start + cols_per_row]):
            button_type = "primary" if visible_product == product else "secondary"
            if cols[offset].button(
                str(visible_product),
                key=f"visible_product_button_v4_{visible_product}",
                use_container_width=True,
                type=button_type,
            ):
                st.session_state.selected_product = visible_product
                st.rerun()


def _render_pattern_links(product: int) -> None:
    if product_pattern_ids is None or get_pattern is None:
        st.markdown('<div class="tmk-note">Pattern library not available in this runtime.</div>', unsafe_allow_html=True)
        return

    pattern_ids = tuple(product_pattern_ids(product))[:8]
    if not pattern_ids:
        st.markdown('<div class="tmk-note">No pattern links attached.</div>', unsafe_allow_html=True)
        return

    pills: list[str] = []
    for pattern_id in pattern_ids:
        pattern = get_pattern(pattern_id)
        pills.append(f'<span class="tmk-pill">{escape(pattern.name)}</span>')
    st.markdown(f'<div class="tmk-soft-list">{"".join(pills)}</div>', unsafe_allow_html=True)

    first = get_pattern(pattern_ids[0])
    st.markdown(
        f'<div class="tmk-note" style="margin-top:0.65rem;">{escape(first.learner_label)}</div>',
        unsafe_allow_html=True,
    )


def _world_map_dimensions(focus_stage_only: bool, selected_stage: str) -> tuple[int, int]:
    lane_x = 26
    lane_w = 1268
    lane_h = 130
    lane_gap = 28
    top = 24
    bottom_padding = 28
    visible_stages = _visible_world_stages(focus_stage_only, selected_stage)
    stage_count = len(visible_stages)
    total_height = top + stage_count * lane_h + max(stage_count - 1, 0) * lane_gap + bottom_padding
    total_width = lane_x + lane_w + 26
    return total_width, total_height


def _visible_world_stages(focus_stage_only: bool, selected_stage: str) -> list[str]:
    stages = [stage for stage in STAGE_ORDER if stage in STAGES]
    if focus_stage_only:
        return [stage for stage in stages if stage == selected_stage]
    return stages


def _world_map_html(
    selected_product: int,
    link_mode: str,
    focus_stage_only: bool,
) -> str:
    lane_x = 26
    lane_w = 1268
    lane_h = 130
    lane_gap = 28
    top = 24
    header_band_h = 42
    left_label_space = 260
    bottom_padding = 28

    selected_record = product_record(selected_product)
    stages = _visible_world_stages(focus_stage_only, selected_record.stage)
    y_positions = {stage: top + index * (lane_h + lane_gap) for index, stage in enumerate(stages)}
    positions = _world_positions(
        lane_x=lane_x,
        lane_w=lane_w,
        lane_h=lane_h,
        lane_gap=lane_gap,
        top=top,
        header_band_h=header_band_h,
        left_label_space=left_label_space,
        stages=stages,
    )
    total_width, total_height = _world_map_dimensions(focus_stage_only, selected_record.stage)

    lane_rects: list[str] = []
    lane_labels: list[str] = []
    for stage in stages:
        y = y_positions[stage]
        stage_record = STAGES[stage]
        fill = _hex_to_rgba(stage_record.color, 0.10)
        stroke = _hex_to_rgba(stage_record.color, 0.26)
        lane_rects.append(
            f'<rect x="{lane_x}" y="{y}" width="{lane_w}" height="{lane_h}" rx="24" fill="{fill}" stroke="{stroke}" stroke-width="2"></rect>'
        )
        lane_labels.append(
            f'<text x="{lane_x + 18}" y="{y + 28}" font-size="18" font-weight="800" fill="var(--tmk-text, #22304f)">{escape(stage_record.label)}</text>'
        )

    background_lines: list[str] = []
    selected_lines: list[str] = []

    if link_mode == "All links":
        for product in ALL_PRODUCTS:
            record = product_record(product)
            if record.stage not in stages:
                continue

            end = positions.get(product)
            factor_a = positions.get(record.intro_route[0])
            factor_b = positions.get(record.intro_route[1])

            if factor_a and end:
                background_lines.append(_svg_line(factor_a[0], factor_a[1], end[0], end[1], "#7d8ba2", 2.8, 0.58, ""))
            if factor_b and end:
                background_lines.append(_svg_line(factor_b[0], factor_b[1], end[0], end[1], "#7d8ba2", 2.8, 0.58, ""))

    if link_mode in ("Selected links", "All links"):
        selected_end = positions[selected_product]
        for factor in selected_record.intro_route:
            if factor in positions:
                sx, sy = positions[factor]
                ex, ey = selected_end
                selected_lines.append(_svg_line(sx, sy, ex, ey, "#ff9f43", 4.0, 0.96, "8 6"))
                selected_lines.append(_svg_line(sx, sy, ex, ey, "#7c3aed", 1.6, 0.96, "2 8"))

    nodes: list[str] = []
    for product in ALL_PRODUCTS:
        record = product_record(product)
        if record.stage not in stages:
            continue

        x, y = positions[product]
        fill = stage_color(record.stage)
        is_selected = product == selected_product
        radius = 36 if is_selected else 24
        outer_radius = radius + 6 if is_selected else radius + 3
        outer_fill = "#ff9f43" if is_selected else _hex_to_rgba(fill, 0.14)
        stroke = "#fff7ee" if is_selected else "#f8fafc"

        nodes.append(f'<circle cx="{x}" cy="{y}" r="{outer_radius}" fill="{outer_fill}" opacity="0.95"></circle>')
        nodes.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="4"></circle>')
        nodes.append(
            f'<text x="{x}" y="{y + 7}" text-anchor="middle" font-size="{22 if is_selected else 16}" font-weight="900" fill="#ffffff">{product}</text>'
        )

    svg = f"""
    <svg viewBox="0 0 {total_width} {total_height}" width="{total_width}" height="{total_height}" xmlns="http://www.w3.org/2000/svg">
        <rect x="0" y="0" width="{total_width}" height="{total_height}" fill="transparent"></rect>
        {''.join(lane_rects)}
        {''.join(background_lines)}
        {''.join(selected_lines)}
        {''.join(lane_labels)}
        {''.join(nodes)}
    </svg>
    """

    return f"""
    <div style="background:transparent;border-radius:24px;overflow:auto;max-width:100%;padding-bottom:{bottom_padding}px;">
        {svg}
    </div>
    """


def _world_positions(
    lane_x: int,
    lane_w: int,
    lane_h: int,
    lane_gap: int,
    top: int,
    header_band_h: int,
    left_label_space: int,
    stages: list[str],
) -> dict[int, tuple[float, float]]:
    positions: dict[int, tuple[float, float]] = {}
    usable_x = lane_w - left_label_space - 76

    for row_index, stage in enumerate(stages):
        products = STAGES[stage].products
        row_top = top + row_index * (lane_h + lane_gap)
        y = row_top + header_band_h + (lane_h - header_band_h) / 2 + 10

        if len(products) == 1:
            positions[products[0]] = (lane_x + left_label_space + usable_x / 2, y)
            continue

        step = usable_x / (len(products) - 1)
        start_x = lane_x + left_label_space
        for index, product in enumerate(products):
            x = start_x + index * step
            positions[product] = (x, y)

    return positions


def _radial_hub_html(product: int) -> str:
    record = product_record(product)
    desktop_svg = _desktop_radial_svg(record)
    mobile_svg = _mobile_radial_svg(record)

    return f"""
    <html>
    <head>
        <style>
            :root {{
                color-scheme: light dark;
            }}

            body {{
                margin: 0;
                padding: 0;
                background: transparent;
                color: #eef4ff;
                font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }}

            .tmk-radial-shell {{
                width: 100%;
            }}

            .tmk-radial-desktop {{
                display: block;
            }}

            .tmk-radial-mobile {{
                display: none;
            }}

            svg {{
                width: 100%;
                height: auto;
                display: block;
            }}

            @media (max-width: 720px) {{
                .tmk-radial-desktop {{
                    display: none;
                }}

                .tmk-radial-mobile {{
                    display: block;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="tmk-radial-shell">
            <div class="tmk-radial-desktop">{desktop_svg}</div>
            <div class="tmk-radial-mobile">{mobile_svg}</div>
        </div>
    </body>
    </html>
    """


def _desktop_radial_svg(record) -> str:
    product = record.product
    cx = 420
    cy = 270
    radius = 86

    entry_routes = _entry_routes_for_radial(record)[:4]
    exit_routes = _exit_routes_for_radial(record)[:4]

    entry_angles = [225, 255, 285, 315][: len(entry_routes)]
    exit_angles = [140, 110, 70, 40][: len(exit_routes)]

    entry_points = [_point_on_circle(cx, cy, 210, angle) for angle in entry_angles]
    exit_points = [_point_on_circle(cx, cy, 220, angle) for angle in exit_angles]

    lines: list[str] = []
    boxes: list[str] = []

    for route, (bx, by) in zip(entry_routes, entry_points):
        ex, ey = _edge_point_toward(cx, cy, bx, by, radius + 14)
        lines.append(_svg_arrow(bx, by + 24, ex, ey, "#dbe4f4", 4))
        boxes.append(_svg_info_box(bx - 64, by, 128, 42, _format_route(route), "#163154", "#dbe4f4", "#ffffff", 18))

    for label, (bx, by) in zip(exit_routes, exit_points):
        sx, sy = _edge_point_toward(cx, cy, bx, by, radius + 14)
        lines.append(_svg_arrow(sx, sy, bx, by + 20, "#9c7cff", 4))
        boxes.append(_svg_info_box(bx - 72, by, 144, 42, label, "#2f1a59", "#d9c4ff", "#ffffff", 18))

    return f"""
    <svg viewBox="0 0 840 560" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <marker id="arrow-end-light" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#dbe4f4"></path>
            </marker>
            <marker id="arrow-end-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#9c7cff"></path>
            </marker>
        </defs>
        <rect x="0" y="0" width="840" height="560" rx="28" fill="#071426"></rect>
        <text x="18" y="28" font-size="18" font-weight="800" fill="#ffffff">Radial Hub View</text>
        <text x="18" y="52" font-size="15" font-weight="500" fill="#d4def1">Entry routes above. Exit routes below. Arrowheads kept clear of the hub.</text>
        <text x="{cx}" y="98" text-anchor="middle" font-size="24" font-weight="800" fill="#ffffff">Entry routes</text>
        <text x="{cx}" y="468" text-anchor="middle" font-size="24" font-weight="800" fill="#ffffff">Exit routes</text>
        {''.join(lines)}
        <circle cx="{cx}" cy="{cy}" r="{radius}" fill="#9ba4b5" stroke="#f5f7fb" stroke-width="5"></circle>
        <text x="{cx}" y="{cy + 14}" text-anchor="middle" font-size="48" font-weight="900" fill="#ffffff">{product}</text>
        {''.join(boxes)}
    </svg>
    """.replace('marker-end="LIGHT"', 'marker-end="url(#arrow-end-light)"').replace(
        'marker-end="PURPLE"', 'marker-end="url(#arrow-end-purple)"'
    )


def _mobile_radial_svg(record) -> str:
    product = record.product
    entry_routes = _entry_routes_for_radial(record)[:4]
    exit_routes = _exit_routes_for_radial(record)[:4]

    entry_cards = []
    exit_cards = []

    entry_y = 90
    for route in entry_routes:
        entry_cards.append(_svg_info_box(40, entry_y, 280, 44, _format_route(route), "#163154", "#dbe4f4", "#ffffff", 18))
        entry_y += 58

    exit_y = 380
    for label in exit_routes:
        exit_cards.append(_svg_info_box(40, exit_y, 280, 44, label, "#2f1a59", "#d9c4ff", "#ffffff", 18))
        exit_y += 58

    return f"""
    <svg viewBox="0 0 360 660" xmlns="http://www.w3.org/2000/svg">
        <rect x="0" y="0" width="360" height="660" rx="28" fill="#071426"></rect>
        <text x="20" y="30" font-size="18" font-weight="800" fill="#ffffff">Radial Hub View</text>
        <text x="20" y="58" font-size="15" font-weight="500" fill="#d4def1">Mobile stacked view</text>
        <text x="40" y="82" font-size="18" font-weight="800" fill="#ffffff">Entry routes</text>
        {''.join(entry_cards)}
        <circle cx="180" cy="322" r="62" fill="#9ba4b5" stroke="#f5f7fb" stroke-width="5"></circle>
        <text x="180" y="336" text-anchor="middle" font-size="38" font-weight="900" fill="#ffffff">{product}</text>
        <text x="40" y="368" font-size="18" font-weight="800" fill="#ffffff">Exit routes</text>
        {''.join(exit_cards)}
    </svg>
    """


def _point_on_circle(cx: float, cy: float, radius: float, angle_degrees: float) -> tuple[float, float]:
    angle_radians = angle_degrees * pi / 180
    return cx + radius * cos(angle_radians), cy + radius * sin(angle_radians)


def _entry_routes_for_radial(record) -> list[tuple[int, int]]:
    routes: list[tuple[int, int]] = []
    intro = record.intro_route
    routes.append(intro)
    if intro[0] != intro[1]:
        routes.append((intro[1], intro[0]))
    for route in record.factor_families:
        if route not in routes:
            routes.append(route)
        reversed_route = (route[1], route[0])
        if reversed_route not in routes and reversed_route != route:
            routes.append(reversed_route)
        if len(routes) >= 4:
            break
    return routes[:4]


def _exit_routes_for_radial(record) -> list[str]:
    labels: list[str] = []
    for divisor, quotient in record.ways_out:
        labels.append(f"{record.product}÷{divisor}={quotient}")
        if len(labels) == 4:
            break
    return labels


def _shared_factors(product_a: int, product_b: int) -> str:
    factors_a = {n for route in product_record(product_a).ways_in for n in route}
    factors_b = {n for route in product_record(product_b).ways_in for n in route}
    shared = sorted(factors_a.intersection(factors_b))
    return ", ".join(str(n) for n in shared) if shared else "none"


def _inverse_labels(product: int) -> tuple[str, ...]:
    record = product_record(product)
    return tuple(f"{product}÷{a}={b}" for a, b in record.ways_out)


def _pill_cloud(items: Iterable[object], accent: bool) -> str:
    pills: list[str] = []
    cls = "tmk-pill tmk-pill-accent" if accent else "tmk-pill"
    for item in items:
        pills.append(f'<span class="{cls}">{escape(_stringify(item))}</span>')
    return f'<div class="tmk-soft-list">{"".join(pills)}</div>'


def _svg_line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color: str,
    width: float,
    opacity: float,
    dash: str,
) -> str:
    dash_attr = f'stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="{width}" opacity="{opacity}" stroke-linecap="round" {dash_attr}></line>'
    )


def _svg_arrow(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color: str,
    width: float,
) -> str:
    marker = "LIGHT" if color == "#dbe4f4" else "PURPLE"
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="{width}" stroke-linecap="round" marker-end="{marker}"></line>'
    )


def _svg_info_box(
    x: float,
    y: float,
    w: float,
    h: float,
    text: str,
    fill: str,
    stroke: str,
    text_fill: str,
    font_size: int,
) -> str:
    return f"""
        <g>
            <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"></rect>
            <text x="{x + w / 2}" y="{y + h / 2 + 6}" text-anchor="middle" font-size="{font_size}" font-weight="800" fill="{text_fill}">{escape(text)}</text>
        </g>
    """


def _edge_point_toward(cx: float, cy: float, tx: float, ty: float, radius: float) -> tuple[float, float]:
    dx = tx - cx
    dy = ty - cy
    length = (dx * dx + dy * dy) ** 0.5
    if length == 0:
        return cx, cy
    scale = radius / length
    return cx + dx * scale, cy + dy * scale


def _hex_to_rgba(hex_color: str, alpha: float) -> str:
    hex_value = hex_color.lstrip("#")
    red = int(hex_value[0:2], 16)
    green = int(hex_value[2:4], 16)
    blue = int(hex_value[4:6], 16)
    return f"rgba({red}, {green}, {blue}, {alpha})"


def _product_option_label(product: int) -> str:
    record = product_record(product)
    return f"{product} · {record.stage} · {_format_route(record.intro_route)}"


def _question_number(question, fallback: int) -> int:
    value = getattr(question, "id", None)
    return value if isinstance(value, int) else fallback


def _render_question_text(question) -> str:
    for field_name in ("pupil_prompt", "prompt", "display_text", "text", "question_text", "body"):
        value = getattr(question, field_name, None)
        if value not in (None, ""):
            return _stringify(value)
    return _stringify(question)


def _coerce_sequence(value) -> tuple:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    if isinstance(value, str):
        return (value,)
    return tuple(value) if isinstance(value, Iterable) else (value,)


def _format_route(route: tuple[int, int]) -> str:
    return f"{route[0]}×{route[1]}"


def _stringify(value) -> str:
    if isinstance(value, tuple) and len(value) == 2:
        return _format_route(value)
    return str(value)


if __name__ == "__main__":
    main()
