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
            "Doubling Route:",
            "6 → 12 → 24 → 48",
            "Matching Products:",
            "2 × 6 = 12",
            "4 × 6 = 24",
            "8 × 6 = 48",
        ),
    )

    resource_child_prompt_strip(
        "What do you notice each time the multiplier doubles?"
    )

    resource_pattern_focus_strip(
        "Doubling chain"
    )

    resource_teacher_panel(
        msvwa={
            "marker": "The pupil notices that the same factor stays fixed while the multiplier doubles.",
            "sequence": "The pupil can follow the chain in order and link each product to the same starting factor.",
            "variation": "The pupil can say what changes and what stays the same across 2×, 4×, and 8×.",
            "working_memory": "The pupil holds the fixed factor and the growing products together while tracking the doubling pattern.",
            "attention": "The pupil attends first to the fixed factor and then to how doubling the multiplier doubles the product.",
        },
        diagnostics={
            "look_for": "Whether the pupil can identify the fixed factor and explain how the products grow as the multiplier doubles.",
            "secure_if": "The pupil can say, for example, 2 × 6 = 12, 4 × 6 = 24, 8 × 6 = 48, and explain that the 6 stays the same.",
            "watch_for": "Treating each new product as a new starting number, losing the fixed factor, or seeing the facts as unrelated.",
            "prompt_if_stuck": "What stays the same in all three facts? Which number doubles each time? What happens to the product when the multiplier doubles?",
            "if_knowledge_is_missing": "Return to one fixed-factor set and compare the equations side by side, for example: 2 × 6 = 12, 4 × 6 = 24, 8 × 6 = 48, before extending to another factor such as 7.",
            "next_move": "Try another fixed-factor chain and compare it to the first one, for example: 2 × 6 = 12, 4 × 6 = 24, 8 × 6 = 48, then 2 × 7 = 14, 4 × 7 = 28, 8 × 7 = 56. Ask what stays fixed and what changes.",
        },
        expanded=False,
        label="Teacher panel",
    )

    resource_controls_footer(
        controls=(),
        key_prefix="number_line_doubler_footer_control",
    )
