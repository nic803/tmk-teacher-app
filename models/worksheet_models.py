from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Mapping, Tuple


# ============================================================
# Canonical TMK type aliases
# ============================================================

StageId = Literal["A", "B", "C", "D", "E", "F", "G"]
Tier = Literal["Support", "Core", "Extension"]

QuestionSection = Literal[
    "product_first",
    "ways_in",
    "ways_out",
    "another_way",
    "belongs",
    "error_repair",
    "final_explanation",
]

AnswerKind = Literal[
    "number",
    "route",
    "route_list",
    "boolean",
    "text",
    "choice",
    "sort",
]

QuizFormat = Literal[
    # light / app-safe interaction formats
    "circle",
    "tick",
    "yes_no",
    "match",
    "fill_box",
    "choose",
    "sort",
    "tick_all",
    "label_from_options",
    # stage_vocabulary.py currently appears to use these as well
    "open_response",
    "write_number",
    "write_equation",
    "write_word",
    "label_route",
    "route_sort",
]


# ============================================================
# Supported value registries
# ============================================================

SUPPORTED_STAGES: tuple[StageId, ...] = ("A", "B", "C", "D", "E", "F", "G")

SUPPORTED_TIERS: tuple[Tier, ...] = ("Support", "Core", "Extension")

SUPPORTED_QUESTION_SECTIONS: tuple[QuestionSection, ...] = (
    "product_first",
    "ways_in",
    "ways_out",
    "another_way",
    "belongs",
    "error_repair",
    "final_explanation",
)

SUPPORTED_ANSWER_KINDS: tuple[AnswerKind, ...] = (
    "number",
    "route",
    "route_list",
    "boolean",
    "text",
    "choice",
    "sort",
)

SUPPORTED_QUIZ_FORMATS: tuple[QuizFormat, ...] = (
    "circle",
    "tick",
    "yes_no",
    "match",
    "fill_box",
    "choose",
    "sort",
    "tick_all",
    "label_from_options",
    "open_response",
    "write_number",
    "write_equation",
    "write_word",
    "label_route",
    "route_sort",
)


# ============================================================
# Validators
# ============================================================

def validate_stage(stage: StageId) -> None:
    if stage not in SUPPORTED_STAGES:
        raise ValueError(f"Invalid stage '{stage}'.")


def validate_tier(tier: Tier) -> None:
    if tier not in SUPPORTED_TIERS:
        raise ValueError(f"Invalid tier '{tier}'.")


def validate_question_section(section: QuestionSection) -> None:
    if section not in SUPPORTED_QUESTION_SECTIONS:
        raise ValueError(f"Invalid question section '{section}'.")


def validate_answer_kind(answer_kind: AnswerKind) -> None:
    if answer_kind not in SUPPORTED_ANSWER_KINDS:
        raise ValueError(f"Invalid answer kind '{answer_kind}'.")


def validate_quiz_format(quiz_format: QuizFormat) -> None:
    if quiz_format not in SUPPORTED_QUIZ_FORMATS:
        raise ValueError(f"Invalid quiz format '{quiz_format}'.")


# ============================================================
# Stage vocabulary model
# This is the model required by domain/stage_vocabulary.py
# ============================================================

@dataclass(frozen=True)
class StageVocabularyRecord:
    """
    Teacher-facing vocabulary guidance for a stage.

    app_safe_words:
        short prompt-safe words suitable for UI / worksheets

    teacher_words:
        broader teacher-side vocabulary for notes / packs

    quiz_formats:
        preferred interaction formats for stage-level activity design
    """

    stage: StageId
    app_safe_words: Tuple[str, ...] = ()
    teacher_words: Tuple[str, ...] = ()
    avoid_words: Tuple[str, ...] = ()
    quiz_formats: Tuple[QuizFormat, ...] = ()

    def __post_init__(self) -> None:
        validate_stage(self.stage)
        validate_stage_vocabulary_record(self)


def validate_stage_vocabulary_record(record: StageVocabularyRecord) -> None:
    validate_stage(record.stage)

    for value in record.app_safe_words:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("app_safe_words must contain non-empty strings.")

    for value in record.teacher_words:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("teacher_words must contain non-empty strings.")

    for value in record.avoid_words:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("avoid_words must contain non-empty strings.")

    for fmt in record.quiz_formats:
        validate_quiz_format(fmt)


# ============================================================
# Worksheet models
# These support worksheet_engine.py and related app code.
# ============================================================

@dataclass(frozen=True)
class WorksheetQuestion:
    id: int
    section: QuestionSection
    prompt_key: str
    answer_kind: AnswerKind
    prompt_data: Mapping[str, Any] = field(default_factory=dict)
    answer_data: Mapping[str, Any] = field(default_factory=dict)
    pattern_ids: Tuple[str, ...] = ()
    msvwa_tags: Tuple[str, ...] = ()
    quiz_format: QuizFormat = "open_response"

    def __post_init__(self) -> None:
        if self.id <= 0:
            raise ValueError("Question id must be positive.")
        validate_question_section(self.section)
        validate_answer_kind(self.answer_kind)
        validate_quiz_format(self.quiz_format)

        if not self.prompt_key or not isinstance(self.prompt_key, str):
            raise ValueError("prompt_key must be a non-empty string.")

        if not isinstance(self.pattern_ids, tuple):
            raise ValueError("pattern_ids must be a tuple of strings.")
        if not isinstance(self.msvwa_tags, tuple):
            raise ValueError("msvwa_tags must be a tuple of strings.")

        for tag in self.pattern_ids:
            if not isinstance(tag, str) or not tag.strip():
                raise ValueError("pattern_ids must contain non-empty strings.")

        for tag in self.msvwa_tags:
            if not isinstance(tag, str) or not tag.strip():
                raise ValueError("msvwa_tags must contain non-empty strings.")


@dataclass(frozen=True)
class WorksheetTeacherKey:
    answers: Tuple[Mapping[str, Any], ...] = ()
    pattern_ids: Tuple[str, ...] = ()
    memory_cue_ids: Tuple[str, ...] = ()
    notes: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for item in self.pattern_ids:
            if not isinstance(item, str) or not item.strip():
                raise ValueError("pattern_ids must contain non-empty strings.")
        for item in self.memory_cue_ids:
            if not isinstance(item, str) or not item.strip():
                raise ValueError("memory_cue_ids must contain non-empty strings.")
        for item in self.notes:
            if not isinstance(item, str) or not item.strip():
                raise ValueError("notes must contain non-empty strings.")


@dataclass(frozen=True)
class Worksheet:
    product: int
    stage: StageId
    tier: Tier
    questions: Tuple[WorksheetQuestion, ...]
    teacher_key: WorksheetTeacherKey

    def __post_init__(self) -> None:
        if self.product <= 0:
            raise ValueError("Worksheet product must be positive.")
        validate_stage(self.stage)
        validate_tier(self.tier)

        if len(self.questions) != 10:
            raise ValueError(
                f"Worksheet must contain exactly 10 questions; found {len(self.questions)}."
            )

        seen_ids = [q.id for q in self.questions]
        if len(set(seen_ids)) != len(seen_ids):
            raise ValueError("Worksheet question ids must be unique.")


# ============================================================
# Convenience helpers
# ============================================================

def supported_stage_ids() -> Tuple[StageId, ...]:
    return SUPPORTED_STAGES


def supported_tiers() -> Tuple[Tier, ...]:
    return SUPPORTED_TIERS


def supported_quiz_formats() -> Tuple[QuizFormat, ...]:
    return SUPPORTED_QUIZ_FORMATS
