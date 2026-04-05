from __future__ import annotations

from typing import Any

from domain.products import ALL_PRODUCTS, product_record, stage_label
from domain.stage_vocabulary import get_stage_vocabulary


def build_instruction_planner_view_model(
    product: int,
    *,
    selected_product: int,
    product_format_func,
    on_product_change,
) -> dict[str, Any]:
    record = product_record(product)
    stage_record = get_stage_vocabulary(record.stage)
    intro_left, intro_right = record.intro_route

    return {
        "title": "Instruction Planner",
        "subtitle": "Teacher explanation flow, stage vocabulary, teacher prompts, and example questions for the current product.",
        "selected_product": record.product,
        "selected_stage_label": stage_label(record.stage),
        "intro_route_label": _format_route(record.intro_route),
        "product_options": ALL_PRODUCTS,
        "selected_product_index": ALL_PRODUCTS.index(selected_product),
        "product_format_func": product_format_func,
        "product_select_key": "instruction_product_select_v20",
        "on_product_change": on_product_change,
        "explanation_steps": _build_explanation_sequence(record.product, intro_left, intro_right),
        "teach_now_vocab": list(getattr(stage_record, "new_vocab", ()) or ()),
        "teacher_prompts": _build_teacher_prompts(record.product, intro_left, intro_right),
        "introduce_if_needed": list(getattr(stage_record, "available_vocab", ()) or ()),
        "example_questions": _instruction_example_questions(stage_record, record.product, intro_left, intro_right),
        "delay_vocab": list(getattr(stage_record, "required_vocab_focus", ()) or ()),
        "teaching_warning": "Do not open route comparison or wider product-network discussion until the entry explanation is secure.",
    }


def _build_explanation_sequence(product: int, left: int, right: int) -> list[str]:
    if right == 9:
        base = left
        ten_value = base * 10
        one_value = base
        return [
            f"What is 10 × {base}?",
            f"What is 1 × {base}?",
            f"What is {ten_value} − {one_value}?",
            f"So what is 9 × {base}?",
        ]

    if left == 9:
        base = right
        ten_value = base * 10
        one_value = base
        return [
            f"What is 10 × {base}?",
            f"What is 1 × {base}?",
            f"What is {ten_value} − {one_value}?",
            f"So what is 9 × {base}?",
        ]

    return [
        f"State the intro route: {_format_route((left, right))}.",
        f"Identify the product: {product}.",
        f"Explain how {_format_route((left, right))} builds {product}.",
        f"Check the product again: {product}.",
    ]


def _build_teacher_prompts(product: int, left: int, right: int) -> list[str]:
    prompts = [
        f"What do we already know about {_format_route((left, right))}?",
        "What product are we building?",
        f"How can we say {_format_route((left, right))} clearly?",
    ]

    if right == 9 or left == 9:
        base = left if right == 9 else right
        prompts.extend(
            [
                f"What is 10 groups of {base}?",
                "How do we adjust from 10× to 9×?",
            ]
        )

    return prompts


def _instruction_example_questions(stage_record: Any, product: int, left: int, right: int) -> list[str]:
    from_stage = list(getattr(stage_record, "example_child_friendly_questions", []) or [])
    if from_stage:
        return [str(item) for item in from_stage]

    return [
        f"{left} × {right} = □",
        f"□ = {product}",
        f"{product} ÷ {left} = □",
    ]


def _format_route(route: tuple[int, int]) -> str:
    return f"{route[0]} × {route[1]}"
