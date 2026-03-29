File: app.py
from __future__ import annotations

from html import escape
from typing import Any, Iterable

import streamlit as st

# -----------------------------
# DOMAIN IMPORTS
# -----------------------------
from domain.routes import (
    distinct_factor_routes,
    entry_routes,
    exit_route_labels,
    inverse_labels,
    shared_factors,
)

from domain.products import (
    ALL_PRODUCTS,
    STAGE_ORDER,
    STAGES,
    product_record,
    stage_label,
)

from domain.product_metadata import (
    available_products as metadata_available_products,
    new_products as metadata_new_products,
    product_metadata,
)

from domain.stage_vocabulary import (
    get_stage_vocabulary,
)

# -----------------------------
# WORKSHEET SYSTEM IMPORTS
# -----------------------------
from models.worksheet_models import (
    ProductSelectionRequest,
)

from services.product_selection_engine import (
    available_selection_modes,
)

from services.worksheet_generation_service import (
    generate_worksheet_bundle,
)

from ui.instruction_planner_page import (
    render_instruction_planner_page,
)

from ui.number_line_doubler_page import (
    render_number_line_doubler_page,
)

APP_TITLE = "TMK Teacher App"
SURFACES = (
    "Structural Planner",
    "Product Lab",
    "Instruction Planner",
    "Worksheet Studio",
    "Number Line Doubler",
)
TIERS = ("Support", "Core", "Extension")
WORKSHEET_FORMATS = ("one_product_10", "three_product_12")
SELECTION_SCOPES = ("new_only", "available_mixed", "hybrid")
PLANNER_LINK_MODES = ("Selected links", "Show selected atlas", "No links")
PLANNER_ZOOM_MODES = ("Selected stage only", "Whole world")
ROUTE_VIEW_MODES = ("Entry routes", "Exit routes")

LIGHT_THEME = {
    "bg": "#E8E1D5",
    "surface": "#F7F4EE",
    "surface_strong": "#FFFFFF",
    "border": "#D9D4C8",
    "text": "#2F3A3C",
    "text_soft": "#6C7A7D",
    "accent": "#497379",
    "accent_soft": "#83B8BE",
    "highlight": "#ECA159",
    "danger": "#FF5E57",
    "hover": "#A9CED2",
    "sidebar_bg": "#91CBCA",
    "sidebar_text": "#2F3A3C",
    "sidebar_text_soft": "#4F6063",
    "sidebar_border": "#6FAFAE",
}

