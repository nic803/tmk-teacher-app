from __future__ import annotations

# ✅ FIX: ensure Streamlit can find local modules
import sys
import os
sys.path.append(os.path.dirname(__file__))

from html import escape
from math import cos, pi, sin
from typing import Iterable

import streamlit as st
import streamlit.components.v1 as components

# ✅ domain imports (this part was fine)
from domain.routes import (
    distinct_factor_routes,
    entry_routes,
    exit_route_labels,
    inverse_labels,
    shared_factors,
)

# ✅ products import (correct)
from products import (
    ALL_PRODUCTS,
    STAGE_ORDER,
    STAGES,
    product_record,
    stage_label,
    visible_products,
)

# ✅ FIX: correct module name
from services.worksheet_service import generate_worksheet


# ✅ safe optional import (leave as-is)
try:
    from patterns import get_pattern, product_pattern_ids
except Exception:
    get_pattern = None
    product_pattern_ids = None


APP_TITLE = "TMK Teacher App"
SURFACES = ("Structural Planner", "Product Lab", "Worksheet Studio")
TIERS = ("Support", "Core", "Extension")
PLANNER_LINK_MODES = ("Selected links", "Show selected atlas", "No links")
PLANNER_ZOOM_MODES = ("Selected stage only", "Whole world")
ROUTE_VIEW_MODES = ("Entry routes", "Exit routes")

LIGHT_THEME = {
    "bg": "#FAF7F2",
    "surface": "#FFFFFF",
    "surface_strong": "#F3ECE3",
    "border": "#DED3C5",
    "text": "#1F2937",
    "text_soft": "#667085",
    "accent": "#C76412",
    "accent_soft": "#E89A3A",
    "map_link_selected": "#C76412",
    "map_link_atlas": "rgba(199, 100, 18, 0.30)",
    "map_node_outline": "#E3D6C6",
    "map_node_selected": "#C76412",
}

DARK_THEME = {
    "bg": "#10151C",
    "surface": "#18212B",
    "surface_strong": "#121922",
    "border": "#2D3948",
    "text": "#F3F6FB",
    "text_soft": "#B7C2D0",
    "accent": "#E89A3A",
    "accent_soft": "#C76412",
    "map_link_selected": "#E89A3A",
    "map_link_atlas": "rgba(232, 154, 58, 0.28)",
    "map_node_outline": "#364454",
    "map_node_selected": "#E89A3A",
}

STAGE_BACKGROUND_SEQUENCE = (
    "#FCF1E7",
    "#EEF3F7",
    "#EDF5F4",
    "#F2EEF5",
    "#EEF3F7",
    "#EDF5F4",
    "#F2EEF5",
    "#FCF1E7",
)

STAGE_BORDER_SEQUENCE = (
    "#F4D4B4",
    "#D5E0EA",
    "#D2E4E1",
    "#DDD3E5",
    "#D5E0EA",
    "#D2E4E1",
    "#DDD3E5",
    "#F4D4B4",
)

STAGE_NODE_SEQUENCE = (
    "#C76412",
    "#4F6D8A",
    "#3F7C85",
    "#6C5B7B",
    "#4F6D8A",
    "#3F7C85",
    "#6C5B7B",
    "#C76412",
)

MAP_NODE_OFFSETS: dict[int, tuple[float, float]] = {
    25: (-30.0, -12.0),
    35: (24.0, -14.0),
}


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

    if st.session_state.surface == "Structural Planner":
        _render_structural_planner(st.session_state.selected_product)
    elif st.session_state.surface == "Product Lab":
        _render_product_lab(st.session_state.selected_product)
    else:
        _render_worksheet_studio(st.session_state.selected_product, st.session_state.selected_tier)

    st.markdown("</div>", unsafe_allow_html=True)


def _ensure_state() -> None:
    if "surface" not in st.session_state:
        st.session_state.surface = "Structural Planner"

    if "selected_product" not in st.session_state:
        st.session_state.selected_product = 36 if 36 in ALL_PRODUCTS else ALL_PRODUCTS[0]

    if "selected_tier" not in st.session_state:
        st.session_state.selected_tier = "Core"

    if "compare_product" not in st.session_state:
        fallback = 24 if 24 in ALL_PRODUCTS else ALL_PRODUCTS[0]
        if fallback == st.session_state.selected_product and len(ALL_PRODUCTS) > 1:
            fallback = ALL_PRODUCTS[1]
        st.session_state.compare_product = fallback

    if "planner_link_mode" not in st.session_state:
        st.session_state.planner_link_mode = "Selected links"

    if "planner_zoom_mode" not in st.session_state:
        st.session_state.planner_zoom_mode = "Selected stage only"

    if "route_view_mode" not in st.session_state:
        st.session_state.route_view_mode = "Entry routes"

    if "selected_route_index" not in st.session_state:
        st.session_state.selected_route_index = 0


def _sync_surface_from_query_params() -> None:
    requested_surface = st.query_params.get("surface")
    if isinstance(requested_surface, list):
        requested_surface = requested_surface[0] if requested_surface else None

    if requested_surface in SURFACES and requested_surface != st.session_state.surface:
        st.session_state.surface = requested_surface


