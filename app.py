from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, Final, Iterable, List, Literal, Tuple

StageKey = Literal["0", "A", "B", "C", "D", "E", "F", "G"]
Route = Tuple[int, int]
StructuralRole = Literal[
    "anchor_hub",
    "single_route_hub",
    "bridge_hub",
    "compression_hub",
    "closure_hub",
]


@dataclass(frozen=True)
class StageRecord:
    key: StageKey
    label: str
    products: Tuple[int, ...]
    color: str


@dataclass(frozen=True)
class ProductRecord:
    product: int
    stage: StageKey
    intro_route: Route
    ways_in: Tuple[Route, ...]
    ways_out: Tuple[Route, ...]
    factor_families: Tuple[Route, ...]
    related_products: Tuple[int, ...]
    structural_role: StructuralRole


STAGE_ORDER: Final[Tuple[StageKey, ...]] = ("0", "A", "B", "C", "D", "E", "F", "G")

STAGES: Final[Dict[StageKey, StageRecord]] = {
    "0": StageRecord("0", "Stage 0 · Foundation", (4, 6, 8, 9, 10), "#475569"),
    "A": StageRecord("A", "Stage A · Identity Anchors", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), "#94a3b8"),
    "B": StageRecord("B", "Stage B · Ten Scaling", (20, 30, 40, 50, 60, 70, 80, 90, 100), "#2563eb"),
    "C": StageRecord("C", "Stage C · Five Midpoints", (15, 25, 35, 45), "#0ea5e9"),
    "D": StageRecord("D", "Stage D · Nine Structure", (18, 27, 36, 54, 63, 72, 81), "#0284c7"),
    "E": StageRecord("E", "Stage E · Doubling Chain", (12, 14, 16, 24, 28, 32, 48, 56, 64), "#0f766e"),
    "F": StageRecord("F", "Stage F · Interleaving", (21, 42), "#7c3aed"),
    "G": StageRecord("G", "Stage G · Closure", (49,), "#ca8a04"),
}

INTRO_ROUTES: Final[Dict[int, Route]] = {
    1: (1, 1),
    2: (1, 2),
    3: (1, 3),
    4: (1, 4),
    5: (1, 5),
    6: (1, 6),
    7: (1, 7),
    8: (1, 8),
    9: (1, 9),
    10: (1, 10),
    12: (2, 6),
    14: (2, 7),
    15: (3, 5),
    16: (2, 8),
    18: (2, 9),
    20: (2, 10),
    21: (3, 7),
    24: (4, 6),
    25: (5, 5),
    27: (3, 9),
    28: (4, 7),
    30: (3, 10),
    32: (4, 8),
    35: (5, 7),
    36: (4, 9),
    40: (4, 10),
    42: (6, 7),
    45: (5, 9),
    48: (6, 8),
    49: (7, 7),
    50: (5, 10),
    54: (6, 9),
    56: (7, 8),
    60: (6, 10),
    63: (7, 9),
    64: (8, 8),
    70: (7, 10),
    72: (8, 9),
    80: (8, 10),
    81: (9, 9),
    90: (9, 10),
    100: (10, 10),
}

PRODUCT_STAGE: Final[Dict[int, StageKey]] = {
    product: stage.key
    for stage in STAGES.values()
    for product in stage.products
}

ALL_PRODUCTS: Final[Tuple[int, ...]] = tuple(sorted(PRODUCT_STAGE))


def _sorted_unique_routes(routes: Iterable[Route]) -> Tuple[Route, ...]:
    return tuple(sorted(set(routes), key=lambda item: (item[0], item[1])))


@lru_cache(maxsize=None)
def stage_rank(stage: StageKey) -> int:
    return STAGE_ORDER.index(stage)


@lru_cache(maxsize=None)
def visible_products(stage: StageKey) -> Tuple[int, ...]:
    unlocked = {
        product
        for stage_key in STAGE_ORDER
        if stage_rank(stage_key) <= stage_rank(stage)
        for product in STAGES[stage_key].products
    }
    return tuple(sorted(unlocked))


@lru_cache(maxsize=None)
def ways_in(product: int) -> Tuple[Route, ...]:
    return tuple(
        (a, b)
        for a in range(1, 11)
        for b in range(1, 11)
        if a * b == product
    )


