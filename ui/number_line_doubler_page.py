from __future__ import annotations

from pathlib import Path

import streamlit as st

from ui.components import (
    render_html_resource,
    resource_child_prompt_strip,
    resource_controls_footer,
    resource_equation_box,
    resource_header_bar,
    resource_main_interaction_end,
    resource_main_interaction_start,
    resource_pattern_focus_strip,
    resource_teacher_panel,
)


def render_number_line_doubler_page() -> None:
    html_path = Path(__file__).parent / "static" / "number_line_doubler.html"

    resource_header_bar(
        title="Number Line Doubler",
        stage="E",
        pattern="Doubling chain",
        purpose="A live doubling animation that makes repeated doubling visible before wider comparison.",
        action_labels=(),
        action_key_prefix="number_line_doubler_header_action",
    )

    resource_main_interaction_start()
    rendered = render_html_resource(
        html_path=html_path,
        height=980,
        scrolling=True,
        frame_class="tmk-game-frame",
    )
    resource_main_interaction_end()

    if not rendered:
        return

    resource_equation_box(
        title="Equation / product box",
        equations=(
            "6 → 12 → 24 → 48",
            "2 × 6 = 12",
            "2 × 12 = 24",
            "2 × 24 = 48",
        ),
    )

    resource_child_prompt_strip(
        "What do you notice each time the value doubles?"
    )

    resource_pattern_focus_strip(
        "Doubling chain"
    )

    resource_teacher_panel(
        msvwa={
            "marker": "The pupil notices that each step is built by doubling the previous value.",
            "sequence": "The pupil can follow the order of the chain from start value to later products.",
            "variation": "The pupil can recognise doubling structure across more than one starting value.",
            "working_memory": "The pupil keeps the current value in mind while building the next doubled value.",
            "attention": "The pupil attends to the multiplicative growth pattern rather than isolated answers.",
        },
        diagnostics={
            "look_for": "Whether the pupil can say what changes at each step and identify the next doubled value.",
            "secure_if": "The pupil can track the chain accurately and explain that each new value is double the previous one.",
            "watch_for": "Losing the current value, skipping a step, or treating the chain as unrelated facts.",
            "prompt_if_stuck": "What is double this number? What would the next step be?",
            "if_knowledge_is_missing": "Return to one clear doubling step with concrete examples before extending the chain.",
            "next_move": "Move from one visible doubling chain to related TMK products that share the same structural idea.",
        },
        expanded=False,
        label="Teacher panel",
    )

    resource_controls_footer(
        controls=(),
        key_prefix="number_line_doubler_footer_control",
    )
