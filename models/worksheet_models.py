from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Sequence


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

    def dict(self) -> dict:
        return {
            "stage": self.stage,
            "format_id": self.format_id,
            "tier": self.tier,
            "selection_scope": self.selection_scope,
            "selection_mode": self.selection_mode,
            "include_recap": self.include_recap,
            "recap_count": self.recap_count,
            "rotation_index": self.rotation_index,
        }

    def model_dump(self) -> dict:
        return self.dict()


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

    def __post_init__(self) -> None:
        for values in (self.selected_products, self.recap_products):
            for value in values:
                if not isinstance(value, int) or value <= 0:
                    raise ValueError("product values must be positive integers")

    def dict(self) -> dict:
        return {
            "stage": self.stage,
            "format_id": self.format_id,
            "tier": self.tier,
            "selection_scope": self.selection_scope,
            "selection_mode": self.selection_mode,
            "selected_products": self.selected_products,
            "recap_products": self.recap_products,
            "selection_reasons": self.selection_reasons,
            "vocab_supported": self.vocab_supported,
            "structural_tags": self.structural_tags,
        }

    def model_dump(self) -> dict:
        return self.dict()


@dataclass
class WorksheetQuestion:
    q_id: int
    prompt: str

    def dict(self) -> dict:
        return {
            "q_id": self.q_id,
            "prompt": self.prompt,
        }

    def model_dump(self) -> dict:
        return self.dict()


@dataclass
class WorksheetAnswer:
    q_id: int
    answer: str
    focus_tags: tuple[str, ...] = field(default_factory=tuple)
    teacher_note: str = ""
    vocab: tuple[str, ...] = field(default_factory=tuple)

    def dict(self) -> dict:
        return {
            "q_id": self.q_id,
            "answer": self.answer,
            "focus_tags": self.focus_tags,
            "teacher_note": self.teacher_note,
            "vocab": self.vocab,
        }

    def model_dump(self) -> dict:
        return self.dict()


@dataclass
class StudentWorksheet:
    questions: tuple[WorksheetQuestion, ...] = field(default_factory=tuple)

    def dict(self) -> dict:
        return {
            "questions": tuple(
                question.dict() if hasattr(question, "dict") else question
                for question in self.questions
            ),
        }

    def model_dump(self) -> dict:
        return self.dict()


@dataclass
class TeacherKey:
    answers: tuple[WorksheetAnswer, ...] = field(default_factory=tuple)

    def dict(self) -> dict:
        return {
            "answers": tuple(
                answer.dict() if hasattr(answer, "dict") else answer
                for answer in self.answers
            ),
        }

    def model_dump(self) -> dict:
        return self.dict()


@dataclass
class WorksheetBundle:
    selection: ProductSelectionResult
    student: StudentWorksheet
    teacher: TeacherKey

    def dict(self) -> dict:
        return {
            "selection": self.selection.dict() if hasattr(self.selection, "dict") else self.selection,
            "student": self.student.dict() if hasattr(self.student, "dict") else self.student,
            "teacher": self.teacher.dict() if hasattr(self.teacher, "dict") else self.teacher,
        }

    def model_dump(self) -> dict:
        return self.dict()


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
