from __future__ import annotations

from dataclasses import dataclass
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

@dataclass(frozen=True)
class ProductMetadataRecord:
    product: int
    stage_introduced: StageId
    intro_family: str

    factor_pairs: tuple[tuple[int, int], ...]

    family_tags: tuple[str, ...]
    structural_tags: tuple[str, ...]
    vocab_tags: tuple[str, ...]

    route_profile: str
    hub_band: str

    has_multiple_routes: bool
    known_routes_at_stage: tuple[tuple[int, int], ...]

    is_square: bool
    has_factor_7: bool

    notes: str


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
        if len(pair) != 2:
            raise ValueError(f"Invalid factor pair for product {record.product}")

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
