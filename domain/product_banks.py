from __future__ import annotations

from typing import Dict, List, Tuple

# ============================================================
# TMK canonical product banks
# ============================================================

TMK_ALL_PRODUCTS: List[int] = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    12, 14, 15, 16, 18, 20, 21, 24, 25, 27,
    28, 30, 32, 35, 36, 40, 42, 45, 48, 49,
    50, 54, 56, 60, 63, 64, 70, 72, 80, 81,
    90, 100,
]

# ============================================================
# Canonical stage-new product banks
# ============================================================

STAGE_PRODUCT_BANKS: Dict[str, List[int]] = {
    "A": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "B": [20, 30, 40, 50, 60, 70, 80, 90, 100],
    "C": [15, 25, 35, 45],
    "D": [18, 27, 36, 54, 63, 72, 81],
    "E": [12, 14, 16, 24, 28, 32, 48, 56, 64],
    "F": [21, 42],
    "G": [49],
}

# ============================================================
# Cumulative stage banks
# ============================================================

STAGE_CUMULATIVE_BANKS: Dict[str, List[int]] = {
    "A": sorted(STAGE_PRODUCT_BANKS["A"]),
    "B": sorted(STAGE_PRODUCT_BANKS["A"] + STAGE_PRODUCT_BANKS["B"]),
    "C": sorted(STAGE_PRODUCT_BANKS["A"] + STAGE_PRODUCT_BANKS["B"] + STAGE_PRODUCT_BANKS["C"]),
    "D": sorted(STAGE_PRODUCT_BANKS["A"] + STAGE_PRODUCT_BANKS["B"] + STAGE_PRODUCT_BANKS["C"] + STAGE_PRODUCT_BANKS["D"]),
    "E": sorted(STAGE_PRODUCT_BANKS["A"] + STAGE_PRODUCT_BANKS["B"] + STAGE_PRODUCT_BANKS["C"] + STAGE_PRODUCT_BANKS["D"] + STAGE_PRODUCT_BANKS["E"]),
    "F": sorted(STAGE_PRODUCT_BANKS["A"] + STAGE_PRODUCT_BANKS["B"] + STAGE_PRODUCT_BANKS["C"] + STAGE_PRODUCT_BANKS["D"] + STAGE_PRODUCT_BANKS["E"] + STAGE_PRODUCT_BANKS["F"]),
    "G": sorted(TMK_ALL_PRODUCTS),
}

# ============================================================
# Recap family banks
# These are family-driven recap pools, not generic prior products.
# ============================================================

RECAP_FAMILY_BANKS: Dict[str, List[int]] = {
    "A": [],
    "B": [],
    "C": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
    "D": [9, 18, 27, 36, 45, 54, 63, 72, 81],
    "E": [2, 4, 8, 12, 14, 16, 20, 24, 28, 32, 40, 48, 56, 64, 80],
    "F": [3, 6, 9, 12, 18, 21, 24, 27, 30, 36, 42, 48, 54, 63, 72, 81],
    "G": [7, 14, 21, 28, 35, 42, 49, 56, 63, 70],
}

# ============================================================
# Structural banks
# ============================================================

MULTI_ROUTE_PRODUCTS: List[int] = [
    4, 6, 8, 9, 10,
    12, 16, 18, 20, 24,
    30, 36, 40,
]

SQUARE_PRODUCTS: List[int] = [
    1, 4, 9, 16, 25, 36, 49, 64, 81, 100,
]

DOUBLING_CHAIN_PRODUCTS: List[int] = [
    12, 14, 16, 24, 28, 32, 48, 56, 64,
]

DOUBLING_CHAIN_TRIPLES: List[Tuple[int, int, int]] = [
    (12, 24, 48),
    (14, 28, 56),
    (16, 32, 64),
]

SPECIAL_FOCUS_PRODUCTS: List[int] = [
    10, 25, 36, 42, 49, 64, 81, 100,
]

STAGE_BRIDGE_PRODUCTS: List[int] = [
    36, 42, 64,
]

