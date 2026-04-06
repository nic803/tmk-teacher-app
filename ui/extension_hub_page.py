from __future__ import annotations

import streamlit as st


def render_eleven_foundations() -> None:
    st.subheader("11× Foundations")
    st.caption("Derive 11× from known structure")
    st.markdown("Main teaching rule:")
    st.latex(r"11 \times n = 10 \times n + 1 \times n")
    st.markdown("### Pattern bank")
    st.write("Ten-plus-one rule: build 11× from 10× and 1×.")
    st.write("Repeated-digit pattern for 11 × 1 to 11 × 9.")
    st.write("Beyond repeated digits: keep using 10× + 1×.")
    st.write("11× opens new extension routes without replacing core routes.")


def render_twelve_foundations() -> None:
    st.subheader("12× Foundations")
    st.caption("Derive 12× from known structure")
    st.markdown("Main teaching rule:")
    st.latex(r"12 \times n = 10 \times n + 2 \times n")
    st.markdown("Support rule:")
    st.latex(r"12 \times n = 2(6 \times n)")
    st.markdown("### Clock cue")
    st.write("A clock has 12 equal sections of 5 minutes.")
    st.latex(r"12 \times 5 = 60")


def render_twelve_route_opening() -> None:
    st.subheader("12× Route Opening")
    st.caption("New extension routes opened through 12×")
    st.write("24: core 4 × 6, 3 × 8 | extension 2 × 12")
    st.write("36: core 4 × 9, 6 × 6 | extension 3 × 12")
    st.write("48: core 6 × 8 | extension 4 × 12")
    st.write("60: core 6 × 10 | extension 5 × 12")
    st.write("72: core 8 × 9 | extension 6 × 12")


def render_core_extension_route_comparison() -> None:
    st.subheader("Core or Extension Route?")
    st.caption("Keep core routes and extension routes separate")
    st.latex(r"\text{core routes} \neq \text{extension routes}")


def render_twelve_derivation_practice() -> None:
    st.subheader("12× Derivation Practice")
    st.caption("Select one 12× fact and derive it from known structure")
    selected_n = st.selectbox("Choose n in 12 × n", options=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12], index=0)
    products = {3: 36, 4: 48, 5: 60, 6: 72, 7: 84, 8: 96, 9: 108, 10: 120, 11: 132, 12: 144}
    p = products[selected_n]
    st.write(f"Selected fact: 12 × {selected_n} = {p}")
    st.write(f"Main derivation: 12 × {selected_n} = 10 × {selected_n} + 2 × {selected_n}")
    st.write(f"Support derivation: 12 × {selected_n} = 2(6 × {selected_n})")


def render_square_strand_intro() -> None:
    st.markdown("---")
    st.markdown("## Square Numbers and Square Roots")


def render_square_numbers_recap() -> None:
    st.subheader("Square Numbers Recap")


def render_square_roots() -> None:
    st.subheader("Square Roots")


def render_odd_even_square_patterns() -> None:
    st.subheader("Odd and Even Square Patterns")


def render_exponent_power_notes() -> None:
    st.subheader("Exponent, Power, and Power of 2")


def render_square_product_selector() -> None:
    st.subheader("Square Product Selector")


def render_square_or_not_square() -> None:
    st.subheader("Square or Not Square?")


def render_extension_hub_page() -> None:
    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Extension Hub</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Resources for teaching 11× and 12×, opening new routes, and extending beyond the core TMK world.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("## 11× and 12× Foundations")
    st.caption("A separate extension strand for derivation rules, clock support, and route opening.")
    render_eleven_foundations()
    render_twelve_foundations()
    render_twelve_route_opening()
    render_core_extension_route_comparison()
    render_twelve_derivation_practice()

    render_square_strand_intro()
    render_square_numbers_recap()
    render_square_roots()
    render_odd_even_square_patterns()
    render_exponent_power_notes()
    render_square_product_selector()
    render_square_or_not_square()

    st.markdown("</div>", unsafe_allow_html=True)