def _apply_styles() -> None:
    light_vars = _theme_css_vars(LIGHT_THEME)
    dark_vars = _theme_css_vars(DARK_THEME)

    st.markdown(
        f"""
        <style>
            :root {{
{light_vars}
            }}

            @media (prefers-color-scheme: dark) {{
                :root {{
{dark_vars}
                }}
            }}

            .stApp {{
                background: var(--tmk-bg);
                color: var(--tmk-text);
            }}

            .block-container {{
                padding-top: 1rem;
                padding-bottom: 2rem;
            }}

            .tmk-shell {{
                max-width: 1240px;
                margin: 0 auto;
                padding-bottom: 2rem;
            }}

            .tmk-header {{
                background: linear-gradient(180deg, var(--tmk-surface) 0%, var(--tmk-surface-strong) 100%);
                border: 1px solid var(--tmk-border);
                border-radius: 24px;
                padding: 1.35rem 1.4rem 1.1rem 1.4rem;
                box-shadow: 0 8px 24px rgba(34, 46, 75, 0.06);
                margin-bottom: 1rem;
            }}

            .tmk-kicker {{
                font-size: 0.78rem;
                font-weight: 800;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                color: var(--tmk-accent);
                margin-bottom: 0.25rem;
            }}

            .tmk-header h1 {{
                margin: 0;
                font-size: 2rem;
                line-height: 1.08;
                color: var(--tmk-text);
            }}

            .tmk-header p {{
                margin: 0.45rem 0 0 0;
                color: var(--tmk-text-soft);
                font-size: 1rem;
                line-height: 1.45;
            }}

            .tmk-nav-strip {{
                display: flex;
                gap: 0.6rem;
                flex-wrap: wrap;
                margin-bottom: 1rem;
            }}

            .tmk-nav-link {{
                display: inline-flex;
                align-items: center;
                padding: 0.6rem 0.95rem;
                border-radius: 999px;
                border: 1px solid var(--tmk-border);
                background: var(--tmk-surface);
                color: var(--tmk-text);
                font-weight: 800;
                font-size: 0.95rem;
                text-decoration: none;
            }}

            .tmk-nav-link-active {{
                background: var(--tmk-accent-soft);
                border-color: var(--tmk-accent);
                color: #ffffff;
            }}

            .tmk-panel {{
                background: var(--tmk-surface);
                border: 1px solid var(--tmk-border);
                border-radius: 24px;
                padding: 1rem;
                box-shadow: 0 10px 30px rgba(34, 46, 75, 0.05);
                margin-bottom: 1rem;
            }}

            .tmk-card {{
                background: linear-gradient(180deg, var(--tmk-surface) 0%, var(--tmk-surface-strong) 100%);
                border: 1px solid var(--tmk-border);
                border-radius: 18px;
                padding: 0.95rem 1rem;
                height: 100%;
                margin-bottom: 0.75rem;
            }}

            .tmk-card-dark {{
                background: linear-gradient(180deg, rgba(8, 23, 47, 0.98) 0%, rgba(13, 28, 50, 0.98) 100%);
                border: 1px solid var(--tmk-border);
                border-radius: 24px;
                padding: 0.75rem;
                margin-bottom: 0.75rem;
            }}

            .tmk-section-title {{
                font-size: 2rem;
                line-height: 1.1;
                font-weight: 800;
                color: var(--tmk-text);
                margin-bottom: 0.2rem;
            }}

            .tmk-section-subtitle {{
                color: var(--tmk-text-soft);
                margin-bottom: 0.8rem;
                font-size: 1rem;
                line-height: 1.45;
            }}

            .tmk-subhead {{
                font-size: 1.18rem;
                font-weight: 800;
                color: var(--tmk-text);
                margin-bottom: 0.5rem;
            }}

            .tmk-small-label {{
                font-size: 0.74rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: var(--tmk-text-soft);
                margin-bottom: 0.3rem;
            }}

            .tmk-value {{
                font-size: 1.3rem;
                font-weight: 800;
                color: var(--tmk-text);
                line-height: 1.2;
            }}

            .tmk-note {{
                color: var(--tmk-text-soft);
                font-size: 0.98rem;
                line-height: 1.55;
            }}

            .tmk-soft-list {{
                display: flex;
                flex-wrap: wrap;
                gap: 0.45rem;
                margin-top: 0.5rem;
            }}

            .tmk-pill {{
                display: inline-flex;
                align-items: center;
                padding: 0.46rem 0.72rem;
                border-radius: 999px;
                background: var(--tmk-surface-strong);
                border: 1px solid var(--tmk-border);
                color: var(--tmk-text);
                font-size: 0.95rem;
                font-weight: 700;
                line-height: 1.2;
            }}

            .tmk-pill-accent {{
                background: var(--tmk-accent-soft);
                border-color: var(--tmk-accent);
                color: #ffffff;
            }}

            .tmk-stage-card {{
                border-radius: 20px;
                border: 1px solid var(--tmk-border);
                padding: 0.9rem;
                margin-bottom: 0.8rem;
                background: var(--tmk-surface);
            }}

            .tmk-stage-title {{
                font-size: 1.05rem;
                font-weight: 800;
                color: var(--tmk-text);
                margin-bottom: 0.55rem;
            }}

            .tmk-map-wrap {{
                overflow-x: auto;
                overflow-y: hidden;
                -webkit-overflow-scrolling: touch;
                border-radius: 20px;
                margin-top: 0.8rem;
            }}

            .tmk-legend-box {{
                background: var(--tmk-surface-strong);
                border: 1px solid var(--tmk-border);
                border-radius: 16px;
                padding: 0.8rem 0.95rem;
                margin-top: 0.8rem;
            }}

            .tmk-legend-row {{
                display: flex;
                flex-wrap: wrap;
                gap: 0.9rem;
                align-items: center;
            }}

            .tmk-legend-item {{
                display: inline-flex;
                align-items: center;
                gap: 0.45rem;
                color: var(--tmk-text-soft);
                font-size: 0.94rem;
                font-weight: 700;
            }}

            .tmk-line-swatch {{
                width: 36px;
                height: 0;
                border-top: 4px solid var(--tmk-map-link-selected);
            }}

            .tmk-line-swatch-purple {{
                width: 36px;
                height: 0;
                border-top: 3px solid var(--tmk-map-link-atlas);
            }}

            .tmk-line-swatch-grey {{
                width: 36px;
                height: 0;
                border-top: 3px solid var(--tmk-border);
            }}

            .tmk-worksheet-frame {{
                background: linear-gradient(180deg, var(--tmk-surface) 0%, var(--tmk-surface-strong) 100%);
                border: 1px solid var(--tmk-border);
                border-radius: 22px;
                padding: 1rem;
                margin-bottom: 0.9rem;
            }}

            .tmk-answer-box {{
                background: var(--tmk-surface);
                border: 1px solid var(--tmk-border);
                border-radius: 16px;
                padding: 0.9rem 0.95rem;
                margin-bottom: 0.7rem;
                color: var(--tmk-text);
            }}

            .tmk-mobile-note {{
                color: var(--tmk-text-soft);
                font-size: 0.9rem;
                margin-top: 0.25rem;
            }}

            .stButton > button {{
                border-radius: 999px;
                border: 1px solid var(--tmk-border);
                background: var(--tmk-surface);
                color: var(--tmk-text);
                font-weight: 800;
                min-height: 2.9rem;
                box-shadow: none;
                font-size: 0.98rem;
                line-height: 1.2;
                white-space: normal;
            }}

            [data-testid="stSidebar"] {{
                background: var(--tmk-surface-strong);
                border-left: 1px solid var(--tmk-border);
            }}

            [data-testid="stSidebar"] * {{
                color: var(--tmk-text);
            }}

            @media (max-width: 640px) {{
                .tmk-header h1 {{
                    font-size: 1.36rem;
                }}

                .tmk-section-title {{
                    font-size: 1.3rem;
                }}

                .tmk-note {{
                    font-size: 0.92rem;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _theme_css_vars(theme: dict[str, str]) -> str:
    return "\n".join(
        [
            f"                --tmk-bg: {theme['bg']};",
            f"                --tmk-surface: {theme['surface']};",
            f"                --tmk-surface-strong: {theme['surface_strong']};",
            f"                --tmk-border: {theme['border']};",
            f"                --tmk-text: {theme['text']};",
            f"                --tmk-text-soft: {theme['text_soft']};",
            f"                --tmk-accent: {theme['accent']};",
            f"                --tmk-accent-soft: {theme['accent_soft']};",
            f"                --tmk-map-link-selected: {theme['map_link_selected']};",
            f"                --tmk-map-link-atlas: {theme['map_link_atlas']};",
            f"                --tmk-map-node-outline: {theme['map_node_outline']};",
            f"                --tmk-map-node-selected: {theme['map_node_selected']};",
        ]
    )


def _render_nav() -> None:
    links: list[str] = []
    for surface in SURFACES:
        active_class = " tmk-nav-link-active" if surface == st.session_state.surface else ""
        href = f"?surface={surface.replace(' ', '%20')}"
        links.append(f'<a class="tmk-nav-link{active_class}" href="{href}">{escape(surface)}</a>')
    st.markdown(f'<div class="tmk-nav-strip">{"".join(links)}</div>', unsafe_allow_html=True)


def _render_sidebar() -> None:
    record = product_record(st.session_state.selected_product)

    with st.sidebar:
        st.markdown("## Current selection")
        st.write(f"**Product:** {record.product}")
        st.write(f"**Stage:** {stage_label(record.stage)}")
        st.write(f"**Intro route:** {_format_route(record.intro_route)}")
        st.write(f"**Full routes:** {len(distinct_factor_routes(record.product))}")
        st.write(f"**Division exits:** {len(record.ways_out)}")
        st.write(f"**Role:** {record.structural_role}")

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


def _render_structural_planner(product: int) -> None:
    record = product_record(product)
    admissible_routes = distinct_factor_routes(record.product)
    focus_stage_only = st.session_state.planner_zoom_mode == "Selected stage only"
    map_height = _world_map_height(focus_stage_only, record.stage)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Structural Planner</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Fixed stage order, stage introductions, pedagogical intro route, wider admissible atlas, division exits, and structural role.</div>',
        unsafe_allow_html=True,
    )

    control_col1, control_col2, control_col3 = st.columns(3)

    with control_col1:
        selected = st.selectbox(
            "Selected product",
            options=ALL_PRODUCTS,
            index=ALL_PRODUCTS.index(st.session_state.selected_product),
            format_func=_product_option_label,
            key="planner_product_select_v14",
        )
        if selected != st.session_state.selected_product:
            st.session_state.selected_product = selected
            st.rerun()

    with control_col2:
        mode = st.selectbox(
            "Link mode",
            options=PLANNER_LINK_MODES,
            index=PLANNER_LINK_MODES.index(st.session_state.planner_link_mode),
            key="planner_link_mode_select_v14",
        )
        if mode != st.session_state.planner_link_mode:
            st.session_state.planner_link_mode = mode
            st.rerun()

    with control_col3:
        zoom = st.selectbox(
            "Planner zoom",
            options=PLANNER_ZOOM_MODES,
            index=PLANNER_ZOOM_MODES.index(st.session_state.planner_zoom_mode),
            key="planner_zoom_mode_select_v14",
        )
        if zoom != st.session_state.planner_zoom_mode:
            st.session_state.planner_zoom_mode = zoom
            st.rerun()

    _metric_card_row(
        [
            ("Selected stage", stage_label(record.stage)),
            ("Introduced here", str(len(STAGES[record.stage].products))),
            ("Full routes", str(len(admissible_routes))),
            ("Division exits", str(len(record.ways_out))),
        ]
    )

    top_col1, top_col2 = st.columns(2)

    with top_col1:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-subhead">Fixed stage unlock order</div>', unsafe_allow_html=True)
        ordered = " → ".join(stage_label(stage) for stage in STAGE_ORDER if stage in STAGES)
        st.markdown(f'<div class="tmk-note">{escape(ordered)}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with top_col2:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-subhead">Pedagogical intro route</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="tmk-note">
                {record.product} is introduced through <strong>{_format_route(record.intro_route)}</strong>.<br>
                This is the pedagogical entry route, not the full route atlas.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    lower_col1, lower_col2 = st.columns(2)

    with lower_col1:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-subhead">Full admissible routes</div>', unsafe_allow_html=True)
        lines = "<br>".join(escape(_format_route(route)) for route in admissible_routes)
        st.markdown(f'<div class="tmk-note">{lines}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with lower_col2:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-subhead">Division exits</div>', unsafe_allow_html=True)
        exits = "<br>".join(escape(label) for label in exit_route_labels(record.product, limit=8))
        st.markdown(
            f"""
            <div class="tmk-note">
                {exits}<br><br>
                Structural role: <strong>{escape(str(record.structural_role))}</strong>
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
        height=map_height,
        scrolling=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="tmk-legend-box">
            <div class="tmk-legend-row">
                <div class="tmk-legend-item"><span class="tmk-line-swatch"></span> pedagogical intro route</div>
                <div class="tmk-legend-item"><span class="tmk-line-swatch-purple"></span> selected product admissible atlas</div>
                <div class="tmk-legend-item"><span class="tmk-line-swatch-grey"></span> stage row structure</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Products introduced at this stage</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tmk-section-subtitle">{stage_label(record.stage)} introduces {len(STAGES[record.stage].products)} products.</div>',
        unsafe_allow_html=True,
    )
    _render_visible_products_grid(product, only_stage=record.stage)
    st.markdown("</div>", unsafe_allow_html=True)


