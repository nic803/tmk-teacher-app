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

    st.markdown("### Examples")
    examples = [
        "11 × 2 = 10 × 2 + 1 × 2 = 20 + 2 = 22",
        "11 × 4 = 10 × 4 + 1 × 4 = 40 + 4 = 44",
        "11 × 7 = 10 × 7 + 1 × 7 = 70 + 7 = 77",
        "11 × 11 = 121",
    ]
    for example in examples:
        st.write(example)

    activity_text = (
        "11× Foundations\n\n"
        "Focus: Derive 11× from known 10× and 1× structure.\n\n"
        "Teacher explanation: 11× is not a separate fact list. It is built from 10× and 1×.\n"
        "Teacher prompt: What is 10×n? What is 1×n? Now combine them.\n\n"
        "Pupil tasks:\n"
        "- Build 11× facts from 10× and 1×.\n"
        "- Notice repeated-digit products where they appear.\n"
        "- Explain why 11× opens new extension routes.\n\n"
        "Example questions:\n"
        "- How can you derive 11 × 6?\n"
        "- Why does 11 × 8 give 88?\n"
        "- What is 11 × 11?\n\n"
        "Teaching note: Keep derivation first. Do not present 11× as a separate memorised table."
    )
    st.text_area(
        "Copy-paste print text — 11× Foundations",
        activity_text,
        height=240,
        key="eleven_foundations_copy_box",
    )


def render_eleven_derivation_practice() -> None:
    st.subheader("11× Derivation Practice")
    st.caption("Select one 11× fact and derive it from known structure")

    records = {
        2: {
            "product": 22,
            "ten_plus_one": "11 × 2 = 10 × 2 + 1 × 2 = 20 + 2 = 22",
            "pattern_note": "Repeated-digit pattern: 22",
        },
        3: {
            "product": 33,
            "ten_plus_one": "11 × 3 = 10 × 3 + 1 × 3 = 30 + 3 = 33",
            "pattern_note": "Repeated-digit pattern: 33",
        },
        4: {
            "product": 44,
            "ten_plus_one": "11 × 4 = 10 × 4 + 1 × 4 = 40 + 4 = 44",
            "pattern_note": "Repeated-digit pattern: 44",
        },
        5: {
            "product": 55,
            "ten_plus_one": "11 × 5 = 10 × 5 + 1 × 5 = 50 + 5 = 55",
            "pattern_note": "Repeated-digit pattern: 55",
        },
        6: {
            "product": 66,
            "ten_plus_one": "11 × 6 = 10 × 6 + 1 × 6 = 60 + 6 = 66",
            "pattern_note": "Repeated-digit pattern: 66",
        },
        7: {
            "product": 77,
            "ten_plus_one": "11 × 7 = 10 × 7 + 1 × 7 = 70 + 7 = 77",
            "pattern_note": "Repeated-digit pattern: 77",
        },
        8: {
            "product": 88,
            "ten_plus_one": "11 × 8 = 10 × 8 + 1 × 8 = 80 + 8 = 88",
            "pattern_note": "Repeated-digit pattern: 88",
        },
        9: {
            "product": 99,
            "ten_plus_one": "11 × 9 = 10 × 9 + 1 × 9 = 90 + 9 = 99",
            "pattern_note": "Repeated-digit pattern: 99",
        },
        10: {
            "product": 110,
            "ten_plus_one": "11 × 10 = 10 × 10 + 1 × 10 = 100 + 10 = 110",
            "pattern_note": "Beyond repeated digits: keep using 10× + 1×.",
        },
        11: {
            "product": 121,
            "ten_plus_one": "11 × 11 = 10 × 11 + 1 × 11 = 110 + 11 = 121",
            "pattern_note": "Extension square: 11² = 121.",
        },
        12: {
            "product": 132,
            "ten_plus_one": "11 × 12 = 10 × 12 + 1 × 12 = 120 + 12 = 132",
            "pattern_note": "Beyond repeated digits: keep using 10× + 1×.",
        },
    }

    selected_n = st.selectbox(
        "Choose n in 11 × n",
        options=list(records.keys()),
        index=0,
        key="eleven_derivation_practice_selector",
    )

    record = records[selected_n]

    st.markdown("### Selected fact")
    st.write(f"11 × {selected_n} = {record['product']}")

    st.markdown("### Main derivation")
    st.write(record["ten_plus_one"])

    st.markdown("### Pattern note")
    st.write(record["pattern_note"])

    st.markdown("### Notice")
    st.write("The main derivation stays 10× + 1×.")
    st.write("Repeated digits appear for 11 × 2 to 11 × 9.")
    st.write("Beyond that, use the derivation rule rather than a visual shortcut.")

    copy_text = (
        f"11× Derivation Practice\n\n"
        f"Selected fact: 11 × {selected_n} = {record['product']}\n\n"
        f"Focus: Derive one 11× fact from known multiplication structure.\n\n"
        f"Teacher explanation: The main derivation is 10× + 1×.\n"
        f"Teacher prompt: How can you build 11 × {selected_n} from known facts?\n\n"
        f"Main derivation:\n- {record['ten_plus_one']}\n\n"
        f"Pattern note:\n- {record['pattern_note']}\n\n"
        f"Teaching note:\nKeep 10× + 1× as the first route of explanation."
    )
    st.text_area(
        "Copy-paste print text — 11× Derivation Practice",
        copy_text,
        height=260,
        key="eleven_derivation_practice_copy_box",
    )


