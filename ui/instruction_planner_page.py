import streamlit as st

from ui.components import page_header


def render_instruction_planner_page(view_model):
    """
    UI-only page.
    Receives data from services.
    No TMK logic allowed here.
    """

    title = view_model.get("title", "Instruction Planner")
    subtitle = view_model.get(
        "subtitle",
        "Teacher explanation flow, stage vocabulary, teacher prompts, and example questions.",
    )
    selected_product = view_model.get("selected_product")
    selected_stage_label = view_model.get("selected_stage_label", "")
    intro_route_label = view_model.get("intro_route_label", "")
    explanation_steps = view_model.get("explanation_steps", [])
    teach_now_vocab = view_model.get("teach_now_vocab", [])
    teacher_prompts = view_model.get("teacher_prompts", [])
    teacher_prompt_groups = view_model.get("teacher_prompt_groups", [])
    introduce_if_needed = view_model.get("introduce_if_needed", [])
    example_questions = view_model.get("example_questions", [])
    example_question_groups = view_model.get("example_question_groups", [])
    delay_vocab = view_model.get("delay_vocab", [])
    teaching_warning = view_model.get(
        "teaching_warning",
        "Do not open route comparison or wider product-network discussion until the entry explanation is secure.",
    )

    lesson_aim = view_model.get("lesson_aim", "")
    suggested_lesson_length = view_model.get("suggested_lesson_length", "")
    stage_pattern_bank = view_model.get("stage_pattern_bank", [])
    stage_product_sequence = view_model.get("stage_product_sequence", [])
    teacher_model = view_model.get("teacher_model", [])
    teacher_explanation_sentence = view_model.get("teacher_explanation_sentence", "")
    inverse_connection = view_model.get("inverse_connection", [])
    check_for_understanding = view_model.get("check_for_understanding", "")
    support_text = view_model.get("support_text", "")
    core_text = view_model.get("core_text", "")
    extension_text = view_model.get("extension_text", "")
    teacher_quick_summary = view_model.get("teacher_quick_summary", "")

    page_header(title, subtitle)

    control_col1, control_col2 = st.columns((1.2, 0.8))

    with control_col1:
        product_options = view_model.get("product_options", [])
        selected_product_index = int(view_model.get("selected_product_index", 0))
        product_format_func = view_model.get("product_format_func")

        if product_options:
            st.selectbox(
                "Selected product",
                options=product_options,
                index=selected_product_index,
                format_func=product_format_func if product_format_func else None,
                key=view_model.get("product_select_key", "instruction_product_select_v20"),
                on_change=view_model.get("on_product_change"),
            )
        else:
            st.write("No product options available.")

    with control_col2:
        st.markdown("### Structural dependency reminder")
        if intro_route_label and selected_stage_label:
            st.write(f"Uses intro route {intro_route_label} in {selected_stage_label}.")
        elif intro_route_label:
            st.write(f"Uses intro route {intro_route_label}.")
        elif selected_stage_label:
            st.write(f"Current stage: {selected_stage_label}.")
        else:
            st.write("No structural dependency reminder available.")

    if lesson_aim or suggested_lesson_length:
        info_left, info_right = st.columns((1.2, 0.8))
        with info_left:
            st.markdown("### Lesson aim")
            st.write(lesson_aim if lesson_aim else "No lesson aim available.")
        with info_right:
            st.markdown("### Suggested lesson length")
            st.write(suggested_lesson_length if suggested_lesson_length else "Not specified.")

    if stage_pattern_bank:
        st.markdown("### TMK stage patterns to use in this lesson")
        for pattern in stage_pattern_bank:
            if isinstance(pattern, dict):
                pattern_title = pattern.get("title", "")
                pattern_description = pattern.get("description", "")
                if pattern_title:
                    st.write(f"**{pattern_title}**")
                if pattern_description:
                    st.write(pattern_description)
            else:
                st.write(f"- {pattern}")

    if stage_product_sequence:
        st.markdown("### Stage D sequence")
        st.write(", ".join(str(item) for item in stage_product_sequence))

    st.markdown("### Explanation sequence")
    if selected_product is not None:
        st.write(f"**Product:** {selected_product}")

    if explanation_steps:
        for index, step in enumerate(explanation_steps, start=1):
            st.markdown(f"**{index}.** {step}")
    else:
        st.write("No explanation sequence available.")

    if teacher_model or teacher_explanation_sentence:
        model_left, model_right = st.columns((1.1, 0.9))
        with model_left:
            st.markdown("### Teacher model")
            if teacher_model:
                for line in teacher_model:
                    if str(line).strip():
                        st.write(f"- {line}")
                    else:
                        st.write("")
            else:
                st.write("No teacher model available.")

        with model_right:
            st.markdown("### Teacher explanation sentence")
            st.write(
                teacher_explanation_sentence
                if teacher_explanation_sentence
                else "No teacher explanation sentence available."
            )

    if inverse_connection:
        st.markdown("### Inverse connection")
        for line in inverse_connection:
            st.write(f"- {line}")

    if check_for_understanding:
        st.markdown("### Check for understanding")
        st.write(check_for_understanding)

    top_left, top_right = st.columns(2)
    bottom_left, bottom_right = st.columns(2)

    with top_left:
        st.markdown("### Teach now vocabulary")
        if teach_now_vocab:
            for item in teach_now_vocab:
                st.write(f"- {item}")
        else:
            st.write("None")

    with top_right:
        st.markdown("### Teacher prompt bank")
        if teacher_prompt_groups:
            _render_group_blocks(teacher_prompt_groups)
        else:
            _render_grouped_list(teacher_prompts)

    with bottom_left:
        st.markdown("### Introduce if needed")
        if introduce_if_needed:
            for item in introduce_if_needed:
                st.write(f"- {item}")
        else:
            st.write("None")

    with bottom_right:
        st.markdown("### Example questions")
        if example_question_groups:
            _render_group_blocks(example_question_groups)
        else:
            _render_grouped_list(example_questions)

    st.markdown("### Delay vocabulary")
    if delay_vocab:
        for item in delay_vocab:
            st.write(f"- {item}")
    else:
        st.write("None")

    if support_text or core_text or extension_text:
        st.markdown("### Support / Core / Extension")
        support_col, core_col, extension_col = st.columns(3)

        with support_col:
            st.markdown("**Support**")
            st.write(support_text if support_text else "None")

        with core_col:
            st.markdown("**Core**")
            st.write(core_text if core_text else "None")

        with extension_col:
            st.markdown("**Extension**")
            st.write(extension_text if extension_text else "None")

    st.markdown("### Teaching warning")
    st.write(teaching_warning)

    if teacher_quick_summary:
        st.markdown("### Teacher quick summary")
        st.write(teacher_quick_summary)


def _render_group_blocks(groups):
    if not groups:
        st.write("None")
        return

    for group in groups:
        title = str(group.get("title", "")).strip()
        items = list(group.get("items", []) or [])

        if title:
            st.markdown(f"**{title}**")

        for item in items:
            item_text = str(item).strip()
            if item_text:
                st.write(f"- {item_text}")


def _render_grouped_list(items):
    if not items:
        st.write("None")
        return

    for item in items:
        text = str(item).strip()
        if not text:
            continue
        if _is_group_heading(text):
            st.markdown(f"**{text}**")
        else:
            st.write(f"- {text}")


def _is_group_heading(text: str) -> bool:
    heading_suffixes = (
        "prompts",
        "questions",
        "product",
        "digit-sum",
        "sequence",
        "explain",
    )
    lower_text = text.lower()
    return any(lower_text.endswith(suffix) for suffix in heading_suffixes)
