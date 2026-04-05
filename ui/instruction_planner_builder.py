from __future__ import annotations


from typing import Any


from domain.products import ALL_PRODUCTS, product_record, stage_label
from domain.stage_vocabulary import get_stage_vocabulary


_STAGE_A_PRODUCTS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
_STAGE_B_PRODUCTS = (20, 30, 40, 50, 60, 70, 80, 90, 100)
_STAGE_D_NEW_PRODUCTS = (18, 27, 36, 54, 63, 72, 81)
_STAGE_E_NEW_PRODUCTS = (12, 14, 16, 24, 28, 32, 48, 56, 64)
_STAGE_G_SQUARE_EXTENSION = (1, 4, 9, 16, 25, 36, 49, 64, 81, 100)


_STAGE_A_PATTERN_BANK = [
    {
        "id": "identity",
        "title": "Identity",
        "description": "Multiplying by 1 keeps the number the same.",
    },
    {
        "id": "anchor_order",
        "title": "Anchor order",
        "description": "The Stage A products from 1 to 10 act as the first stable anchor points in the TMK system.",
    },
]


_STAGE_B_PATTERN_BANK = [
    {
        "id": "ten_times_scaling",
        "title": "Ten-times scaling",
        "description": "Multiplying by 10 scales the number into tens.",
    },
    {
        "id": "tens_benchmark",
        "title": "Tens benchmark",
        "description": "Stage B products are exact multiples of ten and form a stable benchmark set.",
    },
]


_STAGE_D_PATTERN_BANK = [
    {
        "id": "nine_quantifier_build",
        "title": "Nine quantifier-build rule",
        "description": "One less than the quantifier gives the tens digit, and the ones digit completes 9.",
    },
    {
        "id": "nine_digit_sum",
        "title": "Nine digit-sum pattern",
        "description": "The digits of the product add to 9.",
    },
    {
        "id": "nine_rise_fall",
        "title": "Nine rise/fall pattern",
        "description": "Across the 9× sequence, the tens rise and the ones fall.",
    },
]


_STAGE_E_PATTERN_BANK = [
    {
        "id": "doubling_chain",
        "title": "Doubling chain",
        "description": "A product in this stage can help build the next product by doubling.",
    },
    {
        "id": "use_one_product_to_find_another",
        "title": "Use one product to find another",
        "description": "If one product is known, the next related product in the chain can be derived from it.",
    },
    {
        "id": "inverse_connection",
        "title": "Inverse connection",
        "description": "A product can be used to recover its factors through division.",
    },
]


_STAGE_G_PATTERN_BANK = [
    {
        "id": "closure_with_7x7",
        "title": "Closure with 7×7",
        "description": "The product 49 is introduced through 7 × 7.",
    },
    {
        "id": "final_key",
        "title": "Final key",
        "description": "49 is the final new product in the TMK system.",
    },
    {
        "id": "square_product",
        "title": "Square product",
        "description": "49 is a square product because the two factors are the same.",
    },
]


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

    view_model: dict[str, Any] = {
        "title": "Instruction Planner",
        "subtitle": "Teacher explanation flow, stage vocabulary, teacher prompts, and example questions for the current product.",
        "selected_product": record.product,
        "selected_stage_label": stage_label(record.stage),
        "intro_route_label": _format_instruction_intro_route(record.intro_route),
        "product_options": ALL_PRODUCTS,
        "selected_product_index": ALL_PRODUCTS.index(selected_product),
        "product_format_func": product_format_func,
        "product_select_key": "instruction_product_select_v20",
        "on_product_change": on_product_change,
        "explanation_steps": _build_explanation_sequence(record.product, intro_left, intro_right),
        "teach_now_vocab": list(getattr(stage_record, "new_vocab", ()) or ()),
        "teacher_prompts": _build_teacher_prompts(record.product, intro_left, intro_right),
        "teacher_prompt_groups": [],
        "introduce_if_needed": list(getattr(stage_record, "available_vocab", ()) or ()),
        "example_questions": _instruction_example_questions(stage_record, record.product, intro_left, intro_right),
        "example_question_groups": [],
        "delay_vocab": list(getattr(stage_record, "required_vocab_focus", ()) or ()),
        "teaching_warning": "Do not open route comparison or wider product-network discussion until the entry explanation is secure.",
        "lesson_aim": "",
        "suggested_lesson_length": "",
        "stage_pattern_bank": [],
        "teacher_model": [],
        "teacher_explanation_sentence": "",
        "inverse_connection": [],
        "support_text": "",
        "core_text": "",
        "extension_text": "",
        "teacher_quick_summary": "",
        "check_for_understanding": "",
        "stage_product_sequence": [],
    }

    if record.stage == "A":
        view_model.update(
            _build_stage_a_content(
                product=record.product,
                left=intro_left,
                right=intro_right,
            )
        )
    elif record.stage == "B":
        view_model.update(
            _build_stage_b_content(
                product=record.product,
                left=intro_left,
                right=intro_right,
            )
        )
    elif _is_stage_d_route(intro_left, intro_right):
        view_model.update(
            _build_stage_d_content(
                product=record.product,
                left=intro_left,
                right=intro_right,
            )
        )
    elif _is_stage_e_route(intro_left, intro_right):
        view_model.update(
            _build_stage_e_content(
                product=record.product,
                left=intro_left,
                right=intro_right,
            )
        )
    elif record.stage == "G":
        view_model.update(
            _build_stage_g_content(
                product=record.product,
                left=intro_left,
                right=intro_right,
            )
        )
    else:
        view_model.update(
            _build_general_fallback_content(
                product=record.product,
                stage_label_text=stage_label(record.stage),
                left=intro_left,
                right=intro_right,
            )
        )

    return view_model


