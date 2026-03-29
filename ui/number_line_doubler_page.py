from __future__ import annotations
import streamlit as st
from pathlib import Path

def render_number_line_doubler_page() -> None:

    st.markdown("## Number Line Doubler")
    st.caption("Interactive TMK number line doubling race")

    html_path = Path(__file__).parent / "static" / "number_line_doubler.html"

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    st.components.v1.html(
        html,
        height=700,
        scrolling=False
    )
