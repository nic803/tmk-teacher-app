from __future__ import annotations

from pathlib import Path

import streamlit as st


def render_number_line_doubler_page() -> None:
    html_path = Path(__file__).parent / "static" / "number_line_doubler.html"

    if not html_path.exists():
        st.error(f"Game file not found: {html_path}")
        return

    html = html_path.read_text(encoding="utf-8")

    st.markdown(
        """
        <style>
            .tmk-game-frame {
                background: transparent;
                padding-top: 0.25rem;
            }

            .tmk-game-frame iframe {
                border-radius: 18px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="tmk-game-frame">', unsafe_allow_html=True)
    st.components.v1.html(
        html,
        height=980,
        scrolling=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
