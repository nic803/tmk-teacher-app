from __future__ import annotations

import streamlit as st


def render_square_numbers_recap() -> None:
    st.subheader("Square Numbers Recap")
    st.caption("Known products with a same-factor route")
    st.markdown(r"A square number has a route of the form \(n \times n\).")
    st.markdown(r"\(n \times n = n^2\)")


def render_extension_hub_page() -> None:
    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Extension Hub</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Resources for teaching 11× and 12×, opening new routes, and extending beyond the core TMK world.</div>',
        unsafe_allow_html=True,
    )

    render_square_numbers_recap()

    st.markdown("</div>", unsafe_allow_html=True)
