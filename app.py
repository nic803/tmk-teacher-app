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
    prompt_data = question["prompt_data"]

    if prompt_key == "notice_product":
        return f"Find {prompt_data['product']}."

    if prompt_key == "find_product":
        return f"Find {prompt_data['product']}."

    if prompt_key == "notice_product_structure":
        return f"What do you notice about {prompt_data['product']}?"

    if prompt_key == "complete_way_in":
        return f"Complete: {prompt_data['left']} × __ = {prompt_data['product']}"

    if prompt_key == "find_way_in":
        return f"Find a way in to {prompt_data['product']} using {prompt_data['left']}."

    if prompt_key == "show_way_in":
        return f"Show a way in to {prompt_data['product']} using {prompt_data['left']}."

    if prompt_key == "complete_another_way_in":
        return f"Complete: {prompt_data['left']} × __ = {prompt_data['product']}"

    if prompt_key == "find_another_way_in":
        return f"Find another way in to {prompt_data['product']} using {prompt_data['left']}."

    if prompt_key == "show_another_way_in":
        return f"Show another way in to {prompt_data['product']} using {prompt_data['left']}."

    if prompt_key == "single_way_in_notice":
        route = prompt_data["route"]
        return f"This product has one way in: {route['left']} × {route['right']}."

    if prompt_key == "single_way_in_explain":
        route = prompt_data["route"]
        return f"This product has one way in: {route['left']} × {route['right']}. Explain."

    if prompt_key == "complete_way_out":
        return f"{prompt_data['product']} ÷ {prompt_data['divisor']} = __"

    if prompt_key == "show_way_out":
        return f"Show the way out from {prompt_data['product']} using {prompt_data['divisor']}."

    if prompt_key == "complete_another_way_out":
        return f"{prompt_data['product']} ÷ {prompt_data['divisor']} = __"

    if prompt_key == "show_another_way_out":
        return f"Show another way out from {prompt_data['product']} using {prompt_data['divisor']}."

    if prompt_key == "single_way_out_notice":
        division = prompt_data["division"]
        return (
            f"This product has one way out here: "
            f"{division['product']} ÷ {division['divisor']} = {division['quotient']}."
        )

    if prompt_key == "single_way_out_explain":
        division = prompt_data["division"]
        return (
            f"This product has one way out here: "
            f"{division['product']} ÷ {division['divisor']} = {division['quotient']}. Explain."
        )

    if prompt_key == "find_another_way":
        intro = prompt_data["intro_route"]
        return (
            f"One way in is {intro['left']} × {intro['right']}. "
            f"Find another way in to {prompt_data['product']}."
        )

    if prompt_key == "compare_two_ways":
        intro = prompt_data["intro_route"]
        other = prompt_data["other_route"]
        return (
            f"Compare these two ways in to {prompt_data['product']}: "
            f"{intro['left']} × {intro['right']} and {other['left']} × {other['right']}."
        )

    if prompt_key == "one_way_in_only":
        route = prompt_data["route"]
        return f"{prompt_data['product']} has one way in: {route['left']} × {route['right']}."

    if prompt_key == "explain_one_way_in_only":
        route = prompt_data["route"]
        return (
            f"{prompt_data['product']} has one way in: "
            f"{route['left']} × {route['right']}. Explain why there is not another way in."
        )

    if prompt_key == "belongs_yes_no":
        return f"Does {prompt_data['candidate']} belong in the TMK World?"

    if prompt_key == "belongs_explain_outside":
        return f"Does {prompt_data['candidate']} belong in the TMK World? Explain."

    if prompt_key == "repair_broken_output":
        return f"Check: {prompt_data['left']} × {prompt_data['right']} = {prompt_data['product']}. Fix it."

    if prompt_key == "check_true_but_outside_world":
        return (
            f"Check: {prompt_data['left']} × {prompt_data['right']} = {prompt_data['product']}. "
            "Is this a TMK way in? Fix or explain."
        )

    if prompt_key == "repair_broken_route":
        return f"Check: {prompt_data['left']} × {prompt_data['right']} = {prompt_data['product']}. Fix it."

    if prompt_key == "complete_rebuild":
        return f"Complete: I can rebuild {prompt_data['product']} by using __ × __."

    if prompt_key == "explain_rebuild":
        return f"If you forgot {prompt_data['product']}, how could you rebuild it?"

    if prompt_key == "justify_rebuild":
        return f"Explain how you could rebuild {prompt_data['product']} using a known route."

    if prompt_key == "complete_belongs_reason":
        return f"Complete: {prompt_data['product']} belongs in the TMK World because __."

    if prompt_key == "tell_one_true_thing":
        return f"Tell one true thing about {prompt_data['product']}."

    if prompt_key == "explain_structure":
        return f"Explain the structure of {prompt_data['product']}."

    return f"{prompt_key}: {prompt_data}"


def _format_answer(answer: Dict[str, object]) -> str:
    if "value" in answer and len(answer) == 1:
        return str(answer["value"])

    if "value" in answer and "route" in answer:
        route = answer["route"]
        return f"{answer['value']} ({route['left']} × {route['right']})"

    if "value" in answer and "division" in answer:
        division = answer["division"]
        return f"{answer['value']} ({division['product']} ÷ {division['divisor']} = {division['quotient']})"

    if "route" in answer and isinstance(answer["route"], dict):
        route = answer["route"]
        return f"{route['left']} × {route['right']}"

    if "division" in answer and isinstance(answer["division"], dict):
        division = answer["division"]
        return f"{division['product']} ÷ {division['divisor']} = {division['quotient']}"

    if "belongs" in answer:
        return "Yes" if answer["belongs"] else "No"

    if "correct_equation" in answer:
        eq = answer["correct_equation"]
        return f"{eq['left']} × {eq['right']} = {eq['product']}"

    if "classification" in answer:
        return str(answer["classification"])

    if "accepted_routes" in answer:
        routes = [f"{route['left']} × {route['right']}" for route in answer["accepted_routes"]]
        return "; ".join(routes)

    if "accepted_pattern_ids" in answer:
        return ", ".join(answer["accepted_pattern_ids"])

    if "has_another_way_in" in answer:
        return "No"

    if "has_another_way_out" in answer:
        return "No"

    return str(answer)


def _product_option_label(product: int) -> str:
    record = product_record(product)
    return f"{product} · {record.stage}"


def _title_case(value: str) -> str:
    return value.replace("_", " ").title()


if __name__ == "__main__":
    main()