def render_eleven_route_opening() -> None:
    st.subheader("11× Route Opening")
    st.caption("New extension routes opened through 11×")

    records = {
        22: {
            "extension_routes": ["2 × 11"],
            "teacher_note": "22 enters as an 11× extension product.",
        },
        33: {
            "extension_routes": ["3 × 11"],
            "teacher_note": "33 enters as an 11× extension product.",
        },
        44: {
            "extension_routes": ["4 × 11"],
            "teacher_note": "44 enters as an 11× extension product.",
        },
        55: {
            "extension_routes": ["5 × 11"],
            "teacher_note": "55 enters as an 11× extension product.",
        },
        66: {
            "extension_routes": ["6 × 11"],
            "teacher_note": "66 enters as an 11× extension product.",
        },
        77: {
            "extension_routes": ["7 × 11"],
            "teacher_note": "77 enters as an 11× extension product.",
        },
        88: {
            "extension_routes": ["8 × 11"],
            "teacher_note": "88 enters as an 11× extension product.",
        },
        99: {
            "extension_routes": ["9 × 11"],
            "teacher_note": "99 enters as an 11× extension product.",
        },
        121: {
            "extension_routes": ["11 × 11"],
            "teacher_note": "121 is both an 11× product and an extension square.",
        },
        132: {
            "extension_routes": ["11 × 12"],
            "teacher_note": "132 is opened through 11 × 12.",
        },
    }

    selected_product = st.selectbox(
        "Choose an 11× product",
        options=list(records.keys()),
        index=0,
        key="eleven_route_opening_selector",
    )

    record = records[selected_product]

    st.markdown("### Extension route")
    for route in record["extension_routes"]:
        st.write(route)

    st.markdown("### Teacher note")
    st.write(record["teacher_note"])
    st.write("These products belong to the extension strand opened by 11×.")

    copy_text = (
        f"11× Route Opening\n\n"
        f"Selected product: {selected_product}\n\n"
        f"Focus: Show how 11× opens new extension products.\n\n"
        f"Teacher explanation: 11× creates new extension products through the rule 10× + 1×.\n"
        f"Teacher prompt: Which 11× route builds {selected_product}?\n\n"
        f"Extension routes:\n"
        + "\n".join(f"- {route}" for route in record["extension_routes"])
        + "\n\nTeaching note:\n"
        + record["teacher_note"]
    )
    st.text_area(
        "Copy-paste print text — 11× Route Opening",
        copy_text,
        height=240,
        key="eleven_route_opening_copy_box",
    )


