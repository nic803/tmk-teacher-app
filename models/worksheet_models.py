from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Mapping, Tuple


# ============================================================
# Stage system
# ============================================================

StageId = Literal["A", "B", "C", "D", "E", "F", "G"]
StageType = StageId
Stage = StageId

SUPPORTED_STAGES: tuple[StageId, ...] = ("A", "B", "C", "D", "E", "F", "G")


def validate_stage(stage: StageId) -> None:
    if stage not in SUPPORTED_STAGES:
        raise ValueError(f"Invalid TMK stage '{stage}'.")


# ============================================================
# App / worksheet vocabulary interaction formats
# ============================================================

QuizFormat = Literal[
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
]

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


def validate_quiz_format(quiz_format: QuizFormat) -> None:
    if quiz_format not in SUPPORTED_QUIZ_FORMATS:
        raise ValueError(f"Invalid quiz format '{quiz_format}'.")


# ============================================================
# Flexible compatibility base
# ============================================================

class FlexibleRecord:
    def __init__(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            setattr(self, key, self._normalize_field(key, value))
        self._apply_defaults()

    def _normalize_field(self, key: str, value: Any) -> Any:
        tuple_like_fields = {
            "factor_pairs",
            "family_tags",
            "structural_tags",
            "vocab_tags",
            "known_routes_at_stage",
            "new_vocab",
            "available_vocab",
            "required_vocab_focus",
            "preferred_quiz_formats",
            "preferred_vocab_task_types",
            "example_child_friendly_questions",
            "selected_products",
            "recap_products",
            "supported_vocab",
            "structural_tags_out",
            "selection_reasons",
        }

        if key in tuple_like_fields:
            if value is None:
                return ()
            if isinstance(value, tuple):
                return value
            if isinstance(value, list):
                return tuple(value)
            if isinstance(value, set):
                return tuple(value)
            return (value,)

        return value

    def _apply_defaults(self) -> None:
        defaults: dict[str, Any] = {
            "stage": "",
            "stage_id": "",
            "stage_introduced": "",
            "label": "",
            "name": "",
            "notes": "",
            "intro_family": "",
            "route_profile": "",
            "hub_band": "",
            "factor_pairs": (),
            "family_tags": (),
            "structural_tags": (),
            "vocab_tags": (),
            "known_routes_at_stage": (),
            "new_vocab": (),
            "available_vocab": (),
            "required_vocab_focus": (),
            "preferred_quiz_formats": (),
            "preferred_vocab_task_types": (),
            "example_child_friendly_questions": (),
            "product": 0,
            "has_multiple_routes": False,
            "is_square": False,
            "has_factor_7": False,
            "selected_products": (),
            "recap_products": (),
            "supported_vocab": (),
            "structural_tags_out": (),
            "selection_reasons": (),
        }

        for key, value in defaults.items():
            if not hasattr(self, key):
                setattr(self, key, value)

    def dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

    def model_dump(self) -> dict[str, Any]:
        return self.dict()


# ============================================================
# Domain records
# ============================================================

@dataclass
class ProductMetadataRecord:
    product: int
    stage_introduced: StageId
    intro_family: str
    factor_pairs: tuple[tuple[int, int], ...] | list[tuple[int, int]]
    family_tags: tuple[str, ...] | list[str]
    structural_tags: tuple[str, ...] | list[str]
    vocab_tags: tuple[str, ...] | list[str]
    route_profile: str
    hub_band: str
    has_multiple_routes: bool
    known_routes_at_stage: tuple[tuple[int, int], ...] | list[tuple[int, int]]
    is_square: bool
    has_factor_7: bool
    notes: str

    def __post_init__(self) -> None:
        self.factor_pairs = tuple(tuple(pair) for pair in self.factor_pairs)
        self.family_tags = tuple(self.family_tags)
        self.structural_tags = tuple(self.structural_tags)
        self.vocab_tags = tuple(self.vocab_tags)
        self.known_routes_at_stage = tuple(tuple(pair) for pair in self.known_routes_at_stage)


@dataclass
class StageVocabularyRecord:
    stage: StageId
    new_vocab: tuple[str, ...] | list[str]
    available_vocab: tuple[str, ...] | list[str]
    required_vocab_focus: tuple[str, ...] | list[str]
    preferred_quiz_formats: tuple[QuizFormat, ...] | list[QuizFormat]
    preferred_vocab_task_types: tuple[str, ...] | list[str]
    example_child_friendly_questions: tuple[str, ...] | list[str]

    def __post_init__(self) -> None:
        self.new_vocab = tuple(self.new_vocab)
        self.available_vocab = tuple(self.available_vocab)
        self.required_vocab_focus = tuple(self.required_vocab_focus)
        self.preferred_quiz_formats = tuple(self.preferred_quiz_formats)
        self.preferred_vocab_task_types = tuple(self.preferred_vocab_task_types)
        self.example_child_friendly_questions = tuple(self.example_child_friendly_questions)


class ProductMetadataSummary(FlexibleRecord):
    pass


# ============================================================
# Domain validation
# ============================================================

def validate_product_metadata_record(record: ProductMetadataRecord) -> None:
    if not isinstance(record.product, int) or record.product <= 0:
        raise ValueError("product must be a positive integer")

    validate_stage(record.stage_introduced)

    if not record.factor_pairs:
        raise ValueError(f"Product {record.product} must define factor_pairs")

    for pair in record.factor_pairs:
        if not isinstance(pair, tuple) or len(pair) != 2:
            raise ValueError(f"Invalid factor pair for product {record.product}")
        if not all(isinstance(value, int) and value > 0 for value in pair):
            raise ValueError(
                f"Factor pair values must be positive integers for product {record.product}"
            )

    if record.route_profile not in {"single_route", "multi_route", "square_route"}:
        raise ValueError(
            f"Invalid route_profile '{record.route_profile}' for product {record.product}"
        )

    if record.hub_band not in {"low", "medium", "high"}:
        raise ValueError(
            f"Invalid hub_band '{record.hub_band}' for product {record.product}"
        )


def validate_stage_vocabulary_record(record: StageVocabularyRecord) -> None:
    validate_stage(record.stage)

    if not isinstance(record.new_vocab, tuple):
        raise ValueError(f"new_vocab must be tuple for stage {record.stage}")

    if not isinstance(record.available_vocab, tuple):
        raise ValueError(f"available_vocab must be tuple for stage {record.stage}")

    if not isinstance(record.required_vocab_focus, tuple):
        raise ValueError(f"required_vocab_focus must be tuple for stage {record.stage}")

    if not isinstance(record.preferred_quiz_formats, tuple):
        raise ValueError(f"preferred_quiz_formats must be tuple for stage {record.stage}")

    if not isinstance(record.preferred_vocab_task_types, tuple):
        raise ValueError(f"preferred_vocab_task_types must be tuple for stage {record.stage}")

    if not isinstance(record.example_child_friendly_questions, tuple):
        raise ValueError(
            f"example_child_friendly_questions must be tuple for stage {record.stage}"
        )

    for fmt in record.preferred_quiz_formats:
        validate_quiz_format(fmt)


# ============================================================
# Worksheet selection system
# ============================================================

WorksheetFormatId = Literal[
    "one_product_10",
    "three_product_12",
]
FormatId = WorksheetFormatId

WorksheetTier = Literal[
    "Support",
    "Core",
    "Extension",
]
TierId = WorksheetTier

ProductSetMode = Literal[
    "single_hub",
    "same_factor_family",
    "same_stage_products",
    "multi_route_compare",
    "doubling_chain",
    "interleave_compare",
    "square_or_special_focus",
]

SelectionScope = Literal[
    "stage_only",
    "hybrid",
    "available_mixed",
]

SUPPORTED_WORKSHEET_FORMATS: tuple[WorksheetFormatId, ...] = (
    "one_product_10",
    "three_product_12",
)

SUPPORTED_WORKSHEET_TIERS: tuple[WorksheetTier, ...] = (
    "Support",
    "Core",
    "Extension",
)

SUPPORTED_PRODUCT_SET_MODES: tuple[ProductSetMode, ...] = (
    "single_hub",
    "same_factor_family",
    "same_stage_products",
    "multi_route_compare",
    "doubling_chain",
    "interleave_compare",
    "square_or_special_focus",
)

SUPPORTED_SELECTION_SCOPES: tuple[SelectionScope, ...] = (
    "stage_only",
    "hybrid",
    "available_mixed",
)


def validate_worksheet_format_id(format_id: WorksheetFormatId) -> None:
    if format_id not in SUPPORTED_WORKSHEET_FORMATS:
        raise ValueError(f"Invalid worksheet format '{format_id}'.")


def validate_worksheet_tier(tier: WorksheetTier) -> None:
    if tier not in SUPPORTED_WORKSHEET_TIERS:
        raise ValueError(f"Invalid worksheet tier '{tier}'.")


def validate_product_set_mode(mode: ProductSetMode) -> None:
    if mode not in SUPPORTED_PRODUCT_SET_MODES:
        raise ValueError(f"Invalid product set mode '{mode}'.")


def validate_selection_scope(scope: SelectionScope) -> None:
    if scope not in SUPPORTED_SELECTION_SCOPES:
        raise ValueError(f"Invalid selection scope '{scope}'.")


@dataclass(frozen=True)
class ProductSelectionRequest:
    stage: StageId
    format_id: WorksheetFormatId
    tier: WorksheetTier
    selection_scope: SelectionScope
    selection_mode: ProductSetMode | None = None
    include_recap: bool = True
    recap_count: int = 0
    rotation_seed: int = 0

    def __post_init__(self) -> None:
        validate_selection_request(self)


@dataclass(frozen=True)
class ProductSelectionResult:
    stage: StageId
    format_id: WorksheetFormatId
    tier: WorksheetTier
    selection_scope: SelectionScope
    selection_mode: ProductSetMode
    selected_products: tuple[int, ...]
    recap_products: tuple[int, ...] = ()
    supported_vocab: tuple[str, ...] = ()
    structural_tags: tuple[str, ...] = ()
    selection_reasons: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        validate_selection_result(self)


def validate_selection_request(request: ProductSelectionRequest) -> None:
    validate_stage(request.stage)
    validate_worksheet_format_id(request.format_id)
    validate_worksheet_tier(request.tier)
    validate_selection_scope(request.selection_scope)

    if request.selection_mode is not None:
        validate_product_set_mode(request.selection_mode)

    if not isinstance(request.include_recap, bool):
        raise ValueError("include_recap must be bool")

    if not isinstance(request.recap_count, int) or request.recap_count < 0:
        raise ValueError("recap_count must be a non-negative integer")

    if not isinstance(request.rotation_seed, int):
        raise ValueError("rotation_seed must be an integer")


def validate_selection_result(result: ProductSelectionResult) -> None:
    validate_stage(result.stage)
    validate_worksheet_format_id(result.format_id)
    validate_worksheet_tier(result.tier)
    validate_selection_scope(result.selection_scope)
    validate_product_set_mode(result.selection_mode)

    if not isinstance(result.selected_products, tuple):
        raise ValueError("selected_products must be a tuple")

    if not result.selected_products:
        raise ValueError("selected_products must not be empty")

    for product in result.selected_products:
        if not isinstance(product, int) or product <= 0:
            raise ValueError("selected_products must contain positive integers")

    if not isinstance(result.recap_products, tuple):
        raise ValueError("recap_products must be a tuple")

    for product in result.recap_products:
        if not isinstance(product, int) or product <= 0:
            raise ValueError("recap_products must contain positive integers")

    if not isinstance(result.supported_vocab, tuple):
        raise ValueError("supported_vocab must be a tuple")

    if not isinstance(result.structural_tags, tuple):
        raise ValueError("structural_tags must be a tuple")

    if not isinstance(result.selection_reasons, tuple):
        raise ValueError("selection_reasons must be a tuple")


# ============================================================
# Worksheet engine models
# ============================================================

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


def validate_question_section(section: QuestionSection) -> None:
    if section not in SUPPORTED_QUESTION_SECTIONS:
        raise ValueError(f"Invalid question section '{section}'.")


def validate_answer_kind(answer_kind: AnswerKind) -> None:
    if answer_kind not in SUPPORTED_ANSWER_KINDS:
        raise ValueError(f"Invalid answer kind '{answer_kind}'.")


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


@dataclass(frozen=True)
class WorksheetTeacherKey:
    answers: Tuple[Mapping[str, Any], ...] = ()
    pattern_ids: Tuple[str, ...] = ()
    memory_cue_ids: Tuple[str, ...] = ()
    notes: Tuple[str, ...] = ()


@dataclass(frozen=True)
class Worksheet:
    product: int
    stage: StageId
    tier: WorksheetTier
    questions: Tuple[WorksheetQuestion, ...]
    teacher_key: WorksheetTeacherKey

    def __post_init__(self) -> None:
        if self.product <= 0:
            raise ValueError("Worksheet product must be positive.")
        validate_stage(self.stage)
        validate_worksheet_tier(self.tier)
        if len(self.questions) != 10:
            raise ValueError(
                f"Worksheet must contain exactly 10 questions; found {len(self.questions)}."
            )
