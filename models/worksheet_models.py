from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional, Tuple


StageId = Literal["A", "B", "C", "D", "E", "F", "G"]
WorksheetTier = Literal["Support", "Core", "Extension"]

WorksheetFormatId = Literal[
    "one_product_10",
    "three_product_12",
]

SelectionScope = Literal[
    "new_only",
    "available_mixed",
    "hybrid",
]

ProductSetMode = Literal[
    "single_hub",
    "same_factor_family",
    "same_stage_products",
    "multi_route_compare",
    "doubling_chain",
    "interleave_compare",
    "square_or_special_focus",
]

WorksheetItemFamily = Literal[
    "product_recognition",
    "route_in",
    "missing_factor",
    "another_way",
    "compare_routes",
    "route_out",
    "check_match",
    "correct_incorrect",
    "error_repair",
    "structural_grouping",
    "final_explanation",
]

QuizFormat = Literal[
    "circle",
    "tick",
    "yes_no",
    "tick_all",
    "match",
    "sort",
    "choose",
    "fill_box",
    "label_from_options",
]

MSVWATag = Literal["M", "S", "V", "W", "A"]


@dataclass(frozen=True)
class ProductSelectionRequest:
    stage: StageId
    format_id: WorksheetFormatId
    tier: WorksheetTier
    selection_scope: SelectionScope
    include_recap: bool = False
    recap_count: int = 0
    selection_mode: Optional[ProductSetMode] = None


@dataclass(frozen=True)
class ProductSelectionResult:
    stage: StageId
    format_id: WorksheetFormatId
    tier: WorksheetTier
    selection_scope: SelectionScope
    selection_mode: ProductSetMode
    selected_products: Tuple[int, ...]
    recap_products: Tuple[int, ...]
    selection_reasons: Tuple[str, ...]
    vocab_supported: Tuple[str, ...]
    structural_tags: Tuple[str, ...]


@dataclass(frozen=True)
class PlannedWorksheetItem:
    q_id: int
    family: WorksheetItemFamily
    quiz_format: QuizFormat
    target_product: int
    related_products: Tuple[int, ...] = ()
    prompt_stem: str = ""
    answer: str = ""
    vocabulary_words: Tuple[str, ...] = ()
    msvwa_tags: Tuple[MSVWATag, ...] = ()
    teacher_note: str = ""
    bloom_tag: Optional[str] = None
    metadata: Tuple[Tuple[str, str], ...] = ()


@dataclass(frozen=True)
class WorksheetPlan:
    stage: StageId
    tier: WorksheetTier
    format_id: WorksheetFormatId
    selection_scope: SelectionScope
    selection_mode: ProductSetMode
    selected_products: Tuple[int, ...]
    recap_products: Tuple[int, ...]
    items: Tuple[PlannedWorksheetItem, ...]
    stage_new_vocab: Tuple[str, ...]
    stage_available_vocab: Tuple[str, ...]
    required_vocab_focus: Tuple[str, ...]
    metadata: Tuple[Tuple[str, str], ...] = ()


@dataclass(frozen=True)
class StudentWorksheetItem:
    q_id: int
    prompt: str


@dataclass(frozen=True)
class StudentWorksheet:
    stage: StageId
    tier: WorksheetTier
    format_id: WorksheetFormatId
    selected_products: Tuple[int, ...]
    questions: Tuple[StudentWorksheetItem, ...]
    metadata: Tuple[Tuple[str, str], ...] = ()


@dataclass(frozen=True)
class TeacherAnswerEntry:
    q_id: int
    answer: str
    msvwa_tags: Tuple[MSVWATag, ...]
    note: str
    vocabulary_words: Tuple[str, ...] = ()
    bloom_tag: Optional[str] = None


@dataclass(frozen=True)
class TeacherWorksheet:
    stage: StageId
    tier: WorksheetTier
    format_id: WorksheetFormatId
    selected_products: Tuple[int, ...]
    answers: Tuple[TeacherAnswerEntry, ...]
    selection_reasons: Tuple[str, ...] = ()
    vocab_supported: Tuple[str, ...] = ()
    metadata: Tuple[Tuple[str, str], ...] = ()


@dataclass(frozen=True)
class WorksheetBundle:
    student: StudentWorksheet
    teacher: TeacherWorksheet
    plan: WorksheetPlan
    selection: ProductSelectionResult


