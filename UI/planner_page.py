import streamlit as st

from ui.components import (
    page_header,
    render_cumulative_product_map,
    render_stage_summary
)


def render_structural_planner_page(view_model):
    """
    UI-only page.
    Receives data from services.
    No TMK logic allowed here.
    """

    page_header(
        view_model["title"],
        view_model["subtitle"]
    )

    render_cumulative_product_map(
        stage_products=view_model["cumulative_map"],
        active_stage=view_model["selected_stage"],
        active_product=view_model.get("active_product")
    )

    render_stage_summary(
        view_model["stage_summary"]
    )
