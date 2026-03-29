from __future__ import annotations

import streamlit as st

from ui.components import page_header

_EXTENSION_SECTION_KEY = "extension_section_v1"


def render_extension_page() -> None:
    _ensure_extension_state()

    page_header(
        "Extension 11× 12×",
        "Extension content sits outside the bounded TMK core and should be explored separately from core stage structure.",
    )

    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Extension landing page</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Choose one extension area. This page is a stable entry point only and does not alter core TMK products or stages.</div>',
        unsafe_allow_html=True,
    )

    if st.session_state[_EXTENSION_SECTION_KEY] == "landing":
        _render_extension_cards()
    elif st.session_state[_EXTENSION_SECTION_KEY] == "products_hub":
        _render_products_hub_placeholder()
    elif st.session_state[_EXTENSION_SECTION_KEY] == "animations":
        _render_animations_placeholder()
    else:
        st.session_state[_EXTENSION_SECTION_KEY] = "landing"
        _render_extension_cards()

    st.markdown("</div>", unsafe_allow_html=True)


def _ensure_extension_state() -> None:
    if _EXTENSION_SECTION_KEY not in st.session_state:
        st.session_state[_EXTENSION_SECTION_KEY] = "landing"


def _render_extension_cards() -> None:
    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Extension area</div>', unsafe_allow_html=True)
        st.markdown('<div class="tmk-value">Products Hub</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="tmk-note" style="margin-top:0.45rem;">Browse 11× and 12× extension products as objects, compare lawful builds, and keep extension reasoning separate from the core TMK stage system.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="tmk-note" style="margin-top:0.45rem;"><strong>Planned focus:</strong> product selection, family filter, compare forms, lawful builds.</div>',
            unsafe_allow_html=True,
        )
        if st.button(
            "Open Products Hub",
            key="extension_open_products_hub_v1",
            use_container_width=True,
        ):
            st.session_state[_EXTENSION_SECTION_KEY] = "products_hub"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        st.markdown('<div class="tmk-small-label">Extension area</div>', unsafe_allow_html=True)
        st.markdown('<div class="tmk-value">Animations</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="tmk-note" style="margin-top:0.45rem;">Open extension animation resources for 11× and 12× without mixing them into the core resource library or TMK stage structure.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="tmk-note" style="margin-top:0.45rem;"><strong>Planned focus:</strong> animation browser, family tags, player page, reduced or full teacher support.</div>',
            unsafe_allow_html=True,
        )
        if st.button(
            "Open Animations",
            key="extension_open_animations_v1",
            use_container_width=True,
        ):
            st.session_state[_EXTENSION_SECTION_KEY] = "animations"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def _render_products_hub_placeholder() -> None:
    _render_back_button()

    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Products Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="tmk-value">Extension Products Hub</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-note" style="margin-top:0.45rem;">This placeholder reserves the dedicated extension area for 11× and 12× product work.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tmk-note" style="margin-top:0.45rem;">Next step here: connect the page to the extension products registry and render family filter, product selector, lawful build forms, and comparison support.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def _render_animations_placeholder() -> None:
    _render_back_button()

    st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-small-label">Animations</div>', unsafe_allow_html=True)
    st.markdown('<div class="tmk-value">Extension Animations Browser</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-note" style="margin-top:0.45rem;">This placeholder reserves the dedicated extension animation area.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tmk-note" style="margin-top:0.45rem;">Next step here: connect the page to the extension animations registry and render animation cards with family tags and open actions.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def _render_back_button() -> None:
    back_col, _ = st.columns((0.22, 0.78))
    with back_col:
        if st.button(
            "Back",
            key="extension_back_to_landing_v1",
            use_container_width=True,
        ):
            st.session_state[_EXTENSION_SECTION_KEY] = "landing"
            st.rerun()