def render_eleven_core_extension_comparison() -> None:
    st.subheader("11× Core or Extension Route?")
    st.caption("Classify 11× products within the extension strand")

    comparison_rows = [
        {"product": 22, "classification": "extension", "note": "Opened by 2 × 11"},
        {"product": 33, "classification": "extension", "note": "Opened by 3 × 11"},
        {"product": 44, "classification": "extension", "note": "Opened by 4 × 11"},
        {"product": 55, "classification": "extension", "note": "Opened by 5 × 11"},
        {"product": 66, "classification": "extension", "note": "Opened by 6 × 11"},
        {"product": 77, "classification": "extension", "note": "Opened by 7 × 11"},
        {"product": 88, "classification": "extension", "note": "Opened by 8 × 11"},
        {"product": 99, "classification": "extension", "note": "Opened by 9 × 11"},
        {"product": 121, "classification": "extension square", "note": "11 × 11 = 121"},
        {"product": 132, "classification": "extension", "note": "Opened by 11 × 12"},
    ]

    for row in comparison_rows:
        with st.expander(f"Product {row['product']}"):
            st.write(f"Classification: {row['classification']}")
            st.write(f"Note: {row['note']}")

    st.markdown("### Key rule")
    st.write("11× products belong to the extension strand.")
    st.write("121 is a special case because it is also an extension square.")

    activity_text = (
        "11× Core or Extension Route?\n\n"
        "Focus: Classify 11× products in the extension strand.\n\n"
        "Teacher explanation: Products opened by 11× belong to the extension strand. "
        "Some may also have a special role, such as 121 = 11².\n"
        "Teacher prompt: Which kind of extension product is this?\n\n"
        "Pupil tasks:\n"
        "- Read each 11× product.\n"
        "- Identify the extension route.\n"
        "- Notice special cases such as 121.\n\n"
        "Example questions:\n"
        "- Why is 55 an 11× extension product?\n"
        "- Why is 121 special?\n"
        "- Which route builds 132?\n\n"
        "Teaching note: Keep 11× products clearly inside the extension strand."
    )
    st.text_area(
        "Copy-paste print text — 11× Core or Extension Route?",
        activity_text,
        height=240,
        key="eleven_core_extension_comparison_copy_box",
    )


def render_twelve_foundations() -> None:
    st.subheader("12× Foundations")
    st.caption("Derive 12× from known structure")

    st.markdown("Main teaching rule:")
    st.latex(r"12 \times n = 10 \times n + 2 \times n")

    st.markdown("Support rule:")
    st.latex(r"12 \times n = 2(6 \times n)")

    st.markdown("### Pattern bank")
    st.write("Ten-plus-two rule: build 12× from 10× and 2×.")
    st.write("Double-the-6× rule: 12×n = 2(6×n).")
    st.write("Even-product pattern: all 12× products are even.")
    st.write("Growth-by-12 pattern: each new product increases by 12.")

    st.markdown("### Clock cue")
    st.write("A clock has 12 equal sections of 5 minutes.")
    st.latex(r"12 \times 5 = 60")
    st.write("Use the clock cue as support, not as the main derivation rule.")

    st.markdown("### Examples")
    examples = [
        "12 × 3 = 10 × 3 + 2 × 3 = 30 + 6 = 36",
        "12 × 5 = 60",
        "12 × 6 = 10 × 6 + 2 × 6 = 60 + 12 = 72",
        "12 × 12 = 144",
    ]
    for example in examples:
        st.write(example)

    activity_text = (
        "12× Foundations\n\n"
        "Focus: Derive 12× from 10× + 2× and connect it to known structure.\n\n"
        "Teacher explanation: 12× is built from known multiplication facts. The main rule is 10× + 2×. "
        "A second support rule is double 6×. The clock cue supports 12 × 5 = 60.\n"
        "Teacher prompt: What is 10×n? What is 2×n? Now combine them.\n\n"
        "Pupil tasks:\n"
        "- Derive 12× facts from 10× and 2×.\n"
        "- Use the clock cue for 12 × 5.\n"
        "- Notice that all 12× products are even.\n\n"
        "Example questions:\n"
        "- How can you derive 12 × 4?\n"
        "- Why is 12 × 5 equal to 60?\n"
        "- How can 6× help with 12×?\n\n"
        "Teaching note: Keep 10× + 2× as the main rule. The clock cue is support only."
    )
    st.text_area(
        "Copy-paste print text — 12× Foundations",
        activity_text,
        height=260,
        key="twelve_foundations_copy_box",
    )


