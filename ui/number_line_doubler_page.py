from __future__ import annotations

from pathlib import Path

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
        stage="Stage E — Doubling Chain (2× → 4× → 8×)",
        pattern="Fixed factor, doubled multiplier, doubled product",
        purpose=(
            "Show that 2×, 4×, and 8× are connected by doubling with one factor "
            "held fixed, so pupils move from skip-counting to structural comparison."
        ),
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
            "2 × 6 = 12",
            "4 × 6 = 24",
            "8 × 6 = 48",
        ),
    )

    resource_child_prompt_strip(
        "Double it, then double it again!"
    )

    resource_pattern_focus_strip(
        "Fixed factor, doubled multiplier, doubled product"
    )

    resource_teacher_panel(
        msvwa={
            "marker": "The fixed factor stays the same across the chain.",
            "sequence": "The pupil follows the order 2×, 4×, 8× and links each step to a doubled product.",
            "variation": "The multiplier and product change; the factor stays fixed.",
            "working_memory": "Hold the fixed factor, jump sequence, and matching equations together.",
            "attention": "Notice the fixed factor first, then the doubling in the multiplier and product.",
        },
        diagnostics={
            "look_for": "Whether the pupil can identify the fixed factor and explain how the products grow as the multiplier doubles.",
            "secure_if": "The pupil can explain one fixed-factor family clearly and track how doubling the multiplier doubles the product.",
            "watch_for": "Missing the fixed factor, treating each fact as unrelated, or losing the doubling relationship across the chain.",
            "prompt_if_stuck": "What stays the same? Which number doubles? What happens to the product when the multiplier doubles?",
            "if_knowledge_is_missing": "Fixed factor not seen → Rebuild one factor family. Example: 2 × 7 = 14, 4 × 7 = 28, 8 × 7 = 56",
            "next_move": "Change/stay confusion → Name the fixed factor and changing multiplier. Example: 7 stays fixed; 2, 4, 8 change",
        },
        expanded=False,
        label="Teacher panel",
    )

    resource_controls_footer(
        controls=(),
        key_prefix="number_line_doubler_footer_control",
    )
