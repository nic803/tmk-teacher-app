from __future__ import annotations

from typing import Final

from models.worksheet_models import (
    QuizFormat,
    StageId,
    StageVocabularyRecord,
    SUPPORTED_STAGES,
    validate_quiz_format,
    validate_stage,
    validate_stage_vocabulary_record,
)


STAGE_VOCABULARY: Final[dict[StageId, StageVocabularyRecord]] = {
    "A": StageVocabularyRecord(
        stage="A",
        new_vocab=(
            "equal",
            "same",
            "identity",
            "multiply",
            "times",
            "fact",
        ),
        available_vocab=(
            "equal",
            "same",
            "identity",
            "multiply",
            "times",
            "fact",
        ),
        required_vocab_focus=(
            "identity",
            "same",
            "times",
        ),
        preferred_quiz_formats=(
            "circle",
            "tick",
            "yes_no",
            "match",
            "fill_box",
        ),
        preferred_vocab_task_types=(
            "recognise_identity_fact",
            "spot_same_value",
            "complete_identity_fact",
            "match_number_to_1x_fact",
        ),
        example_child_friendly_questions=(
            "Circle the one that stays the same.",
            "Tick the 1× fact.",
            "Yes or no: 1 × 6 = 6",
            "Match the number to its 1× fact.",
        ),
    ),
    "B": StageVocabularyRecord(
        stage="B",
        new_vocab=(
            "product",
            "zero",
            "ten times",
            "place value",
            "groups of ten",
            "scale",
        ),
        available_vocab=(
            "equal",
            "same",
            "identity",
            "multiply",
            "times",
            "fact",
            "product",
            "zero",
            "ten times",
            "place value",
            "groups of ten",
            "scale",
        ),
        required_vocab_focus=(
            "product",
            "ten times",
            "place value",
        ),
        preferred_quiz_formats=(
            "circle",
            "tick",
            "match",
            "choose",
            "fill_box",
        ),
        preferred_vocab_task_types=(
            "recognise_product",
            "match_10x_fact_to_product",
            "identify_scaled_number",
            "complete_10x_fact",
        ),
        example_child_friendly_questions=(
            "Circle the product.",
            "Match each 10× fact to its product.",
            "Tick the numbers that are 10 times bigger.",
            "Fill the box: 10 × 7 = □",
        ),
    ),
    "C": StageVocabularyRecord(
        stage="C",
        new_vocab=(
            "commutative",
            "turn around",
            "half",
            "inverse",
            "factor",
        ),
        available_vocab=(
            "equal",
            "same",
            "identity",
            "multiply",
            "times",
            "fact",
            "product",
            "zero",
            "ten times",
            "place value",
            "groups of ten",
            "scale",
            "commutative",
            "turn around",
            "half",
            "inverse",
            "factor",
        ),
        required_vocab_focus=(
            "commutative",
            "half",
            "inverse",
            "factor",
        ),
        preferred_quiz_formats=(
            "circle",
            "tick",
            "yes_no",
            "match",
            "fill_box",
        ),
        preferred_vocab_task_types=(
            "recognise_commutative_pair",
            "match_turned_around_fact",
            "identify_half_of_ten_structure",
            "use_inverse_division",
        ),
        example_child_friendly_questions=(
            "Circle the commutative pair.",
            "Match each multiplication to its turned-around fact.",
            "Yes or no: 3 × 5 and 5 × 3 make the same product.",
            "Tick the fact that shows half of 10.",
        ),
    ),
    "D": StageVocabularyRecord(
        stage="D",
        new_vocab=(
            "sequence",
            "pattern",
            "missing number",
            "digit sum",
            "subtract one",
        ),
        available_vocab=(
            "equal",
            "same",
            "identity",
            "multiply",
            "times",
            "fact",
            "product",
            "zero",
            "ten times",
            "place value",
            "groups of ten",
            "scale",
            "commutative",
            "turn around",
            "half",
            "inverse",
            "factor",
            "sequence",
            "pattern",
            "missing number",
            "digit sum",
            "subtract one",
        ),
        required_vocab_focus=(
            "sequence",
            "pattern",
            "missing number",
        ),
        preferred_quiz_formats=(
            "circle",
            "tick",
            "match",
            "choose",
            "fill_box",
        ),
        preferred_vocab_task_types=(
            "recognise_9x_pattern",
            "complete_sequence",
            "choose_missing_number",
            "match_fact_to_inverse",
        ),
        example_child_friendly_questions=(
            "Circle the product in each 9× fact.",
            "Tick the next number in the 9× pattern.",
            "Match each 9× fact to its division fact.",
            "Choose the missing number: 9 × □ = 54",
        ),
    ),
    "E": StageVocabularyRecord(
        stage="E",
        new_vocab=(
            "double",
            "doubling",
            "pair",
            "repeated addition",
            "skip-count",
            "even",
        ),
        available_vocab=(
            "equal",
            "same",
            "identity",
            "multiply",
            "times",
            "fact",
            "product",
            "zero",
            "ten times",
            "place value",
            "groups of ten",
            "scale",
            "commutative",
            "turn around",
            "half",
            "inverse",
            "factor",
            "sequence",
            "pattern",
            "missing number",
            "digit sum",
            "subtract one",
            "double",
            "doubling",
            "pair",
            "repeated addition",
            "skip-count",
            "even",
        ),
        required_vocab_focus=(
            "double",
            "doubling",
            "pair",
            "repeated addition",
            "skip-count",
            "even",
        ),
        preferred_quiz_formats=(
            "circle",
            "tick",
            "yes_no",
            "match",
            "sort",
            "fill_box",
        ),
        preferred_vocab_task_types=(
            "recognise_double",
            "match_number_to_double",
            "sort_doubles_not_doubles",
            "complete_double",
            "identify_skip_count_pattern",
        ),
        example_child_friendly_questions=(
            "Circle the double.",
            "Match each number to its double.",
            "Sort into doubles / not doubles.",
            "Fill the box: double 6 is □",
        ),
    ),
    "F": StageVocabularyRecord(
        stage="F",
        new_vocab=(
            "fact family",
            "same family",
            "different family",
            "link",
            "another way",
            "new product",
        ),
        available_vocab=(
            "equal",
            "same",
            "identity",
            "multiply",
            "times",
            "fact",
            "product",
            "zero",
            "ten times",
            "place value",
            "groups of ten",
            "scale",
            "commutative",
            "turn around",
            "half",
            "inverse",
            "factor",
            "sequence",
            "pattern",
            "missing number",
            "digit sum",
            "subtract one",
            "double",
            "doubling",
            "pair",
            "repeated addition",
            "skip-count",
            "even",
            "fact family",
            "same family",
            "different family",
            "link",
            "another way",
            "new product",
        ),
        required_vocab_focus=(
            "fact family",
            "same family",
            "different family",
            "link",
            "another way",
        ),
        preferred_quiz_formats=(
            "tick_all",
            "match",
            "sort",
            "choose",
            "fill_box",
        ),
        preferred_vocab_task_types=(
            "group_same_family_facts",
            "match_multiplication_to_division",
            "identify_linked_facts",
            "recognise_another_way",
        ),
        example_child_friendly_questions=(
            "Tick all the facts in the same family.",
            "Match the multiplication to the division facts.",
            "Sort these into same family / different family.",
            "Circle the new product.",
        ),
    ),
    "G": StageVocabularyRecord(
        stage="G",
        new_vocab=(
            "square",
            "squared",
            "square number",
            "area",
            "perimeter",
            "side length",
        ),
        available_vocab=(
            "equal",
            "same",
            "identity",
            "multiply",
            "times",
            "fact",
            "product",
            "zero",
            "ten times",
            "place value",
            "groups of ten",
            "scale",
            "commutative",
            "turn around",
            "half",
            "inverse",
            "factor",
            "sequence",
            "pattern",
            "missing number",
            "digit sum",
            "subtract one",
            "double",
            "doubling",
            "pair",
            "repeated addition",
            "skip-count",
            "even",
            "fact family",
            "same family",
            "different family",
            "link",
            "another way",
            "new product",
            "square",
            "squared",
            "square number",
            "area",
            "perimeter",
            "side length",
        ),
        required_vocab_focus=(
            "square",
            "squared",
            "square number",
            "area",
            "perimeter",
        ),
        preferred_quiz_formats=(
            "circle",
            "tick",
            "match",
            "choose",
            "fill_box",
            "label_from_options",
        ),
        preferred_vocab_task_types=(
            "recognise_square_fact",
            "match_square_number_to_multiplication",
            "identify_square_number",
            "complete_square_fact",
            "label_square_parts",
        ),
        example_child_friendly_questions=(
            "Circle the square fact.",
            "Tick the square number.",
            "Match each square number to its multiplication.",
            "Fill the box: 7 × 7 = □",
        ),
    ),
}


