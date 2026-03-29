from __future__ import annotations

import streamlit as st


def page_header(title: str, subtitle: str | None = None) -> None:
    st.markdown(
        f"""
        <div class="tmk-card" style="margin-bottom:1rem;">
            <div class="tmk-section-title">{title}</div>
            {f'<div class="tmk-section-subtitle">{subtitle}</div>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )
