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


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="✳️",
    layout="wide",
)


def main() -> None:
    _ensure_state()
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
        st.session_state.compare_product = 24 if 24 in ALL_PRODUCTS else ALL_PRODUCTS[0]


def _apply_styles() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background: #f5f3ef;
                color: #1f2a44;
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
                background: linear-gradient(180deg, #fffdf9 0%, #faf7f1 100%);
                border: 1px solid #eadfd0;
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
                color: #7f5b2e;
                margin-bottom: 0.25rem;
            }

            .tmk-header h1 {
                margin: 0;
                font-size: 2rem;
                line-height: 1.08;
                color: #1f2a44;
            }

            .tmk-header p {
                margin: 0.45rem 0 0 0;
                color: #46516b;
                font-size: 1rem;
                line-height: 1.45;
            }

            .tmk-panel {
                background: rgba(255, 255, 255, 0.74);
                border: 1px solid #eadfd0;
                border-radius: 24px;
                padding: 1rem 1rem;
                box-shadow: 0 10px 30px rgba(34, 46, 75, 0.05);
                margin-bottom: 1rem;
            }

            .tmk-section-title {
                font-size: 2rem;
                line-height: 1.1;
                font-weight: 800;
                color: #22304f;
                margin-bottom: 0.2rem;
            }

            .tmk-section-subtitle {
                color: #59667f;
                margin-bottom: 0.8rem;
                font-size: 1rem;
                line-height: 1.45;
            }

            .tmk-card {
                background: linear-gradient(180deg, #fffcf7 0%, #f9f4eb 100%);
                border: 1px solid #eadfd0;
                border-radius: 18px;
                padding: 0.95rem 1rem;
                height: 100%;
                margin-bottom: 0.75rem;
            }

            .tmk-card-dark {
                background: #041127;
                border: 1px solid #142846;
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
                color: #7d6640;
                margin-bottom: 0.3rem;
            }

            .tmk-value {
                font-size: 1.35rem;
                font-weight: 800;
                color: #22304f;
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
                background: #f3ede4;
                border: 1px solid #e4d6c2;
                color: #22304f;
                font-size: 0.95rem;
                font-weight: 700;
                line-height: 1.2;
            }

            .tmk-pill-accent {
                background: #fff2e1;
                border-color: #f2bf7d;
            }

            .tmk-note {
                color: #59667f;
                font-size: 0.98rem;
                line-height: 1.55;
            }

            .tmk-subhead {
                font-size: 1.18rem;
                font-weight: 800;
                color: #22304f;
                margin-bottom: 0.5rem;
            }

            .tmk-stage-card {
                border-radius: 20px;
                border: 1px solid #eadfd0;
                padding: 0.9rem;
                margin-bottom: 0.8rem;
                background: rgba(255,255,255,0.72);
            }

            .tmk-stage-title {
                font-size: 1.05rem;
                font-weight: 800;
                color: #22304f;
                margin-bottom: 0.55rem;
            }

            .tmk-mobile-map-note {
                font-size: 0.95rem;
                line-height: 1.5;
                color: #59667f;
                margin-bottom: 0.75rem;
            }

            .tmk-worksheet-frame {
                background: linear-gradient(180deg, #fffdf9 0%, #faf6ee 100%);
                border: 1px solid #eadfd0;
                border-radius: 22px;
                padding: 1rem;
                margin-bottom: 0.9rem;
            }

            .tmk-answer-box {
                background: rgba(255,255,255,0.85);
                border: 1px solid #eadfd0;
                border-radius: 16px;
                padding: 0.9rem 0.95rem;
                margin-bottom: 0.7rem;
            }

            .tmk-answer-box strong {
                line-height: 1.45;
            }

            .stButton > button {
                border-radius: 999px;
                border: 1px solid #dfd2bf;
                background: #fffaf2;
                color: #233250;
                font-weight: 800;
                min-height: 2.9rem;
                box-shadow: none;
                font-size: 0.98rem;
                line-height: 1.2;
                white-space: normal;
            }

            .stButton > button:hover {
                border-color: #c8ab7a;
                color: #1d2b47;
            }

            [data-testid="stSidebar"] {
                background: #faf7f1;
                border-left: 1px solid #eadfd0;
            }

            [data-testid="stMetric"] {
                background: transparent;
            }

            .tmk-map-wrap {
                overflow-x: auto;
                overflow-y: hidden;
                -webkit-overflow-scrolling: touch;
                border-radius: 20px;
            }

            .tmk-radial-text-list {
                margin-top: 0.75rem;
            }

            .tmk-radial-text-list .tmk-note {
                margin-bottom: 0.28rem;
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

                .tmk-header p {
                    font-size: 0.98rem;
                }

                .tmk-panel {
                    border-radius: 18px;
                    padding: 0.85rem;
                }

                .tmk-section-title {
                    font-size: 1.55rem;
                }

                .tmk-section-subtitle {
                    font-size: 0.97rem;
                }

                .tmk-card,
                .tmk-card-dark,
                .tmk-worksheet-frame,
                .tmk-answer-box {
                    border-radius: 16px;
                }

                .tmk-value {
                    font-size: 1.18rem;
                }

                .tmk-pill {
                    font-size: 0.92rem;
                    padding: 0.42rem 0.66rem;
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
                .tmk-note {
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
    cols = st.columns(len(SURFACES))
    for index, surface in enumerate(SURFACES):
        kind = "primary" if st.session_state.surface == surface else "secondary"
        if cols[index].button(surface, use_container_width=True, type=kind):
            st.session_state.surface = surface
            st.rerun()


def _render_sidebar() -> None:
    with st.sidebar:
        st.markdown("## Controls")

        product = st.selectbox(
            "Selected product",
            options=ALL_PRODUCTS,
            index=ALL_PRODUCTS.index(st.session_state.selected_product),
            format_func=_product_option_label,
        )
        if product != st.session_state.selected_product:
            st.session_state.selected_product = product
            st.rerun()

        tier = st.radio(
            "Worksheet tier",
            options=TIERS,
            index=TIERS.index(st.session_state.selected_tier),
            horizontal=True,
        )
        st.session_state.selected_tier = tier

        compare_product = st.selectbox(
            "Compare with",
            options=ALL_PRODUCTS,
            index=ALL_PRODUCTS.index(st.session_state.compare_product),
            format_func=_product_option_label,
        )
        st.session_state.compare_product = compare_product

        record = product_record(st.session_state.selected_product)

        st.markdown("---")
        st.markdown("### Current hub")
        st.write(f"**Product:** {record.product}")
        st.write(f"**Stage:** {stage_label(record.stage)}")
        st.write(f"**Intro route:** {_format_route(record.intro_route)}")
        st.write(f"**Routes:** {len(record.factor_families)}")
        st.write(f"**Role:** {record.structural_role}")


def _render_structural_planner(product: int) -> None:
    record = product_record(product)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Structural Planner</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">World map, stage unlock view, visible products, and product-first navigation.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="tmk-mobile-map-note">
            On smaller screens, use the stage cards first. The large network map is still available below in a scrollable frame.
        </div>
        """,
        unsafe_allow_html=True,
    )

    _render_stage_cards(product)

    st.markdown('<div class="tmk-map-wrap">', unsafe_allow_html=True)
    components.html(_world_map_html(product), height=820, scrolling=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Visible products</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tmk-section-subtitle">{stage_label(record.stage)} unlocks {len(visible_products(record.stage))} visible products.</div>',
        unsafe_allow_html=True,
    )
    _render_visible_products_grid(product)
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        _metric_card("Selected product", str(record.product))
        _metric_card("Intro route", _format_route(record.intro_route))
    with col2:
        _metric_card("Stage", stage_label(record.stage))
        _metric_card("Structural role", record.structural_role)


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
    compare = product_record(st.session_state.compare_product)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Product Lab</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Hub overview, truth set, inverse field, pattern links, stage relations, compare products, and differentiation.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    _metric_card_row(
        [
            ("Product", str(record.product)),
            ("Stage", stage_label(record.stage)),
            ("Routes", str(len(record.factor_families))),
            ("Role", record.structural_role),
        ]
    )

    st.markdown('<div class="tmk-card-dark">', unsafe_allow_html=True)
    components.html(_radial_hub_html(product), height=520, scrolling=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Radial route list</div>', unsafe_allow_html=True)
    _render_radial_text_fallback(record)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Hub overview</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="tmk-note"><strong>Product:</strong> {record.product}</div>
        <div class="tmk-note"><strong>Intro route:</strong> {_format_route(record.intro_route)}</div>
        <div class="tmk-note"><strong>Ways in:</strong> {len(record.ways_in)} ordered routes</div>
        <div class="tmk-note"><strong>Ways out:</strong> {len(record.ways_out)} ordered exits</div>
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
    st.markdown(_pill_cloud(_inverse_labels(product), accent=False), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Pattern links</div>', unsafe_allow_html=True)
    _render_pattern_links(product)
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

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-subhead">Differentiation</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="tmk-note">
            Support keeps the same structure with lower working-memory load.<br>
            Core keeps the full product-centred route structure.<br>
            Extension keeps the same product but asks for comparison, justification, and explanation.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def _render_worksheet_studio(product: int, tier: str) -> None:
    worksheet = generate_worksheet(product, tier)

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Worksheet Studio</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Choose product, choose Support/Core/Extension, generate worksheet, review teacher key.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

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
                <div style="font-size:1.02rem;font-weight:700;color:#22304f;line-height:1.5;">{escape(_render_question_text(question))}</div>
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
        for offset, visible_product in enumerate(products[row_start: row_start + cols_per_row]):
            button_type = "primary" if visible_product == product else "secondary"
            label = str(visible_product)
            if cols[offset].button(label, key=f"visible_{visible_product}", use_container_width=True, type=button_type):
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


def _render_radial_text_fallback(record) -> None:
    entry_lines = _entry_routes_for_radial(record)
    exit_lines = _exit_routes_for_radial(record)

    st.markdown('<div class="tmk-radial-text-list">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-note"><strong>Entry routes</strong></div>', unsafe_allow_html=True)
    for route in entry_lines:
        st.markdown(f'<div class="tmk-note">{escape(_format_route(route))}</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="tmk-note"><strong>Exit routes</strong></div>', unsafe_allow_html=True)
    for label in exit_lines:
        st.markdown(f'<div class="tmk-note">{escape(label)}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def _world_map_html(selected_product: int) -> str:
    width = 1320
    lane_x = 26
    lane_w = 1268
    lane_h = 94
    lane_gap = 58
    top = 24
    stages = [stage for stage in STAGE_ORDER if stage in STAGES]
    y_positions = {stage: top + index * (lane_h + lane_gap) for index, stage in enumerate(stages)}
    positions = _world_positions(lane_x, lane_w, lane_h, lane_gap, top)

    lines: list[str] = []
    for product in ALL_PRODUCTS:
        record = product_record(product)
        start = positions.get(record.intro_route[0])
        end = positions.get(product)
        if start and end:
            lines.append(_svg_line(start[0], start[1], end[0], end[1], "#aab5c5", 2.4, 0.34, ""))
        alt = positions.get(record.intro_route[1])
        if alt and end:
            lines.append(_svg_line(alt[0], alt[1], end[0], end[1], "#aab5c5", 2.4, 0.34, ""))

    selected_record = product_record(selected_product)
    selected_end = positions[selected_product]
    for factor in selected_record.intro_route:
        if factor in positions:
            sx, sy = positions[factor]
            ex, ey = selected_end
            lines.append(_svg_line(sx, sy, ex, ey, "#ff9f43", 4.0, 0.96, "8 6"))
            lines.append(_svg_line(sx, sy, ex, ey, "#7c3aed", 1.8, 0.96, "2 8"))

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
            f'<text x="{lane_x + 22}" y="{y + 28}" font-size="22" font-weight="800" fill="#22304f">{escape(stage_record.label)}</text>'
        )

    nodes: list[str] = []
    for product in ALL_PRODUCTS:
        x, y = positions[product]
        record = product_record(product)
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

    legend = """
        <rect x="26" y="708" width="1268" height="48" rx="16" fill="rgba(255,255,255,0.6)" stroke="#eadfd0" stroke-width="1.2"></rect>
        <text x="48" y="738" font-size="17" font-weight="700" fill="#4a5873">Highlighted lines show the selected product’s intro route. Faint lines show the wider route network.</text>
    """

    svg = f"""
    <svg viewBox="0 0 1320 770" width="1320" height="770" xmlns="http://www.w3.org/2000/svg">
        <rect x="0" y="0" width="1320" height="770" fill="#f5f3ef"></rect>
        {''.join(lane_rects)}
        {''.join(lines)}
        {''.join(lane_labels)}
        {''.join(nodes)}
        {legend}
    </svg>
    """

    return f"""
    <div style="background:#f5f3ef;border-radius:24px;overflow:auto;max-width:100%;">
        {svg}
    </div>
    """


def _world_positions(
    lane_x: int,
    lane_w: int,
    lane_h: int,
    lane_gap: int,
    top: int,
) -> dict[int, tuple[float, float]]:
    positions: dict[int, tuple[float, float]] = {}
    usable_x = lane_w - 120

    for row_index, stage in enumerate([stage for stage in STAGE_ORDER if stage in STAGES]):
        products = STAGES[stage].products
        y = top + row_index * (lane_h + lane_gap) + lane_h / 2
        if len(products) == 1:
            positions[products[0]] = (lane_x + lane_w / 2, y)
            continue

        step = usable_x / (len(products) - 1)
        for index, product in enumerate(products):
            x = lane_x + 84 + index * step
            positions[product] = (x, y)

    return positions


def _radial_hub_html(product: int) -> str:
    record = product_record(product)
    cx = 380
    cy = 245
    r = 76
    entry_routes = _entry_routes_for_radial(record)
    exit_routes = _exit_routes_for_radial(record)
    entry_angles = [-90, -152, -28, -210][: len(entry_routes)]
    exit_angles = [90, 152, 28, 210][: len(exit_routes)]

    lines: list[str] = []
    labels: list[str] = []

    for angle, route in zip(entry_angles, entry_routes):
        x2, y2 = _point(cx, cy, 190, angle)
        x1, y1 = _point(cx, cy, r + 10, angle)
        lines.append(_svg_arrow(x2, y2, x1, y1, "#dbe4f4", 4))
        labels.append(
            f'<text x="{x2}" y="{y2 - 14}" text-anchor="middle" font-size="22" font-weight="800" fill="#ffffff">{escape(_format_route(route))}</text>'
        )

    for angle, label in zip(exit_angles, exit_routes):
        x1, y1 = _point(cx, cy, r + 12, angle)
        x2, y2 = _point(cx, cy, 190, angle)
        lines.append(_svg_arrow(x1, y1, x2, y2, "#9c7cff", 4))
        labels.append(
            f'<text x="{x2}" y="{y2 + 22}" text-anchor="middle" font-size="20" font-weight="800" fill="#ffffff">{escape(label)}</text>'
        )

    svg = f"""
    <svg viewBox="0 0 760 490" width="760" height="490" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <marker id="arrow-end-light" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#dbe4f4"></path>
            </marker>
            <marker id="arrow-end-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#9c7cff"></path>
            </marker>
        </defs>
        <rect x="0" y="0" width="760" height="490" rx="28" fill="#031026"></rect>
        <text x="18" y="28" font-size="18" font-weight="800" fill="#ffffff">Radial Hub View</text>
        <text x="18" y="52" font-size="15" font-weight="500" fill="#d4def1">Multiplication routes point inward · Division routes point outward</text>
        {''.join(lines)}
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="#9ba4b5" stroke="#f5f7fb" stroke-width="5"></circle>
        <text x="{cx}" y="{cy + 13}" text-anchor="middle" font-size="42" font-weight="900" fill="#ffffff">{product}</text>
        <text x="{cx}" y="{cy - 100}" text-anchor="middle" font-size="22" font-weight="800" fill="#ffffff">Entry routes</text>
        <text x="{cx}" y="{cy + 126}" text-anchor="middle" font-size="22" font-weight="800" fill="#ffffff">Exit routes</text>
        {''.join(labels)}
    </svg>
    """
    return svg.replace('marker-end="LIGHT"', 'marker-end="url(#arrow-end-light)"').replace(
        'marker-end="PURPLE"', 'marker-end="url(#arrow-end-purple)"'
    )


def _entry_routes_for_radial(record) -> list[tuple[int, int]]:
    routes: list[tuple[int, int]] = []
    intro = record.intro_route
    routes.append(intro)
    if intro[0] != intro[1]:
        routes.append((intro[1], intro[0]))
    for route in record.ways_in:
        if route not in routes:
            routes.append(route)
        if len(routes) == 4:
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
        label = _stringify(item)
        pills.append(f'<span class="{cls}">{escape(label)}</span>')
    return f'<div class="tmk-soft-list">{"".join(pills)}</div>'


def _point(cx: float, cy: float, radius: float, angle_degrees: float) -> tuple[float, float]:
    radians = angle_degrees * pi / 180.0
    return cx + radius * cos(radians), cy + radius * sin(radians)


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
