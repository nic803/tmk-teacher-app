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
    "A": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
    "B": (20, 30, 40, 50, 60, 70, 80, 90, 100),
    "C": (15, 25, 35, 45),
    "D": (18, 27, 36, 54, 63, 72, 81),
    "E": (12, 14, 16, 24, 28, 32, 48, 56, 64),
    "F": (21, 42),
    "G": (49,),
}

STAGES: Final[dict[str, StageDefinition]] = {
    stage_id: StageDefinition(id=stage_id, products=products)
    for stage_id, products in EXPECTED_STAGE_PRODUCTS.items()
}

ALL_PRODUCTS: Final[tuple[int, ...]] = tuple(
    product
    for stage_id in STAGE_ORDER
    for product in STAGES[stage_id].products
)

PRODUCT_STAGE: Final[dict[int, str]] = {
    product: stage_id
    for stage_id in STAGE_ORDER
    for product in STAGES[stage_id].products
}


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


def product_record(product: int) -> ProductRecord:
    if product not in PRODUCT_STAGE:
        raise ValueError(f"Unknown TMK product: {product}")

    factors = factors_for_product(product)

    return ProductRecord(
        product=product,
        stage=PRODUCT_STAGE[product],
        factors=factors,
        commutative=commutative_pairs_for_product(product),
        inverse_pairs=inverse_pairs_for_product(product),
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


def _validate_product_structure() -> None:
    if STAGE_ORDER != ("A", "B", "C", "D", "E", "F", "G"):
        raise ValueError(
            f"STAGE_ORDER must be ('A','B','C','D','E','F','G'). Found: {STAGE_ORDER}"
        )

    extra_stages = set(STAGES) - set(STAGE_ORDER)
    if extra_stages:
        raise ValueError(f"Unexpected stages present in STAGES: {sorted(extra_stages)}")

    duplicates: dict[int, list[str]] = {}
    first_seen_stage: dict[int, str] = {}
    canonical_products_in_stage_order: list[int] = []

    for stage_id in STAGE_ORDER:
        if stage_id not in STAGES:
            raise ValueError(f"Stage '{stage_id}' is missing from STAGES.")

        stage = STAGES[stage_id]

        if not hasattr(stage, "products"):
            raise ValueError(f"Stage '{stage_id}' is missing 'products'.")

        if not isinstance(stage.products, tuple):
            raise ValueError(
                f"Stage '{stage_id}' products must be a tuple. "
                f"Found {type(stage.products).__name__}."
            )

        expected = EXPECTED_STAGE_PRODUCTS[stage_id]
        if stage.products != expected:
            raise ValueError(
                f"Stage '{stage_id}' canonical products do not match TMK mapping.\n"
                f"Expected: {expected}\n"
                f"Found:    {stage.products}"
            )

        for product in stage.products:
            if not isinstance(product, int):
                raise ValueError(
                    f"Stage '{stage_id}' contains non-integer product: {product!r}"
                )

            canonical_products_in_stage_order.append(product)

            if product in first_seen_stage:
                duplicates.setdefault(product, [first_seen_stage[product]]).append(stage_id)
            else:
                first_seen_stage[product] = stage_id

    if duplicates:
        duplicate_lines = []
        for product in sorted(duplicates):
            stages = " -> ".join(duplicates[product])
            duplicate_lines.append(f"{product}: {stages}")

        raise ValueError(
            "Duplicate TMK products detected in canonical stage registry:\n"
            + "\n".join(duplicate_lines)
        )

    canonical_products = tuple(canonical_products_in_stage_order)

    if len(canonical_products) != 42:
        raise ValueError(
            f"Canonical TMK registry must contain exactly 42 unique core products. "
            f"Found {len(canonical_products)}."
        )

    if ALL_PRODUCTS != canonical_products:
        raise ValueError(
            "ALL_PRODUCTS does not match the canonical unique stage product registry.\n"
            f"Expected: {canonical_products}\n"
            f"Found:    {ALL_PRODUCTS}"
        )

    record_products = set()

    for product in ALL_PRODUCTS:
        record = product_record(product)

        for attr in ("product", "stage"):
            if not hasattr(record, attr):
                raise ValueError(
                    f"product_record({product}) returned object missing '{attr}'."
                )

        if record.product != product:
            raise ValueError(
                f"Product record mismatch for {product}: record.product={record.product}"
            )

        if record.stage not in STAGES:
            raise ValueError(
                f"Product {product} references unknown stage '{record.stage}'."
            )

        if product not in STAGES[record.stage].products:
            raise ValueError(
                f"Product {product} says it belongs to stage '{record.stage}' "
                f"but is not present in that canonical stage product list."
            )

        if product in record_products:
            raise ValueError(
                f"Duplicate product record emitted by product_record(): {product}"
            )

        record_products.add(product)

    if record_products != set(ALL_PRODUCTS):
        missing = set(ALL_PRODUCTS) - record_products
        extra = record_products - set(ALL_PRODUCTS)
        raise ValueError(
            "Mismatch between ALL_PRODUCTS and product_record registry.\n"
            f"Missing: {sorted(missing)}\n"
            f"Extra: {sorted(extra)}"
        )


_validate_product_structure()


__all__ = [
    "StageDefinition",
    "ProductRecord",
    "STAGE_ORDER",
    "EXPECTED_STAGE_PRODUCTS",
    "STAGES",
    "ALL_PRODUCTS",
    "PRODUCT_STAGE",
    "factors_for_product",
    "commutative_pairs_for_product",
    "inverse_pairs_for_product",
    "known_routes_at_stage",
    "product_record",
    "available_products",
    "new_products",
]
