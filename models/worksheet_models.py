from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Sequence


# ============================================================
# Core identifiers used across the TMK system
# ============================================================

StageId = Literal["A", "B", "C", "D", "E", "F", "G"]

WorksheetFormatId = Literal[
    "one_product_10",
    "three_product_12",
]

WorksheetTier = Literal[
    "Support",
    "Core",
    "Extension",
]

SelectionScope = Literal[
    "new_only",
    "available_mixed",
    "hybrid",
]


# ============================================================
# Product selection modes
# ============================================================

ProductSetMode = Literal[
    # single product
    "single_hub",
    "multi_route_hub",
    "square_product",
    "special_focus",
    "doubling_chain_product",
    "stage_bridge",
    "closure_product",
    "boundary_focus",
    "benchmark_product",
    "comparison_ready",

    # multi product
    "same_factor_family",
    "same_stage_products",
    "multi_route_compare",
    "doubling_chain",
    "interleave_compare",
    "square_or_special_focus",
]


# ============================================================
# Selection request
# ============================================================

@dataclass
class ProductSelectionRequest:
    stage: StageId
    format_id: WorksheetFormatId
    tier: WorksheetTier
    selection_scope: SelectionScope

    selection_mode: ProductSetMode | None = None

    include_recap: bool = False
    recap_count: int = 0
    rotation_index: int = 0

    def __post_init__(self) -> None:

        if self.recap_count < 0:
            raise ValueError("recap_count cannot be negative")

        if self.rotation_index < 0:
            raise ValueError("rotation_index cannot be negative")

        if not self.include_recap:
            self.recap_count = 0


# ============================================================
# Selection result
# ============================================================

@dataclass
class ProductSelectionResult:

    stage: StageId
    format_id: WorksheetFormatId
    tier: WorksheetTier
    selection_scope: SelectionScope
    selection_mode: ProductSetMode

    selected_products: tuple[int, ...] = field(default_factory=tuple)
    recap_products: tuple[int, ...] = field(default_factory=tuple)

    selection_reasons: tuple[str, ...] = field(default_factory=tuple)
    vocab_supported: tuple[str, ...] = field(default_factory=tuple)
    structural_tags: tuple[str, ...] = field(default_factory=tuple)


# ============================================================
# Worksheet content structures
# ============================================================

@dataclass
class WorksheetQuestion:
    q_id: int
    prompt: str


@dataclass
class WorksheetAnswer:
    q_id: int
    answer: str
    focus_tags: tuple[str, ...] = field(default_factory=tuple)
    teacher_note: str = ""
    vocab: tuple[str, ...] = field(default_factory=tuple)


@dataclass
class StudentWorksheet:
    questions: tuple[WorksheetQuestion, ...] = field(default_factory=tuple)


@dataclass
class TeacherKey:
    answers: tuple[WorksheetAnswer, ...] = field(default_factory=tuple)


@dataclass
class WorksheetBundle:
    selection: ProductSelectionResult
    student: StudentWorksheet
    teacher: TeacherKey


# ============================================================
# Allowed modes by worksheet format
# ============================================================

_ONE_PRODUCT_MODES: tuple[ProductSetMode, ...] = (
    "single_hub",
    "multi_route_hub",
    "square_product",
    "special_focus",
    "doubling_chain_product",
    "stage_bridge",
    "closure_product",
    "boundary_focus",
    "benchmark_product",
    "comparison_ready",
)

_THREE_PRODUCT_MODES: tuple[ProductSetMode, ...] = (
    "same_factor_family",
    "same_stage_products",
    "multi_route_compare",
    "doubling_chain",
    "interleave_compare",
    "square_or_special_focus",
)

_ALLOWED_MODES_BY_FORMAT: dict[WorksheetFormatId, tuple[ProductSetMode, ...]] = {
    "one_product_10": _ONE_PRODUCT_MODES,
    "three_product_12": _THREE_PRODUCT_MODES,
}


# ============================================================
# Validation helpers
# ============================================================

def validate_product_set_mode(mode: ProductSetMode) -> None:
    if mode not in _ONE_PRODUCT_MODES and mode not in _THREE_PRODUCT_MODES:
        raise ValueError(f"Unknown product selection mode: {mode}")


def validate_selection_request(request: ProductSelectionRequest) -> None:

    if request.format_id not in _ALLOWED_MODES_BY_FORMAT:
        raise ValueError(f"Unknown worksheet format: {request.format_id}")

    if request.selection_mode is not None:

        validate_product_set_mode(request.selection_mode)

        allowed = _ALLOWED_MODES_BY_FORMAT[request.format_id]

        if request.selection_mode not in allowed:
            raise ValueError(
                f"Selection mode '{request.selection_mode}' "
                f"is not allowed for format '{request.format_id}'."
            )


def validate_selection_result(result: ProductSelectionResult) -> None:

    if result.format_id == "one_product_10":
        if len(result.selected_products) != 1:
            raise ValueError("one_product_10 requires exactly 1 selected product")

    elif result.format_id == "three_product_12":
        if len(result.selected_products) != 3:
            raise ValueError("three_product_12 requires exactly 3 selected products")


# ============================================================
# Utility helpers
# ============================================================

def allowed_modes_for_format(format_id: WorksheetFormatId) -> tuple[ProductSetMode, ...]:

    if format_id not in _ALLOWED_MODES_BY_FORMAT:
        raise ValueError(f"Unknown worksheet format: {format_id}")

    return _ALLOWED_MODES_BY_FORMAT[format_id]


def coerce_questions(
    items: Sequence[dict | WorksheetQuestion],
) -> tuple[WorksheetQuestion, ...]:

    questions: list[WorksheetQuestion] = []

    for item in items:

        if isinstance(item, WorksheetQuestion):
            questions.append(item)

        else:
            questions.append(WorksheetQuestion(**item))

    return tuple(questions)


def coerce_answers(
    items: Sequence[dict | WorksheetAnswer],
) -> tuple[WorksheetAnswer, ...]:

    answers: list[WorksheetAnswer] = []

    for item in items:

        if isinstance(item, WorksheetAnswer):
            answers.append(item)

        else:
            answers.append(WorksheetAnswer(**item))

    return tuple(answers)
