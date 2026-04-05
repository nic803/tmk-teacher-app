from __future__ import annotations

from html import escape

import streamlit as st

from ui.extension_activities import (
    EXTENSION_ACTIVITY_GROUPS,
    get_extension_activities_for_group,
)
from ui.extension_patterns import (
    EXTENSION_PAGE_SECTIONS,
    get_patterns_for_section,
)
from ui.extension_route_opening import (
    TWELVE_ROUTE_OPENING_PRODUCTS,
    build_twelve_route_opening_activity,
    format_route,
    get_twelve_route_opening_product,
)


def render_extension_hub_page() -> None:
    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Extensions</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Extension mathematics and advanced activity tools, kept separate from the core TMK structure.</div>',
        unsafe_allow_html=True,
    )

    _render_extension_overview()
    _render_pattern_sections()
    _render_activity_sections()
    _render_twelve_route_opening_panel()

    st.markdown("</div>", unsafe_allow_html=True)


def _render_extension_overview() -> None:
    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Extension overview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-note">This page brings together extension pattern banks, activity banks, and route-opening resources for 11× and 12×.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tmk-note" style="margin-top:0.45rem;">Use this area for extension work only. Core TMK structure remains separate.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def _render_pattern_sections() -> None:
    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Extension pattern bank</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-note">Pattern sections group the main 11× and 12× teaching ideas.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    for section in EXTENSION_PAGE_SECTIONS:
        patterns = get_patterns_for_section(section.section_id)

        with st.expander(section.title, expanded=False):
            st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="tmk-small-label">{escape(section.title)}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="tmk-note">{escape(section.subtitle)}</div>',
                unsafe_allow_html=True,
            )

            for pattern in patterns:
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

                if pattern.cue:
                    st.markdown(
                        f'<div class="tmk-note" style="margin-top:0.35rem;"><strong>Cue:</strong> {escape(pattern.cue)}</div>',
                        unsafe_allow_html=True,
                    )
                if pattern.cue_explanation:
                    st.markdown(
                        f'<div class="tmk-note"><strong>Cue explanation:</strong> {escape(pattern.cue_explanation)}</div>',
                        unsafe_allow_html=True,
                    )

                if pattern.examples:
                    st.markdown(
                        '<div class="tmk-small-label" style="margin-top:0.7rem;">Examples</div>',
                        unsafe_allow_html=True,
                    )
                    for example in pattern.examples:
                        if example.working:
                            text = f"{example.expression} — {example.working}"
                        else:
                            text = example.expression
                        st.markdown(
                            f'<div class="tmk-note">- {escape(text)}</div>',
                            unsafe_allow_html=True,
                        )

                st.markdown("</div>", unsafe_allow_html=True)

            if not patterns:
                st.markdown(
                    '<div class="tmk-note">No patterns available for this section yet.</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)


def _render_activity_sections() -> None:
    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Extension activity bank</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-note">These grouped resources turn extension ideas into teacher-facing activity structures.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    group_titles = {
        "11x_resources": "11× Resources",
        "12x_resources": "12× Resources",
        "boundary_resources": "Core / Extension Boundary",
    }

    for group_id, group_title in group_titles.items():
        activities = get_extension_activities_for_group(group_id)

        with st.expander(group_title, expanded=False):
            st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="tmk-small-label">{escape(group_title)}</div>', unsafe_allow_html=True)

            for activity in activities:
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

            if not activities:
                st.markdown(
                    '<div class="tmk-note">No activities available for this group yet.</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)


def _render_twelve_route_opening_panel() -> None:
    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">12× route opening</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-note">This selector turns route-opening products into a generated teacher resource.</div>',
        unsafe_allow_html=True,
    )

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

    st.markdown("</div>", unsafe_allow_html=True)