def render_twelve_route_opening() -> None:
    st.subheader("12× Route Opening")
    st.caption("New extension routes opened through 12×")

    records = {
        24: {
            "core_routes": ["4 × 6", "3 × 8"],
            "extension_routes": ["2 × 12"],
            "teacher_note": "24 gains an extension route through 12×, but its core routes remain separate.",
        },
        36: {
            "core_routes": ["4 × 9", "6 × 6"],
            "extension_routes": ["3 × 12"],
            "teacher_note": "36 is a core multi-route square and also gains the extension route 3 × 12.",
        },
        48: {
            "core_routes": ["6 × 8"],
            "extension_routes": ["4 × 12"],
            "teacher_note": "48 is already core through 6 × 8, and 4 × 12 becomes a new extension route.",
        },
        60: {
            "core_routes": ["6 × 10"],
            "extension_routes": ["5 × 12"],
            "teacher_note": "60 stays a core product through 6 × 10 and gains 5 × 12 in extension.",
        },
        72: {
            "core_routes": ["8 × 9"],
            "extension_routes": ["6 × 12"],
            "teacher_note": "72 is core through 8 × 9 and gains the extension route 6 × 12.",
        },
    }

    selected_product = st.selectbox(
        "Choose a product",
        options=list(records.keys()),
        index=1,
        key="twelve_route_opening_selector",
    )

    record = records[selected_product]

    st.markdown("### Core routes")
    for route in record["core_routes"]:
        st.write(route)

    st.markdown("### Extension routes")
    for route in record["extension_routes"]:
        st.write(route)

    st.markdown("### Teacher note")
    st.write(record["teacher_note"])
    st.write("Core routes and extension routes should stay separate on the page.")

    copy_text = (
        f"12× Route Opening\n\n"
        f"Selected product: {selected_product}\n\n"
        f"Focus: Compare core routes with new extension routes opened through 12×.\n\n"
        f"Teacher explanation: Some products are already known in the core world. "
        f"12× can open a new extension route into the same product, but it does not replace the core routes.\n"
        f"Teacher prompt: Which routes into {selected_product} belong to the core world, and which belong to extension?\n\n"
        f"Core routes:\n"
        + "\n".join(f"- {route}" for route in record["core_routes"])
        + "\n\nExtension routes:\n"
        + "\n".join(f"- {route}" for route in record["extension_routes"])
        + "\n\nTeaching note:\n"
        + record["teacher_note"]
    )
    st.text_area(
        "Copy-paste print text — 12× Route Opening",
        copy_text,
        height=260,
        key="twelve_route_opening_copy_box",
    )


def render_core_extension_route_comparison() -> None:
    st.subheader("Core or Extension Route?")
    st.caption("Keep core routes and extension routes separate")

    comparison_rows = [
        {"product": 24, "core": "4 × 6, 3 × 8", "extension": "2 × 12"},
        {"product": 36, "core": "4 × 9, 6 × 6", "extension": "3 × 12"},
        {"product": 48, "core": "6 × 8", "extension": "4 × 12"},
        {"product": 60, "core": "6 × 10", "extension": "5 × 12"},
        {"product": 72, "core": "8 × 9", "extension": "6 × 12"},
    ]

    for row in comparison_rows:
        with st.expander(f"Product {row['product']}"):
            st.write(f"Core routes: {row['core']}")
            st.write(f"Extension routes: {row['extension']}")

    st.markdown("### Key rule")
    st.latex(r"\text{core routes} \neq \text{extension routes}")

    activity_text = (
        "Core or Extension Route?\n\n"
        "Focus: Sort routes into the correct side of the boundary.\n\n"
        "Teacher explanation: Some routes belong to the core 1–10 world. "
        "Other routes are true, but they belong to the extension world because they use 11 or 12.\n"
        "Teacher prompt: Which routes stay in the core world, and which routes cross into extension?\n\n"
        "Pupil tasks:\n"
        "- Read each route.\n"
        "- Sort it into core or extension.\n"
        "- Explain why the route belongs on that side.\n\n"
        "Example questions:\n"
        "- Why is 3 × 12 an extension route into 36?\n"
        "- Why is 6 × 6 a core route into 36?\n"
        "- Why is 5 × 12 an extension route into 60?\n"
        "- Which core route still belongs to 72?\n\n"
        "Teaching note: Do not mix true extension routes with core routes. Keep the boundary visible."
    )
    st.text_area(
        "Copy-paste print text — Core or Extension Route?",
        activity_text,
        height=260,
        key="core_extension_route_comparison_copy_box",
    )


