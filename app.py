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
PLANNER_LINK_MODES = ("Selected links", "Show selected atlas", "No links")
PLANNER_ZOOM_MODES = ("Whole world", "Selected stage only")
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
        st.session_state.planner_zoom_mode = "Whole world"
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
        st.write(f"**Full routes:** {len(_distinct_factor_routes(record))}")
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
    admissible_routes = _distinct_factor_routes(record)
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
            key="planner_product_select_v12",
        )
        if selected != st.session_state.selected_product:
            st.session_state.selected_product = selected
            st.rerun()

    with control_col2:
        mode = st.selectbox(
            "Link mode",
            options=PLANNER_LINK_MODES,
            index=PLANNER_LINK_MODES.index(st.session_state.planner_link_mode),
            key="planner_link_mode_select_v12",
        )
        if mode != st.session_state.planner_link_mode:
            st.session_state.planner_link_mode = mode
            st.rerun()

    with control_col3:
        zoom = st.selectbox(
            "Planner zoom",
            options=PLANNER_ZOOM_MODES,
            index=PLANNER_ZOOM_MODES.index(st.session_state.planner_zoom_mode),
            key="planner_zoom_mode_select_v12",
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
        exits = "<br>".join(escape(f"{record.product}÷{a}={b}") for a, b in record.ways_out[:8])
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
            key="lab_product_select_v12",
        )
        if selected != st.session_state.selected_product:
            st.session_state.selected_product = selected
            st.rerun()

    compare_options = [item for item in ALL_PRODUCTS if item != st.session_state.selected_product]
    if st.session_state.compare_product not in compare_options:
        st.session_state.compare_product = compare_options[0]

    with control_col2:
        compare_value = st.selectbox(
            "Compare with",
            options=compare_options,
            index=compare_options.index(st.session_state.compare_product),
            format_func=_product_option_label,
            key="lab_compare_select_v12",
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
            key="lab_route_view_mode_v12",
        )
        if mode != st.session_state.route_view_mode:
            st.session_state.route_view_mode = mode
            st.session_state.selected_route_index = 0
            st.rerun()

    compare = product_record(st.session_state.compare_product)

    _metric_card_row(
        [
            ("Product", str(record.product)),
            ("Stage", stage_label(record.stage)),
            ("Routes", str(len(_distinct_factor_routes(record)))),
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

def _route_inspector_items(record, mode: str) -> list[dict[str, str]]:

    items: list[dict[str, str]] = []

    if mode == "Entry routes":
        for route in _entry_routes_for_radial(record):
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