def get_stage_vocabulary(stage: StageId) -> StageVocabularyRecord:
    validate_stage(stage)
    return STAGE_VOCABULARY[stage]


def new_vocab(stage: StageId) -> tuple[str, ...]:
    return get_stage_vocabulary(stage).new_vocab


def available_vocab(stage: StageId) -> tuple[str, ...]:
    return get_stage_vocabulary(stage).available_vocab


def required_vocab_focus(stage: StageId) -> tuple[str, ...]:
    return get_stage_vocabulary(stage).required_vocab_focus


def preferred_quiz_formats(stage: StageId) -> tuple[QuizFormat, ...]:
    return get_stage_vocabulary(stage).preferred_quiz_formats


def preferred_vocab_task_types(stage: StageId) -> tuple[str, ...]:
    return get_stage_vocabulary(stage).preferred_vocab_task_types


def example_child_friendly_questions(stage: StageId) -> tuple[str, ...]:
    return get_stage_vocabulary(stage).example_child_friendly_questions


def stage_vocab_contains(stage: StageId, word: str) -> bool:
    normalized = word.strip().lower()
    return normalized in {item.lower() for item in available_vocab(stage)}


def words_missing_from_stage(stage: StageId, words: tuple[str, ...]) -> tuple[str, ...]:
    available = {item.lower() for item in available_vocab(stage)}
    missing: list[str] = []
    for word in words:
        if word.strip().lower() not in available:
            missing.append(word)
    return tuple(missing)


