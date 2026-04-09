from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit as st

from ui.components import (
    page_header,
    render_html_resource,
    render_tag_pills,
    resource_child_prompt_strip,
    resource_equation_box,
    resource_header_bar,
    resource_main_interaction_end,
    resource_main_interaction_start,
    resource_pattern_focus_strip,
    resource_teacher_panel,
)
from ui.extension_animations_registry import EXTENSION_ANIMATIONS_REGISTRY


_EXTENSION_ANIMATIONS_SELECTED_KEY = "extension_animations_selected_id_v1"
_EXTENSION_ANIMATIONS_FAMILY_FILTER_KEY = "extension_animations_family_filter_v1"


def render_extension_animations_browser_page() -> None:
    _ensure_extension_animation_browser_state()

    page_header(
        "Extension Animations",
        "Browse playable 11× and 12× extension animations separately from the core TMK resource library.",
    )

    resources = list(EXTENSION_ANIMATIONS_REGISTRY.values())
    filtered_resources = _render_family_filter(resources)

    selected_id = st.session_state.get(_EXTENSION_ANIMATIONS_SELECTED_KEY)
    selected_resource = (
        EXTENSION_ANIMATIONS_REGISTRY.get(selected_id)
        if selected_id
        else None
    )

    if selected_resource is None:
        _render_browser_cards(filtered_resources)
        return

    back_col, info_col = st.columns((0.22, 0.78))
    with back_col:
        if st.button(
            "Back to animations",
            key="extension_animations_back_button_v1",
            use_container_width=True,
        ):
            st.session_state[_EXTENSION_ANIMATIONS_SELECTED_KEY] = None
            st.rerun()

    with info_col:
        st.markdown(
            f"""
            <div class="tmk-card" style="margin-bottom:1rem;border:1px solid #D9D4C8;">
                <div class="tmk-small-label">Now showing</div>
                <div class="tmk-section-title" style="margin-top:0.25rem;">{selected_resource.get("title", "")}</div>
                <div class="tmk-note" style="margin-top:0.35rem;">
                    Family: {selected_resource.get("family", "")} · Pattern: {selected_resource.get("pattern", "")}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    _render_selected_animation(selected_resource)


def _ensure_extension_animation_browser_state() -> None:
    if _EXTENSION_ANIMATIONS_SELECTED_KEY not in st.session_state:
        st.session_state[_EXTENSION_ANIMATIONS_SELECTED_KEY] = None

    if _EXTENSION_ANIMATIONS_FAMILY_FILTER_KEY not in st.session_state:
        st.session_state[_EXTENSION_ANIMATIONS_FAMILY_FILTER_KEY] = "All"


def _render_family_filter(resources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    family_options = ["All", "11x", "12x", "both"]

    selected_family = st.selectbox(
        "Family",
        options=family_options,
        index=family_options.index(st.session_state[_EXTENSION_ANIMATIONS_FAMILY_FILTER_KEY]),
        key=_EXTENSION_ANIMATIONS_FAMILY_FILTER_KEY,
    )

    if selected_family == "All":
        return resources

    filtered: list[dict[str, Any]] = []
    for resource in resources:
        family = str(resource.get("family", "")).strip().lower()
        if family == selected_family:
            filtered.append(resource)
        elif selected_family in {"11x", "12x"} and family == "both":
            filtered.append(resource)

    return filtered


def _render_browser_cards(resources: list[dict[str, Any]]) -> None:
    if not resources:
        st.markdown(
            '<div class="tmk-note">No extension animations match the current filter.</div>',
            unsafe_allow_html=True,
        )
        return

    cols = st.columns(2)

    for index, resource in enumerate(resources):
        with cols[index % 2]:
            asset_name = str(resource.get("asset_path", "")).strip()
            status_value = str(resource.get("tags", {}).get("status", "")).strip()
            use_case_tags = tuple(resource.get("tags", {}).get("use_case", ()))
            pattern = str(resource.get("pattern", "")).strip()

            st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="tmk-small-label">{resource.get("family", "")}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="tmk-section-title">{resource.get("title", "")}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="tmk-note" style="margin-bottom:0.75rem;">{resource.get("purpose", "")}</div>',
                unsafe_allow_html=True,
            )

            if pattern:
                st.markdown(
                    '<div class="tmk-small-label">Pattern</div>',
                    unsafe_allow_html=True,
                )
                render_tag_pills((pattern,), accent=True)

            if asset_name:
                st.markdown(
                    f'<div class="tmk-note" style="margin-top:0.75rem;"><strong>HTML asset:</strong> ui/static/{asset_name}</div>',
                    unsafe_allow_html=True,
                )

            if use_case_tags:
                st.markdown(
                    '<div class="tmk-small-label" style="margin-top:0.65rem;">Use case</div>',
                    unsafe_allow_html=True,
                )
                render_tag_pills(tuple(str(item) for item in use_case_tags[:4]))

            if status_value:
                st.markdown(
                    f'<div class="tmk-note" style="margin-top:0.75rem;"><strong>Status:</strong> {status_value}</div>',
                    unsafe_allow_html=True,
                )

            if st.button(
                "Open playable animation",
                key=f"extension_animation_open_{resource.get('id', index)}",
                use_container_width=True,
            ):
                st.session_state[_EXTENSION_ANIMATIONS_SELECTED_KEY] = resource["id"]
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)


def _render_selected_animation(resource: dict[str, Any]) -> None:
    teacher_panel = dict(resource.get("teacher_panel", {}))
    msvwa = dict(teacher_panel.get("msvwa", {}))
    diagnostics = dict(teacher_panel.get("diagnostics", {}))

    resource_header_bar(
        title=str(resource.get("title", "")),
        stage=f"Extension · {resource.get('family', '')}",
        pattern=str(resource.get("pattern", "")),
        purpose=str(resource.get("purpose", "")),
        action_labels=(),
        action_key_prefix=f"extension_animation_header_{resource.get('id', 'resource')}",
    )

    asset_name = str(resource.get("asset_path", "")).strip()
    rendered = False

    if asset_name:
        html_path = Path(__file__).parent / "static" / asset_name

        st.markdown(
            f"""
            <div class="tmk-card" style="margin-bottom:0.75rem;">
                <div class="tmk-small-label">Playable asset</div>
                <div class="tmk-note" style="margin-top:0.35rem;">ui/static/{asset_name}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        resource_main_interaction_start()
        rendered = render_html_resource(
            html_path=html_path,
            height=980,
            scrolling=True,
            frame_class=f"tmk-extension-animation-frame-{resource.get('id', 'resource')}",
        )
        resource_main_interaction_end()

    if not rendered:
        st.markdown(
            '<div class="tmk-note">This extension animation does not yet have a playable asset.</div>',
            unsafe_allow_html=True,
        )

    equation_meta = dict(resource.get("equations", {}))
    equation_examples = tuple(str(item) for item in equation_meta.get("examples", ()))
    if equation_examples:
        resource_equation_box(
            title="Equation / product box",
            equations=equation_examples,
        )

    prompt = str(resource.get("prompt", "")).strip()
    if prompt:
        resource_child_prompt_strip(prompt)

    pattern = str(resource.get("pattern", "")).strip()
    if pattern:
        resource_pattern_focus_strip(pattern)

    teacher_support_level = str(resource.get("teacher_support_level", "")).strip().lower()
    if teacher_support_level == "full" and (msvwa or diagnostics):
        resource_teacher_panel(
            msvwa=msvwa,
            diagnostics=diagnostics,
            expanded=False,
            label="Teacher panel",
        )
    elif teacher_support_level and teacher_support_level != "full":
        st.markdown(
            f'<div class="tmk-note">Teacher support level: {teacher_support_level.title()}</div>',
            unsafe_allow_html=True,
        )
