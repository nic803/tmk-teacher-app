from __future__ import annotations

from typing import Dict, List, Tuple

# ============================================================
# TMK canonical product banks
# ============================================================

# Full set of 42 distinct TMK products in the bounded 10×10 system
TMK_ALL_PRODUCTS: List[int] = [
    1,2,3,4,5,6,7,8,9,10,
    12,14,15,16,18,20,21,24,25,27,
    28,30,32,35,36,40,42,45,48,49,
    50,54,56,60,63,64,70,72,80,81,
    90,100
]

# ============================================================
# Stage product banks
# These are the canonical "new product" banks by stage
# ============================================================

STAGE_PRODUCT_BANKS: Dict[str, List[int]] = {

    # Stage A — Identity & Base anchors
    "A": [1,2,3,4,5,6,7,8,9,10],

    # Stage B — Pure scaling (10× structure)
    "B": [20,30,40,50,60,70,80,90,100],

    # Stage C — Midpoints & halves (5×)
    "C": [15,25,35,45],

    # Stage D — Nine structure
    "D": [18,27,36,54,63,72,81],

    # Stage E — Doubling chains
    "E": [12,14,16,24,28,32,48,56,64],

    # Stage F — Interleaving
    "F": [21,42],

    # Stage G — Closure
    "G": [49],
}

# ============================================================
# Multi-route products
# These have more than one multiplication route
# ============================================================

MULTI_ROUTE_PRODUCTS: List[int] = [
    4,6,8,9,10,
    12,16,18,20,24,
    30,36,40
]

# ============================================================
# Square products
# ============================================================

SQUARE_PRODUCTS: List[int] = [
    1,4,9,16,25,36,49,64,81,100
]

# ============================================================
# Doubling-chain products (Stage E)
# ============================================================

DOUBLING_CHAIN_PRODUCTS: List[int] = [
    12,14,16,24,28,32,48,56,64
]

DOUBLING_CHAIN_TRIPLES: List[Tuple[int,int,int]] = [

    # 3 → 6 → 12
    (12,24,48),

    # 7 doubling chain
    (14,28,56),

    # square doubling chain
    (16,32,64)
]

# ============================================================
# Special focus products
# Structural landmarks in the TMK system
# ============================================================

SPECIAL_FOCUS_PRODUCTS: List[int] = [
    10,25,36,42,49,64,81,100
]

# ============================================================
# RECAP FAMILY BANKS
# These drive recap worksheet pools
# ============================================================

RECAP_FAMILY_BANKS: Dict[str, List[int]] = {

    # Stage C recap – 5× structure
    "C": [5,10,15,20,25,30,35,40,45,50],

    # Stage D recap – 9× structure
    "D": [9,18,27,36,45,54,63,72,81],

    # Stage E recap – 2× / 4× / 8× structure
    "E": [
        2,4,8,
        12,14,16,
        20,24,28,
        32,40,48,
        56,64,80
    ],

    # Stage F recap – 3× / 6× family
    "F": [
        3,6,9,
        12,18,
        21,24,27,30,
        36,42,48,54,
        63,72,81
    ],

    # Stage G recap – 7× closure
    "G": [
        7,14,21,28,35,42,49,56,63,70
    ]
}

# ============================================================
# Stage cumulative banks
# ============================================================

STAGE_CUMULATIVE_BANKS: Dict[str, List[int]] = {

    "A": sorted(STAGE_PRODUCT_BANKS["A"]),

    "B": sorted(
        STAGE_PRODUCT_BANKS["A"]
        + STAGE_PRODUCT_BANKS["B"]
    ),

    "C": sorted(
        STAGE_PRODUCT_BANKS["A"]
        + STAGE_PRODUCT_BANKS["B"]
        + STAGE_PRODUCT_BANKS["C"]
    ),

    "D": sorted(
        STAGE_PRODUCT_BANKS["A"]
        + STAGE_PRODUCT_BANKS["B"]
        + STAGE_PRODUCT_BANKS["C"]
        + STAGE_PRODUCT_BANKS["D"]
    ),

    "E": sorted(
        STAGE_PRODUCT_BANKS["A"]
        + STAGE_PRODUCT_BANKS["B"]
        + STAGE_PRODUCT_BANKS["C"]
        + STAGE_PRODUCT_BANKS["D"]
        + STAGE_PRODUCT_BANKS["E"]
    ),

    "F": sorted(
        STAGE_PRODUCT_BANKS["A"]
        + STAGE_PRODUCT_BANKS["B"]
        + STAGE_PRODUCT_BANKS["C"]
        + STAGE_PRODUCT_BANKS["D"]
        + STAGE_PRODUCT_BANKS["E"]
        + STAGE_PRODUCT_BANKS["F"]
    ),

    "G": sorted(TMK_ALL_PRODUCTS)
}

