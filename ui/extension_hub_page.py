from __future__ import annotations

from pathlib import Path

import streamlit as st


def render_extension_hub_page() -> None:
    st.title("EXTENSION HUB DIAGNOSTIC")
    st.write("If you can read this, the edited file is being loaded.")
    st.write(f"Loaded from: {Path(__file__).resolve()}")
    st.write("SENTINEL: TMK-EXTENSION-HUB-NEW-FILE")