@dataclass(frozen=True)
class StageVocabularyRecord:
    stage: StageId
    new_vocab: Tuple[str, ...]
    available_vocab: Tuple[str, ...]
    required_vocab_focus: Tuple[str, ...]
    preferred_quiz_formats: Tuple[QuizFormat, ...]
    preferred_vocab_task_types: Tuple[str, ...]
    example_child_friendly_questions: Tuple[str, ...]


@dataclass(frozen=True)
class ProductMetadataRecord:
    product: int
    stage_introduced: StageId
    intro_family: str
    factor_pairs: Tuple[Tuple[int, int], ...]
    family_tags: Tuple[str, ...]
    structural_tags: Tuple[str, ...]
    vocab_tags: Tuple[str, ...]
    route_profile: Literal["single_route", "multi_route", "square_route"]
    hub_band: Literal["low", "medium", "high"]
    has_multiple_routes: bool
    known_routes_at_stage: Tuple[Tuple[int, int], ...]
    is_square: bool
    has_factor_7: bool
    notes: str


@dataclass(frozen=True)
class WorksheetValidationResult:
    is_valid: bool
    errors: Tuple[str, ...] = ()
    warnings: Tuple[str, ...] = ()


FORBIDDEN_PUPIL_ITEM_TYPES: Tuple[str, ...] = (
    "stage_membership",
    "stage_introduction",
    "curriculum_placement",
    "TMK_world_membership",
    "system_belonging",
    "dictionary_definition_questions",
)

APPROVED_PUPIL_ITEM_FAMILIES: Tuple[WorksheetItemFamily, ...] = (
    "product_recognition",
    "route_in",
    "missing_factor",
    "another_way",
    "compare_routes",
    "route_out",
    "check_match",
    "correct_incorrect",
    "error_repair",
    "structural_grouping",
    "final_explanation",
)

APPROVED_QUIZ_FORMATS: Tuple[QuizFormat, ...] = (
    "circle",
    "tick",
    "yes_no",
    "tick_all",
    "match",
    "sort",
    "choose",
    "fill_box",
    "label_from_options",
)

SUPPORTED_WORKSHEET_FORMATS: Tuple[WorksheetFormatId, ...] = (
    "one_product_10",
    "three_product_12",
)

SUPPORTED_SELECTION_SCOPES: Tuple[SelectionScope, ...] = (
    "new_only",
    "available_mixed",
    "hybrid",
)

SUPPORTED_PRODUCT_SET_MODES: Tuple[ProductSetMode, ...] = (
    "single_hub",
    "same_factor_family",
    "same_stage_products",
    "multi_route_compare",
    "doubling_chain",
    "interleave_compare",
    "square_or_special_focus",
)

SUPPORTED_TIERS: Tuple[WorksheetTier, ...] = (
    "Support",
    "Core",
    "Extension",
)

SUPPORTED_STAGES: Tuple[StageId, ...] = (
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
)

SUPPORTED_MSVWA_TAGS: Tuple[MSVWATag, ...] = (
    "M",
    "S",
    "V",
    "W",
    "A",
)


def expected_question_count(format_id: WorksheetFormatId) -> int:
    if format_id == "one_product_10":
        return 10
    if format_id == "three_product_12":
        return 12
    raise ValueError(f"Unsupported worksheet format: {format_id}")


def validate_stage(stage: str) -> None:
    if stage not in SUPPORTED_STAGES:
        raise ValueError(
            f"Unsupported stage '{stage}'. Expected one of {SUPPORTED_STAGES}."
        )


def validate_tier(tier: str) -> None:
    if tier not in SUPPORTED_TIERS:
        raise ValueError(
            f"Unsupported tier '{tier}'. Expected one of {SUPPORTED_TIERS}."
        )


def validate_format_id(format_id: str) -> None:
    if format_id not in SUPPORTED_WORKSHEET_FORMATS:
        raise ValueError(
            f"Unsupported worksheet format '{format_id}'. "
            f"Expected one of {SUPPORTED_WORKSHEET_FORMATS}."
        )


def validate_selection_scope(selection_scope: str) -> None:
    if selection_scope not in SUPPORTED_SELECTION_SCOPES:
        raise ValueError(
            f"Unsupported selection scope '{selection_scope}'. "
            f"Expected one of {SUPPORTED_SELECTION_SCOPES}."
        )


def validate_product_set_mode(mode: str) -> None:
    if mode not in SUPPORTED_PRODUCT_SET_MODES:
        raise ValueError(
            f"Unsupported product set mode '{mode}'. "
            f"Expected one of {SUPPORTED_PRODUCT_SET_MODES}."
        )


