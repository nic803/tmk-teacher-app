from __future__ import annotations

import streamlit as st


def render_square_numbers_recap() -> None:
    st.subheader("Square Numbers Recap")
    st.caption("Known products with a same-factor route")

    st.markdown(r"A square number has a route of the form \(n \times n\).")
    st.markdown(r"\(n \times n = n^2\)")

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

    st.markdown(
        "A square root tells us which equal factor builds a square product."
    )
    st.markdown(r"\(\sqrt{n} = a \iff a \times a = n\)")

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

    st.markdown(
        r"If \(n\) is even, then \(n^2\) is even. If \(n\) is odd, then \(n^2\) is odd."
    )

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
        st.write("Square parity follows the parity of the repeated factor.")
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


def render_exponent_power_notes() -> None:
    st.subheader("Exponent, Power, and Power of 2")
    st.caption("New vocabulary for square notation and repeated factors")

    st.markdown(r"In \(n^2\), the small raised \(2\) is the exponent.")
    st.markdown(r"\(n^2\) is read as 'n squared' or 'n to the power of 2'.")

    st.markdown("### Square examples")
    square_examples = [
        "3² = 9 because 3 × 3 = 9",
        "5² = 25 because 5 × 5 = 25",
        "11² = 121 because 11 × 11 = 121",
        "12² = 144 because 12 × 12 = 144",
    ]
    for example in square_examples:
        st.write(example)

    st.markdown("### Power of 2 examples")
    power_two_examples = [
        "2¹ = 2",
        "2² = 4",
        "2³ = 8",
        "2⁴ = 16",
        "2⁵ = 32",
        "2⁶ = 64",
    ]
    for example in power_two_examples:
        st.write(example)

    st.markdown("### Important distinction")
    st.write("A square number has the form n × n.")
    st.write("A power of 2 has base 2 repeated several times.")
    st.write("These ideas sometimes overlap, but they are not the same idea.")
    st.write("For example, 4 = 2² is both a square number and a power of 2.")
    st.write("But 25 = 5² is a square number and not a power of 2.")
    st.write("And 32 = 2⁵ is a power of 2 and not a square number.")

    with st.expander("Teacher note"):
        st.write(
            "Keep the distinction very explicit. Pupils often confuse "
            "'squared' with 'power of 2'."
        )

    activity_text = (
        "Exponent, Power, and Power of 2\n\n"
        "Focus: Distinguish square notation from powers of 2.\n\n"
        "Teacher explanation: In n², the exponent 2 means the same factor is used twice. "
        "In 2^n, the base stays 2 and the exponent changes how many 2s are multiplied.\n"
        "Teacher prompt: Is this number a square, a power of 2, both, or neither?\n\n"
        "Pupil tasks:\n"
        "- Match square notation to multiplication form.\n"
        "- Sort numbers into square, power of 2, both, or neither.\n"
        "- Explain why 25 is square but not a power of 2.\n"
        "- Explain why 32 is a power of 2 but not a square.\n\n"
        "Example questions:\n"
        "- What does the exponent mean in 6²?\n"
        "- Why is 4 both a square number and a power of 2?\n"
        "- Why is 121 a square number?\n"
        "- Is 64 a square number, a power of 2, or both?\n\n"
        "Teaching note: Keep 'square' linked to the route n × n, and 'power of 2' linked to repeated multiplication by 2."
    )
    st.text_area(
        "Copy-paste print text — Exponent, Power, and Power of 2",
        activity_text,
        height=280,
        key="exponent_power_copy_box",
    )


