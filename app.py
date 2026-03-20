from __future__ import annotations

from typing import Dict, Iterable, Tuple

import streamlit as st

from products import ALL_PRODUCTS, product_record, stage_label
from wording_guard import assert_no_forbidden_world_phrasing
from worksheet_engine import VALID_TIERS, generate_worksheet_dict
from worlds import BEYOND_10_WORLD, TMK_WORLD


st.set_page_config(page_title="TMK Worksheet Studio", page_icon="✳️", layout="wide")


def main() -> None:
    _run_wording_guard()

    st.title("TMK Worksheet Studio")
    st.caption(f"Product-based worksheet generation for {TMK_WORLD}")

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
            st.markdown(f"**Q{qid}**")
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
        route_a = data["route_a"]
        route_b = data["route_b"]
        return (
            f"Compare these ways in to {data['product']}: "
            f"{route_a['left']} × {route_a['right']} and {route_b['left']} × {route_b['right']}."
        )

    if prompt_key == "belongs_question":
        return f"Does {data['candidate']} belong in {TMK_WORLD}?"

    if prompt_key == "repair_equation":
        return f"Fix this: {data['left']} × {data['right']} = {data['product']}"

    if prompt_key == "sort_equations":
        route_texts = []
        for route in data["routes"]:
            if isinstance(route, dict):
                route_texts.append(f"{route['left']} × {route['right']}")
            elif isinstance(route, (tuple, list)) and len(route) == 2:
                route_texts.append(f"{route[0]} × {route[1]}")
            else:
                route_texts.append(str(route))
        return f"Which of these make {data['product']}? " + ", ".join(route_texts)

    if prompt_key == "explain_product":
        return f"Explain something true about {data['product']}."

    return f"{prompt_key}: {data}"


def _format_answer(answer: Dict[str, object]) -> str:
    if "value" in answer and len(answer) == 1:
        return str(answer["value"])

    if "value" in answer and "route" in answer:
        route = answer["route"]
        if isinstance(route, dict):
            return f"{answer['value']} ({route['left']} × {route['right']})"
        if isinstance(route, (tuple, list)) and len(route) == 2:
            return f"{answer['value']} ({route[0]} × {route[1]})"

    if "route" in answer:
        route = answer["route"]
        if isinstance(route, dict):
            return f"{route['left']} × {route['right']}"
        if isinstance(route, (tuple, list)) and len(route) == 2:
            return f"{route[0]} × {route[1]}"

    if "belongs" in answer:
        return "Yes" if answer["belongs"] else "No"

    if "correct_equation" in answer:
        eq = answer["correct_equation"]
        if isinstance(eq, dict):
            return f"{eq['left']} × {eq['right']} = {eq['product']}"

    if "correct" in answer:
        eq = answer["correct"]
        if isinstance(eq, dict):
            return f"{eq['left']} × {eq['right']} = {eq['product']}"

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


def _sample_prompts_for_guard() -> Tuple[str, ...]:
    sample_questions = (
        {
            "prompt_key": "belongs_question",
            "prompt_data": {"candidate": 36},
        },
        {
            "prompt_key": "repair_equation",
            "prompt_data": {"left": 3, "right": 12, "product": 36},
        },
        {
            "prompt_key": "explain_product",
            "prompt_data": {"product": 36},
        },
    )

    rendered_samples = tuple(_render_pupil_prompt(question) for question in sample_questions)

    extra_samples = (
        f"Does 77 belong in {BEYOND_10_WORLD}?",
        f"This route is true, but it is outside {TMK_WORLD}.",
        f"This route is true, but it is inside {BEYOND_10_WORLD}.",
    )

    return rendered_samples + extra_samples


def _run_wording_guard() -> None:
    assert_no_forbidden_world_phrasing(_sample_prompts_for_guard())


if __name__ == "__main__":
    main()