def _build_stage_a_content(*, product: int, left: int, right: int) -> dict[str, Any]:
    anchor_value = right if left == 1 else left
    route_label = _format_route((left, right))

    teach_now_vocab = [
        "product",
        "factor",
        "multiply",
        "times",
        "one",
        "same",
        "identity",
        "anchor",
        "order",
        "divide",
        "inverse",
    ]

    introduce_if_needed = [
        "equal",
        "fact",
        "compare",
        "before",
        "after",
        "groups",
    ]

    delay_vocab = [
        "commutative",
        "factor family beyond the stage set",
        "route comparison",
        "bridge hub",
        "compression hub",
    ]

    teacher_prompt_groups = [
        {
            "title": "Entry prompts",
            "items": [
                f"What product are we building when we say {route_label}?",
                f"What is {route_label}?",
                "So what is the product?",
            ],
        },
        {
            "title": "Pattern prompts",
            "items": [
                "What happens when we multiply by 1?",
                "Why does the number stay the same?",
                f"Where does {product} sit in the Stage A set?",
                f"Which numbers come before and after {product}?",
            ],
        },
        {
            "title": "Inverse prompts",
            "items": [
                f"If {route_label} = {product}, what is {product} ÷ 1?",
                f"What is {product} ÷ {product}?",
                "How does division help us get back out of the product?",
            ],
        },
        {
            "title": "Extension prompts",
            "items": [
                "Which other Stage A products are built through 1 × n?",
                "How does the whole Stage A set show the identity pattern?",
                "Which Stage A product comes after 9?",
            ],
        },
    ]

    example_question_groups = [
        {
            "title": "Build the product",
            "items": [
                f"Complete: {route_label} = □",
                f"Circle the product in {route_label} = {product}",
                "Choose the correct statement: multiplying by 1 keeps the number the same",
            ],
        },
        {
            "title": "Identity and anchor questions",
            "items": [
                "Complete: 1 × 8 = □",
                "Tick the Stage A products: 4, 6, 12, 9",
                f"Which number comes just before {product}?",
                f"Which number comes just after {product}?",
            ],
        },
        {
            "title": "Inverse questions",
            "items": [
                f"Complete: {product} ÷ 1 = □",
                f"Complete: {product} ÷ {product} = □",
                f"Match {route_label} = {product} to its division facts",
            ],
        },
        {
            "title": "Explain",
            "items": [
                "Explain what happens when we multiply by 1.",
                f"Explain why {product} belongs in the Stage A set.",
                f"Explain one division fact that comes from {product}.",
            ],
        },
    ]

    return {
        "explanation_steps": [
            f"What is {route_label}?",
            "So what is the product?",
            "What happens when we multiply by 1?",
            f"Where does {product} sit in the Stage A anchor set?",
            f"How can division help us get back out of the product {product}?",
        ],
        "teach_now_vocab": teach_now_vocab,
        "teacher_prompt_groups": teacher_prompt_groups,
        "teacher_prompts": _flatten_groups(teacher_prompt_groups),
        "introduce_if_needed": introduce_if_needed,
        "example_question_groups": example_question_groups,
        "example_questions": _flatten_groups(example_question_groups),
        "delay_vocab": delay_vocab,
        "teaching_warning": (
            f"Do not widen into broader route comparison or cross-stage discussion until learners are secure with the entry route "
            f"{route_label} = {product}, the identity pattern, and the linked inverse facts."
        ),
        "lesson_aim": (
            f"Learners build the product {product} through the identity structure, recognise it as part of the Stage A anchor set, "
            f"and link the product to its inverse division facts."
        ),
        "suggested_lesson_length": "10–15 minutes",
        "stage_pattern_bank": list(_STAGE_A_PATTERN_BANK),
        "stage_product_sequence": list(_STAGE_A_PRODUCTS),
        "teacher_model": [
            f"{route_label} = {product}",
            "",
            "Multiplying by 1 keeps the number the same.",
            "",
            f"{product} ÷ 1 = {product}",
            f"{product} ÷ {product} = 1",
        ],
        "teacher_explanation_sentence": (
            f"One group of {anchor_value} is still {product}."
        ),
        "inverse_connection": [
            f"{route_label} = {product}",
            f"{product} ÷ 1 = {product}",
            f"{product} ÷ {product} = 1",
        ],
        "check_for_understanding": (
            f"Learners should be able to state {route_label} = {product}, explain the identity pattern, "
            f"locate {product} in the Stage A anchor set, and state the linked division facts."
        ),
        "support_text": (
            f"Use one group of {product} objects and show that the amount stays {product}. "
            f"Keep the language simple: one group, same number, product."
        ),
        "core_text": (
            f"Build {product} as {route_label}, then teach the identity pattern and place {product} in the Stage A anchor set. "
            f"Finally connect {product} ÷ 1 = {product} and {product} ÷ {product} = 1."
        ),
        "extension_text": (
            f"Extend from the focus product {product} to the full Stage A set: "
            f"{', '.join(str(value) for value in _STAGE_A_PRODUCTS)}. "
            f"Ask learners to identify which products come from 1 × n, place the Stage A products in order, "
            f"and match multiplication facts to division facts."
        ),
        "teacher_quick_summary": (
            f"Today’s product is {product}. We build it as {route_label}, so the number stays the same. "
            f"Then we teach the identity pattern and place {product} in the Stage A anchor set. "
            f"Finally, we use division facts to move back out of the product."
        ),
    }


