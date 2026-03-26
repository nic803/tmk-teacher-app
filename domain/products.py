from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class StageDefinition:
    id: str
    products: tuple[int, ...]


@dataclass(frozen=True)
class ProductRecord:
    product: int
    stage: str
    factors: tuple[tuple[int, int], ...]
    commutative: tuple[tuple[int, int], ...]
    inverse_pairs: tuple[tuple[int, int, int], ...]
    is_square: bool
    has_factor_7: bool
    has_multiple_routes: bool
    known_routes_at_stage: tuple[str, ...]


STAGE_ORDER: Final[tuple[str, ...]] = ("A", "B", "C", "D", "E", "F", "G")

EXPECTED_STAGE_PRODUCTS: Final[dict[str, tuple[int, ...]]] = {
    "A": (1,2,3,4,5,6,7,8,9,10),
    "B": (20,30,40,50,60,70,80,90,100),
    "C": (15,25,35,45),
    "D": (18,27,36,54,63,72,81),
    "E": (12,14,16,24,28,32,48,56,64),
    "F": (21,42),
    "G": (49,),
}


STAGES: Final[dict[str, StageDefinition]] = {
    stage_id: StageDefinition(id=stage_id, products=products)
    for stage_id, products in EXPECTED_STAGE_PRODUCTS.items()
}


ALL_PRODUCTS: Final[tuple[int, ...]] = tuple(
    p for stage in STAGE_ORDER for p in STAGES[stage].products
)

PRODUCTS: Final[tuple[int, ...]] = ALL_PRODUCTS
ALL_STAGE_IDS: Final[tuple[str, ...]] = STAGE_ORDER


PRODUCT_STAGE: Final[dict[int, str]] = {
    p: stage for stage in STAGE_ORDER for p in STAGES[stage].products
}


def stage_label(stage_id: str) -> str:
    labels = {
        "A": "A — Identity & Base-10 Anchors",
        "B": "B — Pure Scaling (10×)",
        "C": "C — Midpoints & Halves (5×)",
        "D": "D — Complement / Near-Ten Logic (9×)",
        "E": "E — Doubling Chain (2× → 4× → 8×)",
        "F": "F — Interleaving (3× / 6×)",
        "G": "G — Closure / Final Key (7×)",
    }

    if stage_id not in labels:
        raise ValueError(f"Unknown stage: {stage_id}")

    return labels[stage_id]


def factors_for_product(product: int) -> tuple[tuple[int, int], ...]:
    if product not in PRODUCT_STAGE:
        raise ValueError(f"Unknown product {product}")

    pairs = sorted(
        {tuple(sorted((a, b)))
         for a in range(1,11)
         for b in range(1,11)
         if a*b == product}
    )

    return tuple(pairs)


def commutative_pairs_for_product(product: int) -> tuple[tuple[int, int], ...]:
    pairs = []

    for a,b in factors_for_product(product):
        pairs.append((a,b))
        if a != b:
            pairs.append((b,a))

    return tuple(pairs)


def inverse_pairs_for_product(product: int) -> tuple[tuple[int,int,int], ...]:
    return tuple(
        (product, divisor, quotient)
        for divisor, quotient in commutative_pairs_for_product(product)
    )


def known_routes_at_stage(product: int) -> tuple[str, ...]:
    stage = PRODUCT_STAGE[product]

    routes = ["canonical","inverse"]

    if stage == "B":
        routes.append("scale_from_10")
    elif stage == "C":
        routes.append("half_of_10x")
    elif stage == "D":
        routes.append("near_ten")
    elif stage == "E":
        routes.append("doubling_chain")
    elif stage == "F":
        routes.append("interleaving")
    elif stage == "G":
        routes.append("square_closure")

    return tuple(routes)


def product_record(product: int) -> ProductRecord:
    if product not in PRODUCT_STAGE:
        raise ValueError(f"Unknown product {product}")

    factors = factors_for_product(product)

    return ProductRecord(
        product=product,
        stage=PRODUCT_STAGE[product],
        factors=factors,
        commutative=commutative_pairs_for_product(product),
        inverse_pairs=inverse_pairs_for_product(product),
        is_square=any(a==b for a,b in factors),
        has_factor_7=any(7 in pair for pair in factors),
        has_multiple_routes=len(factors) > 1,
        known_routes_at_stage=known_routes_at_stage(product),
    )


def available_products(stage_id: str) -> tuple[int,...]:
    products = []

    for stage in STAGE_ORDER:
        products.extend(STAGES[stage].products)
        if stage == stage_id:
            break

    return tuple(products)


def new_products(stage_id: str) -> tuple[int,...]:
    return STAGES[stage_id].products


def _validate_product_structure() -> None:

    canonical = tuple(
        p for stage in STAGE_ORDER for p in STAGES[stage].products
    )

    if len(canonical) != 42:
        raise ValueError("TMK must contain exactly 42 core products.")

    if canonical != ALL_PRODUCTS:
        raise ValueError("ALL_PRODUCTS mismatch.")

    seen = set()

    for p in canonical:

        if p in seen:
            raise ValueError(f"Duplicate product {p}")

        seen.add(p)

        record = product_record(p)

        if record.stage not in STAGES:
            raise ValueError(f"Invalid stage for {p}")

        if p not in STAGES[record.stage].products:
            raise ValueError(f"Product {p} not in stage list")


_validate_product_structure()


__all__ = [
    "StageDefinition",
    "ProductRecord",
    "STAGE_ORDER",
    "STAGES",
    "ALL_PRODUCTS",
    "PRODUCTS",
    "ALL_STAGE_IDS",
    "PRODUCT_STAGE",
    "stage_label",
    "factors_for_product",
    "commutative_pairs_for_product",
    "inverse_pairs_for_product",
    "known_routes_at_stage",
    "product_record",
    "available_products",
    "new_products",
]