def validate_item_family(family: str) -> None:
    if family not in APPROVED_PUPIL_ITEM_FAMILIES:
        raise ValueError(
            f"Unsupported worksheet item family '{family}'. "
            f"Expected one of {APPROVED_PUPIL_ITEM_FAMILIES}."
        )


def validate_quiz_format(quiz_format: str) -> None:
    if quiz_format not in APPROVED_QUIZ_FORMATS:
        raise ValueError(
            f"Unsupported quiz format '{quiz_format}'. "
            f"Expected one of {APPROVED_QUIZ_FORMATS}."
        )


def validate_msvwa_tags(tags: Tuple[str, ...]) -> None:
    if not tags:
        raise ValueError("Each teacher answer item must include at least one MSVWA tag.")

    if len(tags) > 3:
        raise ValueError("Each teacher answer item must include at most three MSVWA tags.")

    for tag in tags:
        if tag not in SUPPORTED_MSVWA_TAGS:
            raise ValueError(
                f"Unsupported MSVWA tag '{tag}'. Expected one of {SUPPORTED_MSVWA_TAGS}."
            )


def validate_selection_request(request: ProductSelectionRequest) -> None:
    validate_stage(request.stage)
    validate_tier(request.tier)
    validate_format_id(request.format_id)
    validate_selection_scope(request.selection_scope)

    if request.selection_mode is not None:
        validate_product_set_mode(request.selection_mode)

    if request.recap_count < 0:
        raise ValueError("recap_count must be 0 or greater.")

    if not request.include_recap and request.recap_count != 0:
        raise ValueError(
            "recap_count must be 0 when include_recap is False."
        )


def validate_selection_result(result: ProductSelectionResult) -> None:
    validate_stage(result.stage)
    validate_tier(result.tier)
    validate_format_id(result.format_id)
    validate_selection_scope(result.selection_scope)
    validate_product_set_mode(result.selection_mode)

    expected_count = 1 if result.format_id == "one_product_10" else 3
    if len(result.selected_products) != expected_count:
        raise ValueError(
            f"Format '{result.format_id}' requires exactly {expected_count} selected "
            f"product(s). Found {len(result.selected_products)}."
        )

    if len(set(result.selected_products)) != len(result.selected_products):
        raise ValueError("Selected products must be distinct.")

    if len(set(result.recap_products)) != len(result.recap_products):
        raise ValueError("Recap products must be distinct.")


def validate_planned_item(item: PlannedWorksheetItem) -> None:
    if item.q_id < 1:
        raise ValueError("Worksheet item ids must start at 1.")

    validate_item_family(item.family)
    validate_quiz_format(item.quiz_format)

    if item.target_product <= 0:
        raise ValueError("target_product must be a positive integer.")

    if not item.prompt_stem:
        raise ValueError(f"Worksheet item {item.q_id} is missing prompt_stem.")

    if item.answer in ("", None):
        raise ValueError(f"Worksheet item {item.q_id} is missing answer.")

    validate_msvwa_tags(item.msvwa_tags)


def validate_worksheet_plan(plan: WorksheetPlan) -> None:
    validate_stage(plan.stage)
    validate_tier(plan.tier)
    validate_format_id(plan.format_id)
    validate_selection_scope(plan.selection_scope)
    validate_product_set_mode(plan.selection_mode)

    expected_count = expected_question_count(plan.format_id)
    if len(plan.items) != expected_count:
        raise ValueError(
            f"Worksheet plan for format '{plan.format_id}' must contain exactly "
            f"{expected_count} items. Found {len(plan.items)}."
        )

    actual_ids = tuple(item.q_id for item in plan.items)
    expected_ids = tuple(range(1, expected_count + 1))
    if actual_ids != expected_ids:
        raise ValueError(
            f"Worksheet plan item ids must be sequential {expected_ids}. "
            f"Found {actual_ids}."
        )

    for item in plan.items:
        validate_planned_item(item)

    if not any(item.family == "route_in" for item in plan.items):
        raise ValueError("Every worksheet must contain at least one route_in item.")

    if not any(item.family == "route_out" for item in plan.items):
        raise ValueError("Every worksheet must contain at least one route_out item.")

    vocab_item_count = sum(1 for item in plan.items if item.vocabulary_words)
    if vocab_item_count < 1:
        raise ValueError(
            "Every worksheet must contain at least one vocabulary-bearing item."
        )

    if plan.stage not in SUPPORTED_STAGES:
        raise ValueError(f"Unsupported plan stage '{plan.stage}'.")

    if plan.format_id == "one_product_10" and len(plan.selected_products) != 1:
        raise ValueError("one_product_10 plans must contain exactly one selected product.")

    if plan.format_id == "three_product_12" and len(plan.selected_products) != 3:
        raise ValueError("three_product_12 plans must contain exactly three selected products.")


