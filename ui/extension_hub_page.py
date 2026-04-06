from __future__ import annotations

from html import escape

import streamlit as st

from ui.extension_activities import (
    get_extension_activities_for_family,
    get_extension_activities_for_group,
)
from ui.extension_patterns import (
    EXTENSION_PAGE_SECTIONS,
    get_patterns_for_family,
    get_patterns_for_section,
)
from ui.extension_route_opening import (
    TWELVE_ROUTE_OPENING_PRODUCTS,
    build_twelve_route_opening_activity,
    format_route,
    get_twelve_route_opening_product,
)
from ui.extension_squares import (
    build_square_activity_print_text,
    format_square_example,
    get_core_square_examples,
    get_extension_square_examples,
    get_square_patterns_for_section,
)


def render_extension_hub_page() -> None:
    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Extensions</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Extension mathematics and advanced activity tools, kept separate from the core TMK structure.</div>',
        unsafe_allow_html=True,
    )

    _render_extension_overview()
    _render_extension_tabs()

    st.markdown("</div>", unsafe_allow_html=True)


def _render_extension_overview() -> None:
    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Extension overview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-note">Use the internal tabs below to move between extension strands. This keeps Extensions expandable as more sections are added.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tmk-note" style="margin-top:0.45rem;">Current live strands: 11×, 12×, square numbers recap, core versus extension boundary, and 12× route opening.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def _render_extension_tabs() -> None:
    tab_11x, tab_12x, tab_squares, tab_boundary, tab_route_opening, tab_coming_soon = st.tabs(
        [
            "11×",
            "12×",
            "Squares",
            "Core / Extension Boundary",
            "Route Opening",
            "Coming Soon",
        ]
    )

    with tab_11x:
        _render_family_tab(
            family="11x",
            heading="11× Extensions",
            subtitle="Teach 11× through derivation, visible pattern noticing, and extension-route awareness.",
            section_ids={"foundations_11x"},
        )

    with tab_12x:
        _render_family_tab(
            family="12x",
            heading="12× Extensions",
            subtitle="Teach 12× through derivation, clock structure, route opening, and extension-product awareness.",
            section_ids={"foundations_12x"},
        )

    with tab_squares:
        _render_squares_tab()

    with tab_boundary:
        _render_boundary_tab()

    with tab_route_opening:
        _render_route_opening_tab()

    with tab_coming_soon:
        _render_coming_soon_tab()


def _render_family_tab(*, family: str, heading: str, subtitle: str, section_ids: set[str]) -> None:
    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="tmk-small-label">{escape(heading)}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tmk-note">{escape(subtitle)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    _render_family_patterns(family=family, section_ids=section_ids)
    _render_family_activities(family=family)


def _render_family_patterns(*, family: str, section_ids: set[str]) -> None:
    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Pattern bank</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-note">These pattern cards organise the extension teaching ideas for this strand.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    matched_sections = [section for section in EXTENSION_PAGE_SECTIONS if section.section_id in section_ids]
    rendered_any_section = False

    for section in matched_sections:
        patterns = get_patterns_for_section(section.section_id)
        if not patterns:
            continue

        rendered_any_section = True
        with st.expander(section.title, expanded=True):
            st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="tmk-small-label">{escape(section.title)}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="tmk-note">{escape(section.subtitle)}</div>',
                unsafe_allow_html=True,
            )

            for pattern in patterns:
                _render_pattern_card(pattern)

            st.markdown("</div>", unsafe_allow_html=True)

    if not rendered_any_section:
        patterns = get_patterns_for_family(family)
        if not patterns:
            st.markdown(
                '<div class="tmk-note">No patterns available for this strand yet.</div>',
                unsafe_allow_html=True,
            )
            return

        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        for pattern in patterns:
            _render_pattern_card(pattern)
        st.markdown("</div>", unsafe_allow_html=True)