# ============================================================
# Selector mode banks
# ============================================================

NUMBER_TYPE_BANKS: Dict[str, List[int]] = {

    "multi_route_compare": MULTI_ROUTE_PRODUCTS,

    "square_or_special_focus":
        sorted(set(SQUARE_PRODUCTS + SPECIAL_FOCUS_PRODUCTS)),

    "doubling_chain": DOUBLING_CHAIN_PRODUCTS,
}

# ============================================================
# Curated stage triples
# (comparison sets for worksheet generation)
# ============================================================

CURATED_STAGE_TRIPLES: Dict[str, List[Tuple[int,int,int]]] = {

    "D": [

        (18,27,36),

        (36,54,72),

        # cross-stage comparison (allowed)
        (27,36,45),

        (54,63,72)
    ],

    "E": [

        (12,24,48),

        (14,28,56),

        (16,32,64)
    ],

    "F": [

        (21,24,42),
        (21,27,42),
        (21,30,42),
        (21,36,42)
    ],

    "G": [

        (35,42,49),
        (36,42,49),
        (42,49,56)
    ]
}

# ============================================================
# Helper functions used by selector engine
# ============================================================

def products_for_stage(stage: str) -> List[int]:

    if stage not in STAGE_PRODUCT_BANKS:
        raise ValueError(f"Unknown stage {stage}")

    return list(STAGE_PRODUCT_BANKS[stage])


def cumulative_products_for_stage(stage: str) -> List[int]:

    if stage not in STAGE_CUMULATIVE_BANKS:
        raise ValueError(f"Unknown stage {stage}")

    return list(STAGE_CUMULATIVE_BANKS[stage])


def recap_products_for_stage(stage: str) -> List[int]:

    if stage not in RECAP_FAMILY_BANKS:
        return []

    return list(RECAP_FAMILY_BANKS[stage])


def products_for_number_type(selection_mode: str, stage: str | None = None) -> List[int]:

    if selection_mode == "same_stage_products":

        if stage is None:
            raise ValueError("stage required for same_stage_products")

        return products_for_stage(stage)

    if selection_mode not in NUMBER_TYPE_BANKS:
        raise ValueError(f"Unknown selection mode {selection_mode}")

    return list(NUMBER_TYPE_BANKS[selection_mode])


# ============================================================
# Validation
# ============================================================

def validate_product_banks() -> None:

    if len(TMK_ALL_PRODUCTS) != 42:
        raise ValueError("TMK_ALL_PRODUCTS must contain 42 products")

    if len(set(TMK_ALL_PRODUCTS)) != len(TMK_ALL_PRODUCTS):
        raise ValueError("TMK_ALL_PRODUCTS contains duplicates")

    stage_union = sorted(
        set(p for bank in STAGE_PRODUCT_BANKS.values() for p in bank)
    )

    if stage_union != sorted(TMK_ALL_PRODUCTS):
        raise ValueError(
            "Union of stage banks must equal TMK_ALL_PRODUCTS"
        )

    for name, bank in {
        "MULTI_ROUTE_PRODUCTS": MULTI_ROUTE_PRODUCTS,
        "SQUARE_PRODUCTS": SQUARE_PRODUCTS,
        "DOUBLING_CHAIN_PRODUCTS": DOUBLING_CHAIN_PRODUCTS,
        "SPECIAL_FOCUS_PRODUCTS": SPECIAL_FOCUS_PRODUCTS,
    }.items():

        invalid = [p for p in bank if p not in TMK_ALL_PRODUCTS]

        if invalid:
            raise ValueError(f"{name} contains invalid products: {invalid}")
