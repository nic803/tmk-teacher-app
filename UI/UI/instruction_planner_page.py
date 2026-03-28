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
    introduce_if_needed = view_model.get("introduce_if_needed", [])
    example_questions = view_model.get("example_questions", [])
    delay_vocab = view_model.get("delay_vocab", [])
    teaching_warning = view_model.get(
        "teaching_warning",
        "Do not open route comparison or wider product-network discussion until the entry explanation is secure.",
    )

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

    st.markdown("### Explanation sequence")
    if selected_product is not None:
        st.write(f"**Product:** {selected_product}")

    if explanation_steps:
        for index, step in enumerate(explanation_steps, start=1):
            st.markdown(f"**{index}.** {step}")
    else:
        st.write("No explanation sequence available.")

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
        if teacher_prompts:
            for prompt in teacher_prompts:
                st.write(f"- {prompt}")
        else:
            st.write("None")

    with bottom_left:
        st.markdown("### Introduce if needed")
        if introduce_if_needed:
            for item in introduce_if_needed:
                st.write(f"- {item}")
        else:
            st.write("None")

    with bottom_right:
        st.markdown("### Example questions")
        if example_questions:
            for question in example_questions:
                st.write(f"- {question}")
        else:
            st.write("None")

    st.markdown("### Delay vocabulary")
    if delay_vocab:
        for item in delay_vocab:
            st.write(f"- {item}")
    else:
        st.write("None")

    st.markdown("### Teaching warning")
    st.write(teaching_warning)
