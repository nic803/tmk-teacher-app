from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import streamlit as st

from products import ALL_PRODUCTS, product_record, stage_label
from worksheet_engine import generate_worksheet

APP_TITLE = "TMK Worksheet Studio"
APP_CAPTION = "Product-based worksheet generation for the TMK World"
TIERS = ("Support", "Core", "Extension")


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="✳️",
    layout="wide",
)


def main() -> None:
    st.title(APP_TITLE)
    st.caption(APP_CAPTION)

    product, tier = _render_controls()

    worksheet = generate_worksheet(product, tier)

    _render_summary(
        product=worksheet.product,
        stage=worksheet.stage,
        tier=worksheet.tier,
        question_count=len(worksheet.questions),
    )
    _render_product_context(worksheet.product)
    _render_pupil_worksheet(worksheet.questions)
    _render_teacher_key(worksheet.teacher_key)


def _render_controls() -> tuple[int, str]:
    with st.sidebar:
        st.header("Worksheet Settings")

        default_product = 36 if 36 in ALL_PRODUCTS else ALL_PRODUCTS[0]

        product = st.selectbox(
            "Product",
            options=ALL_PRODUCTS,
            index=ALL_PRODUCTS.index(default_product),
            format_func=_product_option_label,
        )

        tier = st.radio(
            "Tier",
            options=TIERS,
            index=1,
            horizontal=True,
        )

        record = product_record(product)

        st.divider()
        st.markdown("**Product Overview**")
        st.write(f"Stage: {stage_label(record.stage)}")
        st.write(f"Intro route: {record.intro_route[0]} × {record.intro_route[1]}")
        st.write(f"Structural role: {record.structural_role}")
        st.write(f"Factor families: {_format_routes(record.factor_families)}")
        st.write(f"Ways in: {_format_routes(record.ways_in)}")

    return product, tier


def _render_summary(product: int, stage: str, tier: str, question_count: int) -> None:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Product", str(product))
    col2.metric("Stage", str(stage))
    col3.metric("Tier", str(tier))
    col4.metric("Questions", str(question_count))

    st.divider()


def _render_product_context(product: int) -> None:
    record = product_record(product)

    with st.expander("Product Context", expanded=False):
        st.write(f"Stage label: {stage_label(record.stage)}")
        st.write(f"Intro route: {record.intro_route[0]} × {record.intro_route[1]}")
        st.write(f"Ways in: {_format_routes(record.ways_in)}")
        st.write(f"Ways out: {_format_routes(record.ways_out)}")
        st.write(f"Factor families: {_format_routes(record.factor_families)}")
        st.write(f"Related products: {_format_scalar_sequence(record.related_products)}")
        st.write(f"Structural role: {record.structural_role}")


def _render_pupil_worksheet(questions: Iterable[Any]) -> None:
    st.subheader("Pupil Worksheet")

    for index, question in enumerate(questions, start=1):
        with st.container(border=True):
            st.markdown(f"**Q{_question_number(question, index)}**")
            st.write(_render_question_text(question))
            _render_question_metadata(question)


def _render_teacher_key(teacher_key: Any) -> None:
    st.divider()

    with st.expander("Teacher Key", expanded=False):
        answers = _coerce_sequence(_get_attr(teacher_key, "answers"))
        pattern_ids = _coerce_sequence(_get_attr(teacher_key, "pattern_ids"))
        memory_cue_ids = _coerce_sequence(_get_attr(teacher_key, "memory_cue_ids"))
        notes = _coerce_sequence(_get_attr(teacher_key, "notes"))

        st.markdown("**Answers**")
        if answers:
            for index, answer in enumerate(answers, start=1):
                st.write(f"Q{index}. {_stringify(answer)}")
        else:
            st.write("No answers available.")

        st.markdown("**Pattern Links**")
        if pattern_ids:
            st.write(", ".join(_stringify(item) for item in pattern_ids))
        else:
            st.write("No pattern links attached.")

        st.markdown("**Memory Cues**")
        if memory_cue_ids:
            st.write(", ".join(_stringify(item) for item in memory_cue_ids))
        else:
            st.write("No memory cues attached.")

        st.markdown("**Teacher Notes**")
        if notes:
            for note in notes:
                st.write(f"- {_stringify(note)}")
        else:
            st.write("No teacher notes attached.")


def _render_question_metadata(question: Any) -> None:
    metadata = []

    prompt_key = _get_attr(question, "prompt_key")
    if prompt_key:
        metadata.append(("Prompt key", prompt_key))

    pattern_id = _get_attr(question, "pattern_id")
    if pattern_id:
        metadata.append(("Pattern", pattern_id))

    memory_cue_id = _get_attr(question, "memory_cue_id")
    if memory_cue_id:
        metadata.append(("Memory cue", memory_cue_id))

    answer = _get_attr(question, "answer")
    if answer not in (None, ""):
        metadata.append(("Expected answer", _stringify(answer)))

    if metadata:
        with st.expander("Question metadata", expanded=False):
            for label, value in metadata:
                st.write(f"{label}: {_stringify(value)}")


def _render_question_text(question: Any) -> str:
    for field_name in (
        "pupil_prompt",
        "prompt",
        "display_text",
        "text",
        "question_text",
        "body",
    ):
        value = _get_attr(question, field_name)
        if value not in (None, ""):
            return _stringify(value)

    prompt_key = _get_attr(question, "prompt_key")
    if prompt_key:
        return f"[{prompt_key}]"

    return _stringify(question)


def _question_number(question: Any, fallback: int) -> int:
    value = _get_attr(question, "id")
    if isinstance(value, int):
        return value
    return fallback


def _product_option_label(product: int) -> str:
    record = product_record(product)
    return f"{product} · {record.stage}"


def _format_routes(routes: Iterable[Any]) -> str:
    items = []
    for route in routes:
        if isinstance(route, tuple) and len(route) == 2:
            items.append(f"{route[0]} × {route[1]}")
        else:
            items.append(_stringify(route))
    return ", ".join(items) if items else "—"


def _format_scalar_sequence(values: Iterable[Any]) -> str:
    items = [_stringify(value) for value in values]
    return ", ".join(items) if items else "—"


def _coerce_sequence(value: Any) -> tuple[Any, ...]:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Iterable):
        return tuple(value)
    return (value,)


def _get_attr(obj: Any, name: str) -> Any:
    return getattr(obj, name, None)


def _stringify(value: Any) -> str:
    if isinstance(value, tuple) and len(value) == 2:
        return f"{value[0]} × {value[1]}"
    return str(value)


if __name__ == "__main__":
    main()