def validate_student_worksheet(worksheet: StudentWorksheet) -> None:
    validate_stage(worksheet.stage)
    validate_tier(worksheet.tier)
    validate_format_id(worksheet.format_id)

    expected_count = expected_question_count(worksheet.format_id)
    if len(worksheet.questions) != expected_count:
        raise ValueError(
            f"Student worksheet for format '{worksheet.format_id}' must contain "
            f"{expected_count} questions. Found {len(worksheet.questions)}."
        )

    actual_ids = tuple(item.q_id for item in worksheet.questions)
    expected_ids = tuple(range(1, expected_count + 1))
    if actual_ids != expected_ids:
        raise ValueError(
            f"Student worksheet question ids must be sequential {expected_ids}. "
            f"Found {actual_ids}."
        )

    for question in worksheet.questions:
        if not question.prompt:
            raise ValueError(f"Student worksheet question {question.q_id} is empty.")


def validate_teacher_entry(entry: TeacherAnswerEntry) -> None:
    if entry.q_id < 1:
        raise ValueError("Teacher answer ids must start at 1.")

    if not entry.answer:
        raise ValueError(f"Teacher answer entry {entry.q_id} is missing answer.")

    if not entry.note:
        raise ValueError(f"Teacher answer entry {entry.q_id} is missing note.")

    validate_msvwa_tags(entry.msvwa_tags)


def validate_teacher_worksheet(worksheet: TeacherWorksheet) -> None:
    validate_stage(worksheet.stage)
    validate_tier(worksheet.tier)
    validate_format_id(worksheet.format_id)

    expected_count = expected_question_count(worksheet.format_id)
    if len(worksheet.answers) != expected_count:
        raise ValueError(
            f"Teacher worksheet for format '{worksheet.format_id}' must contain "
            f"{expected_count} answers. Found {len(worksheet.answers)}."
        )

    actual_ids = tuple(item.q_id for item in worksheet.answers)
    expected_ids = tuple(range(1, expected_count + 1))
    if actual_ids != expected_ids:
        raise ValueError(
            f"Teacher worksheet answer ids must be sequential {expected_ids}. "
            f"Found {actual_ids}."
        )

    for answer in worksheet.answers:
        validate_teacher_entry(answer)


def validate_stage_vocabulary_record(record: StageVocabularyRecord) -> None:
    validate_stage(record.stage)

    for quiz_format in record.preferred_quiz_formats:
        validate_quiz_format(quiz_format)

    if not record.available_vocab:
        raise ValueError(
            f"Stage vocabulary record for stage '{record.stage}' must define available_vocab."
        )

    if not record.required_vocab_focus:
        raise ValueError(
            f"Stage vocabulary record for stage '{record.stage}' must define required_vocab_focus."
        )


def validate_product_metadata_record(record: ProductMetadataRecord) -> None:
    validate_stage(record.stage_introduced)

    if record.product <= 0:
        raise ValueError("Product metadata must use a positive product value.")

    if not record.factor_pairs:
        raise ValueError(
            f"Product metadata for {record.product} must define factor_pairs."
        )

    if record.route_profile not in ("single_route", "multi_route", "square_route"):
        raise ValueError(
            f"Invalid route_profile '{record.route_profile}' for product {record.product}."
        )

    if record.hub_band not in ("low", "medium", "high"):
        raise ValueError(
            f"Invalid hub_band '{record.hub_band}' for product {record.product}."
        )

    if record.has_multiple_routes and len(record.known_routes_at_stage) < 2:
        raise ValueError(
            f"Product {record.product} is marked has_multiple_routes=True but does not "
            f"define at least two known routes."
        )

    if record.is_square and not any(a == b for a, b in record.factor_pairs):
        raise ValueError(
            f"Product {record.product} is marked as square but no square factor pair exists."
        )

    if record.has_factor_7 and not any(7 in pair for pair in record.factor_pairs):
        raise ValueError(
            f"Product {record.product} is marked has_factor_7=True but factor pair does not include 7."
        )


def validate_worksheet_bundle(bundle: WorksheetBundle) -> None:
    validate_selection_result(bundle.selection)
    validate_worksheet_plan(bundle.plan)
    validate_student_worksheet(bundle.student)
    validate_teacher_worksheet(bundle.teacher)