CLOSURE_PRODUCTS: List[int] = [
    49,
]

# Optional richer banks for later use
BOUNDARY_FOCUS_PRODUCTS: List[int] = [
    36, 49, 64, 100,
]

BENCHMARK_PRODUCTS: List[int] = [
    10, 25, 45, 50, 90, 100,
]

COMPARISON_READY_PRODUCTS: List[int] = [
    12, 18, 24, 30, 36, 40, 42, 64,
]

SINGLE_ROUTE_PRODUCTS: List[int] = [
    p for p in TMK_ALL_PRODUCTS if p not in MULTI_ROUTE_PRODUCTS
]

# ============================================================
# Selector mode banks
# same_stage_products remains stage-specific and is handled by helper.
# ============================================================

NUMBER_TYPE_BANKS: Dict[str, List[int]] = {
    "multi_route_compare": MULTI_ROUTE_PRODUCTS,
    "multi_route_hub": MULTI_ROUTE_PRODUCTS,
    "square_or_special_focus": sorted(set(SQUARE_PRODUCTS + SPECIAL_FOCUS_PRODUCTS)),
    "square_product": SQUARE_PRODUCTS,
    "special_focus": SPECIAL_FOCUS_PRODUCTS,
    "doubling_chain": DOUBLING_CHAIN_PRODUCTS,
    "doubling_chain_product": DOUBLING_CHAIN_PRODUCTS,
    "stage_bridge": STAGE_BRIDGE_PRODUCTS,
    "closure_product": CLOSURE_PRODUCTS,
    "boundary_focus": BOUNDARY_FOCUS_PRODUCTS,
    "benchmark_product": BENCHMARK_PRODUCTS,
    "comparison_ready": COMPARISON_READY_PRODUCTS,
}

# ============================================================
# Curated stage triples
# These are curated worksheet/planner comparison sets.
# They are not the canonical banks themselves.
# ============================================================

CURATED_STAGE_TRIPLES: Dict[str, List[Tuple[int, int, int]]] = {
    "D": [
        (18, 27, 36),
        (36, 54, 72),
        (27, 36, 45),  # intentional cross-stage comparison
        (54, 63, 72),
    ],
    "E": [
        (12, 24, 48),
        (14, 28, 56),
        (16, 32, 64),
    ],
    "F": [
        (21, 24, 42),
        (21, 27, 42),
        (21, 30, 42),
        (21, 36, 42),
    ],
    "G": [
        (35, 42, 49),
        (36, 42, 49),
        (42, 49, 56),
    ],
}

# ============================================================
# Helper functions
# ============================================================

def products_for_stage(stage: str) -> List[int]:
    if stage not in STAGE_PRODUCT_BANKS:
        raise ValueError(f"Unknown stage: {stage}")
    return list(STAGE_PRODUCT_BANKS[stage])


def cumulative_products_for_stage(stage: str) -> List[int]:
    if stage not in STAGE_CUMULATIVE_BANKS:
        raise ValueError(f"Unknown stage: {stage}")
    return list(STAGE_CUMULATIVE_BANKS[stage])


def recap_products_for_stage(stage: str) -> List[int]:
    if stage not in RECAP_FAMILY_BANKS:
        raise ValueError(f"Unknown stage: {stage}")
    return list(RECAP_FAMILY_BANKS[stage])


def products_for_number_type(selection_mode: str, stage: str | None = None) -> List[int]:
    if selection_mode == "same_stage_products":
        if stage is None:
            raise ValueError("stage is required for same_stage_products")
        return products_for_stage(stage)

    if selection_mode not in NUMBER_TYPE_BANKS:
        raise ValueError(f"Unknown selection mode: {selection_mode}")

    return list(NUMBER_TYPE_BANKS[selection_mode])