def supports_quiz_format(stage: StageId, quiz_format: QuizFormat) -> bool:
    validate_stage(stage)
    validate_quiz_format(quiz_format)
    return quiz_format in preferred_quiz_formats(stage)


def validate_stage_vocabulary_system() -> None:
    actual_stages = set(STAGE_VOCABULARY.keys())
    expected_stages = set(SUPPORTED_STAGES)
    if actual_stages != expected_stages:
        raise ValueError(
            f"Stage vocabulary registry must contain exactly {expected_stages}. "
            f"Found {actual_stages}."
        )

    cumulative_words: set[str] = set()

    for stage in SUPPORTED_STAGES:
        record = get_stage_vocabulary(stage)
        validate_stage_vocabulary_record(record)

        stage_new = {word.lower() for word in record.new_vocab}
        stage_available = {word.lower() for word in record.available_vocab}
        stage_required = {word.lower() for word in record.required_vocab_focus}

        if not stage_new:
            raise ValueError(f"Stage '{stage}' must define at least one new vocabulary word.")

        if not stage_new.issubset(stage_available):
            missing = stage_new - stage_available
            raise ValueError(
                f"Stage '{stage}' new_vocab must be included in available_vocab. Missing: {missing}"
            )

        if not stage_required.issubset(stage_available):
            missing = stage_required - stage_available
            raise ValueError(
                f"Stage '{stage}' required_vocab_focus must be included in available_vocab. Missing: {missing}"
            )

        if not cumulative_words.issubset(stage_available):
            missing = cumulative_words - stage_available
            raise ValueError(
                f"Stage '{stage}' available_vocab must be cumulative. Missing prior words: {missing}"
            )

        cumulative_words = set(stage_available)

        for quiz_format in record.preferred_quiz_formats:
            validate_quiz_format(quiz_format)

        if not record.preferred_vocab_task_types:
            raise ValueError(
                f"Stage '{stage}' must define preferred_vocab_task_types."
            )

        if not record.example_child_friendly_questions:
            raise ValueError(
                f"Stage '{stage}' must define example_child_friendly_questions."
            )

        for prompt in record.example_child_friendly_questions:
            if not prompt.strip():
                raise ValueError(
                    f"Stage '{stage}' contains an empty example child-friendly question."
                )

            forbidden_fragments = (
                "What does ",
                "What is ",
                "Which stage",
                "Does this belong",
                "TMK world",
            )
            if any(fragment.lower() in prompt.lower() for fragment in forbidden_fragments):
                raise ValueError(
                    f"Stage '{stage}' example prompt violates worksheet vocabulary rules: '{prompt}'"
                )


validate_stage_vocabulary_system()
