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

APP_TITLE = "TMK Teacher App"
SURFACES = ("Structural Planner", "Product Lab", "Worksheet Studio")
TIERS = ("Support", "Core", "Extension")
WORKSHEET_FORMATS = ("one_product_10", "three_product_12")
SELECTION_SCOPES = ("new_only", "available_mixed", "hybrid")
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
    else:
        _render_worksheet_studio()

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

            .tmk-shell {{
                max-width: 1480px;
                margin: 0 auto;
                padding-bottom: 3rem;
            }}

            .tmk-header {{
                background: var(--tmk-surface);
                border: 1px solid var(--tmk-border);
                border-radius: 20px;
                padding: 1.25rem 1.4rem;
                margin-bottom: 1rem;
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
            }}

            .tmk-card {{
                background: var(--tmk-surface-strong);
                border: 1px solid var(--tmk-border);
                border-radius: 18px;
                padding: 0.95rem 1rem;
                margin-bottom: 0.9rem;
            }}

            .tmk-answer-box {{
                background: var(--tmk-surface-strong);
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
                border-color: var(--tmk-accent);
                color: var(--tmk-accent);
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
        ]
    )


# -----------------------------
# NAV / SIDEBAR
# -----------------------------
def _render_nav() -> None:
    cols = st.columns(len(SURFACES))
    for idx, surface in enumerate(SURFACES):
        button_type = "primary" if surface == st.session_state.surface else "secondary"
        if cols[idx].button(
            surface,
            key=f"surface_nav_{surface}",
            use_container_width=True,
            type=button_type,
        ):
            st.session_state.surface = surface
            st.query_params["surface"] = surface
            st.rerun()


def _render_sidebar() -> None:
    with st.sidebar:
        record = product_record(st.session_state.selected_product)

        st.markdown("## TMK summary")
        st.write(f"**Product:** {record.product}")
        st.write(f"**Stage:** {stage_label(record.stage)}")
        st.write(f"**Intro route:** {_format_route(record.intro_route)}")
        st.write(f"**Full routes:** {len(distinct_factor_routes(record.product))}")
        st.write(f"**Division exits:** {len(getattr(record, 'ways_out', ()))}")
        st.write(f"**Role:** {record.structural_role}")

        try:
            meta = product_metadata(record.product)
            st.write(f"**Square:** {'Yes' if meta.is_square else 'No'}")
            st.write(f"**Factor 7:** {'Yes' if meta.has_factor_7 else 'No'}")
            st.write(f"**Multiple routes:** {'Yes' if meta.has_multiple_routes else 'No'}")
        except Exception:
            pass

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
            st.write(f"**Stage:** {st.session_state.selected_stage}")
            st.write(f"**Tier:** {st.session_state.selected_tier}")
            st.write(f"**Format:** {st.session_state.worksheet_format}")
            st.write(f"**Scope:** {st.session_state.selection_scope}")
            st.write(f"**Mode:** {st.session_state.selection_mode}")
            st.write(f"**Include recap:** {'Yes' if st.session_state.include_recap else 'No'}")
            if st.session_state.include_recap:
                st.write(f"**Recap count:** {st.session_state.recap_count}")