def all_banks_summary() -> Dict[str, List[int] | Dict[str, List[int]]]:
    return {
        "TMK_ALL_PRODUCTS": TMK_ALL_PRODUCTS,
        "STAGE_PRODUCT_BANKS": STAGE_PRODUCT_BANKS,
        "STAGE_CUMULATIVE_BANKS": STAGE_CUMULATIVE_BANKS,
        "RECAP_FAMILY_BANKS": RECAP_FAMILY_BANKS,
        "MULTI_ROUTE_PRODUCTS": MULTI_ROUTE_PRODUCTS,
        "SQUARE_PRODUCTS": SQUARE_PRODUCTS,
        "DOUBLING_CHAIN_PRODUCTS": DOUBLING_CHAIN_PRODUCTS,
        "SPECIAL_FOCUS_PRODUCTS": SPECIAL_FOCUS_PRODUCTS,
        "STAGE_BRIDGE_PRODUCTS": STAGE_BRIDGE_PRODUCTS,
        "CLOSURE_PRODUCTS": CLOSURE_PRODUCTS,
    }

# ============================================================
# Validation
# ============================================================

def validate_product_banks() -> None:
    if len(TMK_ALL_PRODUCTS) != 42:
        raise ValueError(f"TMK_ALL_PRODUCTS should contain 42 products, found {len(TMK_ALL_PRODUCTS)}.")

    if len(set(TMK_ALL_PRODUCTS)) != len(TMK_ALL_PRODUCTS):
        raise ValueError("TMK_ALL_PRODUCTS contains duplicates.")

    stage_union = sorted(set(p for bank in STAGE_PRODUCT_BANKS.values() for p in bank))
    if stage_union != sorted(TMK_ALL_PRODUCTS):
        raise ValueError(
            "Union of STAGE_PRODUCT_BANKS does not match TMK_ALL_PRODUCTS.\n"
            f"Stage union: {stage_union}\n"
            f"TMK_ALL_PRODUCTS: {sorted(TMK_ALL_PRODUCTS)}"
        )

    named_banks: dict[str, List[int]] = {
        "MULTI_ROUTE_PRODUCTS": MULTI_ROUTE_PRODUCTS,
        "SQUARE_PRODUCTS": SQUARE_PRODUCTS,
        "DOUBLING_CHAIN_PRODUCTS": DOUBLING_CHAIN_PRODUCTS,
        "SPECIAL_FOCUS_PRODUCTS": SPECIAL_FOCUS_PRODUCTS,
        "STAGE_BRIDGE_PRODUCTS": STAGE_BRIDGE_PRODUCTS,
        "CLOSURE_PRODUCTS": CLOSURE_PRODUCTS,
        "BOUNDARY_FOCUS_PRODUCTS": BOUNDARY_FOCUS_PRODUCTS,
        "BENCHMARK_PRODUCTS": BENCHMARK_PRODUCTS,
        "COMPARISON_READY_PRODUCTS": COMPARISON_READY_PRODUCTS,
        "SINGLE_ROUTE_PRODUCTS": SINGLE_ROUTE_PRODUCTS,
    }

    for stage, bank in RECAP_FAMILY_BANKS.items():
        named_banks[f"RECAP_FAMILY_BANKS[{stage}]"] = bank

    for name, bank in named_banks.items():
        bad = [p for p in bank if p not in TMK_ALL_PRODUCTS]
        if bad:
            raise ValueError(f"{name} contains products outside TMK_ALL_PRODUCTS: {bad}")

    triple_products = sorted(set(p for triple in DOUBLING_CHAIN_TRIPLES for p in triple))
    if triple_products != sorted(DOUBLING_CHAIN_PRODUCTS):
        raise ValueError(
            "DOUBLING_CHAIN_TRIPLES do not match DOUBLING_CHAIN_PRODUCTS.\n"
            f"Triples give: {triple_products}\n"
            f"Bank gives: {sorted(DOUBLING_CHAIN_PRODUCTS)}"
        )

    for stage, triples in CURATED_STAGE_TRIPLES.items():
        for triple in triples:
            bad = [p for p in triple if p not in TMK_ALL_PRODUCTS]
            if bad:
                raise ValueError(
                    f"CURATED_STAGE_TRIPLES[{stage}] contains invalid products in triple {triple}: {bad}"
                )
