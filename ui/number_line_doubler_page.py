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
from ui.core_resource_registry import get_core_resource


def render_number_line_doubler_page() -> None:
    resource = get_core_resource("number_line_doubler")
    html_path = Path(__file__).parent / "static" / str(resource["asset_path"])

    resource_header_bar(
        title=str(resource["title"]),
        stage=str(resource["stage"]),
        pattern=str(resource["pattern"]),
        purpose=str(resource["purpose"]),
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

    equation_meta = dict(resource.get("equations", {}))
    equation_examples = tuple(str(item) for item in equation_meta.get("examples", ()))

    resource_equation_box(
        title="Equation / product box",
        equations=equation_examples,
    )

    resource_child_prompt_strip(
        str(resource.get("prompt", ""))
    )

    resource_pattern_focus_strip(
        str(resource.get("pattern", ""))
    )

    teacher_panel = dict(resource.get("teacher_panel", {}))
    msvwa = dict(teacher_panel.get("msvwa", {}))
    diagnostics = dict(teacher_panel.get("diagnostics", {}))

    resource_teacher_panel(
        msvwa=msvwa,
        diagnostics=diagnostics,
        expanded=False,
        label="Teacher panel",
    )

    controls = tuple(str(item) for item in resource.get("controls", ()))
    resource_controls_footer(
        controls=controls,
        key_prefix="number_line_doubler_footer_control",
    )
