from __future__ import annotations

import streamlit as st


def render_extension_hub_page() -> None:
    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Extension Hub</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Smoke test: extension page import is working.</div>',
        unsafe_allow_html=True,
    )
    st.write("Import OK.")
    st.markdown("</div>", unsafe_allow_html=True)