def _build_stage_b_content(*, product: int, left: int, right: int) -> dict[str, Any]:
    scale_value = right if left == 10 else left
    route_label = _format_route((left, right))

    teach_now_vocab = [
        "product",
        "factor",
        "multiply",
        "times",
        "ten times",
        "scale",
        "tens",
        "place value",
        "benchmark",
        "divide",
        "inverse",
    ]

    introduce_if_needed = [
        "equal",
        "fact",
        "compare",
        "before",
        "after",
        "groups of ten",
    ]

    delay_vocab = [
        "commutative",
        "factor family beyond the stage set",
        "route comparison",
        "bridge hub",
        "compression hub",
    ]

    teacher_prompt_groups = [
        {
            "title": "Entry prompts",
            "items": [
                f"What product are we building when we say {route_label}?",
                f"What is {route_label}?",
                "So what is the product?",
            ],
        },
        {
            "title": "Pattern prompts",
            "items": [
                "What happens when we multiply by 10?",
                f"Why is {product} a tens product?",
                "Which Stage B products are multiples of ten?",
                f"Which Stage B products come before and after {product}?",
            ],
        },
        {
            "title": "Inverse prompts",
            "items": [
                f"If {route_label} = {product}, what is {product} ÷ 10?",
                f"What is {product} ÷ {scale_value}?",
                "How does division help us get back out of the product?",
            ],
        },
        {
            "title": "Extension prompts",
            "items": [
                "Which other Stage B products belong to the 10× family?",
                "How does the whole Stage B set show scaling by ten?",
                "Which Stage B product comes after 70?",
            ],
        },
    ]

    example_question_groups = [
        {
            "title": "Build the product",
            "items": [
                f"Complete: {route_label} = □",
                f"Circle the product in {route_label} = {product}",
                f"Choose the correct statement: ten groups of {scale_value} make {product}",
            ],
        },
        {
            "title": "Scaling and tens questions",
            "items": [
                "Complete: 10 × 6 = □",
                "Tick the Stage B products: 40, 45, 60, 100",
                f"Which number comes just before {product} in the Stage B set?",
                f"Which number comes just after {product} in the Stage B set?",
            ],
        },
        {
            "title": "Inverse questions",
            "items": [
                f"Complete: {product} ÷ 10 = □",
                f"Complete: {product} ÷ {scale_value} = □",
                f"Match {route_label} = {product} to its division facts",
            ],
        },
        {
            "title": "Explain",
            "items": [
                "Explain what happens when we multiply by 10.",
                f"Explain why {product} belongs in the Stage B set.",
                f"Explain one division fact that comes from {product}.",
            ],
        },
    ]

    return {
        "explanation_steps": [
            f"What is {route_label}?",
            "So what is the product?",
            "What happens when we multiply by 10?",
            f"Why does {product} belong in the Stage B set?",
            f"How can division help us get back out of the product {product}?",
        ],
        "teach_now_vocab": teach_now_vocab,
        "teacher_prompt_groups": teacher_prompt_groups,
        "teacher_prompts": _flatten_groups(teacher_prompt_groups),
        "introduce_if_needed": introduce_if_needed,
        "example_question_groups": example_question_groups,
        "example_questions": _flatten_groups(example_question_groups),
        "delay_vocab": delay_vocab,
        "teaching_warning": (
            f"Do not widen into broader route comparison or cross-stage discussion until learners are secure with the entry route "
            f"{route_label} = {product}, the ten-times scaling pattern, and the linked inverse facts."
        ),
        "lesson_aim": (
            f"Learners build the product {product} through 10× scaling, recognise it as part of the Stage B tens set, "
            f"and link the product to its inverse division facts."
        ),
        "suggested_lesson_length": "10–15 minutes",
        "stage_pattern_bank": list(_STAGE_B_PATTERN_BANK),
        "stage_product_sequence": list(_STAGE_B_PRODUCTS),
        "teacher_model": [
            f"{route_label} = {product}",
            "",
            f"Multiplying by 10 makes {scale_value} groups of ten.",
            "",
            f"{product} ÷ 10 = {scale_value}",
            f"{product} ÷ {scale_value} = 10",
        ],
        "teacher_explanation_sentence": (
            f"Ten groups of {scale_value} make {product}, so {product} is a tens product."
        ),
        "inverse_connection": [
            f"{route_label} = {product}",
            f"{product} ÷ 10 = {scale_value}",
            f"{product} ÷ {scale_value} = 10",
        ],
        "check_for_understanding": (
            f"Learners should be able to state {route_label} = {product}, explain the 10× scaling pattern, "
            f"recognise {product} as a Stage B product, and state the linked division facts."
        ),
        "support_text": (
            f"Use groups of ten objects or a place-value model to show 10 groups of {scale_value}. "
            f"Keep the language simple: ten groups, tens, product."
        ),
        "core_text": (
            f"Build {product} as {route_label}, then teach the 10× scaling pattern and place {product} in the Stage B set. "
            f"Finally connect {product} ÷ 10 = {scale_value} and {product} ÷ {scale_value} = 10."
        ),
        "extension_text": (
            f"Extend from the focus product {product} to the full Stage B set: "
            f"{', '.join(str(value) for value in _STAGE_B_PRODUCTS)}. "
            f"Ask learners to identify which products come from 10 × n, place the Stage B products in order, "
            f"and match multiplication facts to division facts."
        ),
        "teacher_quick_summary": (
            f"Today’s product is {product}. We build it as {route_label}, so it becomes a tens product. "
            f"Then we teach the 10× scaling pattern and place {product} in the Stage B set. "
            f"Finally, we use division facts to move back out of the product."
        ),
    }


