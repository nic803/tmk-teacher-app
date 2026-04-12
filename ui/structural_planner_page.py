import streamlit as st

from ui.components import (
    page_header,
    render_cumulative_product_map,
    render_stage_summary,
    # NEW (you will add this component next step)
    render_pattern_view,
)


def render_structural_planner_page(view_model):
    """
    UI-only page.
    Receives data from services.
    No TMK logic allowed here.
    """

    title = view_model.get("title", "")
    subtitle = view_model.get("subtitle", "")

    # EXISTING
    cumulative_map = view_model.get("cumulative_map", {})
    selected_stage = view_model.get("selected_stage")
    active_product = view_model.get("active_product")
    stage_summary = view_model.get("stage_summary", {})

    # NEW
    view_mode = view_model.get("view_mode", "stage")
    patterns = view_model.get("patterns", ())
    selected_pattern = view_model.get("selected_pattern")
    pattern_products = view_model.get("pattern_products", ())

    page_header(title, subtitle)

    # =========================
    # 🔵 VIEW MODE SWITCH
    # =========================
    view_mode = st.radio(
        "View",
        options=["Stage", "Pattern"],
        horizontal=True,
        index=0 if view_mode == "stage" else 1,
    )

    # =========================
    # 🟢 STAGE VIEW (UNCHANGED)
    # =========================
    if view_mode == "Stage":
        render_cumulative_product_map(
            stage_products=cumulative_map,
            active_stage=selected_stage,
            active_product=active_product,
        )

        render_stage_summary(stage_summary)

    # =========================
    # 🟣 PATTERN VIEW (NEW)
    # =========================
    else:
        pattern_options = [p.id for p in patterns]

        selected_pattern = st.selectbox(
            "Select pattern",
            options=pattern_options,
            index=pattern_options.index(selected_pattern)
            if selected_pattern in pattern_options
            else 0,
        )

        render_pattern_view(
            patterns=patterns,
            selected_pattern=selected_pattern,
            pattern_products=pattern_products,
        )
