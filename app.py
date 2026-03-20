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
    _render_questions(worksheet["questions"], str(worksheet["tier"]))
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


def _render_questions(questions: Iterable[Dict[str, object]], tier: str) -> None:
    st.subheader("Pupil Worksheet")

    for question in questions:
        with st.container(border=True):
            qid = question["id"]
            section = _title_case(str(question["section"]))
            st.markdown(f"**Q{qid}. {section}**")
            st.write(render_pupil_prompt(question, tier))


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


def render_pupil_prompt(question: Dict[str, object], tier: str) -> str:
    question_id = int(question["id"])
    prompt_data = question["prompt_data"]

    if question_id == 1:
        return _render_q1(tier, prompt_data)
    if question_id == 2:
        return _render_q2(tier, prompt_data)
    if question_id == 3:
        return _render_q3(tier, prompt_data)
    if question_id == 4:
        return _render_q4(tier, prompt_data)
    if question_id == 5:
        return _render_q5(tier, prompt_data)
    if question_id == 6:
        return _render_q6(tier, prompt_data)
    if question_id == 7:
        return _render_q7(tier, prompt_data)
    if question_id == 8:
        return _render_q8(tier, prompt_data)
    if question_id == 9:
        return _render_q9(tier, prompt_data)
    if question_id == 10:
        return _render_q10(tier, prompt_data)

    return ""


def _render_q1(tier: str, prompt_data: Dict[str, object]) -> str:
    product = prompt_data["product"]

    if tier == "Support":
        return f"Find {product}."
    if tier == "Core":
        return f"Find {product}."
    return f"What do you notice about {product}?"


def _render_q2(tier: str, prompt_data: Dict[str, object]) -> str:
    left = prompt_data["left"]
    product = prompt_data["product"]

    if tier == "Support":
        return f"Complete: {left} × __ = {product}"
    if tier == "Core":
        return f"Find a way in to {product} using {left}."
    return f"Show a way in to {product} using {left}."


def _render_q3(tier: str, prompt_data: Dict[str, object]) -> str:
    left = prompt_data["left"]
    product = prompt_data["product"]

    if tier == "Support":
        return f"Complete: {left} × __ = {product}"
    if tier == "Core":
        return f"Find another way in to {product} using {left}."
    return f"Show another way in to {product} using {left}."


def _render_q4(tier: str, prompt_data: Dict[str, object]) -> str:
    product = prompt_data["product"]
    divisor = prompt_data["divisor"]

    if tier == "Support":
        return f"{product} ÷ {divisor} = __"
    if tier == "Core":
        return f"{product} ÷ {divisor} = __"
    return f"Show the way out from {product} using {divisor}."


def _render_q5(tier: str, prompt_data: Dict[str, object]) -> str:
    product = prompt_data["product"]
    divisor = prompt_data["divisor"]

    if tier == "Support":
        return f"{product} ÷ {divisor} = __"
    if tier == "Core":
        return f"{product} ÷ {divisor} = __"
    return f"Show another way out from {product} using {divisor}."


def _render_q6(tier: str, prompt_data: Dict[str, object]) -> str:
    product = prompt_data["product"]
    intro_route = prompt_data.get("intro_route")

    if intro_route:
        route_text = f"{intro_route['left']} × {intro_route['right']}"
    else:
        route_text = ""

    if tier == "Support":
        return f"One way in is {route_text}. Find another way in to {product}."
    if tier == "Core":
        return f"One way in is {route_text}. Find another way in to {product}."
    return f"{product} has more than one way in. Show another one."


def _render_q7(tier: str, prompt_data: Dict[str, object]) -> str:
    if "candidate" in prompt_data:
        candidate = prompt_data["candidate"]
    else:
        candidate = prompt_data["candidates"][0]

    if tier == "Support":
        return f"Does {candidate} belong in the TMK World? Yes or no?"
    if tier == "Core":
        return f"Does {candidate} belong in the TMK World?"
    return f"Does {candidate} belong in the TMK World? Explain."


def _render_q8(tier: str, prompt_data: Dict[str, object]) -> str:
    left = prompt_data["left"]
    right = prompt_data["right"]
    product = prompt_data["product"]

    if tier == "Support":
        return f"Check: {left} × {right} = {product}. Fix it."
    if tier == "Core":
        return f"Check: {left} × {right} = {product}. Fix it."
    return f"Check: {left} × {right} = {product}. Is it inside the TMK World? Fix or explain."


def _render_q9(tier: str, prompt_data: Dict[str, object]) -> str:
    product = prompt_data["product"]

    if tier == "Support":
        return f"Complete: I can rebuild {product} by using __ × __."
    if tier == "Core":
        return f"If you forgot {product}, how could you rebuild it?"
    return f"Explain how you could rebuild {product} using a known route."


def _render_q10(tier: str, prompt_data: Dict[str, object]) -> str:
    product = prompt_data["product"]

    if tier == "Support":
        return f"Complete: {product} belongs in the TMK World because __."
    if tier == "Core":
        return f"Tell one true thing about {product}."
    return f"Explain the structure of {product}."


def _product_option_label(product: int) -> str:
    record = product_record(product)
    return f"{product} · {record.stage}"


def _title_case(value: str) -> str:
    return value.replace("_", " ").title()


if __name__ == "__main__":
    main()
