from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


# ============================================================
# Stage system
# ============================================================

StageId = Literal["A", "B", "C", "D", "E", "F", "G"]

SUPPORTED_STAGES: tuple[StageId, ...] = ("A", "B", "C", "D", "E", "F", "G")


def validate_stage(stage: StageId) -> None:
    if stage not in SUPPORTED_STAGES:
        raise ValueError(f"Invalid TMK stage '{stage}'.")


# ============================================================
# Product metadata record
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


# ============================================================
# Metadata validation
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
            raise ValueError(f"Factor pair values must be positive integers for product {record.product}")

    if record.route_profile not in {
        "single_route",
        "multi_route",
        "square_route",
    }:
        raise ValueError(
            f"Invalid route_profile '{record.route_profile}' for product {record.product}"
        )

    if record.hub_band not in {"low", "medium", "high"}:
        raise ValueError(
            f"Invalid hub_band '{record.hub_band}' for product {record.product}"
        )

    if not isinstance(record.family_tags, tuple):
        raise ValueError(f"family_tags must be tuple for product {record.product}")

    if not isinstance(record.structural_tags, tuple):
        raise ValueError(f"structural_tags must be tuple for product {record.product}")

    if not isinstance(record.vocab_tags, tuple):
        raise ValueError(f"vocab_tags must be tuple for product {record.product}")

    if not isinstance(record.known_routes_at_stage, tuple):
        raise ValueError(
            f"known_routes_at_stage must be tuple for product {record.product}"
        )


# ============================================================
# Worksheet selection system
# ============================================================

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
    "same_factor_family",
    "same_stage_products",
    "multi_route_compare",
    "doubling_chain",
    "interleave_compare",
    "square_or_special_focus",
]


# ============================================================
# Selection request / result
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
        self.selected_products = tuple(self.selected_products)
        self.recap_products = tuple(self.recap_products)
        self.selection_reasons = tuple(self.selection_reasons)
        self.vocab_supported = tuple(self.vocab_supported)
        self.structural_tags = tuple(self.structural_tags)

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


# ============================================================
# Validation helpers used by services
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


def validate_product_set_mode(mode: ProductSetMode) -> None:
    if mode not in _ONE_PRODUCT_MODES and mode not in _THREE_PRODUCT_MODES:
        raise ValueError(f"Unknown product selection mode: {mode}")


def validate_selection_request(request: ProductSelectionRequest) -> None:
    if request.selection_mode is not None:
        validate_product_set_mode(request.selection_mode)


def validate_selection_result(result: ProductSelectionResult) -> None:
    if result.format_id == "one_product_10":
        if len(result.selected_products) != 1:
            raise ValueError("one_product_10 requires exactly 1 selected product")
    elif result.format_id == "three_product_12":
        if len(result.selected_products) != 3:
            raise ValueError("three_product_12 requires exactly 3 selected products")


# ============================================================
# Legacy / compatibility aliases
# ============================================================

SelectionMode = ProductSetMode
NumberTypeSelectionMode = ProductSetMode
WorksheetSelectionMode = ProductSetMode
StageType = StageId
Stage = StageId
FormatId = WorksheetFormatId
TierId = WorksheetTier
ScopeId = SelectionScope