def render_twelve_derivation_practice() -> None:
    st.subheader("12× Derivation Practice")
    st.caption("Select one 12× fact and derive it from known structure")

    records = {
        3: {
            "product": 36,
            "ten_plus_two": "12 × 3 = 10 × 3 + 2 × 3 = 30 + 6 = 36",
            "double_six": "12 × 3 = 2(6 × 3) = 2(18) = 36",
            "clock_cue": "No clock cue focus here.",
        },
        4: {
            "product": 48,
            "ten_plus_two": "12 × 4 = 10 × 4 + 2 × 4 = 40 + 8 = 48",
            "double_six": "12 × 4 = 2(6 × 4) = 2(24) = 48",
            "clock_cue": "No clock cue focus here.",
        },
        5: {
            "product": 60,
            "ten_plus_two": "12 × 5 = 10 × 5 + 2 × 5 = 50 + 10 = 60",
            "double_six": "12 × 5 = 2(6 × 5) = 2(30) = 60",
            "clock_cue": "Clock cue: 12 sections of 5 minutes make 60 minutes.",
        },
        6: {
            "product": 72,
            "ten_plus_two": "12 × 6 = 10 × 6 + 2 × 6 = 60 + 12 = 72",
            "double_six": "12 × 6 = 2(6 × 6) = 2(36) = 72",
            "clock_cue": "No clock cue focus here.",
        },
        7: {
            "product": 84,
            "ten_plus_two": "12 × 7 = 10 × 7 + 2 × 7 = 70 + 14 = 84",
            "double_six": "12 × 7 = 2(6 × 7) = 2(42) = 84",
            "clock_cue": "No clock cue focus here.",
        },
        8: {
            "product": 96,
            "ten_plus_two": "12 × 8 = 10 × 8 + 2 × 8 = 80 + 16 = 96",
            "double_six": "12 × 8 = 2(6 × 8) = 2(48) = 96",
            "clock_cue": "No clock cue focus here.",
        },
        9: {
            "product": 108,
            "ten_plus_two": "12 × 9 = 10 × 9 + 2 × 9 = 90 + 18 = 108",
            "double_six": "12 × 9 = 2(6 × 9) = 2(54) = 108",
            "clock_cue": "No clock cue focus here.",
        },
        10: {
            "product": 120,
            "ten_plus_two": "12 × 10 = 10 × 10 + 2 × 10 = 100 + 20 = 120",
            "double_six": "12 × 10 = 2(6 × 10) = 2(60) = 120",
            "clock_cue": "No clock cue focus here.",
        },
        11: {
            "product": 132,
            "ten_plus_two": "12 × 11 = 10 × 11 + 2 × 11 = 110 + 22 = 132",
            "double_six": "12 × 11 = 2(6 × 11) = 2(66) = 132",
            "clock_cue": "No clock cue focus here.",
        },
        12: {
            "product": 144,
            "ten_plus_two": "12 × 12 = 10 × 12 + 2 × 12 = 120 + 24 = 144",
            "double_six": "12 × 12 = 2(6 × 12) = 2(72) = 144",
            "clock_cue": "No clock cue focus here.",
        },
    }

    selected_n = st.selectbox(
        "Choose n in 12 × n",
        options=list(records.keys()),
        index=0,
        key="twelve_derivation_practice_selector",
    )

    record = records[selected_n]

    st.markdown("### Selected fact")
    st.write(f"12 × {selected_n} = {record['product']}")

    st.markdown("### Main derivation")
    st.write(record["ten_plus_two"])

    st.markdown("### Support derivation")
    st.write(record["double_six"])

    st.markdown("### Clock cue")
    st.write(record["clock_cue"])

    st.markdown("### Notice")
    st.write("The ten-plus-two derivation stays primary.")
    st.write("The double-6× route is support.")
    st.write("The product is always even.")

    copy_text = (
        f"12× Derivation Practice\n\n"
        f"Selected fact: 12 × {selected_n} = {record['product']}\n\n"
        f"Focus: Derive one 12× fact from known multiplication structure.\n\n"
        f"Teacher explanation: The main derivation is 10× + 2×. A support derivation is double 6×.\n"
        f"Teacher prompt: How can you build 12 × {selected_n} from known facts?\n\n"
        f"Main derivation:\n- {record['ten_plus_two']}\n\n"
        f"Support derivation:\n- {record['double_six']}\n\n"
        f"Clock cue:\n- {record['clock_cue']}\n\n"
        f"Teaching note:\nKeep 10× + 2× as the first route of explanation."
    )
    st.text_area(
        "Copy-paste print text — 12× Derivation Practice",
        copy_text,
        height=260,
        key="twelve_derivation_practice_copy_box",
    )


