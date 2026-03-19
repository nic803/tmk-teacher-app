from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, Final, Tuple, List

from products import (
    ways_in,
    ways_out,
    factor_families,
    structural_role,
)

PatternKey = str


@dataclass(frozen=True)
class Pattern:
    key: PatternKey
    name: str
    description: str


PATTERNS: Final[Dict[PatternKey, Pattern]] = {

    # Core structural patterns

    "product_hub": Pattern(
        "product_hub",
        "Product Hub",
        "Multiplication routes converge at a product hub."
    ),

    "entry_routes": Pattern(
        "entry_routes",
        "Entry Routes",
        "Multiplication routes that lead into a product."
    ),

    "exit_routes": Pattern(
        "exit_routes",
        "Exit Routes",
        "Division routes that leave a product."
    ),

    "inverse_relationship": Pattern(
        "inverse_relationship",
        "Inverse Relationship",
        "Multiplication and division are inverse routes through a product."
    ),

    "commutative_switch": Pattern(
        "commutative_switch",
        "Commutative Switch",
        "a × b and b × a produce the same product."
    ),

    "factor_family": Pattern(
        "factor_family",
        "Factor Family",
        "Products belong to families defined by their factors."
    ),

    "product_family_overlap": Pattern(
        "product_family_overlap",
        "Product Family Overlap",
        "Multiple factor families produce the same product."
    ),

    "single_route_product": Pattern(
        "single_route_product",
        "Single Route Product",
        "Products with only one factor pair."
    ),

    "multiple_route_product": Pattern(
        "multiple_route_product",
        "Multiple Route Product",
        "Products that have more than one factor pair."
    ),

    # Stage patterns

    "identity_product": Pattern(
        "identity_product",
        "Identity Product",
        "Products involving multiplication by 1."
    ),

    "ten_scaling": Pattern(
        "ten_scaling",
        "Ten Scaling",
        "Multiplying by 10 extends a product through place value."
    ),

    "five_midpoint": Pattern(
        "five_midpoint",
        "Five Midpoint",
        "Products involving 5 create midpoint relationships."
    ),

    "nine_quantifier_build": Pattern(
        "nine_quantifier_build",
        "Nine Quantifier Build",
        "Products involving 9 relate to the structure of 10."
    ),

    "doubling_chain": Pattern(
        "doubling_chain",
        "Doubling Chain",
        "Products created by doubling another factor relationship."
    ),

    "interleaving_structure": Pattern(
        "interleaving_structure",
        "Interleaving Structure",
        "Products that combine structures from different factor groups."
    ),

    "square_product": Pattern(
        "square_product",
        "Square Product",
        "Products where both factors are the same."
    ),

    "closure_square": Pattern(
        "closure_square",
        "Closure Square",
        "Terminal square product closing a structural chain."
    ),

    # Structural compression

    "compression_hub": Pattern(
        "compression_hub",
        "Compression Hub",
        "Products that gather many multiplication routes."
    ),

    "bridge_hub": Pattern(
        "bridge_hub",
        "Bridge Hub",
        "Products that connect multiple structural regions."
    ),

    "closure_hub": Pattern(
        "closure_hub",
        "Closure Hub",
        "Terminal product closing a region of the system."
    ),

    # Relationship patterns

    "route_derivation": Pattern(
        "route_derivation",
        "Route Derivation",
        "A multiplication route derived from another known route."
    ),

    "product_reconstruction": Pattern(
        "product_reconstruction",
        "Product Reconstruction",
        "Rebuilding a product using known factor relationships."
    ),

    "factor_overlap": Pattern(
        "factor_overlap",
        "Factor Overlap",
        "Products sharing common factors."
    ),

    "factor_chain": Pattern(
        "factor_chain",
        "Factor Chain",
        "A sequence of products connected by shared factors."
    ),

    # Structural observations

    "even_product": Pattern(
        "even_product",
        "Even Product",
        "Products resulting from an even factor."
    ),

    "odd_product": Pattern(
        "odd_product",
        "Odd Product",
        "Products resulting from two odd factors."
    ),

    "doubling_bridge": Pattern(
        "doubling_bridge",
        "Doubling Bridge",
        "Products linked through doubling relationships."
    ),

    "half_relationship": Pattern(
        "half_relationship",
        "Half Relationship",
        "Products linked through halving structures."
    ),

    "pattern_transition": Pattern(
        "pattern_transition",
        "Pattern Transition",
        "Movement between structural multiplication patterns."
    ),
}


@lru_cache(maxsize=None)
def patterns_for_product(product: int) -> Tuple[PatternKey, ...]:

    patterns: List[PatternKey] = []

    patterns.append("product_hub")

    if len(ways_in(product)) > 1:
        patterns.append("multiple_route_product")
    else:
        patterns.append("single_route_product")

    if structural_role(product) == "compression_hub":
        patterns.append("compression_hub")

    if structural_role(product) == "bridge_hub":
        patterns.append("bridge_hub")

    if structural_role(product) == "closure_hub":
        patterns.append("closure_hub")

    if any(a == b for a, b in ways_in(product)):
        patterns.append("square_product")

    if product % 2 == 0:
        patterns.append("even_product")
    else:
        patterns.append("odd_product")

    if len(factor_families(product)) > 1:
        patterns.append("product_family_overlap")

    return tuple(patterns)
