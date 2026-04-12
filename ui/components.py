from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Iterable, Sequence

import streamlit as st


def page_header(title: str, subtitle: str | None = None) -> None:
    st.markdown(
        f"""
        <div class="tmk-card" style="margin-bottom:1rem;">
            <div class="tmk-section-title">{escape(title)}</div>
            {f'<div class="tmk-section-subtitle">{escape(subtitle)}</div>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def resource_header_bar(
    *,
    title: str,
    stage: str | None = None,
    pattern: str | None = None,
    purpose: str | None = None,
    action_labels: Sequence[str] | None = None,
    action_key_prefix: str = "resource_action",
) -> str | None:
    """
    Render the shared resource header bar and return the clicked action label,
    if any.

    This is UI-only and intentionally stateless beyond the button click that
    Streamlit already manages.
    """
    st.markdown('<div class="tmk-card" style="margin-bottom:1rem;">', unsafe_allow_html=True)

    meta_parts: list[str] = []
    if stage:
        meta_parts.append(f"Stage {stage}")
    if pattern:
        meta_parts.append(pattern)

    meta_line = " · ".join(meta_parts)

    header_left, header_right = st.columns((0.72, 0.28))

    with header_left:
        st.markdown(
            f'<div class="tmk-section-title">{escape(title)}</div>',
            unsafe_allow_html=True,
        )
        if meta_line:
            st.markdown(
                f'<div class="tmk-small-label" style="margin-top:0.35rem;">{escape(meta_line)}</div>',
                unsafe_allow_html=True,
            )
        if purpose:
            st.markdown(
                f'<div class="tmk-section-subtitle" style="margin-top:0.45rem;margin-bottom:0;">{escape(purpose)}</div>',
                unsafe_allow_html=True,
            )

    clicked_action: str | None = None
    labels = list(action_labels or ())

    with header_right:
        if labels:
            button_cols = st.columns(min(3, len(labels)))
            for index, label in enumerate(labels):
                col = button_cols[index % len(button_cols)]
                if col.button(
                    label,
                    key=f"{action_key_prefix}_{index}_{label.lower().replace(' ', '_')}",
                    use_container_width=True,
                ):
                    clicked_action = label

    st.markdown("</div>", unsafe_allow_html=True)
    return clicked_action


def resource_main_interaction_start() -> None:
    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-small-label">Main interaction area</div>',
        unsafe_allow_html=True,
    )


def resource_main_interaction_end() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def resource_equation_box(
    *,
    title: str = "Equation / product box",
    equations: Sequence[str] | None = None,
) -> None:
    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tmk-small-label">{escape(title)}</div>',
        unsafe_allow_html=True,
    )

    items = [str(item) for item in (equations or ()) if str(item).strip()]
    if items:
        for item in items:
            st.markdown(
                f'<div class="tmk-answer-box">{escape(item)}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="tmk-note">No equation or product relationship provided.</div>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def resource_child_prompt_strip(prompt: str | None) -> None:
    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Child prompt</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tmk-value" style="font-size:1rem;">{escape(prompt or "No prompt provided.")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def resource_pattern_focus_strip(label: str | None) -> None:
    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Pattern focus</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tmk-note">{escape(label or "No pattern focus label provided.")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def resource_teacher_panel(
    *,
    msvwa: dict[str, str] | None = None,
    diagnostics: dict[str, str] | None = None,
    expanded: bool = False,
    label: str = "Teacher panel",
) -> None:
    with st.expander(label, expanded=expanded):
        left_col, right_col = st.columns(2)

        with left_col:
            st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
            st.markdown('<div class="tmk-small-label">MSVWA</div>', unsafe_allow_html=True)

            if msvwa:
                for key in ("marker", "sequence", "variation", "working_memory", "attention"):
                    value = msvwa.get(key)
                    if value:
                        key_label = key.replace("_", " ").title()
                        st.markdown(
                            f"""
                            <div class="tmk-answer-box">
                                <div class="tmk-small-label">{escape(key_label)}</div>
                                <div class="tmk-note">{escape(value)}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
            else:
                st.markdown(
                    '<div class="tmk-note">No MSVWA guidance provided.</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)

        with right_col:
            st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
            st.markdown('<div class="tmk-small-label">Diagnostics</div>', unsafe_allow_html=True)

            ordered_keys = (
                "look_for",
                "secure_if",
                "watch_for",
                "prompt_if_stuck",
                "if_knowledge_is_missing",
                "next_move",
            )

            if diagnostics:
                for key in ordered_keys:
                    value = diagnostics.get(key)
                    if value:
                        key_label = key.replace("_", " ").title()
                        st.markdown(
                            f"""
                            <div class="tmk-answer-box">
                                <div class="tmk-small-label">{escape(key_label)}</div>
                                <div class="tmk-note">{escape(value)}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
            else:
                st.markdown(
                    '<div class="tmk-note">No diagnostics guidance provided.</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)


def resource_controls_footer(
    *,
    controls: Sequence[str] | None = None,
    key_prefix: str = "resource_footer_control",
) -> str | None:
    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Teacher controls</div>', unsafe_allow_html=True)

    items = [str(item) for item in (controls or ()) if str(item).strip()]
    if not items:
        st.markdown(
            '<div class="tmk-note">No controls configured for this resource.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        return None

    clicked: str | None = None
    cols = st.columns(min(4, len(items)))
    for index, control in enumerate(items):
        col = cols[index % len(cols)]
        if col.button(
            control.replace("_", " ").title(),
            key=f"{key_prefix}_{index}_{control.lower()}",
            use_container_width=True,
        ):
            clicked = control

    st.markdown("</div>", unsafe_allow_html=True)
    return clicked


def render_html_resource(
    *,
    html_path: str | Path,
    height: int = 980,
    scrolling: bool = True,
    frame_class: str = "tmk-game-frame",
) -> bool:
    """
    Safe shared HTML embed renderer.

    Returns True if rendered, False if the file was missing.
    """
    path = Path(html_path)

    if not path.exists():
        st.error(f"Resource file not found: {path}")
        return False

    html = path.read_text(encoding="utf-8")

    escaped_srcdoc = html.replace("&", "&amp;").replace('"', "&quot;")

    wrapper_html = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <style>
          html, body {{
            margin: 0;
            padding: 0;
            background: transparent;
            overflow: hidden;
          }}

          .{frame_class} {{
            background: transparent;
            padding-top: 0.25rem;
          }}

          .{frame_class} iframe {{
            width: 100%;
            height: {height}px;
            border: 0;
            border-radius: 18px;
            background: white;
          }}
        </style>
      </head>
      <body>
        <div class="{frame_class}">
          <iframe
            srcdoc="{escaped_srcdoc}"
            {"scrolling='yes'" if scrolling else "scrolling='no'"}
            sandbox="allow-scripts allow-same-origin allow-popups allow-forms"
            allowfullscreen
          ></iframe>
        </div>
      </body>
    </html>
    """

    st.components.v1.html(
        wrapper_html,
        height=height + 8,
        scrolling=False,
    )
    return True


def render_tag_pills(values: Iterable[str], *, accent: bool = False) -> None:
    items = [str(value) for value in values if str(value).strip()]
    if not items:
        st.markdown('<div class="tmk-note">None</div>', unsafe_allow_html=True)
        return

    class_name = "tmk-pill tmk-pill-accent" if accent else "tmk-pill"
    pills = "".join(
        f'<span class="{class_name}">{escape(item)}</span>'
        for item in items
    )
    st.markdown(f'<div class="tmk-soft-list">{pills}</div>', unsafe_allow_html=True)


def render_pattern_view(
    *,
    patterns,
    selected_pattern,
    pattern_products,
) -> None:
    """
    Render pattern-first view for Structural Planner.

    UI only.
    Receives precomputed pattern data from services/view models.
    No TMK logic is computed here.
    """
    pattern_map = {pattern.id: pattern for pattern in patterns}
    pattern = pattern_map.get(selected_pattern)

    if not pattern:
        st.warning("Pattern not found.")
        return

    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tmk-section-title">{escape(pattern.name)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="tmk-section-subtitle">{escape(pattern.learner_label)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="tmk-small-label" style="margin-top:0.35rem;">Stage {escape(pattern.stage)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="tmk-note" style="margin-top:0.5rem;">{escape(pattern.teacher_note)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Prompt</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="tmk-value">{escape(pattern.short_prompt)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Child text</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="tmk-note">{escape(pattern.child_text)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Canonical examples</div>', unsafe_allow_html=True)

        if pattern.examples:
            for value in pattern.examples:
                st.markdown(
                    f'<div class="tmk-answer-box">{escape(str(value))}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                '<div class="tmk-note">No examples provided.</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-small-label">Products showing this pattern</div>',
        unsafe_allow_html=True,
    )

    if pattern_products:
        render_tag_pills((str(product) for product in pattern_products), accent=True)
    else:
        st.markdown(
            '<div class="tmk-note">No products mapped.</div>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