def _build_stage_d_content(*, product: int, left: int, right: int) -> dict[str, Any]:
    base = _stage_d_base_value(left, right)

    teach_now_vocab = [
        "product",
        "factor",
        "multiply",
        "times",
        "groups",
        "sequence",
        "pattern",
        "missing number",
        "digit sum",
        "subtract one",
        "quantifier",
        "tens digit",
        "ones digit",
        "divide",
        "inverse",
    ]

    introduce_if_needed = [
        "equal",
        "same",
        "fact",
        "ten times",
        "groups of ten",
        "compare",
        "before",
        "after",
    ]

    delay_vocab = [
        "commutative",
        "factor family",
        "route comparison beyond the stage set",
        "bridge hub",
        "compression hub",
    ]

    teacher_prompt_groups = [
        {
            "title": "Entry prompts",
            "items": [
                f"What product are we building when we say 9 × {base}?",
                f"What is 10 × {base}?",
                f"What is 1 × {base}?",
                f"What must we subtract to get 9 × {base}?",
                f"So what is 9 × {base}?",
            ],
        },
        {
            "title": "Pattern prompts",
            "items": [
                f"In 9 × {base}, what is the quantifier?",
                f"What is one less than {base}?",
                f"So what is the tens digit in {product}?",
                "What must the ones digit be so the digits add to 9?",
                f"What do the digits in {product} add to?",
                f"Which Stage D product comes before {product}?",
                f"Which Stage D product comes after {product}?",
                "What happens to the tens digits across the sequence?",
                "What happens to the ones digits across the sequence?",
            ],
        },
        {
            "title": "Inverse prompts",
            "items": [
                f"If 9 × {base} = {product}, what is {product} ÷ 9?",
                f"What is {product} ÷ {base}?",
                "How does division help us get back out of the product?",
            ],
        },
        {
            "title": "Extension prompts",
            "items": [
                "Which other new Stage D products belong to the same 9× family?",
                "Which Stage D product comes after 54?",
                "Which Stage D product has digits 8 and 1?",
                "How does the whole Stage D set show the 9× pattern?",
            ],
        },
    ]

    example_question_groups = [
        {
            "title": "Build the product",
            "items": [
                f"Complete: 10 × {base} = □",
                f"Complete: 1 × {base} = □",
                f"Complete: {base * 10} − {base} = □",
                f"So: 9 × {base} = □",
                f"Choose the correct statement: 9 × {base} is one group of {base} less than 10 × {base}.",
            ],
        },
        {
            "title": "Quantifier-build and digit-sum",
            "items": [
                f"In 9 × {base}, one less than {base} is □.",
                f"Complete: 9 × {base} = {product // 10} tens and □ ones.",
                f"Complete: {product // 10} + {product % 10} = □.",
                f"Which product fits the 9× digit-sum pattern: {product}, {product - 1}, {product - 2}?",
            ],
        },
        {
            "title": "Rise/fall and sequence",
            "items": [
                f"Which product comes just before {product} in the Stage D sequence?",
                f"Which product comes just after {product} in the Stage D sequence?",
                "Complete the Stage D sequence: 18, 27, 36, □, □, □, □.",
                "Tick the true statement: the tens rise and the ones fall.",
            ],
        },
        {
            "title": "Inverse questions",
            "items": [
                f"Complete: {product} ÷ 9 = □",
                f"Complete: {product} ÷ {base} = □",
                f"Match 9 × {base} = {product} to its division facts.",
            ],
        },
        {
            "title": "Explain",
            "items": [
                f"Explain how to derive 9 × {base} from 10 × {base}.",
                f"Explain how {product} fits the 9× pattern.",
                f"Explain one division fact that comes from {product}.",
            ],
        },
    ]

    return {
        "explanation_steps": [
            f"What is 10 × {base}?",
            f"What is 1 × {base}?",
            f"What is {base * 10} − {base}?",
            f"So what is 9 × {base}?",
            f"In 9 × {base}, what is one less than {base}?",
            f"So what is the tens digit in {product}?",
            "What must the ones digit be so the digits add to 9?",
            f"Where does {product} sit in the Stage D sequence?",
            "What happens to the tens digits across the sequence?",
            "What happens to the ones digits across the sequence?",
        ],
        "teach_now_vocab": teach_now_vocab,
        "teacher_prompt_groups": teacher_prompt_groups,
        "teacher_prompts": _flatten_groups(teacher_prompt_groups),
        "introduce_if_needed": introduce_if_needed,
        "example_question_groups": example_question_groups,
        "example_questions": _flatten_groups(example_question_groups),
        "delay_vocab": delay_vocab,
        "teaching_warning": (
            f"Do not widen into broader route comparison or cross-stage product-network discussion "
            f"until learners are secure with the entry route 9 × {base} = {product} and the three core Stage D patterns."
        ),
        "lesson_aim": (
            f"Learners build the product {product} through the 9× structure, use all core Stage D patterns, "
            f"and extend their understanding across the other new Stage D products."
        ),
        "suggested_lesson_length": "15–20 minutes",
        "stage_pattern_bank": list(_STAGE_D_PATTERN_BANK),
        "stage_product_sequence": list(_STAGE_D_NEW_PRODUCTS),
        "teacher_model": [
            f"10 × {base} = {base * 10}",
            f"1 × {base} = {base}",
            f"{base * 10} − {base} = {product}",
            f"9 × {base} = {product}",
            "",
            f"In 9 × {base}, one less than {base} is {product // 10}, so the tens digit is {product // 10}.",
            f"The ones digit must be {product % 10}, so the digits add to 9.",
        ],
        "teacher_explanation_sentence": (
            f"Nine groups of {base} is one group of {base} less than ten groups of {base}."
        ),
        "inverse_connection": [
            f"9 × {base} = {product}",
            f"{product} ÷ 9 = {base}",
            f"{product} ÷ {base} = 9",
        ],
        "check_for_understanding": (
            f"Learners should be able to derive 9 × {base} = {product}, explain how {product} fits the 9× pattern, "
            f"and state the linked division facts."
        ),
        "support_text": (
            f"Use counters or arrays to show 10 groups of {base}, then remove 1 group of {base}. "
            f"Keep the language simple: ten groups, one less group, nine groups, product."
        ),
        "core_text": (
            f"Build {product} from 10 × {base} − {base}, then teach all three Stage D patterns through the product: "
            f"quantifier-build, digit sum, and rise/fall. Finally connect {product} ÷ 9 = {base} and {product} ÷ {base} = 9."
        ),
        "extension_text": (
            f"Extend from the focus product {product} to the full Stage D set: "
            f"{', '.join(str(value) for value in _STAGE_D_NEW_PRODUCTS)}. "
            f"Use nearby products first, then widen to the whole Stage D set. "
            f"Ask learners to place all Stage D products in order, identify the quantifier for each product, "
            f"check the digit sum in each product, describe how the tens rise and the ones fall, and match multiplication facts to division facts."
        ),
        "teacher_quick_summary": (
            f"Today’s product is {product}. We first build it as 9 × {base} by starting from 10 × {base} "
            f"and subtracting one group of {base}. Then we teach the full Stage D pattern bank through {product}: "
            f"one less than the quantifier gives the tens digit, the digits add to 9, and across the sequence "
            f"the tens rise while the ones fall. Finally, we extend this understanding across the other new Stage D products "
            f"and use division facts to move back out of the product."
        ),
    }