def _render_pattern_card(pattern: object) -> None:
    st.markdown('<div class="tmk-answer-box">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tmk-value">{escape(pattern.title)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="tmk-note" style="margin-top:0.35rem;"><strong>Rule:</strong> {escape(pattern.rule)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="tmk-note"><strong>Teacher explanation:</strong> {escape(pattern.teacher_explanation)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="tmk-note"><strong>Teaching use:</strong> {escape(pattern.teaching_use)}</div>',
        unsafe_allow_html=True,
    )

    if getattr(pattern, "cue", None):
        st.markdown(
            f'<div class="tmk-note" style="margin-top:0.35rem;"><strong>Cue:</strong> {escape(pattern.cue)}</div>',
            unsafe_allow_html=True,
        )
    if getattr(pattern, "cue_explanation", None):
        st.markdown(
            f'<div class="tmk-note"><strong>Cue explanation:</strong> {escape(pattern.cue_explanation)}</div>',
            unsafe_allow_html=True,
        )

    examples = getattr(pattern, "examples", [])
    if examples:
        st.markdown(
            '<div class="tmk-small-label" style="margin-top:0.7rem;">Examples</div>',
            unsafe_allow_html=True,
        )
        for example in examples:
            if getattr(example, "working", None):
                text = f"{example.expression} — {example.working}"
            else:
                text = example.expression
            st.markdown(
                f'<div class="tmk-note">- {escape(text)}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)


def _render_family_activities(*, family: str) -> None:
    activities = get_extension_activities_for_family(family)

    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Activity bank</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-note">These activities turn the strand into teacher-facing lesson and resource structures.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if not activities:
        st.markdown(
            '<div class="tmk-note">No activities available for this strand yet.</div>',
            unsafe_allow_html=True,
        )
        return

    for activity in activities:
        _render_activity_card(activity)


def _render_activity_card(activity: object) -> None:
    st.markdown('<div class="tmk-answer-box">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tmk-value">{escape(activity.title)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="tmk-note" style="margin-top:0.35rem;"><strong>Focus:</strong> {escape(activity.focus)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="tmk-note"><strong>Teacher explanation:</strong> {escape(activity.teacher_explanation)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="tmk-note"><strong>Teacher prompt:</strong> {escape(activity.teacher_prompt)}</div>',
        unsafe_allow_html=True,
    )

    if activity.pupil_tasks:
        st.markdown(
            '<div class="tmk-small-label" style="margin-top:0.7rem;">Pupil tasks</div>',
            unsafe_allow_html=True,
        )
        for task in activity.pupil_tasks:
            st.markdown(
                f'<div class="tmk-note">- {escape(task)}</div>',
                unsafe_allow_html=True,
            )

    if activity.example_questions:
        st.markdown(
            '<div class="tmk-small-label" style="margin-top:0.7rem;">Example questions</div>',
            unsafe_allow_html=True,
        )
        for question in activity.example_questions:
            st.markdown(
                f'<div class="tmk-note">- {escape(question)}</div>',
                unsafe_allow_html=True,
            )

    if activity.teaching_note:
        st.markdown(
            f'<div class="tmk-note" style="margin-top:0.55rem;"><strong>Teaching note:</strong> {escape(activity.teaching_note)}</div>',
            unsafe_allow_html=True,
        )

    st.text_area(
        f"Copy for website form — {activity.title}",
        value=activity.print_text,
        height=220,
        key=f"extension_activity_print_text_{activity.activity_id}",
    )
    st.markdown("</div>", unsafe_allow_html=True)


def _render_squares_tab() -> None:
    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Square Numbers Recap</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-note">Known products with a same-factor route.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tmk-note" style="margin-top:0.45rem;">A square number is a product that can be made with the same factor twice.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Key rule</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-note">A square number has a route of the form <strong>n × n</strong>.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tmk-note"><strong>n × n = n²</strong></div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    core_examples = get_core_square_examples()
    extension_examples = get_extension_square_examples()

    left_col, right_col = st.columns((1.0, 1.0))

    with left_col:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Core squares</div>', unsafe_allow_html=True)
        for item in core_examples:
            st.markdown(
                f'<div class="tmk-note">- {escape(format_square_example(item))}</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Extension squares</div>', unsafe_allow_html=True)
        for item in extension_examples:
            st.markdown(
                f'<div class="tmk-note">- {escape(format_square_example(item))}</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Pattern bank</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-note">These first patterns keep square work tied to route structure and the core / extension boundary.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    patterns = get_square_patterns_for_section("square_numbers_recap")
    for pattern in patterns:
        with st.expander(pattern.title, expanded=False):
            st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="tmk-small-label">{escape(pattern.title)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="tmk-note">{escape(pattern.summary)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="tmk-note" style="margin-top:0.45rem;"><strong>Teacher note:</strong> {escape(pattern.teacher_note)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="tmk-small-label" style="margin-top:0.7rem;">Examples</div>',
                unsafe_allow_html=True,
            )
            for example in pattern.examples:
                st.markdown(
                    f'<div class="tmk-note">- {escape(example)}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Activity</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-note">Find the square route.</div>',
        unsafe_allow_html=True,
    )
    st.text_area(
        "Copy-paste print text",
        value=build_square_activity_print_text("find_the_square_route"),
        height=260,
        key="square_numbers_recap_print_text",
    )
    st.markdown("</div>", unsafe_allow_html=True)


def _render_boundary_tab() -> None:
    activities = get_extension_activities_for_group("boundary_resources")

    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Core / Extension Boundary</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-note">Use this strand to keep the TMK core bounded and make the extension layer explicit.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if not activities:
        st.markdown(
            '<div class="tmk-note">No boundary activities available yet.</div>',
            unsafe_allow_html=True,
        )
        return

    for activity in activities:
        _render_activity_card(activity)


def _render_route_opening_tab() -> None:
    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">12× Route Opening</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-note">Use this selector to turn route-opening products into a generated teacher resource.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    selected_product = st.selectbox(
        "Choose a product",
        options=[item.product for item in TWELVE_ROUTE_OPENING_PRODUCTS],
        format_func=lambda value: str(value),
        key="extension_route_opening_product_select_v1",
    )

    item = get_twelve_route_opening_product(selected_product)
    activity = build_twelve_route_opening_activity(selected_product)

    if item is not None:
        upper_left, upper_right = st.columns((1.0, 1.0))

        with upper_left:
            st.markdown('<div class="tmk-answer-box">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="tmk-value">Product {item.product}</div>',
                unsafe_allow_html=True,
            )
            if item.intro_route is not None:
                st.markdown(
                    f'<div class="tmk-note" style="margin-top:0.35rem;"><strong>Intro route:</strong> {escape(format_route(item.intro_route))}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown(
                f'<div class="tmk-note"><strong>Teacher focus:</strong> {escape(item.teacher_focus)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with upper_right:
            st.markdown('<div class="tmk-answer-box">', unsafe_allow_html=True)
            st.markdown('<div class="tmk-small-label">Core routes</div>', unsafe_allow_html=True)
            for route in item.core_routes:
                st.markdown(
                    f'<div class="tmk-note">- {escape(format_route(route))}</div>',
                    unsafe_allow_html=True,
                )

            st.markdown(
                '<div class="tmk-small-label" style="margin-top:0.7rem;">Extension routes</div>',
                unsafe_allow_html=True,
            )
            for route in item.extension_routes:
                st.markdown(
                    f'<div class="tmk-note">- {escape(format_route(route))}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

    if activity is not None:
        st.markdown('<div class="tmk-answer-box">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="tmk-value">{escape(activity.title)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="tmk-note" style="margin-top:0.35rem;"><strong>Focus:</strong> {escape(activity.focus)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="tmk-note"><strong>Teacher explanation:</strong> {escape(activity.teacher_explanation)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="tmk-note"><strong>Teacher prompt:</strong> {escape(activity.teacher_prompt)}</div>',
            unsafe_allow_html=True,
        )

        lower_left, lower_right = st.columns((1.0, 1.0))

        with lower_left:
            st.markdown(
                '<div class="tmk-small-label" style="margin-top:0.7rem;">Pupil tasks</div>',
                unsafe_allow_html=True,
            )
            for task in activity.pupil_tasks:
                st.markdown(
                    f'<div class="tmk-note">- {escape(task)}</div>',
                    unsafe_allow_html=True,
                )

        with lower_right:
            st.markdown(
                '<div class="tmk-small-label" style="margin-top:0.7rem;">Example questions</div>',
                unsafe_allow_html=True,
            )
            for question in activity.example_questions:
                st.markdown(
                    f'<div class="tmk-note">- {escape(question)}</div>',
                    unsafe_allow_html=True,
                )

        st.markdown(
            '<div class="tmk-small-label" style="margin-top:0.7rem;">Key noticing</div>',
            unsafe_allow_html=True,
        )
        for noticing in activity.key_noticing:
            st.markdown(
                f'<div class="tmk-note">- {escape(noticing)}</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            f'<div class="tmk-note" style="margin-top:0.55rem;"><strong>Teaching note:</strong> {escape(activity.teaching_note)}</div>',
            unsafe_allow_html=True,
        )

        st.text_area(
            "Copy for website form — 12× route opening",
            value=activity.print_text,
            height=320,
            key=f"extension_route_opening_print_text_{activity.product}",
        )
        st.markdown("</div>", unsafe_allow_html=True)


def _render_coming_soon_tab() -> None:
    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Planned extension strands</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-note">These sections should be added as future strands inside Extensions, not as new top-level app tabs.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tmk-note" style="margin-top:0.45rem;">Planned strands: square roots, area and perimeter, and later extension resource families.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