def render_eleven_twelve_comparison() -> None:
    st.subheader("11× versus 12× Comparison")
    st.caption("Compare the two extension derivation rules")

    st.markdown("### Main rules")
    st.latex(r"11 \times n = 10 \times n + 1 \times n")
    st.latex(r"12 \times n = 10 \times n + 2 \times n")

    comparison_examples = [
        {"n": 3, "eleven": "11 × 3 = 30 + 3 = 33", "twelve": "12 × 3 = 30 + 6 = 36"},
        {"n": 5, "eleven": "11 × 5 = 50 + 5 = 55", "twelve": "12 × 5 = 50 + 10 = 60"},
        {"n": 6, "eleven": "11 × 6 = 60 + 6 = 66", "twelve": "12 × 6 = 60 + 12 = 72"},
        {"n": 11, "eleven": "11 × 11 = 110 + 11 = 121", "twelve": "12 × 11 = 110 + 22 = 132"},
    ]

    for row in comparison_examples:
        with st.expander(f"Compare at n = {row['n']}"):
            st.write(row["eleven"])
            st.write(row["twelve"])

    st.markdown("### Notice")
    st.write("11× adds one more group of n.")
    st.write("12× adds two more groups of n.")
    st.write("12× can also use the support rule 2(6×n).")
    st.write("11× often shows repeated digits for 2 to 9, while 12× does not.")

    activity_text = (
        "11× versus 12× Comparison\n\n"
        "Focus: Compare the derivation structure of 11× and 12×.\n\n"
        "Teacher explanation: 11× adds one more group of n to 10×n. "
        "12× adds two more groups of n to 10×n.\n"
        "Teacher prompt: What changes when we move from 11× to 12×?\n\n"
        "Pupil tasks:\n"
        "- Compare 11×n and 12×n for the same value of n.\n"
        "- Identify the ten-plus-one and ten-plus-two structures.\n"
        "- Notice where repeated-digit patterns appear and where they do not.\n\n"
        "Example questions:\n"
        "- Compare 11 × 6 and 12 × 6.\n"
        "- Why does 11 × 8 give 88 but 12 × 8 gives 96?\n"
        "- What changes between 11 × 11 and 12 × 11?\n\n"
        "Teaching note: Keep the comparison structural, not just numerical."
    )
    st.text_area(
        "Copy-paste print text — 11× versus 12× Comparison",
        activity_text,
        height=260,
        key="eleven_twelve_comparison_copy_box",
    )


