from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class StageDefinition:
    id: str
    label: str
    structural_role: str
    products: tuple[int, ...]


@dataclass(frozen=True)
class ProductRecord:
    product: int
    stage: str
    factors: tuple[tuple[int, int], ...]
    commutative: tuple[tuple[int, int], ...]
    inverse_pairs: tuple[tuple[int, int, int], ...]
    intro_route: tuple[int, int]
    ways_out: tuple[tuple[int, int, int], ...]
    structural_role: str
    is_square: bool
    has_factor_7: bool
    has_multiple_routes: bool
    known_routes_at_stage: tuple[str, ...]


STAGE_ORDER: Final[tuple[str, ...]] = ("A", "B", "C", "D", "E", "F", "G")

EXPECTED_STAGE_PRODUCTS: Final[dict[str, tuple[int, ...]]] = {
    "A": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
    "B": (20, 30, 40, 50, 60, 70, 80, 90, 100),
    "C": (15, 25, 35, 45),
    "D": (18, 27, 36, 54, 63, 72, 81),
    "E": (12, 14, 16, 24, 28, 32, 48, 56, 64),
    "F": (21, 42),
    "G": (49,),
}

STAGE_LABELS: Final[dict[str, str]] = {
    "A": "A — Identity & Base-10 Anchors",
    "B": "B — Pure Scaling (10×)",
    "C": "C — Midpoints & Halves (5×)",
    "D": "D — Complement / Near-Ten Logic (9×)",
    "E": "E — Doubling Chain (2× → 4× → 8×)",
    "F": "F — Interleaving (3× / 6×)",
    "G": "G — Closure / Final Key (7×)",
}

STAGE_STRUCTURAL_ROLES: Final[dict[str, str]] = {
    "A": "identity and magnitude grounding",
    "B": "base-10 scaling",
    "C": "midpoints and halving",
    "D": "near-ten complement logic",
    "E": "doubling chain growth",
    "F": "interleaving composite reasoning",
    "G": "square closure",
}

STAGES: Final[dict[str, StageDefinition]] = {
    stage_id: StageDefinition(
        id=stage_id,
        label=STAGE_LABELS[stage_id],
        structural_role=STAGE_STRUCTURAL_ROLES[stage_id],
        products=products,
    )
    for stage_id, products in EXPECTED_STAGE_PRODUCTS.items()
}

ALL_PRODUCTS: Final[tuple[int, ...]] = tuple(
    product
    for stage_id in STAGE_ORDER
    for product in STAGES[stage_id].products
)

PRODUCTS: Final[tuple[int, ...]] = ALL_PRODUCTS
ALL_STAGE_IDS: Final[tuple[str, ...]] = STAGE_ORDER

PRODUCT_STAGE: Final[dict[int, str]] = {
    product: stage_id
    for stage_id in STAGE_ORDER
    for product in STAGES[stage_id].products
}


def stage_label(stage_id: str) -> str:
    if stage_id not in STAGE_LABELS:
        raise ValueError(f"Unknown TMK stage: {stage_id}")
    return STAGE_LABELS[stage_id]


def factors_for_product(product: int) -> tuple[tuple[int, int], ...]:
    if product not in PRODUCT_STAGE:
        raise ValueError(f"Unknown TMK product: {product}")

    pairs = sorted(
        {
            tuple(sorted((a, b)))
            for a in range(1, 11)
            for b in range(1, 11)
            if a * b == product
        }
    )
    return tuple(pairs)


def commutative_pairs_for_product(product: int) -> tuple[tuple[int, int], ...]:
    factors = factors_for_product(product)
    pairs: list[tuple[int, int]] = []

    for a, b in factors:
        pairs.append((a, b))
        if a != b:
            pairs.append((b, a))

    return tuple(pairs)


def inverse_pairs_for_product(product: int) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (product, divisor, quotient)
        for divisor, quotient in commutative_pairs_for_product(product)
    )


def known_routes_at_stage(product: int) -> tuple[str, ...]:
    stage = PRODUCT_STAGE[product]

    routes: list[str] = ["canonical", "inverse"]

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


def intro_route_for_product(product: int) -> tuple[int, int]:
    factors = factors_for_product(product)
    stage = PRODUCT_STAGE[product]

    preferred_by_stage: dict[str, tuple[int, int] | None] = {
        "A": next(((a, b) for a, b in factors if 1 in (a, b)), None),
        "B": next(((a, b) for a, b in factors if 10 in (a, b)), None),
        "C": next(((a, b) for a, b in factors if 5 in (a, b)), None),
        "D": next(((a, b) for a, b in factors if 9 in (a, b)), None),
        "E": next(((a, b) for a, b in factors if a in (2, 4, 8) or b in (2, 4, 8)), None),
        "F": next(((a, b) for a, b in factors if a in (3, 6) or b in (3, 6)), None),
        "G": (7, 7) if product == 49 else None,
    }

    preferred = preferred_by_stage.get(stage)
    return preferred if preferred is not None else factors[0]


def structural_role_for_product(product: int) -> str:
    stage = PRODUCT_STAGE[product]

    if stage == "A":
        return "anchor product"
    if stage == "B":
        return "base-10 scaling product"
    if stage == "C":
        return "midpoint / halving product"
    if stage == "D":
        return "near-ten complement product"
    if stage == "E":
        return "doubling-chain product"
    if stage == "F":
        return "interleaving product"
    if stage == "G":
        return "square-closure product"
    return "core product"