# -----------------------------
# STRUCTURAL PLANNER
# -----------------------------
def _render_structural_planner(product: int) -> None:
    record = product_record(product)
    admissible_routes = distinct_factor_routes(record.product)
    stage_record = get_stage_vocabulary(record.stage)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Structural Planner</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Fixed stage order, stage introductions, admissible routes, cumulative products, and the stage word bank.</div>',
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
            ("Selected stage", stage_label(record.stage)),
            ("Introduced here", str(len(STAGES[record.stage].products))),
            ("Full routes", str(len(admissible_routes))),
            ("Division exits", str(len(getattr(record, "ways_out", ())))),
        ]
    )

    col_a, col_b = st.columns((1.2, 1.0))

    with col_a:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Selected product</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="tmk-value">{record.product}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="tmk-note">Intro route: {escape(_format_route(record.intro_route))}. Structural role: {escape(record.structural_role)}.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Stage-introduced products</div>', unsafe_allow_html=True)
        _render_pill_list(STAGES[record.stage].products, selected=record.product)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Cumulative available products</div>', unsafe_allow_html=True)
        _render_pill_list(metadata_available_products(record.stage), selected=record.product)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">New products at this stage</div>', unsafe_allow_html=True)
        _render_pill_list(metadata_new_products(record.stage), selected=record.product)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Admissible routes</div>', unsafe_allow_html=True)
        route_labels = [_format_route(route) for route in admissible_routes]
        st.markdown(
            f'<div class="tmk-note">{escape(", ".join(route_labels) if route_labels else "No routes available.")}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        _render_stage_cards(record.product)

        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Word bank</div>', unsafe_allow_html=True)

        st.markdown("**New vocabulary**")
        _render_word_list(stage_record.new_vocab)

        st.markdown("**Available cumulative vocabulary**")
        _render_word_list(stage_record.available_vocab)

        st.markdown("**Required worksheet vocabulary focus**")
        _render_word_list(stage_record.required_vocab_focus)

        st.markdown("**Preferred quiz formats**")
        _render_word_list(stage_record.preferred_quiz_formats)

        st.markdown("**Preferred vocab task types**")
        _render_word_list(stage_record.preferred_vocab_task_types)

        st.markdown("**Example child-friendly questions**")
        for prompt in stage_record.example_child_friendly_questions:
            st.markdown(
                f'<div class="tmk-answer-box">{escape(prompt)}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def _render_stage_cards(selected_product: int) -> None:
    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Stage sequence</div>', unsafe_allow_html=True)

    for stage in [stage for stage in STAGE_ORDER if stage in STAGES]:
        stage_record = STAGES[stage]
        pills: list[str] = []
        for product in stage_record.products:
            cls = "tmk-pill tmk-pill-accent" if product == selected_product else "tmk-pill"
            pills.append(f'<span class="{cls}">{product}</span>')
        st.markdown(
            f"""
            <div class="tmk-answer-box">
                <div class="tmk-value">{escape(stage_record.label)}</div>
                <div class="tmk-note" style="margin-bottom:0.35rem;">{escape(stage_label(stage))}</div>
                <div class="tmk-soft-list">{''.join(pills)}</div>
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

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Product Lab</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Hub overview, entry routes, division exits, inverse labels, patterns, and comparisons.</div>',
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
            ("Product", str(record.product)),
            ("Stage", stage_label(record.stage)),
            ("Distinct routes", str(len(distinct_factor_routes(record.product)))),
            ("Compare with", str(compare.product)),
        ]
    )

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Hub overview</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="tmk-value">{record.product}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="tmk-note">Intro route: {escape(_format_route(record.intro_route))}. Structural role: {escape(record.structural_role)}.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        _render_route_inspector(record.product)

        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Inverse labels</div>', unsafe_allow_html=True)
        labels = inverse_labels(record.product)
        if labels:
            for label in labels:
                st.markdown(f'<div class="tmk-answer-box">{escape(_stringify(label))}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="tmk-note">No inverse labels available.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Compare products</div>', unsafe_allow_html=True)
        shared = shared_factors(record.product, compare.product)
        st.markdown(
            f'<div class="tmk-note">Shared factors: {escape(", ".join(str(value) for value in shared) if shared else "None")}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Selected product routes</div>', unsafe_allow_html=True)
        for route in distinct_factor_routes(record.product):
            st.markdown(
                f'<div class="tmk-answer-box">{escape(_format_route(route))}</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Compare product routes</div>', unsafe_allow_html=True)
        for route in distinct_factor_routes(compare.product):
            st.markdown(
                f'<div class="tmk-answer-box">{escape(_format_route(route))}</div>',
                unsafe_allow_html=True,
            )
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

    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    title = st.session_state.route_view_mode[:-1] if st.session_state.route_view_mode.endswith("s") else st.session_state.route_view_mode
    st.markdown(f'<div class="tmk-small-label">{escape(title)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tmk-value">{escape(selected_item["headline"])}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tmk-note" style="margin-top:0.55rem;">{escape(selected_item["explanation"])}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


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


# -----------------------------
# WORKSHEET STUDIO
# -----------------------------

def _render_worksheet_studio() -> None:
    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Worksheet Studio</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Generate worksheets from stage, format, tier, selection scope, optional mode, and recap controls.</div>',
        unsafe_allow_html=True,
    )

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

    if st.button("Generate worksheet", type="primary"):
        try:
            bundle = generate_worksheet_bundle(request)
            st.session_state.last_bundle = bundle
            st.session_state.last_request_signature = request_signature
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

    col_a, col_b = st.columns((1.15, 0.85))

    with col_a:
        st.markdown('<div class="tmk-worksheet-frame">', unsafe_allow_html=True)
        st.markdown("### Pupil worksheet")
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

    with col_b:
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
        "recap_count": int(st.session_state.recap_count),
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
            if value is not None and key in {"stage", "format_id", "tier", "selection_scope", "selection_mode", "include_recap", "recap_count"}
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