def render_square_product_selector() -> None:
    st.subheader("Square Product Selector")
    st.caption("Choose a square product and inspect its routes and patterns")

    square_records = {
        1: {
            "square_route": "1 × 1",
            "other_routes": [],
            "square_root": 1,
            "parity": "odd",
            "boundary": "core",
            "route_type": "single-route square",
        },
        4: {
            "square_route": "2 × 2",
            "other_routes": ["1 × 4"],
            "square_root": 2,
            "parity": "even",
            "boundary": "core",
            "route_type": "multi-route square",
        },
        9: {
            "square_route": "3 × 3",
            "other_routes": ["1 × 9"],
            "square_root": 3,
            "parity": "odd",
            "boundary": "core",
            "route_type": "multi-route square",
        },
        16: {
            "square_route": "4 × 4",
            "other_routes": ["2 × 8"],
            "square_root": 4,
            "parity": "even",
            "boundary": "core",
            "route_type": "multi-route square",
        },
        25: {
            "square_route": "5 × 5",
            "other_routes": [],
            "square_root": 5,
            "parity": "odd",
            "boundary": "core",
            "route_type": "single-route square",
        },
        36: {
            "square_route": "6 × 6",
            "other_routes": ["4 × 9"],
            "square_root": 6,
            "parity": "even",
            "boundary": "core",
            "route_type": "multi-route square",
        },
        49: {
            "square_route": "7 × 7",
            "other_routes": [],
            "square_root": 7,
            "parity": "odd",
            "boundary": "core",
            "route_type": "single-route square",
        },
        64: {
            "square_route": "8 × 8",
            "other_routes": [],
            "square_root": 8,
            "parity": "even",
            "boundary": "core",
            "route_type": "single-route square",
        },
        81: {
            "square_route": "9 × 9",
            "other_routes": [],
            "square_root": 9,
            "parity": "odd",
            "boundary": "core",
            "route_type": "single-route square",
        },
        100: {
            "square_route": "10 × 10",
            "other_routes": [],
            "square_root": 10,
            "parity": "even",
            "boundary": "core",
            "route_type": "single-route square",
        },
        121: {
            "square_route": "11 × 11",
            "other_routes": [],
            "square_root": 11,
            "parity": "odd",
            "boundary": "extension",
            "route_type": "single-route square",
        },
        144: {
            "square_route": "12 × 12",
            "other_routes": [],
            "square_root": 12,
            "parity": "even",
            "boundary": "extension",
            "route_type": "single-route square",
        },
    }

    selected_product = st.selectbox(
        "Choose a square product",
        options=list(square_records.keys()),
        index=5,
        key="square_product_selector",
    )

    record = square_records[selected_product]

    st.markdown("### Product summary")
    st.write(f"Product: {selected_product}")
    st.write(f"Square route: {record['square_route']}")
    st.write(f"Square root: √{selected_product} = {record['square_root']}")
    st.write(f"Odd or even: {record['parity']}")
    st.write(f"Boundary: {record['boundary']}")
    st.write(f"Route type: {record['route_type']}")

    st.markdown("### Routes in")
    st.write(f"Square route: {record['square_route']}")
    if record["other_routes"]:
        st.write("Other routes:")
        for route in record["other_routes"]:
            st.write(f"- {route}")
    else:
        st.write("No other routes shown in this bounded view.")

    st.markdown("### Pattern notes")
    if record["parity"] == "even":
        st.write("This is an even square because the repeated factor is even.")
    else:
        st.write("This is an odd square because the repeated factor is odd.")

    if record["route_type"] == "multi-route square":
        st.write("This square also connects to another factor family.")
    else:
        st.write("This square is shown here as a single-route square.")

    if record["boundary"] == "extension":
        st.write("This square sits beyond the core 1–10 world.")
    else:
        st.write("This square belongs to the core TMK world.")

    copy_text = (
        f"Square Product Selector\n\n"
        f"Selected product: {selected_product}\n\n"
        f"Focus: Analyse one square product through route structure and pattern structure.\n\n"
        f"Teacher explanation: A square product has a same-factor route. We can also check "
        f"whether it has another route, find its square root, and classify it as odd or even.\n"
        f"Teacher prompt: What do you notice about the product {selected_product}?\n\n"
        f"Product summary:\n"
        f"- Square route: {record['square_route']}\n"
        f"- Square root: √{selected_product} = {record['square_root']}\n"
        f"- Odd or even: {record['parity']}\n"
        f"- Boundary: {record['boundary']}\n"
        f"- Route type: {record['route_type']}\n\n"
        f"Questions:\n"
        f"- Which same-factor route builds {selected_product}?\n"
        f"- Does {selected_product} have another route?\n"
        f"- What is the square root of {selected_product}?\n"
        f"- Is this square product odd or even?\n"
        f"- Is it core or extension?\n"
    )

    st.text_area(
        "Copy-paste print text — Square Product Selector",
        copy_text,
        height=280,
        key="square_product_selector_copy_box",
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
    render_exponent_power_notes()
    render_square_product_selector()

    st.markdown("</div>", unsafe_allow_html=True)
