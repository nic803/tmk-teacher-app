import streamlit as st

from ui.components import (
    page_header,
    render_cumulative_product_map,
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

    page_header(
        title,
        subtitle,
    )

    render_cumulative_product_map(
        stage_products=cumulative_map,
        active_stage=selected_stage,
        active_product=active_product,
    )

    render_stage_summary(
        stage_summary,
    )
