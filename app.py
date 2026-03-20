from __future__ import annotations

from typing import Tuple

import streamlit as st

from engine_registry import initialize_engine_registry
from products import ALL_PRODUCTS, product_record, stage_label
from pupil_prompt_map import render_pupil_prompt
from teacher_render_map import render_teacher_answers
from worksheet_service import generate_worksheet_package
from worlds import TMK_WORLD


st.set_page_config(
    page_title="TMK Worksheet Studio",
    page_icon="✳️",
    layout="wide",
)


def main() -> None:
    initialize_engine_registry()

    st.title("TMK Worksheet Studio")
    st.caption(f"Product-based worksheet generation for {TMK_WORLD}")

    product, tier = _render_controls()

    worksheet = generate_worksheet_package(product, tier)

    _render_summary(worksheet.product, worksheet.stage, worksheet.tier, len(worksheet.questions))
    _render_pupil_worksheet(worksheet.questions)
    _render_teacher_key(worksheet.teacher_key)


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
            options=("Support", "Core", "Extension"),
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


def _render_summary(product: int, stage: str, tier: str, question_count: int) -> None:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Product", str(product))
    col2.metric("Stage", str(stage))
    col3.metric("Tier", str(tier))
    col4.metric("Questions", str(question_count))

    st.divider()


def _render_pupil_worksheet(questions) -> None:
    st.subheader("Pupil Worksheet")

    for question in questions:
        with st.container(border=True):
            st.markdown(f"**Q{question.id}**")
            st.write(render_pupil_prompt(question))


def _render_teacher_key(teacher_key) -> None:
    st.divider()

    with st.expander("Teacher Key", expanded=False):

        st.markdown("**Answers**")

        rendered_answers = render_teacher_answers(teacher_key.answers)

        for index, answer in enumerate(rendered_answers, start=1):
            st.write(f"Q{index}. {answer}")

        st.markdown("**Pattern Links**")

        if teacher_key.pattern_ids:
            st.write(", ".join(teacher_key.pattern_ids))
        else:
            st.write("No pattern links attached.")

        st.markdown("**Memory Cues**")

        if teacher_key.memory_cue_ids:
            st.write(", ".join(teacher_key.memory_cue_ids))
        else:
            st.write("No memory cues attached.")

        st.markdown("**Teacher Notes**")

        for note in teacher_key.notes:
            st.write(f"- {note}")


def _product_option_label(product: int) -> str:
    record = product_record(product)
    return f"{product} · {record.stage}"


if __name__ == "__main__":
    main()
