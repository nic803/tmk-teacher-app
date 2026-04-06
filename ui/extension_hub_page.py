from __future__ import annotations

import streamlit as st


def render_square_numbers_recap() -> None:
    st.subheader("Square Numbers Recap")
    st.caption("Known products with a same-factor route")

    st.markdown("A square number has a route of the form:")
    st.latex(r"n \times n")
    st.latex(r"n \times n = n^2")

    st.markdown("### Core squares")
    core_examples = [
        "1 = 1 × 1",
        "4 = 2 × 2 = 1 × 4",
        "9 = 3 × 3 = 1 × 9",
        "16 = 4 × 4 = 2 × 8",
        "25 = 5 × 5",
        "36 = 6 × 6 = 4 × 9",
        "49 = 7 × 7",
        "64 = 8 × 8",
        "81 = 9 × 9",
        "100 = 10 × 10",
    ]
    for example in core_examples:
        st.write(example)

    st.markdown("### Extension squares")
    extension_examples = [
        "121 = 11 × 11",
        "144 = 12 × 12",
    ]
    for example in extension_examples:
        st.write(example)

    with st.expander("Pattern bank"):
        st.write("A square number has a same-factor route.")
        st.write("Some squares have only the square route in this bounded view.")
        st.write("Some squares also connect to another factor family.")
        st.write("Core and extension squares should stay visibly separate.")

    activity_text = (
        "Square Numbers Recap\n\n"
        "Focus: Recognise square numbers as products with a same-factor route.\n\n"
        "Teacher explanation: A square number is a product that can be made with the same factor twice.\n"
        "Teacher prompt: Which products have a route of the form n × n?\n\n"
        "Pupil tasks:\n"
        "- Circle the square numbers.\n"
        "- Write the square route for each one.\n"
        "- Decide whether each square has only one route or more than one route.\n\n"
        "Example questions:\n"
        "- Why is 25 a square number?\n"
        "- Which route shows that 36 is square?\n"
        "- Which extension squares come after 100?\n\n"
        "Teaching note: Keep square structure product-first. Start from routes in."
    )
    st.text_area(
        "Copy-paste print text — Square Numbers Recap",
        activity_text,
        height=260,
        key="square_numbers_recap_copy_box",
    )


def render_square_roots() -> None:
    st.subheader("Square Roots")
    st.caption("Recover the equal factor from a square product")

    st.markdown("A square root tells us which equal factor builds a square product.")
    st.latex(r"\sqrt{n} = a \iff a \times a = n")

    st.markdown("### Core square roots")
    core_examples = [
        ("√1", "1", "1 × 1 = 1"),
        ("√4", "2", "2 × 2 = 4"),
        ("√9", "3", "3 × 3 = 9"),
        ("√16", "4", "4 × 4 = 16"),
        ("√25", "5", "5 × 5 = 25"),
        ("√36", "6", "6 × 6 = 36"),
        ("√49", "7", "7 × 7 = 49"),
        ("√64", "8", "8 × 8 = 64"),
        ("√81", "9", "9 × 9 = 81"),
        ("√100", "10", "10 × 10 = 100"),
    ]
    for root_text, value, reason in core_examples:
        st.write(f"{root_text} = {value} because {reason}")

    st.markdown("### Extension square roots")
    extension_examples = [
        ("√121", "11", "11 × 11 = 121"),
        ("√144", "12", "12 × 12 = 144"),
    ]
    for root_text, value, reason in extension_examples:
        st.write(f"{root_text} = {value} because {reason}")

    with st.expander("Teacher note"):
        st.write(
            "Keep square root as same-factor recovery. Start from the product, "
            "find the equal-factor route, then name the square root."
        )

    activity_text = (
        "Square Roots\n\n"
        "Focus: Recover the equal factor from a square product.\n\n"
        "Teacher explanation: A square root tells us which equal factor builds the square product.\n"
        "Teacher prompt: Which number times itself makes this product?\n\n"
        "Pupil tasks:\n"
        "- Match each square product to its square root.\n"
        "- Explain each answer using a same-factor route.\n"
        "- Separate core square roots from extension square roots.\n\n"
        "Example questions:\n"
        "- What is the square root of 36?\n"
        "- Why is the square root of 49 equal to 7?\n"
        "- Which extension square root matches 121?\n"
        "- Which extension square root matches 144?\n\n"
        "Teaching note: Keep square root as same-factor recovery, not as a detached symbol rule."
    )
    st.text_area(
        "Copy-paste print text — Square Roots",
        activity_text,
        height=260,
        key="square_roots_copy_box",
    )


def render_odd_even_square_patterns() -> None:
    st.subheader("Odd and Even Square Patterns")
    st.caption("Look at parity in square products")

    st.markdown("Square parity follows the parity of the repeated factor.")
    st.latex(r"\text{if } n \text{ is even, then } n^2 \text{ is even}")
    st.latex(r"\text{if } n \text{ is odd, then } n^2 \text{ is odd}")

    st.markdown("### Even squares")
    even_examples = [
        "2 × 2 = 4",
        "4 × 4 = 16",
        "6 × 6 = 36",
        "8 × 8 = 64",
        "10 × 10 = 100",
        "12 × 12 = 144",
    ]
    for example in even_examples:
        st.write(example)

    st.markdown("### Odd squares")
    odd_examples = [
        "1 × 1 = 1",
        "3 × 3 = 9",
        "5 × 5 = 25",
        "7 × 7 = 49",
        "9 × 9 = 81",
        "11 × 11 = 121",
    ]
    for example in odd_examples:
        st.write(example)

    st.markdown("### Notice")
    st.write("Even inputs give even square products.")
    st.write("Odd inputs give odd square products.")
    st.write("There is no odd number with an even square.")
    st.write("There is no even number with an odd square.")

    with st.expander("Pattern bank"):
        st.write("Even × even gives an even square.")
        st.write("Odd × odd gives an odd square.")
        st.write("This pattern continues for 11² and 12².")

    activity_text = (
        "Odd and Even Square Patterns\n\n"
        "Focus: Notice parity patterns in square products.\n\n"
        "Teacher explanation: Square products keep the odd/even structure of the repeated factor.\n"
        "Teacher prompt: Look at the factor first. Is it odd or even? Then predict the square product.\n\n"
        "Pupil tasks:\n"
        "- Sort square products into odd squares and even squares.\n"
        "- Match each square product to an odd factor or an even factor.\n"
        "- Explain why 121 is odd and 144 is even.\n\n"
        "Example questions:\n"
        "- Is 25 an odd square or an even square?\n"
        "- Why is 36 an even square?\n"
        "- What do you notice about 49 and 81?\n"
        "- Why is 144 even?\n\n"
        "Teaching note: Keep the language product-first. Start from the route n × n, then classify the square by parity."
    )
    st.text_area(
        "Copy-paste print text — Odd and Even Square Patterns",
        activity_text,
        height=260,
        key="odd_even_squares_copy_box",
    )


def render_extension_hub_page() -> None:
    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Extension Hub</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Resources for teaching 11× and 12×, opening new routes, and extending beyond the core TMK world.</div>',
        unsafe_allow_html=True,
    )

    render_square_numbers_recap()
    render_square_roots()
    render_odd_even_square_patterns()

    st.markdown("</div>", unsafe_allow_html=True)
