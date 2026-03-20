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

            prompt_key = str(question["prompt_key"])
            prompt_data = question["prompt_data"]
            st.write(_render_prompt(prompt_key, prompt_data))

            with st.expander("Question metadata"):
                st.write({"prompt_key": prompt_key})
                st.write({"prompt_data": prompt_data})
                st.write({"pattern_ids": question["pattern_ids"]})
                st.write({"msvwa_tags": question["msvwa_tags"]})


def _render_teacher_key(teacher_key: Dict[str, object]) -> None:
    st.divider()
    with st.expander("Teacher Key", expanded=False):
        st.markdown("**Answers**")
        for index, answer in enumerate(teacher_key["answers"], start=1):
            st.write(f"Q{index}", answer)

        st.markdown("**Pattern Links**")
        pattern_ids = teacher_key.get("pattern_ids", [])
        if pattern_ids:
            st.write(list(pattern_ids))
        else:
            st.write("No pattern links attached.")

        st.markdown("**Memory Cues**")
        memory_cue_ids = teacher_key.get("memory_cue_ids", [])
        if memory_cue_ids:
            st.write(list(memory_cue_ids))
        else:
            st.write("No teacher memory cues attached.")

        st.markdown("**Teacher Notes**")
        notes = teacher_key.get("notes", [])
        for note in notes:
            st.write(f"- {note}")


def _product_option_label(product: int) -> str:
    record = product_record(product)
    return f"{product} · {record.stage}"


def _title_case(value: str) -> str:
    return value.replace("_", " ").title()


def _render_prompt(prompt_key: str, prompt_data: Dict[str, object]) -> str:
    if prompt_key == "notice_product":
        return f"Notice the product {prompt_data['product']}."

    if prompt_key == "identify_product":
        return f"Find the product {prompt_data['product']}."

    if prompt_key == "explain_product_notice":
        return f"What do you notice about the product {prompt_data['product']}?"

    if prompt_key == "complete_intro_way_in":
        return f"Complete the way in: {prompt_data['left']} × ___ = {prompt_data['product']}"

    if prompt_key == "complete_other_way_in":
        return f"Find another way in: {prompt_data['left']} × ___ = {prompt_data['product']}"

    if prompt_key == "find_intro_way_in":
        return f"Find the intro way in for {prompt_data['product']} using {prompt_data['left']}."

    if prompt_key == "find_other_way_in":
        return f"Find another way in for {prompt_data['product']} using {prompt_data['left']}."

    if prompt_key == "justify_intro_way_in":
        return f"Build and explain the intro way in for {prompt_data['product']} using {prompt_data['left']}."

    if prompt_key == "justify_other_way_in":
        return f"Build and explain another way in for {prompt_data['product']} using {prompt_data['left']}."

    if prompt_key == "complete_intro_way_out":
        return f"Complete the way out: {prompt_data['product']} ÷ {prompt_data['divisor']} = ___"

    if prompt_key == "complete_other_way_out":
        return f"Find another way out: {prompt_data['product']} ÷ {prompt_data['divisor']} = ___"

    if prompt_key == "find_intro_way_out":
        return f"Find the way out from {prompt_data['product']} using divisor {prompt_data['divisor']}."

    if prompt_key == "find_other_way_out":
        return f"Find another way out from {prompt_data['product']} using divisor {prompt_data['divisor']}."

    if prompt_key == "justify_intro_way_out":
        return f"Explain the way out from {prompt_data['product']} using divisor {prompt_data['divisor']}."

    if prompt_key == "justify_other_way_out":
        return f"Explain another way out from {prompt_data['product']} using divisor {prompt_data['divisor']}."

    if prompt_key == "match_another_way":
        intro_route = _route_text(prompt_data["intro_route"])
        other_route = _route_text(prompt_data["other_route"])
        return f"Compare the ways in for {prompt_data['product']}: {intro_route} and {other_route}."

    if prompt_key == "find_another_way":
        intro_route = _route_text(prompt_data["intro_route"])
        return f"The intro way in is {intro_route}. Find another way in for {prompt_data['product']}."

    if prompt_key == "compare_another_way":
        intro_route = _route_text(prompt_data["intro_route"])
        other_route = _route_text(prompt_data["other_route"])
        return f"Compare these two ways in for {prompt_data['product']}: {intro_route} and {other_route}."

    if prompt_key == "choose_belongs_number":
        candidates = prompt_data["candidates"]
        return f"Which number belongs to the TMK World: {candidates[0]} or {candidates[1]}?"

    if prompt_key == "does_number_belong":
        return f"Does {prompt_data['candidate']} belong to the TMK World?"

    if prompt_key == "explain_belongs_decision":
        return f"Does {prompt_data['candidate']} belong to the TMK World? Explain."

    if prompt_key == "repair_broken_output":
        return f"Check the route: {prompt_data['left']} × {prompt_data['right']} = {prompt_data['product']}. Fix it."

    if prompt_key == "repair_broken_route":
        return f"Check the route: {prompt_data['left']} × {prompt_data['right']} = {prompt_data['product']}. Fix the route."

    if prompt_key == "classify_true_but_outside_world":
        return (
            f"Check this route: {prompt_data['left']} × {prompt_data['right']} = {prompt_data['product']}. "
            "Is it inside the TMK World?"
        )

    if prompt_key == "say_how_to_rebuild":
        return f"How could you rebuild {prompt_data['product']}?"

    if prompt_key == "choose_product_fact":
        return f"Choose a true fact about the product {prompt_data['product']}."

    if prompt_key == "explain_how_to_rebuild":
        return f"Explain how you could rebuild {prompt_data['product']} if you forgot it."

    if prompt_key == "explain_product_structure":
        return f"Explain the structure of the product {prompt_data['product']}."

    if prompt_key == "justify_rebuild_strategy":
        return f"Justify a strong rebuild strategy for {prompt_data['product']}."

    if prompt_key == "generalise_product_structure":
        return f"What structure can you generalise from the product {prompt_data['product']}?"

    return f"{prompt_key}: {prompt_data}"


def _route_text(route_data: Dict[str, object]) -> str:
    return f"{route_data['left']} × {route_data['right']}"


if __name__ == "__main__":
    main()