def _build_stage_e_content(*, product: int, left: int, right: int) -> dict[str, Any]:
    chain_routes = _stage_e_chain_routes(product, left, right)
    chain_products = [route[0] * route[1] for route in chain_routes]
    focus_index = chain_products.index(product)
    route_labels = [_format_route(route) for route in chain_routes]
    current_route_label = route_labels[focus_index]

    teacher_model = [f"{label} = {value}" for label, value in zip(route_labels, chain_products)]

    inverse_connection = [
        f"{current_route_label} = {product}",
        f"{product} ÷ {left} = {right}",
        f"{product} ÷ {right} = {left}",
    ]

    teach_now_vocab = [
        "product",
        "factor",
        "multiply",
        "times",
        "double",
        "doubling",
        "chain",
        "pattern",
        "sequence",
        "groups",
        "divide",
        "inverse",
    ]

    introduce_if_needed = [
        "equal",
        "same",
        "fact",
        "compare",
        "before",
        "after",
        "half",
    ]

    delay_vocab = [
        "commutative",
        "factor family",
        "route comparison beyond the chain",
        "bridge hub",
        "compression hub",
    ]

    teacher_prompt_groups = [
        {
            "title": "Entry prompts",
            "items": [
                f"What product are we building when we say {current_route_label}?",
                f"What is {current_route_label}?",
                "So what is the product?",
            ],
        },
        {
            "title": "Pattern prompts",
            "items": _stage_e_pattern_prompts(chain_products, route_labels, focus_index, product),
        },
        {
            "title": "Inverse prompts",
            "items": [
                f"If {current_route_label} = {product}, what is {product} ÷ {left}?",
                f"What is {product} ÷ {right}?",
                f"How does division help us get back out of the product {product}?",
            ],
        },
        {
            "title": "Extension prompts",
            "items": _stage_e_extension_prompts(chain_products, product),
        },
    ]

    example_question_groups = [
        {
            "title": "Build the product",
            "items": [
                f"Complete: {current_route_label} = □",
                f"Circle the product in {current_route_label} = {product}",
                f"Choose the correct statement: {current_route_label} makes {product}",
            ],
        },
        {
            "title": "Doubling-chain questions",
            "items": _stage_e_chain_questions(chain_products, route_labels, focus_index),
        },
        {
            "title": "Inverse questions",
            "items": [
                f"Complete: {product} ÷ {left} = □",
                f"Complete: {product} ÷ {right} = □",
                f"Match {current_route_label} = {product} to its division facts",
            ],
        },
        {
            "title": "Explain",
            "items": _stage_e_explain_questions(chain_products, focus_index),
        },
    ]

    lesson_aim = (
        f"Learners build the product {product} through the doubling-chain structure, use repeated doubling "
        f"to connect it to related Stage E products, and link the product to its inverse division facts."
    )

    check_for_understanding = _stage_e_check_for_understanding(
        product=product,
        left=left,
        right=right,
        chain_products=chain_products,
        focus_index=focus_index,
    )

    support_text = (
        f"Use counters or arrays to show {left} groups of {right}. Then show that doubling the product gives "
        f"the next step in the chain. Keep the language simple: groups, double, product."
    )

    core_text = _stage_e_core_text(product, left, right, chain_products, route_labels, focus_index)

    extension_text = _stage_e_extension_text(product, chain_products)

    teacher_quick_summary = _stage_e_teacher_quick_summary(
        product=product,
        chain_products=chain_products,
        route_labels=route_labels,
        focus_index=focus_index,
    )

    return {
        "explanation_steps": _stage_e_explanation_steps(product, chain_products, route_labels, focus_index),
        "teach_now_vocab": teach_now_vocab,
        "teacher_prompt_groups": teacher_prompt_groups,
        "teacher_prompts": _flatten_groups(teacher_prompt_groups),
        "introduce_if_needed": introduce_if_needed,
        "example_question_groups": example_question_groups,
        "example_questions": _flatten_groups(example_question_groups),
        "delay_vocab": delay_vocab,
        "teaching_warning": (
            f"Do not widen into unrelated route comparison or broader cross-stage product discussion until learners "
            f"are secure with the entry route {current_route_label} = {product}, the doubling-chain structure, and the linked inverse facts."
        ),
        "lesson_aim": lesson_aim,
        "suggested_lesson_length": "15–20 minutes",
        "stage_pattern_bank": list(_STAGE_E_PATTERN_BANK),
        "stage_product_sequence": list(_STAGE_E_NEW_PRODUCTS),
        "teacher_model": teacher_model,
        "teacher_explanation_sentence": (
            f"We start with {current_route_label} = {product}, then double the product to build the next facts in the chain."
        ),
        "inverse_connection": inverse_connection,
        "check_for_understanding": check_for_understanding,
        "support_text": support_text,
        "core_text": core_text,
        "extension_text": extension_text,
        "teacher_quick_summary": teacher_quick_summary,
    }