def _render_stage_cards(selected_product: int) -> None:
    for stage in [stage for stage in STAGE_ORDER if stage in STAGES]:
        style = _stage_palette(stage)
        stage_record = STAGES[stage]
        pills: list[str] = []
        for product in stage_record.products:
            cls = "tmk-pill tmk-pill-accent" if product == selected_product else "tmk-pill"
            pills.append(f'<span class="{cls}">{product}</span>')
        st.markdown(
            f"""
            <div class="tmk-stage-card" style="background:{style['background']}; border-color:{style['border']};">
                <div class="tmk-stage-title">{escape(stage_record.label)}</div>
                <div class="tmk-soft-list">{''.join(pills)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_product_lab(product: int) -> None:
    record = product_record(product)
    compare = product_record(st.session_state.compare_product)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Product Lab</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Hub overview, distinct entry routes, division exits, inverse field, patterns, and comparisons.</div>',
        unsafe_allow_html=True,
    )

    control_col1, control_col2, control_col3 = st.columns(3)

    with control_col1:
        selected = st.selectbox(
            "Selected product",
            options=ALL_PRODUCTS,
            index=ALL_PRODUCTS.index(st.session_state.selected_product),
            format_func=_product_option_label,
            key="lab_product_select_v14",
        )
        if selected != st.session_state.selected_product:
            st.session_state.selected_product = selected
            if st.session_state.compare_product == selected and len(ALL_PRODUCTS) > 1:
                st.session_state.compare_product = next(item for item in ALL_PRODUCTS if item != selected)
            st.session_state.selected_route_index = 0
            st.rerun()

    compare_options = [item for item in ALL_PRODUCTS if item != st.session_state.selected_product]
    if st.session_state.compare_product not in compare_options:
        st.session_state.compare_product = compare_options[0]
        compare = product_record(st.session_state.compare_product)

    with control_col2:
        compare_value = st.selectbox(
            "Compare with",
            options=compare_options,
            index=compare_options.index(st.session_state.compare_product),
            format_func=_product_option_label,
            key="lab_compare_select_v14",
        )
        if compare_value != st.session_state.compare_product:
            st.session_state.compare_product = compare_value
            st.rerun()

    with control_col3:
        mode = st.radio(
            "Route view",
            options=ROUTE_VIEW_MODES,
            index=ROUTE_VIEW_MODES.index(st.session_state.route_view_mode),
            horizontal=True,
            key="lab_route_view_mode_v14",
        )
        if mode != st.session_state.route_view_mode:
            st.session_state.route_view_mode = mode
            st.session_state.selected_route_index = 0
            st.rerun()

    record = product_record(st.session_state.selected_product)
    compare = product_record(st.session_state.compare_product)

    _metric_card_row(
        [
            ("Product", str(record.product)),
            ("Stage", stage_label(record.stage)),
            ("Routes", str(len(distinct_factor_routes(record.product)))),
            ("Role", record.structural_role),
        ]
    )

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Radial hub view</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-note">Only distinct multiplication pairings are shown as entry routes. Mirrored duplicates are removed.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="tmk-card-dark">', unsafe_allow_html=True)
    components.html(_radial_hub_html(record.product), height=720, scrolling=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="tmk-mobile-note">Mobile layout switches to stacked route cards below 720px width.</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    _render_route_inspector(record)

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-subhead">Distinct entry routes</div>', unsafe_allow_html=True)
        for route in entry_routes(record.product):
            st.markdown(
                f'<div class="tmk-note">{escape(_format_route(route))}</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-subhead">Exit routes</div>', unsafe_allow_html=True)
        for label in exit_route_labels(record.product, limit=4):
            st.markdown(
                f'<div class="tmk-note">{escape(label)}</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Truth set</div>', unsafe_allow_html=True)
    st.markdown(_pill_cloud(distinct_factor_routes(record.product), accent=True), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Inverse field</div>', unsafe_allow_html=True)
    st.markdown(_pill_cloud(inverse_labels(record.product), accent=False), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Pattern links</div>', unsafe_allow_html=True)
    _render_pattern_links(record.product)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Compare products</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="tmk-note"><strong>{record.product}</strong> · {stage_label(record.stage)} · {_format_route(record.intro_route)}</div>
        <div class="tmk-note"><strong>{compare.product}</strong> · {stage_label(compare.stage)} · {_format_route(compare.intro_route)}</div>
        <div class="tmk-note">Shared factors: {shared_factors(record.product, compare.product)}</div>
        <div class="tmk-note">Distinct route counts: {len(distinct_factor_routes(record.product))} vs {len(distinct_factor_routes(compare.product))}</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def _route_inspector_items(record, mode: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []

    if mode == "Entry routes":
        for route in entry_routes(record.product):
            items.append(
                {
                    "label": _format_route(route),
                    "headline": f"{route[0]} × {route[1]} = {record.product}",
                    "explanation": f"This distinct multiplication route makes {record.product}.",
                }
            )
        return items

    for divisor, quotient in record.ways_out[:4]:
        items.append(
            {
                "label": f"{record.product}÷{divisor}={quotient}",
                "headline": f"{record.product} ÷ {divisor} = {quotient}",
                "explanation": f"This exit route recovers the factor {quotient} from {record.product}.",
            }
        )

    return items


def _render_route_inspector(record) -> None:
    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Route inspector</div>', unsafe_allow_html=True)

    items = _route_inspector_items(record, st.session_state.route_view_mode)
    if not items:
        st.markdown('<div class="tmk-note">No routes available.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    if st.session_state.selected_route_index >= len(items):
        st.session_state.selected_route_index = 0

    button_cols = st.columns(min(4, len(items)))
    for index, item in enumerate(items):
        col = button_cols[index % len(button_cols)]
        button_type = "primary" if index == st.session_state.selected_route_index else "secondary"
        if col.button(
            item["label"],
            key=f"route_inspector_button_v14_{st.session_state.route_view_mode}_{index}",
            use_container_width=True,
            type=button_type,
        ):
            st.session_state.selected_route_index = index
            st.rerun()

    selected_item = items[st.session_state.selected_route_index]

    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    title = st.session_state.route_view_mode[:-1] if st.session_state.route_view_mode.endswith("s") else st.session_state.route_view_mode
    st.markdown(f'<div class="tmk-small-label">{escape(title)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tmk-value">{escape(selected_item["headline"])}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tmk-note" style="margin-top:0.55rem;">{escape(selected_item["explanation"])}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def _render_worksheet_studio(product: int, tier: str) -> None:
    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Worksheet Studio</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Choose product, choose Support/Core/Extension, generate worksheet, review teacher key.</div>',
        unsafe_allow_html=True,
    )

    control_col1, control_col2 = st.columns(2)

    with control_col1:
        selected = st.selectbox(
            "Selected product",
            options=ALL_PRODUCTS,
            index=ALL_PRODUCTS.index(st.session_state.selected_product),
            format_func=_product_option_label,
            key="worksheet_product_select_v14",
        )
        if selected != st.session_state.selected_product:
            st.session_state.selected_product = selected
            st.rerun()

    with control_col2:
        selected_tier = st.radio(
            "Worksheet tier",
            options=TIERS,
            index=TIERS.index(st.session_state.selected_tier),
            horizontal=True,
            key="worksheet_tier_radio_v14",
        )
        if selected_tier != st.session_state.selected_tier:
            st.session_state.selected_tier = selected_tier
            st.rerun()

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
    st.markdown("</div>", unsafe_allow_html=True)


def _metric_card_row(items: list[tuple[str, str]]) -> None:
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        with col:
            st.markdown(
                f"""
                <div class="tmk-card">
                    <div class="tmk-small-label">{escape(label)}</div>
                    <div class="tmk-value">{escape(value)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_visible_products_grid(product: int, only_stage: str | None = None) -> None:
    if only_stage is None:
        record = product_record(product)
        products = visible_products(record.stage)
    else:
        products = STAGES[only_stage].products

    cols_per_row = 4
    for row_start in range(0, len(products), cols_per_row):
        cols = st.columns(cols_per_row)
        for offset, visible_product in enumerate(products[row_start : row_start + cols_per_row]):
            button_type = "primary" if visible_product == product else "secondary"
            if cols[offset].button(
                str(visible_product),
                key=f"visible_product_button_v14_{only_stage}_{visible_product}",
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


def _world_map_height(focus_stage_only: bool, selected_stage: str) -> int:
    lane_h = 108
    lane_gap = 32
    top = 24
    bottom = 28
    stages = _visible_world_stages(focus_stage_only, selected_stage)
    return top + len(stages) * lane_h + max(0, len(stages) - 1) * lane_gap + bottom + 20


def _world_map_html(
    selected_product: int,
    link_mode: str,
    focus_stage_only: bool,
) -> str:
    lane_x = 26
    lane_w = 1268
    lane_h = 108
    lane_gap = 32
    top = 24
    header_band_h = 44
    left_label_space = 250

    selected_record = product_record(selected_product)
    stages = _visible_world_stages(focus_stage_only, selected_record.stage)
    total_height = _world_map_height(focus_stage_only, selected_record.stage)
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

    light_vars = _theme_css_vars(LIGHT_THEME)
    dark_vars = _theme_css_vars(DARK_THEME)

    lane_rects: list[str] = []
    lane_labels: list[str] = []
    structure_lines: list[str] = []
    atlas_lines: list[str] = []
    selected_lines: list[str] = []

    for index, stage in enumerate(stages):
        y = top + index * (lane_h + lane_gap)
        style = _stage_palette(stage)
        stage_record = STAGES[stage]
        stage_key_label, stage_name_label = _split_stage_label(stage, stage_record.label)

        lane_rects.append(
            f'<rect x="{lane_x}" y="{y}" width="{lane_w}" height="{lane_h}" rx="24" fill="{style["background"]}" stroke="{style["border"]}" stroke-width="2"></rect>'
        )
        lane_labels.append(
            f'<text x="{lane_x + 18}" y="{y + 24}" font-size="12" font-weight="800" letter-spacing="1.4" fill="var(--tmk-text-soft)">{escape(stage_key_label.upper())}</text>'
        )
        lane_labels.append(
            f'<text x="{lane_x + 18}" y="{y + 43}" font-size="15" font-weight="700" fill="var(--tmk-text)">{escape(stage_name_label)}</text>'
        )

        stage_products = STAGES[stage].products
        if len(stage_products) > 1:
            xs = [positions[p][0] for p in stage_products]
            structure_y = positions[stage_products[0]][1]
            structure_lines.append(
                _svg_line(min(xs), structure_y, max(xs), structure_y, "var(--tmk-border)", 2.0, 0.85, "")
            )

    if link_mode == "Show selected atlas":
        end_x, end_y = positions[selected_product]
        atlas_factors: set[int] = set()
        for route in distinct_factor_routes(selected_record.product):
            atlas_factors.update(route)
        for factor in sorted(atlas_factors):
            if factor in positions:
                start_x, start_y = positions[factor]
                atlas_lines.append(
                    _svg_line(start_x, start_y, end_x, end_y, "var(--tmk-map-link-atlas)", 2.6, 1.0, "")
                )

    if link_mode in ("Selected links", "Show selected atlas"):
        end_x, end_y = positions[selected_product]
        for factor in selected_record.intro_route:
            if factor in positions:
                start_x, start_y = positions[factor]
                selected_lines.append(
                    _svg_line(start_x, start_y, end_x, end_y, "var(--tmk-map-link-selected)", 4.0, 1.0, "")
                )

    nodes: list[str] = []
    for product in ALL_PRODUCTS:
        record = product_record(product)
        if record.stage not in stages:
            continue

        style = _stage_palette(record.stage)
        x, y = positions[product]
        is_selected = product == selected_product
        radius = 21 if is_selected else 18
        outer_radius = 24 if is_selected else 20

        if is_selected:
            nodes.append(f'<circle cx="{x}" cy="{y}" r="{outer_radius}" fill="var(--tmk-map-node-selected)" opacity="0.22"></circle>')
            nodes.append(
                f'<circle cx="{x}" cy="{y}" r="{radius}" fill="var(--tmk-map-node-selected)" stroke="#FFFFFF" stroke-width="3" filter="url(#selected-shadow)"></circle>'
            )
        else:
            nodes.append(f'<circle cx="{x}" cy="{y}" r="{outer_radius}" fill="{style["node"]}" opacity="0.14"></circle>')
            nodes.append(
                f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{style["node"]}" stroke="var(--tmk-map-node-outline)" stroke-width="2"></circle>'
            )

        nodes.append(
            f'<text x="{x}" y="{y + 5}" text-anchor="middle" font-size="{18 if is_selected else 15}" font-weight="900" fill="#ffffff">{product}</text>'
        )

    return f"""
    <html>
    <head>
        <style>
            :root {{
{light_vars}
            }}

            @media (prefers-color-scheme: dark) {{
                :root {{
{dark_vars}
                }}
            }}

            body {{
                margin: 0;
                background: transparent;
                color: var(--tmk-text);
                font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }}
        </style>
    </head>
    <body>
        <div style="background:transparent;border-radius:24px;overflow:auto;max-width:100%;">
            <svg viewBox="0 0 1320 {total_height}" width="1320" height="{total_height}" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <filter id="selected-shadow" x="-50%" y="-50%" width="200%" height="200%">
                        <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="rgba(0,0,0,0.15)"/>
                    </filter>
                </defs>
                <rect x="0" y="0" width="1320" height="{total_height}" fill="transparent"></rect>
                {''.join(lane_rects)}
                {''.join(structure_lines)}
                {''.join(atlas_lines)}
                {''.join(selected_lines)}
                {''.join(lane_labels)}
                {''.join(nodes)}
            </svg>
        </div>
    </body>
    </html>
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
        y = row_top + header_band_h + (lane_h - header_band_h) / 2 + 6

        if len(products) == 1:
            base_x = lane_x + left_label_space + usable_x / 2
            dx, dy = MAP_NODE_OFFSETS.get(products[0], (0.0, 0.0))
            positions[products[0]] = (base_x + dx, y + dy)
            continue

        step = usable_x / (len(products) - 1)
        start_x = lane_x + left_label_space
        for index, product in enumerate(products):
            base_x = start_x + index * step
            dx, dy = MAP_NODE_OFFSETS.get(product, (0.0, 0.0))
            positions[product] = (base_x + dx, y + dy)

    return positions


def _visible_world_stages(focus_stage_only: bool, selected_stage: str) -> list[str]:
    stages = [stage for stage in STAGE_ORDER if stage in STAGES]
    if focus_stage_only:
        return [stage for stage in stages if stage == selected_stage]
    return stages


def _radial_hub_html(product: int) -> str:
    record = product_record(product)
    desktop_svg = _desktop_radial_svg(record)
    mobile_svg = _mobile_radial_svg(record)
    light_vars = _theme_css_vars(LIGHT_THEME)
    dark_vars = _theme_css_vars(DARK_THEME)

    return f"""
    <html>
    <head>
        <style>
            :root {{
{light_vars}
            }}

            @media (prefers-color-scheme: dark) {{
                :root {{
{dark_vars}
                }}
            }}

            body {{
                margin: 0;
                padding: 0;
                background: transparent;
                color: var(--tmk-text);
                font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
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
        <div class="tmk-radial-desktop">{desktop_svg}</div>
        <div class="tmk-radial-mobile">{mobile_svg}</div>
    </body>
    </html>
    """


def _desktop_radial_svg(record) -> str:
    product = record.product
    style = _stage_palette(record.stage)
    cx = 420
    cy = 270
    r = 86

    entry_route_list = entry_routes(record.product)[:4]
    exit_labels = exit_route_labels(record.product, limit=4)

    entry_angles = [225, 255, 285, 315][: len(entry_route_list)]
    exit_angles = [140, 110, 70, 40][: len(exit_labels)]

    entry_points = [_point_on_circle(cx, cy, 210, angle) for angle in entry_angles]
    exit_points = [_point_on_circle(cx, cy, 220, angle) for angle in exit_angles]

    lines: list[str] = []
    boxes: list[str] = []

    for route, (bx, by) in zip(entry_route_list, entry_points):
        x1, y1 = _edge_point_toward(cx, cy, bx, by, r + 10)
        lines.append(_svg_arrow(bx, by + 22, x1, y1, "#dbe4f4", 4))
        boxes.append(_svg_info_box(bx - 64, by, 128, 42, _format_route(route), "#ffffff", "#cfd8e6", "#20304a", 18))

    for label, (bx, by) in zip(exit_labels, exit_points):
        x1, y1 = _edge_point_toward(cx, cy, bx, by, r + 10)
        lines.append(_svg_arrow(x1, y1, bx, by + 20, "#9c7cff", 4))
        boxes.append(_svg_info_box(bx - 70, by, 140, 42, label, "#241448", "#d9c4ff", "#ffffff", 18))

    return f"""
    <svg viewBox="0 0 840 520" width="840" height="520" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <marker id="arrow-end-light" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#dbe4f4"></path>
            </marker>
            <marker id="arrow-end-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#9c7cff"></path>
            </marker>
        </defs>
        <rect x="0" y="0" width="840" height="520" rx="28" fill="#031026"></rect>
        <text x="18" y="28" font-size="18" font-weight="800" fill="#ffffff">Radial Hub View</text>
        <text x="18" y="52" font-size="15" font-weight="500" fill="#d4def1">Entry routes point inward. Exit routes point outward. Distinct pairings only.</text>
        {''.join(lines)}
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="{style["node"]}" stroke="#f5f7fb" stroke-width="5"></circle>
        <text x="{cx}" y="{cy + 14}" text-anchor="middle" font-size="44" font-weight="900" fill="#ffffff">{product}</text>
        <text x="{cx}" y="98" text-anchor="middle" font-size="20" font-weight="800" fill="#ffffff">Entry routes</text>
        <text x="{cx}" y="430" text-anchor="middle" font-size="20" font-weight="800" fill="#ffffff">Exit routes</text>
        {''.join(boxes)}
    </svg>
    """.replace('marker-end="LIGHT"', 'marker-end="url(#arrow-end-light)"').replace(
        'marker-end="PURPLE"', 'marker-end="url(#arrow-end-purple)"'
    )


def _mobile_radial_svg(record) -> str:
    product = record.product
    style = _stage_palette(record.stage)
    entry_route_list = entry_routes(record.product)[:4]
    exit_labels = exit_route_labels(record.product, limit=4)

    entry_cards = []
    exit_cards = []

    entry_y = 90
    for route in entry_route_list:
        entry_cards.append(_svg_info_box(40, entry_y, 280, 44, _format_route(route), "#ffffff", "#cfd8e6", "#20304a", 18))
        entry_y += 58

    exit_y = 380
    for label in exit_labels:
        exit_cards.append(_svg_info_box(40, exit_y, 280, 44, label, "#241448", "#d9c4ff", "#ffffff", 18))
        exit_y += 58

    return f"""
    <svg viewBox="0 0 360 660" xmlns="http://www.w3.org/2000/svg">
        <rect x="0" y="0" width="360" height="660" rx="28" fill="#031026"></rect>
        <text x="20" y="30" font-size="18" font-weight="800" fill="#ffffff">Radial Hub View</text>
        <text x="20" y="58" font-size="15" font-weight="500" fill="#d4def1">Mobile stacked view</text>
        <text x="40" y="82" font-size="18" font-weight="800" fill="#ffffff">Entry routes</text>
        {''.join(entry_cards)}
        <circle cx="180" cy="322" r="62" fill="{style["node"]}" stroke="#f5f7fb" stroke-width="4"></circle>
        <text x="180" y="336" text-anchor="middle" font-size="38" font-weight="900" fill="#ffffff">{product}</text>
        <text x="40" y="368" font-size="18" font-weight="800" fill="#ffffff">Exit routes</text>
        {''.join(exit_cards)}
    </svg>
    """


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
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{color}" stroke-width="{width}" opacity="{opacity}" stroke-linecap="round" {dash_attr}></line>'
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
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" marker-end="{marker}"></line>'
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


def _point_on_circle(cx: float, cy: float, radius: float, angle_degrees: float) -> tuple[float, float]:
    angle_radians = angle_degrees * pi / 180
    return cx + radius * cos(angle_radians), cy + radius * sin(angle_radians)


def _stage_palette(stage: str) -> dict[str, str]:
    visible = [item for item in STAGE_ORDER if item in STAGES]
    index = visible.index(stage) if stage in visible else 0
    if index >= len(STAGE_BACKGROUND_SEQUENCE):
        index = index % len(STAGE_BACKGROUND_SEQUENCE)
    return {
        "background": STAGE_BACKGROUND_SEQUENCE[index],
        "border": STAGE_BORDER_SEQUENCE[index],
        "node": STAGE_NODE_SEQUENCE[index],
    }


def _split_stage_label(stage_key: str, label: str) -> tuple[str, str]:
    clean = label.strip()
    lowered = clean.lower()
    if lowered.startswith("stage "):
        parts = clean.split(" ", 2)
        if len(parts) >= 3:
            return f"{parts[0]} {parts[1]}", parts[2]
    return f"Stage {stage_key}", clean


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

if __name__ == "__main__":
    main()
