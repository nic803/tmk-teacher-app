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
from ui.core_resource_registry import CORE_RESOURCE_REGISTRY


_RESOURCE_LIBRARY_SELECTED_KEY = "resource_library_selected_id_v1"
_RESOURCE_LIBRARY_STAGE_FILTER_KEY = "resource_library_stage_filter_v1"
_RESOURCE_LIBRARY_STATUS_FILTER_KEY = "resource_library_status_filter_v1"


def render_resource_library_page() -> None:
    _ensure_resource_library_state()

    resources = list(CORE_RESOURCE_REGISTRY.values())

    page_header(
        "TMK Structural Resource Library",
        "Browse structural resources, filter lightly, and open one resource at a time.",
    )

    filtered_resources = _render_library_filters(resources)

    selected_id = st.session_state.get(_RESOURCE_LIBRARY_SELECTED_KEY)
    selected_resource = CORE_RESOURCE_REGISTRY.get(selected_id) if selected_id else None

    if selected_resource is None:
        _render_library_browser(filtered_resources)
        return

    back_col, spacer_col = st.columns((0.2, 0.8))
    with back_col:
        if st.button(
            "Back to library",
            key="resource_library_back_button_v1",
            use_container_width=True,
        ):
            st.session_state[_RESOURCE_LIBRARY_SELECTED_KEY] = None
            st.rerun()

    _render_resource_player(selected_resource)


def _ensure_resource_library_state() -> None:
    if _RESOURCE_LIBRARY_SELECTED_KEY not in st.session_state:
        st.session_state[_RESOURCE_LIBRARY_SELECTED_KEY] = None

    if _RESOURCE_LIBRARY_STAGE_FILTER_KEY not in st.session_state:
        st.session_state[_RESOURCE_LIBRARY_STAGE_FILTER_KEY] = "All"

    if _RESOURCE_LIBRARY_STATUS_FILTER_KEY not in st.session_state:
        st.session_state[_RESOURCE_LIBRARY_STATUS_FILTER_KEY] = "All"


def _render_library_filters(resources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    stages = ["All"] + sorted({str(resource.get("stage", "")) for resource in resources if resource.get("stage")})
    statuses = ["All"] + sorted(
        {
            str(resource.get("tags", {}).get("status", ""))
            for resource in resources
            if resource.get("tags", {}).get("status")
        }
    )

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        stage_filter = st.selectbox(
            "Stage",
            options=stages,
            index=stages.index(st.session_state[_RESOURCE_LIBRARY_STAGE_FILTER_KEY]),
            key=_RESOURCE_LIBRARY_STAGE_FILTER_KEY,
        )

    with filter_col2:
        status_filter = st.selectbox(
            "Status",
            options=statuses,
            index=statuses.index(st.session_state[_RESOURCE_LIBRARY_STATUS_FILTER_KEY]),
            key=_RESOURCE_LIBRARY_STATUS_FILTER_KEY,
        )

    filtered = []
    for resource in resources:
        stage_value = str(resource.get("stage", ""))
        status_value = str(resource.get("tags", {}).get("status", ""))

        if stage_filter != "All" and stage_value != stage_filter:
            continue
        if status_filter != "All" and status_value != status_filter:
            continue

        filtered.append(resource)

    return filtered


def _render_library_browser(resources: list[dict[str, Any]]) -> None:
    if not resources:
        st.markdown(
            '<div class="tmk-note">No resources match the current filters.</div>',
            unsafe_allow_html=True,
        )
        return

    cols = st.columns(2)

    for index, resource in enumerate(resources):
        with cols[index % 2]:
            st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="tmk-small-label">{resource.get("stage", "")}</div>',
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

            pattern = resource.get("pattern")
            if pattern:
                st.markdown(
                    f'<div class="tmk-small-label">Pattern</div>',
                    unsafe_allow_html=True,
                )
                render_tag_pills((str(pattern),), accent=True)

            access_tags = tuple(resource.get("tags", {}).get("access", ()))
            if access_tags:
                st.markdown(
                    f'<div class="tmk-small-label" style="margin-top:0.65rem;">Access</div>',
                    unsafe_allow_html=True,
                )
                render_tag_pills(tuple(str(item) for item in access_tags[:4]))

            status_value = resource.get("tags", {}).get("status")
            if status_value:
                st.markdown(
                    f'<div class="tmk-note" style="margin-top:0.75rem;"><strong>Status:</strong> {status_value}</div>',
                    unsafe_allow_html=True,
                )

            if st.button(
                "Open resource",
                key=f"resource_library_open_{resource.get('id', index)}",
                use_container_width=True,
            ):
                st.session_state[_RESOURCE_LIBRARY_SELECTED_KEY] = resource["id"]
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)


def _render_resource_player(resource: dict[str, Any]) -> None:
    teacher_panel = dict(resource.get("teacher_panel", {}))
    msvwa = dict(teacher_panel.get("msvwa", {}))
    diagnostics = dict(teacher_panel.get("diagnostics", {}))

    resource_header_bar(
        title=str(resource.get("title", "")),
        stage=str(resource.get("stage", "")),
        pattern=str(resource.get("pattern", "")),
        purpose=str(resource.get("purpose", "")),
        action_labels=(),
        action_key_prefix=f"resource_player_header_{resource.get('id', 'resource')}",
    )

    asset_name = str(resource.get("asset_path", "")).strip()
    rendered = False

    if asset_name:
        html_path = Path(__file__).parent / "static" / asset_name
        resource_main_interaction_start()
        rendered = render_html_resource(
            html_path=html_path,
            height=980,
            scrolling=True,
            frame_class=f"tmk-resource-frame-{resource.get('id', 'resource')}",
        )
        resource_main_interaction_end()

    if not rendered:
        st.markdown(
            '<div class="tmk-note">This resource does not yet have a playable asset.</div>',
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

    if msvwa or diagnostics:
        resource_teacher_panel(
            msvwa=msvwa,
            diagnostics=diagnostics,
            expanded=False,
            label="Teacher panel",
        )
