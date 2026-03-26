import streamlit as st

from ui.components import (
    page_header,
    render_product_hub,
    render_product_identity,
    render_relationships_card,
)


def render_product_lab_page(view_model):

    page_header(
        view_model["title"],
        view_model["subtitle"]
    )

    render_product_hub(
        product_label=view_model["product_meta"]["product"],
        entry_routes=view_model["entry_routes"],
        exit_routes=view_model["exit_routes"]
    )

    render_product_identity(
        view_model["product_meta"]
    )

    render_relationships_card(
        "Representations",
        view_model["representations"]
    )

    render_relationships_card(
        "Inverse Links",
        view_model["inverse_links"]
    )
