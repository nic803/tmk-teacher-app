from __future__ import annotations

from html import escape
from typing import Any, Iterable

import streamlit as st

from domain.routes import (
    canonical_routes_for,
    derived_routes_for,
)
from domain.products import PRODUCTS
from domain.product_metadata import PRODUCT_METADATA
from domain.stage_vocabulary import STAGE_LABELS

from worksheets.generator import generate_worksheet_bundle


SURFACES = (
    "Structural Planner",
    "Product Lab",
    "Worksheet Studio",
)


# -----------------------------------------------------
# Navigation
# -----------------------------------------------------

def _render_nav() -> str:
    return st.radio(
        "Surface",
        SURFACES,
        horizontal=True,
        label_visibility="collapsed",
    )


# -----------------------------------------------------
# Structural Planner
# -----------------------------------------------------

def _render_structural_planner() -> None:

    st.title("Structural Planner")

    stage = st.selectbox(
        "Stage",
        list(STAGE_LABELS.keys()),
        format_func=lambda s: STAGE_LABELS.get(s, s),
    )

    stage_products = [
        p for p in PRODUCTS if PRODUCT_METADATA[p]["stage"] == stage
    ]

    st.subheader("Products introduced")

    cols = st.columns(6)

    for i, product in enumerate(stage_products):
        with cols[i % 6]:
            st.button(str(product), key=f"planner_product_{product}")

    st.divider()

    st.subheader("Stage role")

    role = PRODUCT_METADATA.get(stage_products[0], {}).get("role", "")

    st.write(role)


# -----------------------------------------------------
# Product Lab
# -----------------------------------------------------

def _render_product_lab() -> None:

    st.title("Product Lab")

    product = st.selectbox(
        "Product",
        PRODUCTS,
        format_func=str,
    )

    meta = PRODUCT_METADATA.get(product, {})

    st.markdown("### Product identity")

    st.write(
        {
            "product": product,
            "stage": meta.get("stage"),
            "role": meta.get("role"),
        }
    )

    st.divider()

    st.markdown("### Canonical routes")

    routes = canonical_routes_for(product)

    for r in routes:
        st.write(f"{r['a']} × {r['b']}")

    st.divider()

    st.markdown("### Derived routes")

    derived = derived_routes_for(product)

    for r in derived:
        st.write(f"{r['source']} → {r['product']}")


# -----------------------------------------------------
# Worksheet Studio
# -----------------------------------------------------

def _render_worksheet_studio() -> None:

    st.title("Worksheet Studio")

    stage = st.selectbox(
        "Stage",
        list(STAGE_LABELS.keys()),
        format_func=lambda s: STAGE_LABELS.get(s, s),
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Core", "Stretch"],
    )

    if st.button("Generate worksheet"):

        bundle = generate_worksheet_bundle(
            stage=stage,
            difficulty=difficulty,
        )

        st.session_state["worksheet_bundle"] = bundle

    bundle = st.session_state.get("worksheet_bundle")

    if bundle:

        st.subheader("Worksheet preview")

        for line in bundle["questions"]:
            st.write(line)


# -----------------------------------------------------
# Main
# -----------------------------------------------------

def main() -> None:

    surface = _render_nav()

    if surface == "Structural Planner":
        _render_structural_planner()

    elif surface == "Product Lab":
        _render_product_lab()

    elif surface == "Worksheet Studio":
        _render_worksheet_studio()


if __name__ == "__main__":
    main()