@lru_cache(maxsize=None)
def ways_out(product: int) -> Tuple[Route, ...]:
    return tuple(
        (d, product // d)
        for d in range(1, 11)
        if product % d == 0 and 1 <= product // d <= 10
    )


@lru_cache(maxsize=None)
def factor_families(product: int) -> Tuple[Route, ...]:
    families = {tuple(sorted((a, b))) for a, b in ways_in(product)}
    return tuple(sorted(families, key=lambda item: (item[0], item[1])))


@lru_cache(maxsize=None)
def route_count(product: int) -> int:
    return len(ways_in(product))


@lru_cache(maxsize=None)
def family_count(product: int) -> int:
    return len(factor_families(product))


@lru_cache(maxsize=None)
def is_square(product: int) -> bool:
    return any(a == b for a, b in factor_families(product))


@lru_cache(maxsize=None)
def factors_used(product: int) -> Tuple[int, ...]:
    return tuple(sorted({n for route in ways_in(product) for n in route}))


@lru_cache(maxsize=None)
def related_products(product: int) -> Tuple[int, ...]:
    target_factors = set(factors_used(product))
    related = []
    for other in ALL_PRODUCTS:
        if other == product:
            continue
        if target_factors.intersection(factors_used(other)):
            related.append(other)
    return tuple(sorted(related))


@lru_cache(maxsize=None)
def structural_role(product: int) -> StructuralRole:
    if product == 49:
        return "closure_hub"
    if product in {21, 42}:
        return "bridge_hub"
    if family_count(product) >= 3:
        return "compression_hub"
    if family_count(product) == 1:
        return "single_route_hub"
    return "anchor_hub"


@lru_cache(maxsize=None)
def stage_of(product: int) -> StageKey:
    return PRODUCT_STAGE[product]


@lru_cache(maxsize=None)
def intro_route(product: int) -> Route:
    return INTRO_ROUTES[product]


@lru_cache(maxsize=None)
def intro_factors(product: int) -> Tuple[int, int]:
    return INTRO_ROUTES[product]


@lru_cache(maxsize=None)
def belongs_to_p10(number: int) -> bool:
    return any(a * b == number for a in range(1, 11) for b in range(1, 11))


@lru_cache(maxsize=None)
def product_record(product: int) -> ProductRecord:
    return ProductRecord(
        product=product,
        stage=stage_of(product),
        intro_route=intro_route(product),
        ways_in=ways_in(product),
        ways_out=ways_out(product),
        factor_families=factor_families(product),
        related_products=related_products(product),
        structural_role=structural_role(product),
    )


@lru_cache(maxsize=None)
def records_by_stage(stage: StageKey) -> Tuple[ProductRecord, ...]:
    return tuple(product_record(product) for product in STAGES[stage].products)


@lru_cache(maxsize=None)
def all_product_records() -> Tuple[ProductRecord, ...]:
    return tuple(product_record(product) for product in ALL_PRODUCTS)


@lru_cache(maxsize=None)
def stage_products(stage: StageKey) -> Tuple[int, ...]:
    return STAGES[stage].products


def stage_label(stage: StageKey) -> str:
    return STAGES[stage].label


def stage_color(stage: StageKey) -> str:
    return STAGES[stage].color


def has_multiple_families(product: int) -> bool:
    return family_count(product) > 1


def has_multiple_routes(product: int) -> bool:
    return route_count(product) > 2


def is_intro_route(product: int, route: Route) -> bool:
    return intro_route(product) == route


def ordered_route_exists(product: int, route: Route) -> bool:
    return route in ways_in(product)


def family_route_exists(product: int, route: Route) -> bool:
    return tuple(sorted(route)) in factor_families(product)


def products_in_family(factor: int) -> Tuple[int, ...]:
    return tuple(
        sorted(
            product
            for product in ALL_PRODUCTS
            if any(factor in route for route in factor_families(product))
        )
    )


def stage_summary() -> Tuple[Tuple[StageKey, Tuple[int, ...]], ...]:
    return tuple((stage, STAGES[stage].products) for stage in STAGE_ORDER)