def product_record(product: int) -> ProductRecord:
    if product not in PRODUCT_STAGE:
        raise ValueError(f"Unknown TMK product: {product}")

    factors = factors_for_product(product)
    inverse_pairs = inverse_pairs_for_product(product)

    return ProductRecord(
        product=product,
        stage=PRODUCT_STAGE[product],
        factors=factors,
        commutative=commutative_pairs_for_product(product),
        inverse_pairs=inverse_pairs,
        intro_route=intro_route_for_product(product),
        ways_out=inverse_pairs,
        structural_role=structural_role_for_product(product),
        is_square=any(a == b for a, b in factors),
        has_factor_7=any(7 in pair for pair in factors),
        has_multiple_routes=len(factors) > 1,
        known_routes_at_stage=known_routes_at_stage(product),
    )


def available_products(stage_id: str) -> tuple[int, ...]:
    if stage_id not in STAGES:
        raise ValueError(f"Unknown stage: {stage_id}")

    products: list[int] = []
    for current_stage in STAGE_ORDER:
        products.extend(STAGES[current_stage].products)
        if current_stage == stage_id:
            break

    return tuple(products)


def new_products(stage_id: str) -> tuple[int, ...]:
    if stage_id not in STAGES:
        raise ValueError(f"Unknown stage: {stage_id}")
    return STAGES[stage_id].products


def get_stage(stage_id: str) -> StageDefinition:
    if stage_id not in STAGES:
        raise ValueError(f"Unknown stage: {stage_id}")
    return STAGES[stage_id]


def get_available_products(stage_id: str) -> tuple[int, ...]:
    return available_products(stage_id)


def get_new_products(stage_id: str) -> tuple[int, ...]:
    return new_products(stage_id)


def get_product(product: int) -> ProductRecord:
    return product_record(product)


def get_stage_products(stage_id: str, cumulative: bool = True) -> tuple[int, ...]:
    return available_products(stage_id) if cumulative else new_products(stage_id)


def get_structure(stage_id: str) -> dict[str, object]:
    if stage_id not in STAGES:
        raise ValueError(f"Unknown stage: {stage_id}")

    products = available_products(stage_id)

    return {
        "stage": stage_id,
        "products": tuple(product_record(product) for product in products),
        "routes": (),
        "available_products": products,
        "new_products": new_products(stage_id),
        "metadata": {
            "stage_type": "core",
            "stage_label": stage_label(stage_id),
        },
    }


def _validate_product_structure() -> None:
    if STAGE_ORDER != ("A", "B", "C", "D", "E", "F", "G"):
        raise ValueError(
            f"STAGE_ORDER must be ('A','B','C','D','E','F','G'). Found: {STAGE_ORDER}"
        )

    extra_stages = set(STAGES) - set(STAGE_ORDER)
    if extra_stages:
        raise ValueError(f"Unexpected stages present in STAGES: {sorted(extra_stages)}")

    canonical_products_in_stage_order: list[int] = []
    first_seen_stage: dict[int, str] = {}
    duplicates: dict[int, list[str]] = {}

    for stage_id in STAGE_ORDER:
        stage = STAGES[stage_id]
        expected = EXPECTED_STAGE_PRODUCTS[stage_id]

        if stage.products != expected:
            raise ValueError(
                f"Stage '{stage_id}' canonical products do not match TMK mapping.\n"
                f"Expected: {expected}\n"
                f"Found:    {stage.products}"
            )

        for product in stage.products:
            canonical_products_in_stage_order.append(product)
            if product in first_seen_stage:
                duplicates.setdefault(product, [first_seen_stage[product]]).append(stage_id)
            else:
                first_seen_stage[product] = stage_id

    if duplicates:
        raise ValueError(f"Duplicate TMK products detected: {duplicates}")

    canonical_products = tuple(canonical_products_in_stage_order)

    if len(canonical_products) != 42:
        raise ValueError(
            f"Canonical TMK registry must contain exactly 42 products. Found {len(canonical_products)}."
        )

    if ALL_PRODUCTS != canonical_products:
        raise ValueError(
            "ALL_PRODUCTS does not match canonical registry.\n"
            f"Expected: {canonical_products}\n"
            f"Found:    {ALL_PRODUCTS}"
        )

    for product in ALL_PRODUCTS:
        record = product_record(product)

        if record.product != product:
            raise ValueError(f"Product record mismatch for {product}")

        if record.stage not in STAGES:
            raise ValueError(f"Unknown stage in record for product {product}")

        if product not in STAGES[record.stage].products:
            raise ValueError(
                f"Product {product} is not present in canonical stage {record.stage}"
            )


_validate_product_structure()


__all__ = [
    "StageDefinition",
    "ProductRecord",
    "STAGE_ORDER",
    "EXPECTED_STAGE_PRODUCTS",
    "STAGE_LABELS",
    "STAGE_STRUCTURAL_ROLES",
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
    "intro_route_for_product",
    "structural_role_for_product",
    "product_record",
    "get_product",
    "available_products",
    "new_products",
    "get_available_products",
    "get_new_products",
    "get_stage",
    "get_stage_products",
    "get_structure",
]
