import streamlit as st

from ui.components import (
    page_header,
    render_cumulative_product_map,
    render_pattern_view,
    render_stage_summary,
)


def render_structural_planner_page(view_model):
    """
    UI-only page.
    Receives data from services.
    No TMK logic allowed here.
    """

    title = view_model.get("title", "")
    subtitle = view_model.get("subtitle", "")

    cumulative_map = view_model.get("cumulative_map", {})
    selected_stage = view_model.get("selected_stage")
    active_product = view_model.get("active_product")
    stage_summary = view_model.get("stage_summary", {})

    patterns = view_model.get("patterns", ())
    selected_pattern = view_model.get("selected_pattern")
    pattern_products = view_model.get("pattern_products", ())

    default_mode = view_model.get("view_mode", "stage").lower()
    mode_index = 0 if default_mode == "stage" else 1

    page_header(title, subtitle)

    view_mode = st.radio(
        "Planner view",
        options=["Stage", "Pattern"],
        index=mode_index,
        horizontal=True,
    )

    if view_mode == "Stage":
        render_cumulative_product_map(
            stage_products=cumulative_map,
            active_stage=selected_stage,
            active_product=active_product,
        )
        render_stage_summary(stage_summary)
        return

    if not patterns:
        st.info("No pattern data supplied to the Structural Planner.")
        return

    pattern_options = [pattern.id for pattern in patterns]
    pattern_labels = {
        pattern.id: f"{pattern.name} ({pattern.stage})"
        for pattern in patterns
    }

    if selected_pattern not in pattern_options:
        selected_pattern = pattern_options[0]

    selected_pattern = st.selectbox(
        "Select pattern",
        options=pattern_options,
        index=pattern_options.index(selected_pattern),
        format_func=lambda pattern_id: pattern_labels.get(pattern_id, pattern_id),
    )

    render_pattern_view(
        patterns=patterns,
        selected_pattern=selected_pattern,
        pattern_products=pattern_products,
    )