def render_square_strand_intro() -> None:
    st.markdown("### Overview")
    st.write("This strand focuses on square products, square roots, parity patterns, and square vocabulary.")


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


def render_exponent_power_notes() -> None:
    st.subheader("Exponent, Power, and Power of 2")
    st.caption("New vocabulary for square notation and repeated factors")

    st.markdown("In square notation, the small raised 2 is the exponent.")
    st.latex(r"n^2")
    st.markdown("This is read as:")
    st.write("n squared")
    st.write("n to the power of 2")

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
    st.markdown("A power of 2 keeps the base equal to 2:")
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
    st.write("4 = 2² is both a square number and a power of 2.")
    st.write("25 = 5² is a square number and not a power of 2.")
    st.write("32 = 2⁵ is a power of 2 and not a square number.")

    with st.expander("Teacher note"):
        st.write(
            "Keep the distinction explicit. Pupils often confuse "
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
        "Teaching note: Keep square linked to the route n × n, and power of 2 linked to repeated multiplication by 2."
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

    st.session_state["square_product_selector_copy_box"] = copy_text
    st.text_area(
        "Copy-paste print text — Square Product Selector",
        key="square_product_selector_copy_box",
        height=280,
    )


def render_square_or_not_square() -> None:
    st.subheader("Square or Not Square?")
    st.caption("Compare square products and non-square products")

    products = [12, 16, 18, 25, 36, 42, 49, 64, 72, 81, 100, 121, 144]
    square_products = {16, 25, 36, 49, 64, 81, 100, 121, 144}

    st.markdown("### Mixed product set")
    st.write(", ".join(str(p) for p in products))

    st.markdown("### Square products in this set")
    st.write(", ".join(str(p) for p in products if p in square_products))

    st.markdown("### Non-square products in this set")
    st.write(", ".join(str(p) for p in products if p not in square_products))

    with st.expander("Teacher note"):
        st.write(
            "Ask first for a same-factor route. If no route of the form n × n exists, "
            "then the product is not square."
        )

    activity_text = (
        "Square or Not Square?\n\n"
        "Focus: Decide whether a product has a same-factor route.\n\n"
        "Teacher explanation: A product is square if it can be written in the form n × n. "
        "If it has no same-factor route, it is not a square number.\n"
        "Teacher prompt: Which of these products have a same-factor route?\n\n"
        "Pupil tasks:\n"
        "- Sort the mixed products into square and non-square.\n"
        "- Write a square route for each square product.\n"
        "- Explain why each non-square product is not square.\n\n"
        "Example questions:\n"
        "- Why is 16 square?\n"
        "- Why is 18 not square?\n"
        "- Which route shows that 49 is square?\n"
        "- Why is 72 not square?\n"
        "- Which extension products in this set are square?\n\n"
        "Teaching note: Keep the decision rule structural. Look for a same-factor route."
    )
    st.text_area(
        "Copy-paste print text — Square or Not Square?",
        activity_text,
        height=260,
        key="square_or_not_square_copy_box",
    )


def render_extension_hub_page() -> None:
    st.markdown('<div class="tmk-panel">', unsafe_allow_html=True)
    st.markdown('<div class="tmk-section-title">Extension Hub</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tmk-section-subtitle">Resources for teaching 11× and 12×, opening new routes, and extending beyond the core TMK world.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("11× and 12× Extension Strand", expanded=False):
        st.caption("Derivation rules, route opening, and comparison work for 11× and 12×.")
        render_eleven_foundations()
        render_eleven_derivation_practice()
        render_eleven_route_opening()
        render_eleven_core_extension_comparison()
        render_twelve_foundations()
        render_twelve_route_opening()
        render_core_extension_route_comparison()
        render_twelve_derivation_practice()
        render_eleven_twelve_comparison()

    with st.expander("Square Numbers and Square Roots Strand", expanded=False):
        render_square_strand_intro()
        render_square_numbers_recap()
        render_square_roots()
        render_odd_even_square_patterns()
        render_exponent_power_notes()
        render_square_product_selector()
        render_square_or_not_square()

    st.markdown("</div>", unsafe_allow_html=True)