def _build_stage_g_content(*, product: int, left: int, right: int) -> dict[str, Any]:
    route_label = _format_route((left, right))

    teach_now_vocab = [
        "product",
        "factor",
        "multiply",
        "times",
        "square",
        "square product",
        "same factors",
        "final",
        "closure",
        "divide",
        "inverse",
    ]

    introduce_if_needed = [
        "equal",
        "same",
        "fact",
        "compare",
        "before",
        "after",
        "diagonal",
    ]

    delay_vocab = [
        "commutative",
        "factor family beyond the product",
        "broader product-network comparison",
        "bridge hub",
        "compression hub",
    ]

    teacher_prompt_groups = [
        {
            "title": "Entry prompts",
            "items": [
                f"What product are we building when we say {route_label}?",
                f"What is {route_label}?",
                "So what is the product?",
            ],
        },
        {
            "title": "Pattern prompts",
            "items": [
                f"What do you notice about the two factors in {route_label}?",
                f"Why is {product} called a square product?",
                f"Why is {product} special in TMK?",
                f"What does it mean to say that {product} closes the system?",
            ],
        },
        {
            "title": "Inverse prompts",
            "items": [
                f"If {route_label} = {product}, what is {product} ÷ {left}?",
                "How does division help us get back out of the product?",
            ],
        },
        {
            "title": "Extension prompts",
            "items": [
                "Which other products are square products?",
                f"How is {product} different from earlier square products?",
                "Why is there only one new Stage G product?",
                f"Why is {product} called the final key?",
            ],
        },
    ]

    example_question_groups = [
        {
            "title": "Build the product",
            "items": [
                f"Complete: {route_label} = □",
                f"Circle the product in {route_label} = {product}",
                f"Choose the correct statement: {route_label} makes {product}",
            ],
        },
        {
            "title": "Square and closure questions",
            "items": [
                f"Tick the true statement: both factors in {route_label} are the same.",
                f"Why is {product} a square product?",
                "Which number is the final new TMK product?",
                f"Complete: {product} is built from □ × □.",
            ],
        },
        {
            "title": "Inverse questions",
            "items": [
                f"Complete: {product} ÷ {left} = □",
                f"Match {route_label} = {product} to its division fact.",
            ],
        },
        {
            "title": "Explain",
            "items": [
                f"Explain why {product} is a square product.",
                f"Explain why {product} is the final new product in TMK.",
                f"Explain the division fact that comes from {product}.",
            ],
        },
    ]

    return {
        "explanation_steps": [
            f"What is {route_label}?",
            "So what is the product?",
            f"Why is {product} a square product?",
            f"Why is {product} special in TMK?",
            f"How can division help us get back out of the product {product}?",
        ],
        "teach_now_vocab": teach_now_vocab,
        "teacher_prompt_groups": teacher_prompt_groups,
        "teacher_prompts": _flatten_groups(teacher_prompt_groups),
        "introduce_if_needed": introduce_if_needed,
        "example_question_groups": example_question_groups,
        "example_questions": _flatten_groups(example_question_groups),
        "delay_vocab": delay_vocab,
        "teaching_warning": (
            f"Do not widen into broad route comparison or cross-stage product-network discussion until learners are secure with the entry route "
            f"{route_label} = {product}, the square-product idea, and the closure role of {product}."
        ),
        "lesson_aim": (
            f"Learners build the product {product} through the {route_label} square structure, "
            f"recognise it as the final new product in TMK, and link it to its inverse division fact."
        ),
        "suggested_lesson_length": "15–20 minutes",
        "stage_pattern_bank": list(_STAGE_G_PATTERN_BANK),
        "stage_product_sequence": [product],
        "teacher_model": [
            f"{route_label} = {product}",
            "",
            f"Both factors are the same, so {product} is a square product.",
            "",
            f"{product} ÷ {left} = {right}",
        ],
        "teacher_explanation_sentence": (
            f"We build {product} as {route_label}, and this closes the final missing product in the TMK system."
        ),
        "inverse_connection": [
            f"{route_label} = {product}",
            f"{product} ÷ {left} = {right}",
        ],
        "check_for_understanding": (
            f"Learners should be able to state {route_label} = {product}, explain why {product} is a square product, "
            f"explain why it is the final new TMK product, and state the linked division fact."
        ),
        "support_text": (
            f"Use an array or square arrangement to show {left} rows of {right}. "
            f"Keep the language simple: same groups, square, product."
        ),
        "core_text": (
            f"Build {product} as {route_label}, then teach the Stage G patterns through the product: "
            f"square product, closure, and final key. Finally connect {product} ÷ {left} = {right}."
        ),
        "extension_text": (
            f"Extend conceptually from the focus product {product} to the wider square pattern: "
            f"{', '.join(str(value) for value in _STAGE_G_SQUARE_EXTENSION)}. "
            f"Ask learners to identify which products are square products, explain what makes {product} special among them, "
            f"and describe why it is the final new TMK product."
        ),
        "teacher_quick_summary": (
            f"Today’s product is {product}. We build it as {route_label}, so it is a square product with the same factor on both sides. "
            f"Then we teach why {product} is special in TMK: it is the final new product, so it closes the system. "
            f"Finally, we use division to move back out of the product."
        ),
    }


