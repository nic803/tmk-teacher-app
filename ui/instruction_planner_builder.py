from __future__ import annotations


from typing import Any


from domain.products import ALL_PRODUCTS, product_record, stage_label
from domain.stage_vocabulary import get_stage_vocabulary


_STAGE_C_NEW_PRODUCTS = (15, 25, 35, 45)
_STAGE_D_NEW_PRODUCTS = (18, 27, 36, 54, 63, 72, 81)
_STAGE_F_NEW_PRODUCTS = (21, 42)


_STAGE_C_PATTERN_BANK = [
    {
        "id": "five_as_half_of_ten",
        "title": "Five as half of ten",
        "description": "A 5× product can be built by finding the matching 10× product and halving it.",
    },
    {
        "id": "use_one_product_to_find_another",
        "title": "Use one product to find another",
        "description": "A known 10× product can be used to derive the related 5× product.",
    },
    {
        "id": "five_times_visible_ending",
        "title": "Five-times visible ending",
        "description": "5× products end in 0 or 5.",
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


_STAGE_F_PATTERN_BANK = [
    {
        "id": "interleaving",
        "title": "Interleaving",
        "description": "The 3× and 6× families are taught together, so learners can compare how products are related across the stage.",
    },
    {
        "id": "new_product_new_route",
        "title": "New product / new route",
        "description": "Not every 3× or 6× fact gives a new product. In this stage, 21 and 42 are the genuinely new products.",
    },
    {
        "id": "six_is_double_three",
        "title": "Six is double three",
        "description": "If a 3× product is known, the related 6× product can be built by doubling.",
    },
    {
        "id": "three_times_digit_sum_cycle",
        "title": "Three-times digit-sum cycle",
        "description": "3× products belong to the digit-sum cycle 3, 6, 9.",
    },
    {
        "id": "three_times_odd_even_alternation",
        "title": "Three-times odd/even alternation",
        "description": "3× products alternate odd, even, odd, even.",
    },
    {
        "id": "six_times_always_even",
        "title": "Six-times always even",
        "description": "All 6× products are even.",
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


    if _is_stage_c_route(intro_left, intro_right):
        view_model.update(
            _build_stage_c_content(
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
    elif _is_stage_f_route(intro_left, intro_right):
        view_model.update(
            _build_stage_f_content(
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




def _build_stage_c_content(*, product: int, left: int, right: int) -> dict[str, Any]:
    base = _stage_c_base_value(left, right)
    ten_value = base * 10


    teach_now_vocab = [
        "product",
        "factor",
        "multiply",
        "times",
        "groups",
        "half",
        "halve",
        "pattern",
        "sequence",
        "ending digit",
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
                f"What product are we building when we say 5 × {base}?",
                f"What is 10 × {base}?",
                f"What is half of {ten_value}?",
                f"So what is 5 × {base}?",
            ],
        },
        {
            "title": "Pattern prompts",
            "items": [
                f"What does {product} end in?",
                "What do 5× products often end in?",
                "Which other Stage C products end in 5?",
                f"How does knowing 10 × {base} help us find 5 × {base}?",
            ],
        },
        {
            "title": "Inverse prompts",
            "items": [
                f"If 5 × {base} = {product}, what is {product} ÷ 5?",
                f"What is {product} ÷ {base}?",
                "How does division help us get back out of the product?",
            ],
        },
        {
            "title": "Extension prompts",
            "items": [
                "Which other new Stage C products belong to the 5× family?",
                "Which Stage C product comes after 25?",
                "Which Stage C product has digits 4 and 5?",
                "How does the whole Stage C set show the 5× pattern?",
            ],
        },
    ]


    example_question_groups = [
        {
            "title": "Build the product",
            "items": [
                f"Complete: 10 × {base} = □",
                f"Complete: {ten_value} ÷ 2 = □",
                f"So: 5 × {base} = □",
                f"Choose the correct statement: 5 × {base} is half of 10 × {base}.",
            ],
        },
        {
            "title": "Half-of-ten and ending pattern",
            "items": [
                f"Complete: {product} ends in □.",
                "Tick the products that fit the 5× ending pattern: 15, 16, 25, 26.",
                "Which product belongs to Stage C: 15, 18, 19?",
                "Complete: 5 × 5 = □",
            ],
        },
        {
            "title": "Inverse questions",
            "items": [
                f"Complete: {product} ÷ 5 = □",
                f"Complete: {product} ÷ {base} = □",
                f"Match 5 × {base} = {product} to its division facts.",
            ],
        },
        {
            "title": "Explain",
            "items": [
                f"Explain how to derive 5 × {base} from 10 × {base}.",
                f"Explain how the ending digit shows that {product} fits the 5× pattern.",
                f"Explain one division fact that comes from {product}.",
            ],
        },
    ]


    return {
        "explanation_steps": [
            f"What is 10 × {base}?",
            f"What is half of {ten_value}?",
            f"So what is 5 × {base}?",
            f"What do you notice about the ending digit in {product}?",
            "Which other Stage C products end in 5?",
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
            f"Do not widen into broader route comparison or cross-stage product-network discussion "
            f"until learners are secure with the entry route 5 × {base} = {product}, the half-of-ten structure, and the linked inverse facts."
        ),
        "lesson_aim": (
            f"Learners build the product {product} through the 5× half-of-ten structure, "
            f"use core Stage C patterns, and extend their understanding across the other new Stage C products."
        ),
        "suggested_lesson_length": "15–20 minutes",
        "stage_pattern_bank": list(_STAGE_C_PATTERN_BANK),
        "stage_product_sequence": list(_STAGE_C_NEW_PRODUCTS),
        "teacher_model": [
            f"10 × {base} = {ten_value}",
            f"{ten_value} ÷ 2 = {product}",
            f"5 × {base} = {product}",
            "",
            f"{product} ends in 5, so it fits the 5× family pattern.",
        ],
        "teacher_explanation_sentence": (
            f"Five groups of {base} is half of ten groups of {base}."
        ),
        "inverse_connection": [
            f"5 × {base} = {product}",
            f"{product} ÷ 5 = {base}",
            f"{product} ÷ {base} = 5",
        ],
        "check_for_understanding": (
            f"Learners should be able to derive 5 × {base} = {product} from 10 × {base}, "
            f"explain why {product} fits the 5× pattern, and state the linked division facts."
        ),
        "support_text": (
            f"Use counters or arrays to show 10 groups of {base}, then split them into two equal halves. "
            f"Keep the language simple: ten groups, half, product."
        ),
        "core_text": (
            f"Build {product} from 10 × {base} ÷ 2, then teach the Stage C patterns through the product: "
            f"half-of-ten and visible ending. Finally connect {product} ÷ 5 = {base} and {product} ÷ {base} = 5."
        ),
        "extension_text": (
            f"Extend from the focus product {product} to the full Stage C set: "
            f"{', '.join(str(value) for value in _STAGE_C_NEW_PRODUCTS)}. "
            f"Ask learners to identify how each product is built from the related 10× fact, "
            f"check the ending digit in each product, and match multiplication facts to division facts."
        ),
        "teacher_quick_summary": (
            f"Today’s product is {product}. We first build it as 5 × {base} by finding 10 × {base} "
            f"and halving it. Then we teach the Stage C patterns through {product}: 5× is half of 10×, "
            f"and 5× products end in 0 or 5. Finally, we extend this understanding across the other new Stage C products "
            f"and use division facts to move back out of the product."
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




def _build_stage_f_content(*, product: int, left: int, right: int) -> dict[str, Any]:
    base = _stage_f_base_value(left, right)
    entry_multiplier = 3 if left == 3 or right == 3 else 6
    partner_multiplier = 6 if entry_multiplier == 3 else 3
    partner_product = product * 2 if entry_multiplier == 3 else product // 2
    entry_route = f"{entry_multiplier} × {base}"
    partner_route = f"{partner_multiplier} × {base}"

    digit_sum = sum(int(ch) for ch in str(product))
    odd_even_label = "even" if product % 2 == 0 else "odd"

    teach_now_vocab = [
        "product",
        "factor",
        "multiply",
        "times",
        "double",
        "doubling",
        "pattern",
        "sequence",
        "digit sum",
        "odd",
        "even",
        "divide",
        "inverse",
        "new product",
        "new route",
    ]

    introduce_if_needed = [
        "equal",
        "same",
        "fact",
        "compare",
        "before",
        "after",
        "family",
    ]

    delay_vocab = [
        "commutative",
        "factor family beyond the stage set",
        "route comparison beyond the interleaving link",
        "bridge hub",
        "compression hub",
    ]

    teacher_prompt_groups = [
        {
            "title": "Entry prompts",
            "items": [
                f"What product are we building when we say {entry_route}?",
                f"What is {entry_route}?",
                "So what is the product?",
                f"Is {product} a new product in this stage?",
            ],
        },
        {
            "title": "Pattern prompts",
            "items": [
                f"What do the digits in {product} add to?",
                f"Does {product} fit the 3× digit-sum cycle?",
                f"Is {product} odd or even?",
                f"What happens if we {'double' if entry_multiplier == 3 else 'halve'} {product}?",
                f"Which fact does that give us?",
                f"Why is {partner_product} connected to {product}?",
            ],
        },
        {
            "title": "Inverse prompts",
            "items": [
                f"If {entry_route} = {product}, what is {product} ÷ {entry_multiplier}?",
                f"What is {product} ÷ {base}?",
                "How does division help us get back out of the product?",
            ],
        },
        {
            "title": "Extension prompts",
            "items": [
                f"Which other new Stage F product belongs with {product}?",
                f"How does {partner_product} grow from {product}?" if entry_multiplier == 3 else f"How is {product} connected back to {partner_product}?",
                "Which fact shows that 6 is double 3?",
                "What is new in this stage: the product, the route, or both?",
            ],
        },
    ]

    example_question_groups = [
        {
            "title": "Build the product",
            "items": [
                f"Complete: {entry_route} = □",
                f"Circle the product in {entry_route} = {product}",
                f"Choose the correct statement: {entry_route} makes {product}",
            ],
        },
        {
            "title": "Interleaving and doubling",
            "items": [
                f"{'Double' if entry_multiplier == 3 else 'Halve'} {product}: □",
                f"Complete: {partner_route} = □",
                f"Match {entry_route} = {product} with {partner_route} = {partner_product}",
                f"Complete: {partner_product} = 2 × □" if entry_multiplier == 3 else f"Complete: {product} = 2 × □",
            ],
        },
        {
            "title": "Pattern questions",
            "items": [
                f"Complete: {' + '.join(ch for ch in str(product))} = □",
                f"Is {product} odd or even?",
                "Tick the true statement: 3× products alternate odd and even",
                "Tick the true statement: 6× products are always even",
            ],
        },
        {
            "title": "Inverse questions",
            "items": [
                f"Complete: {product} ÷ {entry_multiplier} = □",
                f"Complete: {product} ÷ {base} = □",
                f"Match {entry_route} = {product} to its division facts",
            ],
        },
        {
            "title": "Explain",
            "items": [
                f"Explain why {product} is a new Stage F product.",
                f"Explain how {partner_product} can be built from {product}." if entry_multiplier == 3 else f"Explain how {product} links back to {partner_product}.",
                f"Explain one division fact that comes from {product}.",
            ],
        },
    ]

    teacher_model = [
        f"{entry_route} = {product}",
        f"{partner_route} = {partner_product}",
        f"{partner_product} = 2 × {product}" if entry_multiplier == 3 else f"{product} = 2 × {partner_product}",
        "",
        f"The digits in {product} add to:",
        f"{' + '.join(ch for ch in str(product))} = {digit_sum}",
        "",
        f"So {product} fits the 3× digit-sum cycle.",
        "",
        f"{product} is {odd_even_label}, so it fits the 3× odd/even alternation." if entry_multiplier == 3 else f"{product} is even, so it fits the 6× always-even pattern.",
    ]

    return {
        "explanation_steps": [
            f"What is {entry_route}?",
            "So what is the product?",
            f"Is {product} a new product in Stage F?",
            f"If we {'double' if entry_multiplier == 3 else 'halve'} {product}, what do we get?",
            f"So what is {partner_route}?",
            f"What do the digits in {product} add to?",
            f"Is {product} odd or even?",
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
            f"Do not widen into broad route comparison across earlier stages until learners are secure with the entry route "
            f"{entry_route} = {product}, the interleaving link to {partner_product}, and the distinction between a new product and a new route."
        ),
        "lesson_aim": (
            f"Learners build the product {product} through the {entry_multiplier}× structure, recognise it as a genuinely new Stage F product, "
            f"connect it to {partner_product} through {'doubling' if entry_multiplier == 3 else 'the interleaving link'}, and link the product to its inverse division facts."
        ),
        "suggested_lesson_length": "15–20 minutes",
        "stage_pattern_bank": list(_STAGE_F_PATTERN_BANK),
        "stage_product_sequence": list(_STAGE_F_NEW_PRODUCTS),
        "teacher_model": teacher_model,
        "teacher_explanation_sentence": (
            f"We build {product} as {entry_route}, then use {'doubling to connect it to ' + str(partner_product) if entry_multiplier == 3 else 'the interleaving link back to ' + str(partner_product)}."
        ),
        "inverse_connection": [
            f"{entry_route} = {product}",
            f"{product} ÷ {entry_multiplier} = {base}",
            f"{product} ÷ {base} = {entry_multiplier}",
        ],
        "check_for_understanding": (
            f"Learners should be able to state {entry_route} = {product}, explain why {product} is a genuinely new Stage F product, "
            f"connect it to {partner_product} through {'doubling' if entry_multiplier == 3 else 'the interleaving relationship'}, and state the linked division facts."
        ),
        "support_text": (
            f"Use counters or arrays to show {entry_multiplier} groups of {base}. Then show that "
            f"{'doubling the product gives ' + str(partner_product) if entry_multiplier == 3 else str(product) + ' links back to ' + str(partner_product)}. "
            f"Keep the language simple: groups, double, product."
        ),
        "core_text": (
            f"Build {product} as {entry_route}, then connect it to {partner_product} through the Stage F interleaving link. "
            f"Teach the Stage F patterns through the product: new product / new route, 3× digit-sum cycle, odd/even behaviour, and inverse facts."
        ),
        "extension_text": (
            f"Extend from the focus product {product} to the full Stage F set: "
            f"{', '.join(str(value) for value in _STAGE_F_NEW_PRODUCTS)}. "
            f"Ask learners to compare {entry_route} = {product} and {partner_route} = {partner_product}. "
            f"Then ask them to identify what is new in Stage F, explain how {partner_product} is built from {product} or linked back to it, "
            f"check the digit-sum pattern, and compare odd/even behaviour in the 3× and 6× families."
        ),
        "teacher_quick_summary": (
            f"Today’s product is {product}. We first build it as {entry_route}. Then we connect it to {partner_product} "
            f"through the Stage F interleaving link, showing how the 3× and 6× families work together in this stage. "
            f"We also teach that {product} is a genuinely new product, that its digits add to {digit_sum}, "
            f"and that division facts help us move back out of the product."
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




def _is_stage_c_route(left: int, right: int) -> bool:
    return left == 5 or right == 5




def _is_stage_d_route(left: int, right: int) -> bool:
    return left == 9 or right == 9




def _is_stage_f_route(left: int, right: int) -> bool:
    return left in (3, 6) or right in (3, 6)




def _stage_c_base_value(left: int, right: int) -> int:
    return left if right == 5 else right




def _stage_d_base_value(left: int, right: int) -> int:
    return left if right == 9 else right




def _stage_f_base_value(left: int, right: int) -> int:
    if left in (3, 6):
        return right
    return left




def _format_instruction_intro_route(route: tuple[int, int]) -> str:
    left, right = route
    if left == 9 or right == 9:
        base = _stage_d_base_value(left, right)
        return f"9 × {base}"
    return _format_route(route)




def _format_route(route: tuple[int, int]) -> str:
    return f"{route[0]} × {route[1]}"