DARK_THEME = {
    "bg": "#2F3A3C",
    "surface": "#344244",
    "surface_strong": "#3E4D4F",
    "border": "#6C7A7D",
    "text": "#F7F4EE",
    "text_soft": "#D9D4C8",
    "accent": "#83B8BE",
    "accent_soft": "#A9CED2",
    "highlight": "#ECA159",
    "danger": "#FF5E57",
    "hover": "#497379",
    "sidebar_bg": "#497379",
    "sidebar_text": "#F7F4EE",
    "sidebar_text_soft": "#E8E1D5",
    "sidebar_border": "#6C7A7D",
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
                <p>Structural planner first. Product hubs visible. Worksheets generated from stage, format, tier, and product-set logic.</p>
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
    elif st.session_state.surface == "Instruction Planner":
        _render_instruction_planner(st.session_state.selected_product)
    elif st.session_state.surface == "Worksheet Studio":
        _render_worksheet_studio()
    elif st.session_state.surface == "Number Line Doubler":
        render_number_line_doubler_page()
    else:
        _render_structural_planner(st.session_state.selected_product)

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# STATE
# -----------------------------
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

    if "selected_stage" not in st.session_state:
        st.session_state.selected_stage = product_record(st.session_state.selected_product).stage

    if "worksheet_format" not in st.session_state:
        st.session_state.worksheet_format = "one_product_10"

    if "selection_scope" not in st.session_state:
        st.session_state.selection_scope = "new_only"

    if "selection_mode" not in st.session_state:
        st.session_state.selection_mode = "Auto"

    if "include_recap" not in st.session_state:
        st.session_state.include_recap = False

    if "recap_count" not in st.session_state:
        st.session_state.recap_count = 1

    if "worksheet_rotation_index" not in st.session_state:
        st.session_state.worksheet_rotation_index = 0

    if "last_bundle" not in st.session_state:
        st.session_state.last_bundle = None

    if "last_request_signature" not in st.session_state:
        st.session_state.last_request_signature = None


def _sync_surface_from_query_params() -> None:
    requested_surface = st.query_params.get("surface")
    if isinstance(requested_surface, list):
        requested_surface = requested_surface[0] if requested_surface else None

    if requested_surface in SURFACES and requested_surface != st.session_state.surface:
        st.session_state.surface = requested_surface


# -----------------------------
# STYLES
# -----------------------------
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
            }}

            .tmk-shell {{
                max-width: 1480px;
                margin: 0 auto;
                padding-bottom: 3rem;
            }}

            .tmk-header {{
                background: linear-gradient(180deg, var(--tmk-surface-strong) 0%, var(--tmk-surface) 100%);
                border: 1px solid var(--tmk-border);
                border-radius: 20px;
                padding: 1.25rem 1.4rem;
                margin-bottom: 1rem;
                box-shadow: 0 8px 24px rgba(47, 58, 60, 0.05);
            }}

            .tmk-kicker {{
                font-size: 0.84rem;
                font-weight: 800;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                color: var(--tmk-accent);
                margin-bottom: 0.2rem;
            }}

            .tmk-header h1 {{
                margin: 0 0 0.25rem 0;
                color: var(--tmk-text);
                font-size: 2rem;
                line-height: 1.15;
            }}

            .tmk-header p {{
                margin: 0;
                color: var(--tmk-text-soft);
                font-size: 1rem;
            }}

            .tmk-panel {{
                background: var(--tmk-surface);
                border: 1px solid var(--tmk-border);
                border-radius: 20px;
                padding: 1.1rem 1.2rem;
                margin-bottom: 1rem;
                box-shadow: 0 6px 18px rgba(47, 58, 60, 0.04);
            }}

            .tmk-card {{
                background: var(--tmk-surface-strong);
                border: 1px solid var(--tmk-border);
                border-radius: 18px;
                padding: 0.95rem 1rem;
                margin-bottom: 0.9rem;
            }}

            .tmk-answer-box {{
                background: var(--tmk-surface);
                border: 1px solid var(--tmk-border);
                border-radius: 16px;
                padding: 0.85rem 0.95rem;
                margin-bottom: 0.75rem;
            }}

            .tmk-section-title {{
                font-size: 1.25rem;
                font-weight: 800;
                color: var(--tmk-text);
                margin-bottom: 0.2rem;
            }}

            .tmk-section-subtitle {{
                color: var(--tmk-text-soft);
                margin-bottom: 1rem;
            }}

            .tmk-small-label {{
                font-size: 0.78rem;
                font-weight: 800;
                letter-spacing: 0.04em;
                text-transform: uppercase;
                color: var(--tmk-accent);
                margin-bottom: 0.25rem;
            }}

            .tmk-value {{
                font-size: 1.1rem;
                font-weight: 800;
                color: var(--tmk-text);
                line-height: 1.3;
            }}

            .tmk-note {{
                color: var(--tmk-text-soft);
                line-height: 1.45;
            }}

            .tmk-pill {{
                display: inline-block;
                padding: 0.18rem 0.58rem;
                border-radius: 999px;
                border: 1px solid var(--tmk-border);
                background: var(--tmk-surface);
                color: var(--tmk-text);
                font-size: 0.86rem;
                margin: 0.1rem 0.25rem 0.1rem 0;
                font-weight: 700;
            }}

            .tmk-pill-accent {{
                border-color: var(--tmk-highlight);
                background: color-mix(in srgb, var(--tmk-highlight) 16%, var(--tmk-surface-strong) 84%);
                color: var(--tmk-text);
            }}

            .tmk-soft-list {{
                line-height: 1.8;
            }}

            .tmk-worksheet-frame {{
                background: var(--tmk-surface);
                border: 1px solid var(--tmk-border);
                border-radius: 20px;
                padding: 1rem;
                margin-top: 1rem;
                box-shadow: 0 6px 18px rgba(47, 58, 60, 0.04);
            }}

            section[data-testid="stSidebar"] {{
                background: var(--tmk-sidebar-bg);
                border-right: 1px solid var(--tmk-sidebar-border);
            }}

            section[data-testid="stSidebar"] * {{
                color: var(--tmk-sidebar-text);
            }}

            section[data-testid="stSidebar"] hr {{
                border-color: var(--tmk-sidebar-border);
            }}

            section[data-testid="stSidebar"] .stMarkdown,
            section[data-testid="stSidebar"] .stText,
            section[data-testid="stSidebar"] p,
            section[data-testid="stSidebar"] li,
            section[data-testid="stSidebar"] span,
            section[data-testid="stSidebar"] label,
            section[data-testid="stSidebar"] div {{
                color: var(--tmk-sidebar-text);
            }}

            section[data-testid="stSidebar"] .stSelectbox label,
            section[data-testid="stSidebar"] .stRadio label,
            section[data-testid="stSidebar"] .stCheckbox label,
            section[data-testid="stSidebar"] .stNumberInput label {{
                color: var(--tmk-sidebar-text) !important;
            }}

            section[data-testid="stSidebar"] h1,
            section[data-testid="stSidebar"] h2,
            section[data-testid="stSidebar"] h3,
            section[data-testid="stSidebar"] h4,
            section[data-testid="stSidebar"] h5,
            section[data-testid="stSidebar"] h6 {{
                color: var(--tmk-sidebar-text) !important;
            }}

            .stButton > button {{
                border-radius: 12px;
                border: 1px solid var(--tmk-border);
            }}

            .stButton > button[kind="primary"] {{
                background: var(--tmk-danger);
                border-color: var(--tmk-danger);
                color: #FFFFFF;
            }}

            .stButton > button[kind="secondary"] {{
                background: var(--tmk-surface-strong);
                color: var(--tmk-text);
                border-color: var(--tmk-border);
            }}

            .stSelectbox div[data-baseweb="select"] > div,
            .stMultiSelect div[data-baseweb="select"] > div,
            .stNumberInput input,
            .stTextInput input,
            .stTextArea textarea {{
                background: var(--tmk-surface-strong);
                border-color: var(--tmk-border);
                color: var(--tmk-text);
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _theme_css_vars(theme: dict[str, str]) -> str:
    return "\n".join(
        [
            f"--tmk-bg: {theme['bg']};",
            f"--tmk-surface: {theme['surface']};",
            f"--tmk-surface-strong: {theme['surface_strong']};",
            f"--tmk-border: {theme['border']};",
            f"--tmk-text: {theme['text']};",
            f"--tmk-text-soft: {theme['text_soft']};",
            f"--tmk-accent: {theme['accent']};",
            f"--tmk-accent-soft: {theme['accent_soft']};",
            f"--tmk-highlight: {theme['highlight']};",
            f"--tmk-danger: {theme['danger']};",
            f"--tmk-hover: {theme['hover']};",
            f"--tmk-sidebar-bg: {theme['sidebar_bg']};",
            f"--tmk-sidebar-text: {theme['sidebar_text']};",
            f"--tmk-sidebar-text-soft: {theme['sidebar_text_soft']};",
            f"--tmk-sidebar-border: {theme['sidebar_border']};",
        ]
    )


# -----------------------------
# NAV / SIDEBAR
# -----------------------------
def _render_nav() -> None:
    nav_cols = st.columns(len(SURFACES))

    for idx, surface in enumerate(SURFACES):
        button_type = "primary" if surface == st.session_state.surface else "secondary"
        widget_key = f"tmk_top_nav_{idx}_{surface.lower().replace(' ', '_')}"

        if nav_cols[idx].button(
            surface,
            key=widget_key,
            use_container_width=True,
            type=button_type,
        ):
            st.session_state.surface = surface
            st.query_params["surface"] = surface
            st.rerun()


def _render_sidebar() -> None:
    with st.sidebar:
        record = product_record(st.session_state.selected_product)

        st.markdown("## TMK context")
        st.write(f"**Surface:** {st.session_state.surface}")
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
        elif st.session_state.surface == "Instruction Planner":
            st.write("**Focus:** explanation and vocabulary")
            st.write(f"**Current stage:** {stage_label(record.stage)}")
        elif st.session_state.surface == "Worksheet Studio":
            st.write(f"**Worksheet stage:** {stage_label(st.session_state.selected_stage)}")
            st.write(f"**Tier:** {st.session_state.selected_tier}")
            st.write(f"**Format:** {st.session_state.worksheet_format}")
            st.write(f"**Scope:** {st.session_state.selection_scope}")
            if st.session_state.selection_mode != "Auto":
                st.write(f"**Mode:** {st.session_state.selection_mode}")
            st.write(f"**Recap:** {'On' if st.session_state.include_recap else 'Off'}")
        elif st.session_state.surface == "Number Line Doubler":
            st.write("**Focus:** animated doubling race")
            st.write("**Asset type:** embedded HTML game")
            st.write("**TMK link:** doubling chain visual")
        else:
            st.write("**Status:** ready")


# -----------------------------
# STRUCTURAL PLANNER
# -----------------------------
def _render_structural_planner(product: int) -> None:
    record = product_record(product)
    current_stage_products = tuple(STAGES[record.stage].products)
    new_stage_products = tuple(metadata_new_products(record.stage))
    earlier_secured_products = tuple(
        value for value in metadata_available_products(record.stage) if value not in current_stage_products
    )

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Structural Planner</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Stage focus, products introduced at this stage, compact stage sequence, and cumulative support products.</div>',
        unsafe_allow_html=True,
    )

    control_col1, control_col2, control_col3 = st.columns(3)

    with control_col1:
        selected = st.selectbox(
            "Selected product",
            options=ALL_PRODUCTS,
            index=ALL_PRODUCTS.index(st.session_state.selected_product),
            format_func=_product_option_label,
            key="planner_product_select_v20",
        )
        if selected != st.session_state.selected_product:
            st.session_state.selected_product = selected
            st.session_state.selected_stage = product_record(selected).stage
            st.rerun()

    with control_col2:
        mode = st.selectbox(
            "Link mode",
            options=PLANNER_LINK_MODES,
            index=PLANNER_LINK_MODES.index(st.session_state.planner_link_mode),
            key="planner_link_mode_select_v20",
        )
        if mode != st.session_state.planner_link_mode:
            st.session_state.planner_link_mode = mode
            st.rerun()

    with control_col3:
        zoom = st.selectbox(
            "Planner zoom",
            options=PLANNER_ZOOM_MODES,
            index=PLANNER_ZOOM_MODES.index(st.session_state.planner_zoom_mode),
            key="planner_zoom_mode_select_v20",
        )
        if zoom != st.session_state.planner_zoom_mode:
            st.session_state.planner_zoom_mode = zoom
            st.rerun()

    _metric_card_row(
        [
            ("Current stage", stage_label(record.stage)),
            ("Selected product", str(record.product)),
            ("Intro route", _format_route(record.intro_route)),
            ("New here", str(len(new_stage_products))),
        ]
    )

    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Stage focus</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tmk-value">{escape(stage_label(record.stage))}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tmk-note" style="margin-top:0.35rem;">Selected product: {record.product}. Intro route: {escape(_format_route(record.intro_route))}. Structural role: {escape(record.structural_role)}.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="tmk-note" style="margin-top:0.5rem;">Products introduced in this stage: {escape(", ".join(str(value) for value in new_stage_products) if new_stage_products else "None")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tmk-note" style="margin-top:0.5rem;">Teacher warning: keep first exposure focused on current-stage products before opening cumulative support.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    col_a, col_b = st.columns((1.35, 0.85))

    with col_a:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Products introduced in this stage</div>', unsafe_allow_html=True)
        _render_pill_list(current_stage_products, selected=record.product)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        _render_stage_cards(record.stage)

    with st.expander("Earlier secured products available for support", expanded=False):
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Earlier secured products</div>', unsafe_allow_html=True)
        if earlier_secured_products:
            _render_pill_list(earlier_secured_products, selected=record.product)
        else:
            st.markdown('<div class="tmk-note">No earlier secured products available.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def _render_stage_cards(current_stage: str) -> None:
    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Stage sequence</div>', unsafe_allow_html=True)

    for stage in [stage for stage in STAGE_ORDER if stage in STAGES]:
        stage_record = STAGES[stage]
        is_current = stage == current_stage
        stage_name = stage_label(stage)
        product_count = len(stage_record.products)
        marker = "Current stage" if is_current else f"{product_count} products"

        note_style = "margin-top:0.2rem;"
        if is_current:
            note_style = "margin-top:0.2rem;font-weight:700;color:var(--tmk-accent);"

        st.markdown(
            f"""
            <div class="tmk-answer-box">
                <div class="tmk-value">{escape(stage_record.label)}</div>
                <div class="tmk-note" style="margin-top:0.2rem;">{escape(stage_name)}</div>
                <div class="tmk-note" style="{note_style}">{escape(marker)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# PRODUCT LAB
# -----------------------------
def _render_product_lab(product: int) -> None:
    record = product_record(product)
    compare = product_record(st.session_state.compare_product)
    selected_routes = tuple(distinct_factor_routes(record.product))
    compare_routes = tuple(distinct_factor_routes(compare.product))
    inverse_family = tuple(inverse_labels(record.product))
    shared = tuple(shared_factors(record.product, compare.product))

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Product Lab</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Selected product first, with local routes, inverse family, whole-product context, and controlled comparison.</div>',
        unsafe_allow_html=True,
    )

    control_col1, control_col2, control_col3 = st.columns(3)

    with control_col1:
        selected = st.selectbox(
            "Selected product",
            options=ALL_PRODUCTS,
            index=ALL_PRODUCTS.index(st.session_state.selected_product),
            format_func=_product_option_label,
            key="lab_product_select_v20",
        )
        if selected != st.session_state.selected_product:
            st.session_state.selected_product = selected
            st.session_state.selected_stage = product_record(selected).stage
            if st.session_state.compare_product == selected and len(ALL_PRODUCTS) > 1:
                st.session_state.compare_product = next(item for item in ALL_PRODUCTS if item != selected)
            st.session_state.selected_route_index = 0
            st.rerun()

    compare_options = [item for item in ALL_PRODUCTS if item != st.session_state.selected_product]
    if st.session_state.compare_product not in compare_options:
        st.session_state.compare_product = compare_options[0]
        compare = product_record(st.session_state.compare_product)
        compare_routes = tuple(distinct_factor_routes(compare.product))
        shared = tuple(shared_factors(record.product, compare.product))

    with control_col2:
        compare_value = st.selectbox(
            "Compare with",
            options=compare_options,
            index=compare_options.index(st.session_state.compare_product),
            format_func=_product_option_label,
            key="lab_compare_select_v20",
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
            key="lab_route_view_mode_v20",
        )
        if mode != st.session_state.route_view_mode:
            st.session_state.route_view_mode = mode
            st.session_state.selected_route_index = 0
            st.rerun()

    _metric_card_row(
        [
            ("Selected product", str(record.product)),
            ("Stage", stage_label(record.stage)),
            ("Intro route", _format_route(record.intro_route)),
            ("Compare with", str(compare.product)),
        ]
    )

    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Selected product</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tmk-value">{record.product}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tmk-note" style="margin-top:0.35rem;">Intro route: {escape(_format_route(record.intro_route))}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="tmk-note">Structural role: {escape(record.structural_role)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="tmk-note">Stage introduced: {escape(stage_label(record.stage))}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tmk-note" style="margin-top:0.5rem;">Teaching order note: lead with the intro route before opening wider route comparison.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    col_a, col_b = st.columns((1.3, 0.7))

    with col_a:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Radial hub</div>', unsafe_allow_html=True)
        _render_route_inspector(record.product)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Inverse family</div>', unsafe_allow_html=True)
        if inverse_family:
            for label in inverse_family:
                st.markdown(f'<div class="tmk-answer-box">{escape(_stringify(label))}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="tmk-note">No inverse family available.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    _render_structure_explorer(record.product, compare.product)

    lower_left, lower_right = st.columns((1.0, 1.0))

    with lower_left:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Connected products</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="tmk-note">Shared factors with {compare.product}: {escape(", ".join(str(value) for value in shared) if shared else "None")}</div>',
            unsafe_allow_html=True,
        )

        connected_products = _connected_products_for(record.product, compare.product)
        if connected_products:
            _render_pill_list(connected_products, selected=record.product)
        else:
            st.markdown('<div class="tmk-note">No connected products available.</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with lower_right:
        with st.expander("Additional lawful forms", expanded=False):
            st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
            st.markdown('<div class="tmk-small-label">Additional lawful forms</div>', unsafe_allow_html=True)

            commutative = _commutative_form(record.intro_route)
            st.markdown(
                f'<div class="tmk-note"><strong>Commutative form:</strong> {escape(commutative)}</div>',
                unsafe_allow_html=True,
            )

            comparison_route = _comparison_route_text(compare_routes)
            st.markdown(
                f'<div class="tmk-note" style="margin-top:0.35rem;"><strong>Later comparison route:</strong> {escape(comparison_route)}</div>',
                unsafe_allow_html=True,
            )

            if inverse_family:
                st.markdown('<div class="tmk-note" style="margin-top:0.35rem;"><strong>Inverse family:</strong></div>', unsafe_allow_html=True)
                for label in inverse_family:
                    st.markdown(f'<div class="tmk-answer-box">{escape(_stringify(label))}</div>', unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Selected product routes", expanded=False):
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Selected product routes</div>', unsafe_allow_html=True)
        for route in selected_routes:
            st.markdown(
                f'<div class="tmk-answer-box">{escape(_format_route(route))}</div>',
                unsafe_allow_html=True,
            )
        if not selected_routes:
            st.markdown('<div class="tmk-note">No routes available.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Compare product routes", expanded=False):
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Compare product routes</div>', unsafe_allow_html=True)
        for route in compare_routes:
            st.markdown(
                f'<div class="tmk-answer-box">{escape(_format_route(route))}</div>',
                unsafe_allow_html=True,
            )
        if not compare_routes:
            st.markdown('<div class="tmk-note">No routes available.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def _render_route_inspector(product: int) -> None:
    items = _route_items_for_product(product, st.session_state.route_view_mode)
    if not items:
        st.markdown('<div class="tmk-note">No routes available.</div>', unsafe_allow_html=True)
        return

    if st.session_state.selected_route_index >= len(items):
        st.session_state.selected_route_index = 0

    button_cols = st.columns(min(4, len(items)))
    for index, item in enumerate(items):
        col = button_cols[index % len(button_cols)]
        button_type = "primary" if index == st.session_state.selected_route_index else "secondary"
        if col.button(
            item["label"],
            key=f"route_inspector_button_{st.session_state.route_view_mode}_{index}",
            use_container_width=True,
            type=button_type,
        ):
            st.session_state.selected_route_index = index
            st.rerun()

    selected_item = items[st.session_state.selected_route_index]

    title = st.session_state.route_view_mode[:-1] if st.session_state.route_view_mode.endswith("s") else st.session_state.route_view_mode
    st.markdown(f'<div class="tmk-small-label">{escape(title)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tmk-value">{escape(selected_item["headline"])}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tmk-note" style="margin-top:0.55rem;">{escape(selected_item["explanation"])}</div>',
        unsafe_allow_html=True,
    )


def _route_items_for_product(product: int, mode: str) -> list[dict[str, str]]:
    if mode == "Entry routes":
        items: list[dict[str, str]] = []
        for route in entry_routes(product):
            label = _format_route(route)
            items.append(
                {
                    "label": label,
                    "headline": label,
                    "explanation": f"Multiplication route into {product}.",
                }
            )
        return items

    items = []
    for label in exit_route_labels(product):
        items.append(
            {
                "label": _stringify(label),
                "headline": _stringify(label),
                "explanation": f"Division route out from {product}.",
            }
        )
    return items


def _render_structure_explorer(selected_product: int, compare_product: int) -> None:
    selected_record = product_record(selected_product)
    compare_record = product_record(compare_product)

    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Structure explorer</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tmk-note">Selected product {selected_product} sits in {escape(stage_label(selected_record.stage))}. Comparison product {compare_product} sits in {escape(stage_label(compare_record.stage))}.</div>',
        unsafe_allow_html=True,
    )

    for stage in [stage for stage in STAGE_ORDER if stage in STAGES]:
        marker = ""
        if stage == selected_record.stage and stage == compare_record.stage:
            marker = "Selected and compare stage"
        elif stage == selected_record.stage:
            marker = "Selected product stage"
        elif stage == compare_record.stage:
            marker = "Compare product stage"

        st.markdown('<div class="tmk-answer-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="tmk-value">{escape(STAGES[stage].label)}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="tmk-note" style="margin-top:0.2rem;">{escape(stage_label(stage))}</div>', unsafe_allow_html=True)

        if marker:
            st.markdown(f'<div class="tmk-note" style="margin-top:0.2rem;">{escape(marker)}</div>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top:0.45rem;">', unsafe_allow_html=True)
        _render_pill_list(STAGES[stage].products, selected=selected_product)
        st.markdown('</div>', unsafe_allow_html=True)

        if compare_product in STAGES[stage].products and compare_product != selected_product:
            st.markdown(
                f'<div class="tmk-note" style="margin-top:0.35rem;">Compare product highlighted by stage context: {compare_product}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def _render_instruction_planner(product: int) -> None:
    render_instruction_planner_page(
        _build_instruction_planner_view_model(product)
    )


def _build_instruction_planner_view_model(product: int) -> dict[str, Any]:
    record = product_record(product)
    stage_record = get_stage_vocabulary(record.stage)
    intro_left, intro_right = record.intro_route

    return {
        "title": "Instruction Planner",
        "subtitle": "Teacher explanation flow, stage vocabulary, teacher prompts, and example questions for the current product.",
        "selected_product": record.product,
        "selected_stage_label": stage_label(record.stage),
        "intro_route_label": _format_route(record.intro_route),
        "product_options": ALL_PRODUCTS,
        "selected_product_index": ALL_PRODUCTS.index(st.session_state.selected_product),
        "product_format_func": _product_option_label,
        "product_select_key": "instruction_product_select_v20",
        "on_product_change": _on_instruction_product_change,
        "explanation_steps": _build_explanation_sequence(record.product, intro_left, intro_right),
        "teach_now_vocab": list(getattr(stage_record, "new_vocab", ()) or ()),
        "teacher_prompts": _build_teacher_prompts(record.product, intro_left, intro_right),
        "introduce_if_needed": list(getattr(stage_record, "available_vocab", ()) or ()),
        "example_questions": _instruction_example_questions(stage_record, record.product, intro_left, intro_right),
        "delay_vocab": list(getattr(stage_record, "required_vocab_focus", ()) or ()),
        "teaching_warning": "Do not open route comparison or wider product-network discussion until the entry explanation is secure.",
    }


def _on_instruction_product_change() -> None:
    selected = st.session_state.get("instruction_product_select_v20")
    if selected in ALL_PRODUCTS and selected != st.session_state.selected_product:
        st.session_state.selected_product = selected
        st.session_state.selected_stage = product_record(selected).stage


def _connected_products_for(selected_product: int, compare_product: int) -> tuple[int, ...]:
    connected: list[int] = []
    selected_factors = set(shared_factors(selected_product, selected_product))
    compare_shared = set(shared_factors(selected_product, compare_product))

    for product in ALL_PRODUCTS:
        if product == selected_product:
            continue
        product_shared = set(shared_factors(selected_product, product))
        if product_shared & (selected_factors | compare_shared):
            connected.append(product)

    deduped = []
    seen = set()
    for product in connected:
        if product not in seen:
            seen.add(product)
            deduped.append(product)

    return tuple(deduped[:12])


def _commutative_form(route: tuple[int, int]) -> str:
    return f"{route[1]} × {route[0]}"


def _comparison_route_text(compare_routes: tuple[tuple[int, int], ...]) -> str:
    if not compare_routes:
        return "No comparison route available."
    return _format_route(compare_routes[0])


def _build_explanation_sequence(product: int, left: int, right: int) -> list[str]:
    if right == 9:
        base = left
        ten_value = base * 10
        one_value = base
        return [
            f"What is 10 × {base}?",
            f"What is 1 × {base}?",
            f"What is {ten_value} − {one_value}?",
            f"So what is 9 × {base}?",
        ]

    if left == 9:
        base = right
        ten_value = base * 10
        one_value = base
        return [
            f"What is 10 × {base}?",
            f"What is 1 × {base}?",
            f"What is {ten_value} − {one_value}?",
            f"So what is 9 × {base}?",
        ]

    return [
        f"State the intro route: {_format_route((left, right))}.",
        f"Identify the product: {product}.",
        f"Explain how {_format_route((left, right))} builds {product}.",
        f"Check the product again: {product}.",
    ]


def _build_teacher_prompts(product: int, left: int, right: int) -> list[str]:
    prompts = [
        f"What do we already know about {_format_route((left, right))}?",
        f"What product are we building?",
        f"How can we say {_format_route((left, right))} clearly?",
    ]

    if right == 9 or left == 9:
        base = left if right == 9 else right
        prompts.extend(
            [
                f"What is 10 groups of {base}?",
                f"How do we adjust from 10× to 9×?",
            ]
        )

    return prompts


def _instruction_example_questions(stage_record: Any, product: int, left: int, right: int) -> list[str]:
    from_stage = list(getattr(stage_record, "example_child_friendly_questions", []) or [])
    if from_stage:
        return [str(item) for item in from_stage]

    return [
        f"{left} × {right} = □",
        f"□ = {product}",
        f"{product} ÷ {left} = □",
    ]


# -----------------------------
# WORKSHEET STUDIO
# -----------------------------
def _render_worksheet_studio() -> None:
    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Worksheet Studio</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Configure the worksheet first, then generate and review the selected product set, pupil sheet, rationale, teacher key, vocabulary, and structural tags.</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Worksheet configuration</div>', unsafe_allow_html=True)

    top_left, top_mid, top_right = st.columns(3)
    bottom_left, bottom_mid, bottom_right = st.columns(3)

    with top_left:
        selected_stage = st.selectbox(
            "Worksheet stage",
            options=STAGE_ORDER,
            index=STAGE_ORDER.index(st.session_state.selected_stage),
            format_func=stage_label,
            key="worksheet_stage_select_v20",
        )
        if selected_stage != st.session_state.selected_stage:
            st.session_state.selected_stage = selected_stage
            st.session_state.selection_mode = "Auto"
            _invalidate_worksheet_bundle()
            st.rerun()

    with top_mid:
        selected_format = st.selectbox(
            "Worksheet format",
            options=WORKSHEET_FORMATS,
            index=WORKSHEET_FORMATS.index(st.session_state.worksheet_format),
            key="worksheet_format_select_v20",
            format_func=lambda value: "One product (10)" if value == "one_product_10" else "Three products (12)",
        )
        if selected_format != st.session_state.worksheet_format:
            st.session_state.worksheet_format = selected_format
            st.session_state.selection_mode = "Auto"
            _invalidate_worksheet_bundle()
            st.rerun()

    with top_right:
        selected_tier = st.radio(
            "Worksheet tier",
            options=TIERS,
            index=TIERS.index(st.session_state.selected_tier),
            horizontal=True,
            key="worksheet_tier_radio_v20",
        )
        if selected_tier != st.session_state.selected_tier:
            st.session_state.selected_tier = selected_tier
            st.session_state.selection_mode = "Auto"
            _invalidate_worksheet_bundle()
            st.rerun()

    with bottom_left:
        selected_scope = st.selectbox(
            "Selection scope",
            options=SELECTION_SCOPES,
            index=SELECTION_SCOPES.index(st.session_state.selection_scope),
            key="worksheet_scope_select_v20",
        )
        if selected_scope != st.session_state.selection_scope:
            st.session_state.selection_scope = selected_scope
            st.session_state.selection_mode = "Auto"
            _invalidate_worksheet_bundle()
            st.rerun()

    mode_options = ("Auto",) + available_selection_modes(
        stage=st.session_state.selected_stage,
        format_id=st.session_state.worksheet_format,
        tier=st.session_state.selected_tier,
    )

    with bottom_mid:
        if st.session_state.selection_mode not in mode_options:
            st.session_state.selection_mode = "Auto"

        selected_mode = st.selectbox(
            "Selection mode",
            options=mode_options,
            index=mode_options.index(st.session_state.selection_mode),
            key="worksheet_mode_select_v20",
        )
        if selected_mode != st.session_state.selection_mode:
            st.session_state.selection_mode = selected_mode
            _invalidate_worksheet_bundle()
            st.rerun()

    with bottom_right:
        include_recap = st.checkbox(
            "Include recap products",
            value=st.session_state.include_recap,
            key="worksheet_include_recap_v20",
        )
        if include_recap != st.session_state.include_recap:
            st.session_state.include_recap = include_recap
            if include_recap and int(st.session_state.recap_count) < 1:
                st.session_state.recap_count = 1
            if not include_recap:
                st.session_state.recap_count = 0
            _invalidate_worksheet_bundle()
            st.rerun()

        if st.session_state.include_recap:
            recap_count = st.number_input(
                "Recap count",
                min_value=1,
                max_value=3,
                value=int(st.session_state.recap_count),
                step=1,
                key="worksheet_recap_count_v20",
            )
            if int(recap_count) != int(st.session_state.recap_count):
                st.session_state.recap_count = int(recap_count)
                _invalidate_worksheet_bundle()
                st.rerun()

    request = _build_product_selection_request()
    request_signature = _worksheet_request_signature(request)

    if st.session_state.last_request_signature != request_signature:
        st.session_state.last_bundle = None

    generate_label = "Generate worksheet" if st.session_state.worksheet_rotation_index == 0 else "Generate next worksheet"

    st.markdown(
        f'<div class="tmk-note" style="margin-top:0.35rem;">Current setup: {escape(stage_label(st.session_state.selected_stage))} · {escape("One product (10)" if st.session_state.worksheet_format == "one_product_10" else "Three products (12)")} · {escape(st.session_state.selected_tier)} · {escape(st.session_state.selection_scope)}</div>',
        unsafe_allow_html=True,
    )

    if st.button(generate_label, type="primary", key="worksheet_generate_button_v20"):
        try:
            previous_bundle = st.session_state.last_bundle
            previous_selection = _bundle_part(previous_bundle, "selection") if previous_bundle else None
            previous_products = tuple(_field(previous_selection, "selected_products", default=())) if previous_selection else ()

            new_bundle = None
            new_request_signature = None
            found_different = False
            last_candidate_bundle = None
            last_candidate_signature = None

            for _ in range(12):
                current_request = _build_product_selection_request()
                current_signature = _worksheet_request_signature(current_request)

                candidate_bundle = generate_worksheet_bundle(current_request)
                candidate_selection = _bundle_part(candidate_bundle, "selection")
                candidate_products = tuple(_field(candidate_selection, "selected_products", default=()))

                last_candidate_bundle = candidate_bundle
                last_candidate_signature = current_signature

                if not previous_products or candidate_products != previous_products:
                    new_bundle = candidate_bundle
                    new_request_signature = current_signature
                    found_different = True
                    break

                st.session_state.worksheet_rotation_index += 1

            if new_bundle is None:
                new_bundle = last_candidate_bundle
                new_request_signature = last_candidate_signature

            st.session_state.last_bundle = new_bundle
            st.session_state.last_request_signature = new_request_signature

            st.session_state.worksheet_rotation_index += 1

            if previous_products and not found_different:
                st.warning(
                    "No different selected product set was available for this exact configuration. "
                    "Try changing selection mode or scope."
                )

        except Exception as exc:
            msg = str(exc)
            if "No valid" in msg or "no valid" in msg:
                st.info(
                    "No worksheet can be generated for this combination. "
                    "Try a different selection mode or scope."
                )
            else:
                st.error(f"Worksheet generation failed: {exc}")
            st.markdown("</div>", unsafe_allow_html=True)
            return

    st.markdown("</div>", unsafe_allow_html=True)

    bundle = st.session_state.last_bundle
    if bundle is None:
        st.markdown(
            '<div class="tmk-note">Choose a stage and options, then generate a worksheet.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        return

    selection = _bundle_part(bundle, "selection")
    student = _bundle_part(bundle, "student", "student_worksheet")
    teacher = _bundle_part(bundle, "teacher", "teacher_key")

    selected_products = tuple(_field(selection, "selected_products", default=()))
    recap_products = tuple(_field(selection, "recap_products", default=()))
    vocab_supported = tuple(_field(selection, "vocab_supported", default=()))
    structural_tags = tuple(_field(selection, "structural_tags", default=()))
    selection_reasons = tuple(
        _field(
            selection,
            "selection_reasons",
            "reasons",
            "rationale",
            default=(),
        )
    )

    _metric_card_row(
        [
            ("Stage", stage_label(st.session_state.selected_stage)),
            ("Format", "10Q" if st.session_state.worksheet_format == "one_product_10" else "12Q"),
            ("Selected products", ", ".join(str(v) for v in selected_products) if selected_products else "—"),
            ("Recap", ", ".join(str(v) for v in recap_products) if recap_products else "None"),
        ]
    )

    upper_left, upper_right = st.columns((0.95, 1.05))

    with upper_left:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Selected product set</div>', unsafe_allow_html=True)
        if selected_products:
            _render_pill_list(selected_products)
        else:
            st.markdown('<div class="tmk-note">No selected products available.</div>', unsafe_allow_html=True)

        if recap_products:
            st.markdown('<div class="tmk-small-label" style="margin-top:0.7rem;">Recap products</div>', unsafe_allow_html=True)
            _render_pill_list(recap_products)
        else:
            st.markdown('<div class="tmk-note" style="margin-top:0.45rem;">No recap products included.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with upper_right:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Structural audit</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="tmk-note"><strong>Stage integrity:</strong> {escape(stage_label(st.session_state.selected_stage))}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="tmk-note"><strong>Selection mode:</strong> {escape(st.session_state.selection_mode)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="tmk-note"><strong>Selection scope:</strong> {escape(st.session_state.selection_scope)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="tmk-note"><strong>Recap included:</strong> {escape("Yes" if st.session_state.include_recap else "No")}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="tmk-note"><strong>Rotation index:</strong> {escape(str(st.session_state.worksheet_rotation_index))}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    lower_left, lower_right = st.columns((1.15, 0.85))

    with lower_left:
        st.markdown('<div class="tmk-worksheet-frame">', unsafe_allow_html=True)
        st.markdown("### Output preview")
        st.markdown('<div class="tmk-small-label">Pupil worksheet</div>', unsafe_allow_html=True)
        questions = list(_field(student, "questions", default=[]))
        for index, question in enumerate(questions, start=1):
            q_id = _field(question, "q_id", default=index)
            prompt = _field(question, "prompt", "question", default="")
            st.markdown(
                f"""
                <div class="tmk-answer-box">
                    <div class="tmk-small-label">Q{q_id}</div>
                    <div style="font-size:1.02rem;font-weight:700;color:inherit;line-height:1.5;">{escape(_stringify(prompt))}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="tmk-worksheet-frame">', unsafe_allow_html=True)
        st.markdown("### Selection rationale")
        if selection_reasons:
            for reason in selection_reasons:
                st.markdown(
                    f'<div class="tmk-answer-box">{escape(_stringify(reason))}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown('<div class="tmk-note">No selection reasons available.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with lower_right:
        st.markdown('<div class="tmk-worksheet-frame">', unsafe_allow_html=True)
        st.markdown("### Teacher key")
        answers = list(_field(teacher, "answers", default=[]))
        for index, answer in enumerate(answers, start=1):
            q_id = _field(answer, "q_id", default=index)
            answer_text = _field(answer, "answer", default="")
            focus_tags = _field(answer, "focus_tags", "structural_focus", "msvwa", "msvwa_tags", default=())
            teacher_note = _field(answer, "teacher_note", "note", default="")
            vocab = _field(answer, "vocab", "vocabulary_words", default=None)

            tags_text = ", ".join(str(tag) for tag in _coerce_sequence(focus_tags)) if focus_tags else "—"

            vocab_text = ""
            if vocab:
                vocab_items = _coerce_sequence(vocab)
                vocab_text = f"<div class='tmk-note'><strong>Vocab:</strong> {escape(', '.join(str(v) for v in vocab_items))}</div>"

            st.markdown(
                f"""
                <div class="tmk-answer-box">
                    <div class="tmk-small-label">Q{q_id}</div>
                    <div><strong>Answer:</strong> {escape(_stringify(answer_text))}</div>
                    <div class="tmk-note"><strong>Focus:</strong> {escape(tags_text)}</div>
                    {vocab_text}
                    <div class="tmk-note" style="margin-top:0.35rem;">{escape(_stringify(teacher_note))}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="tmk-worksheet-frame">', unsafe_allow_html=True)
        st.markdown("### Supported vocabulary")
        if vocab_supported:
            _render_word_list(vocab_supported)
        else:
            st.markdown('<div class="tmk-note">No vocabulary summary available.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="tmk-worksheet-frame">', unsafe_allow_html=True)
        st.markdown("### Structural tags")
        if structural_tags:
            _render_word_list(structural_tags)
        else:
            st.markdown('<div class="tmk-note">No structural tag summary available.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# HELPERS
# -----------------------------
def _build_product_selection_request() -> ProductSelectionRequest:
    payload = {
        "stage": st.session_state.selected_stage,
        "stage_id": st.session_state.selected_stage,
        "format_id": st.session_state.worksheet_format,
        "worksheet_format": st.session_state.worksheet_format,
        "tier": st.session_state.selected_tier,
        "selection_scope": st.session_state.selection_scope,
        "scope": st.session_state.selection_scope,
        "selection_mode": None if st.session_state.selection_mode == "Auto" else st.session_state.selection_mode,
        "mode": None if st.session_state.selection_mode == "Auto" else st.session_state.selection_mode,
        "include_recap": bool(st.session_state.include_recap),
        "recap_count": int(st.session_state.recap_count) if bool(st.session_state.include_recap) else 0,
        "rotation_index": int(st.session_state.worksheet_rotation_index),
    }

    try:
        import inspect

        signature = inspect.signature(ProductSelectionRequest)
        supported = {
            name: value
            for name, value in payload.items()
            if name in signature.parameters and value is not None
        }
        return ProductSelectionRequest(**supported)
    except Exception:
        fallback = {
            key: value
            for key, value in payload.items()
            if value is not None and key in {
                "stage",
                "format_id",
                "tier",
                "selection_scope",
                "selection_mode",
                "include_recap",
                "recap_count",
                "rotation_index",
            }
        }
        return ProductSelectionRequest(**fallback)


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


def _render_pill_list(values: Iterable[Any], selected: Any | None = None) -> None:
    pills: list[str] = []
    for value in values:
        cls = "tmk-pill tmk-pill-accent" if selected is not None and value == selected else "tmk-pill"
        pills.append(f'<span class="{cls}">{escape(_stringify(value))}</span>')
    st.markdown(f'<div class="tmk-soft-list">{"".join(pills)}</div>', unsafe_allow_html=True)


def _render_word_list(values: Iterable[Any]) -> None:
    items = list(values)
    if not items:
        st.markdown('<div class="tmk-note">None</div>', unsafe_allow_html=True)
        return
    _render_pill_list(items)


def _product_option_label(product: int) -> str:
    record = product_record(product)
    return f"{product} · {stage_label(record.stage)}"


def _format_route(route: tuple[int, int]) -> str:
    return f"{route[0]} × {route[1]}"


def _worksheet_request_signature(request: ProductSelectionRequest | dict[str, Any] | Any) -> tuple[tuple[str, str], ...]:
    """
    Signature for worksheet configuration only.

    rotation_index is intentionally excluded so the current worksheet remains
    visible after generation, while the next click rotates to the next set.
    """
    if hasattr(request, "model_dump"):
        payload = request.model_dump()
    elif hasattr(request, "dict"):
        payload = request.dict()
    elif isinstance(request, dict):
        payload = dict(request)
    else:
        payload = {}
        for name in (
            "stage",
            "stage_id",
            "format_id",
            "worksheet_format",
            "tier",
            "selection_scope",
            "scope",
            "selection_mode",
            "mode",
            "include_recap",
            "recap_count",
        ):
            if hasattr(request, name):
                payload[name] = getattr(request, name)

    payload.pop("rotation_index", None)

    normalized: dict[str, str] = {}
    for key, value in payload.items():
        if value is None:
            normalized[key] = ""
        elif isinstance(value, (list, tuple, set)):
            normalized[key] = ",".join(str(item) for item in value)
        else:
            normalized[key] = str(value)

    return tuple(sorted(normalized.items()))


def _invalidate_worksheet_bundle() -> None:
    st.session_state.last_bundle = None
    st.session_state.last_request_signature = None
    st.session_state.worksheet_rotation_index = 0


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _coerce_sequence(value: Any) -> tuple[Any, ...]:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    if isinstance(value, set):
        return tuple(value)
    return (value,)


def _bundle_part(bundle: Any, *names: str) -> Any:
    for name in names:
        if isinstance(bundle, dict) and name in bundle:
            return bundle[name]
        if hasattr(bundle, name):
            return getattr(bundle, name)
    return None


def _field(obj: Any, *names: str, default: Any = None) -> Any:
    if obj is None:
        return default

    for name in names:
        if isinstance(obj, dict) and name in obj:
            return obj[name]
        if hasattr(obj, name):
            return getattr(obj, name)

    return default


if __name__ == "__main__":
    main()