def _build_general_fallback_content(
    *,
    product: int,
    stage_label_text: str,
    left: int,
    right: int,
) -> dict[str, Any]:
    route_label = _format_route((left, right))
    teacher_prompt_groups = [
        {
            "title": "Entry prompts",
            "items": [
                f"What do we already know about {route_label}?",
                "What product are we building?",
                f"How can we say {route_label} clearly?",
            ],
        },
    ]

    example_question_groups = [
        {
            "title": "Example questions",
            "items": [
                f"{left} × {right} = □",
                f"□ = {product}",
                f"{product} ÷ {left} = □",
            ],
        },
    ]

    return {
        "teacher_prompt_groups": teacher_prompt_groups,
        "teacher_prompts": _flatten_groups(teacher_prompt_groups),
        "example_question_groups": example_question_groups,
        "example_questions": _flatten_groups(example_question_groups),
        "lesson_aim": (
            f"Learners build the product {product} through the intro route {route_label} "
            f"and explain how it fits within {stage_label_text}."
        ),
        "suggested_lesson_length": "10–15 minutes",
        "stage_pattern_bank": [],
        "stage_product_sequence": [],
        "teacher_model": [
            f"{route_label} = {product}",
            f"{product} ÷ {left} = {right}",
            f"{product} ÷ {right} = {left}",
        ],
        "teacher_explanation_sentence": (
            f"The intro route {route_label} builds the product {product}."
        ),
        "inverse_connection": [
            f"{route_label} = {product}",
            f"{product} ÷ {left} = {right}",
            f"{product} ÷ {right} = {left}",
        ],
        "check_for_understanding": (
            f"Learners should be able to state {route_label} = {product} and give the linked division facts."
        ),
        "support_text": (
            f"Keep the focus on the intro route {route_label} and the product {product}. "
            f"Use concrete groups or arrays if the product is not yet secure."
        ),
        "core_text": (
            f"State the intro route {route_label}, identify the product {product}, "
            f"and connect the multiplication fact to its linked division facts."
        ),
        "extension_text": (
            f"Once {route_label} is secure, compare it with other products from {stage_label_text} "
            f"without opening full route comparison too early."
        ),
        "teacher_quick_summary": (
            f"Today’s product is {product}. We focused on the intro route {route_label}, "
            f"identified the product clearly, and linked multiplication to the inverse division facts."
        ),
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


def _flatten_groups(groups: list[dict[str, Any]]) -> list[str]:
    flattened: list[str] = []
    for group in groups:
        title = str(group.get("title", "")).strip()
        items = list(group.get("items", []) or [])
        if title:
            flattened.append(title)
        for item in items:
            item_text = str(item).strip()
            if item_text:
                flattened.append(item_text)
    return flattened


def _is_stage_d_route(left: int, right: int) -> bool:
    return left == 9 or right == 9


def _stage_d_base_value(left: int, right: int) -> int:
    return left if right == 9 else right


def _is_stage_e_route(left: int, right: int) -> bool:
    return left in (2, 4, 8) or right in (2, 4, 8)


def _stage_e_chain_factor(left: int, right: int) -> int:
    if left in (2, 4, 8):
        return right
    return left


def _stage_e_chain_routes(product: int, left: int, right: int) -> list[tuple[int, int]]:
    factor = _stage_e_chain_factor(left, right)
    candidate_routes = [(2, factor), (4, factor), (8, factor)]
    candidate_products = [a * b for a, b in candidate_routes]
    return [
        route
        for route, value in zip(candidate_routes, candidate_products)
        if value in _STAGE_E_NEW_PRODUCTS
    ]


def _stage_e_explanation_steps(
    product: int,
    chain_products: list[int],
    route_labels: list[str],
    focus_index: int,
) -> list[str]:
    steps = [
        f"What is {route_labels[focus_index]}?",
        "So what is the product?",
    ]

    if focus_index < len(chain_products) - 1:
        next_product = chain_products[focus_index + 1]
        next_route = route_labels[focus_index + 1]
        steps.extend(
            [
                f"If we double {product}, what do we get?",
                f"So what is {next_route}?",
            ]
        )

        if focus_index + 1 < len(chain_products) - 1:
            later_product = chain_products[focus_index + 2]
            later_route = route_labels[focus_index + 2]
            steps.extend(
                [
                    f"If we double {next_product}, what do we get?",
                    f"So what is {later_route}?",
                ]
            )

    steps.extend(
        [
            "What happens as we move along the doubling chain?",
            f"How can division help us get back out of the product {product}?",
        ]
    )
    return steps


def _stage_e_pattern_prompts(
    chain_products: list[int],
    route_labels: list[str],
    focus_index: int,
    product: int,
) -> list[str]:
    prompts: list[str] = []

    if focus_index < len(chain_products) - 1:
        next_product = chain_products[focus_index + 1]
        prompts.extend(
            [
                f"What happens if we double {product}?",
                "Which fact does that give us?",
            ]
        )
        if focus_index + 1 < len(chain_products) - 1:
            prompts.extend(
                [
                    f"What happens if we double {next_product}?",
                    "How does the doubling chain grow?",
                ]
            )
    else:
        prompts.extend(
            [
                f"Which earlier product in the chain doubles to make {product}?",
                "How does the doubling chain grow?",
            ]
        )

    prompts.append(f"Which products are in the same doubling track as {product}?")
    return prompts


def _stage_e_extension_prompts(chain_products: list[int], product: int) -> list[str]:
    prompts: list[str] = []
    if product in chain_products:
        focus_index = chain_products.index(product)
        if focus_index < len(chain_products) - 1:
            prompts.append(f"Which Stage E product is double {product}?")
        if focus_index + 1 < len(chain_products) - 1:
            prompts.append(f"Which Stage E product is double {chain_products[focus_index + 1]}?")
    prompts.extend(
        [
            "Which other Stage E products are built through doubling?",
            "How does the whole Stage E set show repeated doubling?",
        ]
    )
    return prompts


def _stage_e_chain_questions(
    chain_products: list[int],
    route_labels: list[str],
    focus_index: int,
) -> list[str]:
    questions: list[str] = []

    current_product = chain_products[focus_index]
    if focus_index < len(chain_products) - 1:
        next_product = chain_products[focus_index + 1]
        next_route = route_labels[focus_index + 1]
        questions.extend(
            [
                f"Double {current_product}: □",
                f"Complete: {next_route} = □",
            ]
        )
        if focus_index + 1 < len(chain_products) - 1:
            later_product = chain_products[focus_index + 1]
            later_route = route_labels[focus_index + 2]
            questions.extend(
                [
                    f"Double {later_product}: □",
                    f"Complete: {later_route} = □",
                ]
            )

    if len(chain_products) > 1:
        display_items = [str(value) for value in chain_products[:2]]
        display_items.append("□")
        questions.append(f"Complete the chain: {', '.join(display_items)}")

    return questions


def _stage_e_explain_questions(chain_products: list[int], focus_index: int) -> list[str]:
    questions: list[str] = []
    if focus_index < len(chain_products) - 1:
        questions.append(
            f"Explain how {chain_products[focus_index + 1]} can be built from {chain_products[focus_index]}."
        )
        if focus_index + 1 < len(chain_products) - 1:
            questions.append(
                f"Explain how {chain_products[focus_index + 2]} can be built from {chain_products[focus_index + 1]}."
            )
    else:
        questions.append(
            f"Explain how {chain_products[focus_index]} can be linked back to the earlier doubling chain."
        )
    questions.append(
        f"Explain one division fact that comes from {chain_products[focus_index]}."
    )
    return questions


def _stage_e_check_for_understanding(
    *,
    product: int,
    left: int,
    right: int,
    chain_products: list[int],
    focus_index: int,
) -> str:
    statements = [f"state {_format_route((left, right))} = {product}"]

    later_products = chain_products[focus_index + 1 :]
    if later_products:
        if len(later_products) == 1:
            statements.append(f"use doubling to derive {later_products[0]}")
        else:
            statements.append(
                "use doubling to derive " + " and ".join(str(value) for value in later_products)
            )

    statements.append(f"state the linked division facts for {product}")
    return "Learners should be able to " + ", ".join(statements) + "."


def _stage_e_core_text(
    product: int,
    left: int,
    right: int,
    chain_products: list[int],
    route_labels: list[str],
    focus_index: int,
) -> str:
    sentences = [f"Build {product} as {_format_route((left, right))}."]
    if focus_index < len(chain_products) - 1:
        derived = [
            f"{label} = {value}"
            for label, value in zip(route_labels[focus_index + 1 :], chain_products[focus_index + 1 :])
        ]
        if derived:
            sentences.append("Then use repeated doubling to derive " + " and ".join(derived) + ".")
    sentences.append(
        f"Finally connect {product} ÷ {left} = {right} and {product} ÷ {right} = {left}."
    )
    return " ".join(sentences)


def _stage_e_extension_text(product: int, chain_products: list[int]) -> str:
    same_track = ", ".join(str(value) for value in chain_products)
    stage_set = ", ".join(str(value) for value in _STAGE_E_NEW_PRODUCTS)
    return (
        f"Extend from the focus product {product} to the same-track chain: {same_track}. "
        f"Then widen to the full Stage E set: {stage_set}. "
        f"Ask learners to identify which products belong to the same doubling track, "
        f"describe how each product is built from the previous one, and match multiplication facts to division facts."
    )


def _stage_e_teacher_quick_summary(
    *,
    product: int,
    chain_products: list[int],
    route_labels: list[str],
    focus_index: int,
) -> str:
    current_route = route_labels[focus_index]
    summary = [f"Today’s product is {product}. We first build it as {current_route}."]
    later_links = [str(value) for value in chain_products[focus_index + 1 :]]
    if later_links:
        summary.append(
            "Then we use doubling to connect it to "
            + " and ".join(later_links)
            + ", showing how Stage E products grow through the doubling chain."
        )
    summary.append("Finally, we use division facts to move back out of the product.")
    return " ".join(summary)


def _format_instruction_intro_route(route: tuple[int, int]) -> str:
    left, right = route
    if left == 9 or right == 9:
        base = _stage_d_base_value(left, right)
        return f"9 × {base}"
    return _format_route(route)


def _format_route(route: tuple[int, int]) -> str:
    return f"{route[0]} × {route[1]}"
