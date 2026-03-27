from __future__ import annotations

from typing import Literal, Sequence

from pydantic import BaseModel, Field, root_validator, validator


# ============================================================
# Core TMK worksheet type aliases
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

ProductSetMode = Literal[
    # one-product modes
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
    # three-product modes
    "same_factor_family",
    "same_stage_products",
    "multi_route_compare",
    "doubling_chain",
    "interleave_compare",
    "square_or_special_focus",
]


# ============================================================
# Selection request / result models
# ============================================================

class ProductSelectionRequest(BaseModel):
    stage: StageId
    format_id: WorksheetFormatId
    tier: WorksheetTier
    selection_scope: SelectionScope

    selection_mode: ProductSetMode | None = None

    include_recap: bool = False
    recap_count: int = 0

    rotation_index: int = 0

    @validator("recap_count")
    def _validate_recap_count(cls, value: int) -> int:
        if value < 0:
            raise ValueError("recap_count cannot be negative")
        return value

    @validator("rotation_index")
    def _validate_rotation_index(cls, value: int) -> int:
        if value < 0:
            raise ValueError("rotation_index cannot be negative")
        return value

    @root_validator
    def _normalize_recap(cls, values: dict) -> dict:
        include_recap = values.get("include_recap", False)
        if not include_recap:
            values["recap_count"] = 0
        return values


class ProductSelectionResult(BaseModel):
    stage: StageId
    format_id: WorksheetFormatId
    tier: WorksheetTier
    selection_scope: SelectionScope
    selection_mode: ProductSetMode

    selected_products: tuple[int, ...] = Field(default_factory=tuple)
    recap_products: tuple[int, ...] = Field(default_factory=tuple)

    selection_reasons: tuple[str, ...] = Field(default_factory=tuple)
    vocab_supported: tuple[str, ...] = Field(default_factory=tuple)
    structural_tags: tuple[str, ...] = Field(default_factory=tuple)

    @validator("selected_products", "recap_products")
    def _validate_products_are_positive(cls, values: tuple[int, ...]) -> tuple[int, ...]:
        for value in values:
            if not isinstance(value, int) or value <= 0:
                raise ValueError("product values must be positive integers")
        return values


# ============================================================
# Worksheet payload models
# ============================================================

class WorksheetQuestion(BaseModel):
    q_id: int
    prompt: str


class WorksheetAnswer(BaseModel):
    q_id: int
    answer: str
    focus_tags: tuple[str, ...] = Field(default_factory=tuple)
    teacher_note: str = ""
    vocab: tuple[str, ...] = Field(default_factory=tuple)


class StudentWorksheet(BaseModel):
    questions: tuple[WorksheetQuestion, ...] = Field(default_factory=tuple)


class TeacherKey(BaseModel):
    answers: tuple[WorksheetAnswer, ...] = Field(default_factory=tuple)


class WorksheetBundle(BaseModel):
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
# Public validation helpers used by services
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
                f"Selection mode '{request.selection_mode}' is not allowed for format '{request.format_id}'."
            )


def validate_selection_result(result: ProductSelectionResult) -> None:
    if result.format_id == "one_product_10":
        if len(result.selected_products) != 1:
            raise ValueError("one_product_10 requires exactly 1 selected product")
    elif result.format_id == "three_product_12":
        if len(result.selected_products) != 3:
            raise ValueError("three_product_12 requires exactly 3 selected products")
    else:
        raise ValueError(f"Unknown worksheet format: {result.format_id}")

    if len(set(result.selected_products)) != len(result.selected_products):
        raise ValueError("selected_products contains duplicates")

    if len(set(result.recap_products)) != len(result.recap_products):
        raise ValueError("recap_products contains duplicates")

    if result.selection_mode not in _ALLOWED_MODES_BY_FORMAT[result.format_id]:
        raise ValueError(
            f"Selection mode '{result.selection_mode}' is not valid for format '{result.format_id}'."
        )


# ============================================================
# Small utility helpers
# ============================================================

def allowed_modes_for_format(format_id: WorksheetFormatId) -> tuple[ProductSetMode, ...]:
    if format_id not in _ALLOWED_MODES_BY_FORMAT:
        raise ValueError(f"Unknown worksheet format: {format_id}")
    return _ALLOWED_MODES_BY_FORMAT[format_id]


def is_one_product_mode(mode: ProductSetMode) -> bool:
    return mode in _ONE_PRODUCT_MODES


def is_three_product_mode(mode: ProductSetMode) -> bool:
    return mode in _THREE_PRODUCT_MODES


def coerce_questions(items: Sequence[dict | WorksheetQuestion]) -> tuple[WorksheetQuestion, ...]:
    questions: list[WorksheetQuestion] = []
    for item in items:
        if isinstance(item, WorksheetQuestion):
            questions.append(item)
        else:
            questions.append(WorksheetQuestion(**item))
    return tuple(questions)


def coerce_answers(items: Sequence[dict | WorksheetAnswer]) -> tuple[WorksheetAnswer, ...]:
    answers: list[WorksheetAnswer] = []
    for item in items:
        if isinstance(item, WorksheetAnswer):
            answers.append(item)
        else:
            answers.append(WorksheetAnswer(**item))
    return tuple(answers)
