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
