from __future__ import annotations

from typing import Dict, Iterable, Tuple

import streamlit as st

from products import ALL_PRODUCTS, product_record, stage_label
from worksheet_engine import VALID_TIERS, generate_worksheet_dict


st.set_page_config(page_title="TMK Worksheet Studio", page_icon="✳️", layout="wide")


def main() -> None:
    st.title("TMK Worksheet Studio")
    st.caption("Product-based worksheet generation for the TMK World")

    product, tier = _render_controls()
    worksheet = generate_worksheet_dict(product, tier)

    _render_summary(worksheet)
    _render_questions(worksheet["questions"])
    _render_teacher_key(worksheet["teacher_key"])


def _render_controls() -> Tuple[int, str]:
    with st.sidebar:
        st.header("Worksheet Settings")

        product = st.selectbox(
            "Product",
            options=ALL_PRODUCTS,
            index=ALL_PRODUCTS.index(36) if 36 in ALL_PRODUCTS else 0,
            format_func=_product_option_label,
        )

        tier = st.radio(
            "Tier",
            options=VALID_TIERS,
            index=1,
            horizontal=True,
        )

        record = product_record(product)

        st.divider()
        st.markdown("**Product Overview**")
        st.write(f"Stage: {stage_label(record.stage)}")
        st.write(f"Intro route: {record.intro_route[0]} × {record.intro_route[1]}")
        st.write(f"Structural role: {record.structural_role}")

    return product, tier


def _render_summary(worksheet: Dict[str, object]) -> None:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Product", str(worksheet["product"]))
    col2.metric("Stage", str(worksheet["stage"]))
    col3.metric("Tier", str(worksheet["tier"]))
    col4.metric("Questions", str(len(worksheet["questions"])))
    st.divider()


def _render_questions(questions: Iterable[Dict[str, object]]) -> None:
    st.subheader("Pupil Worksheet")

    for question in questions:
        with st.container(border=True):
            qid = question["id"]
            section = _title_case(str(question["section"]))
            st.markdown(f"**Q{qid}. {section}**")
            st.write(_render_pupil_prompt(question))


def _render_teacher_key(teacher_key: Dict[str, object]) -> None:
    st.divider()

    with st.expander("Teacher Key", expanded=False):
        st.markdown("**Answers**")
        for index, answer in enumerate(teacher_key["answers"], start=1):
            st.write(f"Q{index}. {_format_answer(answer)}")

        st.markdown("**Pattern Links**")
        pattern_ids = teacher_key.get("pattern_ids", [])
        if pattern_ids:
            st.write(", ".join(pattern_ids))
        else:
            st.write("No pattern links attached.")

        st.markdown("**Memory Cues**")
        memory_cue_ids = teacher_key.get("memory_cue_ids", [])
        if memory_cue_ids:
            st.write(", ".join(memory_cue_ids))
        else:
            st.write("No teacher memory cues attached.")

        st.markdown("**Teacher Notes**")
        notes = teacher_key.get("notes", [])
        for note in notes:
            st.write(f"- {note}")

def _render_pupil_prompt(question: Dict[str, object]) -> str:

    prompt_key = str(question["prompt_key"])
    data = question["prompt_data"]

    if prompt_key == "identify_product":
        return f"Find {data['product']}."

    if prompt_key == "complete_way_in":
        return f"Complete: {data['left']} × __ = {data['product']}"

    if prompt_key == "missing_factor":
        return f"__ × {data['right']} = {data['product']}"

    if prompt_key == "division_way_out":
        return f"{data['product']} ÷ {data['divisor']} = __"

    if prompt_key == "check_equation":
        return f"Check: {data['left']} × {data['right']} = {data['product']}. True or false?"

    if prompt_key == "compare_routes":
        r1 = data["route_a"]
        r2 = data["route_b"]
        return (
            f"Compare these ways in to {data['product']}: "
            f"{r1['left']} × {r1['right']} and {r2['left']} × {r2['right']}."
        )

    if prompt_key == "belongs_question":
        return f"Does {data['candidate']} belong in the TMK World?"

    if prompt_key == "repair_equation":
        return f"Fix this: {data['left']} × {data['right']} = {data['product']}"

    if prompt_key == "sort_equations":
        routes = []
        for r in data["routes"]:
            routes.append(f"{r[0]} × {r[1]}")
        return f"Which of these make {data['product']}? " + ", ".join(routes)

    if prompt_key == "explain_product":
        return f"Explain something true about {data['product']}."

    return str(prompt_key)


def _format_answer(answer: Dict[str, object]) -> str:
    if "value" in answer and len(answer) == 1:
        return str(answer["value"])

    if "value" in answer and "route" in answer:
        route = answer["route"]
        if isinstance(route, dict):
            return f"{answer['value']} ({route['left']} × {route['right']})"
        if isinstance(route, (tuple, list)) and len(route) == 2:
            return f"{answer['value']} ({route[0]} × {route[1]})"

    if "value" in answer and "division" in answer:
        division = answer["division"]
        if isinstance(division, dict):
            return f"{answer['value']} ({division['product']} ÷ {division['divisor']} = {division['quotient']})"

    if "route" in answer:
        route = answer["route"]
        if isinstance(route, dict):
            return f"{route['left']} × {route['right']}"
        if isinstance(route, (tuple, list)) and len(route) == 2:
            return f"{route[0]} × {route[1]}"

    if "division" in answer:
        division = answer["division"]
        if isinstance(division, dict):
            return f"{division['product']} ÷ {division['divisor']} = {division['quotient']}"

    if "belongs" in answer:
        return "Yes" if answer["belongs"] else "No"

    if "correct_equation" in answer:
        eq = answer["correct"]
        if isinstance(eq, dict):
            return f"{eq['left']} × {eq['right']} = {eq['product']}"

    if "correct" in answer:
        eq = answer["correct"]
        if isinstance(eq, dict):
            return f"{eq['left']} × {eq['right']} = {eq['product']}"

    if "classification" in answer:
        return str(answer["classification"])

    if "accepted_routes" in answer:
        formatted_routes = []
        for route in answer["accepted_routes"]:
            if isinstance(route, dict):
                formatted_routes.append(f"{route['left']} × {route['right']}")
            elif isinstance(route, (tuple, list)) and len(route) == 2:
                formatted_routes.append(f"{route[0]} × {route[1]}")
            else:
                formatted_routes.append(str(route))
        return "; ".join(formatted_routes)

    if "accepted_pattern_ids" in answer:
        return ", ".join(str(pattern_id) for pattern_id in answer["accepted_pattern_ids"])

    if "has_another_way_in" in answer:
        return "No"

    if "has_another_way_out" in answer:
        return "No"

    if "comparison" in answer:
        return str(answer["comparison"])

    if "valid_routes" in answer:
        formatted_routes = []
        for route in answer["valid_routes"]:
            if isinstance(route, (tuple, list)) and len(route) == 2:
                formatted_routes.append(f"{route[0]} × {route[1]}")
            else:
                formatted_routes.append(str(route))
        return "; ".join(formatted_routes)

    return str(answer)


def _product_option_label(product: int) -> str:
    record = product_record(product)
    return f"{product} · {record.stage}"


def _title_case(value: str) -> str:
    return value.replace("_", " ").title()


if __name__ == "__main__":
    main()
