from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, Final, Tuple

from products import (
    factor_families,
    stage_of,
    structural_role,
    ways_in,
)

PatternId = str


@dataclass(frozen=True)
class Pattern:
    id: PatternId
    name: str
    learner_label: str
    short_prompt: str
    stage: str
    examples: Tuple[int, ...]
    child_text: str
    teacher_note: str


PATTERNS: Final[Dict[PatternId, Pattern]] = {
    "product_hub": Pattern(
        id="product_hub",
        name="Product hub",
        learner_label="One product can have more than one way in",
        short_prompt="Find the product and its ways in",
        stage="0+",
        examples=(18, 24, 36),
        child_text="A product can have more than one way in.",
        teacher_note="The product is the central object. Learners study one product together with its routes.",
    ),
    "route_in_route_out": Pattern(
        id="route_in_route_out",
        name="Route in / route out",
        learner_label="A way in gives a way out",
        short_prompt="Use a way in to find a way out",
        stage="0+",
        examples=(18, 24, 36),
        child_text="A way in gives a way out.",
        teacher_note="Multiplication and division are paired through one shared product hub.",
    ),
    "commutative_switch": Pattern(
        id="commutative_switch",
        name="Commutative switch",
        learner_label="The factors can switch places",
        short_prompt="Switch the factors",
        stage="0+",
        examples=(24, 36, 42),
        child_text="The factors can switch places and keep the same product.",
        teacher_note="Different ordered expressions can describe the same factor pair.",
    ),
    "boundary_belonging": Pattern(
        id="boundary_belonging",
        name="Boundary belonging",
        learner_label="A product belongs if both factors fit inside the TMK world",
        short_prompt="Does it belong?",
        stage="0+",
        examples=(42, 49),
        child_text="A number belongs if it has a way in with factors up to 10.",
        teacher_note="Belonging is determined by valid factor pairs inside the bounded multiplication world.",
    ),
    "identity_pattern": Pattern(
        id="identity_pattern",
        name="Identity",
        learner_label="One times a number keeps the number",
        short_prompt="Use one times",
        stage="A",
        examples=(1, 2, 3, 7, 10),
        child_text="One times a number keeps the number.",
        teacher_note="Stage A anchors the product world through identity routes.",
    ),
    "ten_times_benchmark": Pattern(
        id="ten_times_benchmark",
        name="Ten-times benchmark",
        learner_label="Ten times gives the benchmark",
        short_prompt="Find ten times",
        stage="B",
        examples=(20, 40, 70, 100),
        child_text="Ten times gives a benchmark product.",
        teacher_note="Ten-times products supply fast anchor values and place-value structure.",
    ),
    "five_half_ten": Pattern(
        id="five_half_ten",
        name="Five times as half of ten",
        learner_label="Five times is half of ten times",
        short_prompt="Find ten times, then halve",
        stage="C",
        examples=(15, 25, 35, 45),
        child_text="Five times is half of ten times.",
        teacher_note="Core Stage C teaching pattern.",
    ),
    "five_ends_0_or_5": Pattern(
        id="five_ends_0_or_5",
        name="Five times ends in 0 or 5",
        learner_label="Five times ends in 0 or 5",
        short_prompt="Check the ending",
        stage="C",
        examples=(15, 25, 35, 45),
        child_text="Five times ends in 0 or 5.",
        teacher_note="Visible output feature for checking and predicting 5-family products.",
    ),
    "nine_quantifier_build": Pattern(
        id="nine_quantifier_build",
        name="Nine-times quantifier-build rule",
        learner_label="Nine times builds with one less and make 9",
        short_prompt="Build the 9-times product",
        stage="D",
        examples=(18, 27, 36, 54, 63, 72, 81),
        child_text="Nine times builds with one less and make 9.",
        teacher_note="Preferred constructive rule for the 9-family. Use this, not nine_minus_one.",
    ),
    "nine_digit_sum": Pattern(
        id="nine_digit_sum",
        name="Nine-times digit-sum-to-9",
        learner_label="The digits add to 9",
        short_prompt="Check the digits",
        stage="D",
        examples=(18, 27, 36, 54, 63, 72, 81),
        child_text="The digits add to 9.",
        teacher_note="Check pattern and recovery cue inside the 9-family.",
    ),
    "nine_rise_fall": Pattern(
        id="nine_rise_fall",
        name="Nine-times rise/fall",
        learner_label="One digit rises and one digit falls",
        short_prompt="Compare the 9-times products",
        stage="D",
        examples=(18, 27, 36, 45, 54, 63, 72, 81),
        child_text="One digit rises and one digit falls.",
        teacher_note="Children see lawful variation across the 9-family instead of isolated facts.",
    ),
    "doubling_chain": Pattern(
        id="doubling_chain",
        name="Doubling chain",
        learner_label="Known products can double into new products",
        short_prompt="Double the known product",
        stage="E",
        examples=(12, 24, 48, 14, 28, 56, 16, 32, 64),
        child_text="A known product can double into a new product.",
        teacher_note="The 2×, 4×, and 8× families are linked by repeated doubling.",
    ),
    "three_digit_sum_cycle": Pattern(
        id="three_digit_sum_cycle",
        name="Three-times digit-sum cycle",
        learner_label="Three times stays in the 3, 6, 9 family",
        short_prompt="Check the digit sum family",
        stage="F",
        examples=(12, 15, 18, 21, 24, 27),
        child_text="Three times stays in the 3, 6, 9 digit-sum family.",
        teacher_note="Recurring check pattern inside the 3-family.",
    ),
    "three_odd_even_alternation": Pattern(
        id="three_odd_even_alternation",
        name="Three-times odd/even alternation",
        learner_label="Three times alternates odd and even",
        short_prompt="Compare odd and even products",
        stage="F",
        examples=(15, 18, 21, 24, 27, 30),
        child_text="Three times alternates odd and even.",
        teacher_note="Links the 3-family to parity structure.",
    ),
    "six_digit_sum_cycle": Pattern(
        id="six_digit_sum_cycle",
        name="Six-times digit-sum cycle",
        learner_label="Six times also stays in the 3, 6, 9 family",
        short_prompt="Check the digit sum family",
        stage="F",
        examples=(12, 18, 24, 30, 36, 42),
        child_text="Six times also stays in the 3, 6, 9 digit-sum family.",
        teacher_note="Shows that the 6-family shares structural traces with the 3-family.",
    ),
    "six_always_even": Pattern(
        id="six_always_even",
        name="Six-times always even",
        learner_label="Six times is always even",
        short_prompt="Check evenness",
        stage="F",
        examples=(12, 18, 24, 30, 36, 42),
        child_text="Six times is always even.",
        teacher_note="The 6-family inherits evenness because 6 = 2 × 3.",
    ),
    "six_is_double_three": Pattern(
        id="six_is_double_three",
        name="Six is double three",
        learner_label="Six times is double three times",
        short_prompt="Double the 3-times product",
        stage="F",
        examples=(12, 18, 24, 30, 36, 42),
        child_text="Six times is double three times.",
        teacher_note="The 6-family is derived from the 3-family by doubling.",
    ),
    "new_product_or_new_route": Pattern(
        id="new_product_or_new_route",
        name="New product vs new route",
        learner_label="Sometimes a fact gives a new product and sometimes only a new way",
        short_prompt="Is it a new product or a new route?",
        stage="F",
        examples=(21, 24, 42),
        child_text="A fact can give a new product or just a new way to a known product.",
        teacher_note="Stage F is organized by the distinction between genuinely new products and new routes.",
    ),
    "use_one_product_for_another": Pattern(
        id="use_one_product_for_another",
        name="Use one product to find another product",
        learner_label="One product can help find another",
        short_prompt="Use a known product",
        stage="Across",
        examples=(20, 35, 40, 42),
        child_text="One product can help find another product.",
        teacher_note="TMK aims at re-derivation, not isolated recall.",
    ),
    "product_family_overlap": Pattern(
        id="product_family_overlap",
        name="Product-family overlap",
        learner_label="One product can belong to more than one family",
        short_prompt="Find the overlap",
        stage="Across",
        examples=(18, 24, 36, 42),
        child_text="One product can belong to more than one family.",
        teacher_note="Overlap compresses the system and links stages together.",
    ),
    "square_pattern": Pattern(
        id="square_pattern",
        name="Square products",
        learner_label="A square product is the same factor times itself",
        short_prompt="Find the square",
        stage="0+",
        examples=(1, 4, 9, 16, 25, 36, 49, 64, 81, 100),
        child_text="A square product is the same factor times itself.",
        teacher_note="Squares are structurally salient products inside the bounded world.",
    ),
    "closure_with_7x7": Pattern(
        id="closure_with_7x7",
        name="Closure with 49 = 7×7",
        learner_label="Forty-nine closes the TMK world",
        short_prompt="See the final new product",
        stage="G",
        examples=(49,),
        child_text="Forty-nine closes the TMK world.",
        teacher_note="Stage G completes the bounded system.",
    ),
    "parity_structure": Pattern(
        id="parity_structure",
        name="Factor parity and product parity",
        learner_label="The factors help predict whether the product is odd or even",
        short_prompt="Predict odd or even",
        stage="A+",
        examples=(15, 24, 35, 40),
        child_text="The factors help predict whether the product is odd or even.",
        teacher_note="Parity is an early structural filter for prediction and route elimination.",
    ),
    "odd_times_odd_is_odd": Pattern(
        id="odd_times_odd_is_odd",
        name="Odd × odd gives odd",
        learner_label="Odd times odd gives odd",
        short_prompt="Check the odd factors",
        stage="A+",
        examples=(9, 15, 21, 25, 35, 49, 63, 81),
        child_text="Odd times odd gives odd.",
        teacher_note="Predicts odd outputs and helps identify possible routes.",
    ),
    "odd_times_even_is_even": Pattern(
        id="odd_times_even_is_even",
        name="Odd × even gives even",
        learner_label="Odd times even gives even",
        short_prompt="Check one even factor",
        stage="A+",
        examples=(6, 10, 14, 18, 30, 40, 56, 70),
        child_text="Odd times even gives even.",
        teacher_note="One even factor is enough to force an even product.",
    ),
    "even_times_even_is_even": Pattern(
        id="even_times_even_is_even",
        name="Even × even gives even",
        learner_label="Even times even gives even",
        short_prompt="Check both even factors",
        stage="B+",
        examples=(4, 8, 12, 16, 24, 32, 48, 64),
        child_text="Even times even gives even.",
        teacher_note="Supports early classification in doubling and scaling families.",
    ),
    "odd_product_excludes_even_route": Pattern(
        id="odd_product_excludes_even_route",
        name="Odd product excludes even routes",
        learner_label="An odd product cannot have an even factor route",
        short_prompt="Rule out impossible routes",
        stage="A+",
        examples=(15, 21, 25, 35, 49, 63, 81),
        child_text="An odd product cannot have an even factor route.",
        teacher_note="Children can reject impossible routes before calculation.",
    ),
    "same_product_different_routes": Pattern(
        id="same_product_different_routes",
        name="Same product, different routes",
        learner_label="Different routes can reach the same product",
        short_prompt="Compare the routes",
        stage="0+",
        examples=(18, 24, 36, 40, 42),
        child_text="Different routes can reach the same product.",
        teacher_note="Makes overlap explicit at the route level, not only the family level.",
    ),
    "route_multiplicity": Pattern(
        id="route_multiplicity",
        name="One product, one or many routes",
        learner_label="A product can have one route family or many",
        short_prompt="How many route families?",
        stage="0+",
        examples=(24, 36, 42, 49),
        child_text="A product can have one route family or many.",
        teacher_note="Distinguishes product identity from route multiplicity and supports structural-role coding.",
    ),
}


PATTERN_ORDER: Final[Tuple[PatternId, ...]] = tuple(PATTERNS.keys())

STAGE_PATTERN_IDS: Final[Dict[str, Tuple[PatternId, ...]]] = {
    "0": (
        "product_hub",
        "route_in_route_out",
        "commutative_switch",
        "boundary_belonging",
        "square_pattern",
        "same_product_different_routes",
        "route_multiplicity",
    ),
    "A": (
        "identity_pattern",
        "parity_structure",
        "odd_times_odd_is_odd",
        "odd_times_even_is_even",
        "odd_product_excludes_even_route",
    ),
    "B": (
        "ten_times_benchmark",
        "even_times_even_is_even",
    ),
    "C": (
        "five_half_ten",
        "five_ends_0_or_5",
    ),
    "D": (
        "nine_quantifier_build",
        "nine_digit_sum",
        "nine_rise_fall",
    ),
    "E": (
        "doubling_chain",
    ),
    "F": (
        "three_digit_sum_cycle",
        "three_odd_even_alternation",
        "six_digit_sum_cycle",
        "six_always_even",
        "six_is_double_three",
        "new_product_or_new_route",
    ),
    "G": (
        "closure_with_7x7",
    ),
    "Across": (
        "use_one_product_for_another",
        "product_family_overlap",
    ),
}


@lru_cache(maxsize=None)
def get_pattern(pattern_id: PatternId) -> Pattern:
    return PATTERNS[pattern_id]


@lru_cache(maxsize=None)
def all_patterns() -> Tuple[Pattern, ...]:
    return tuple(PATTERNS[pattern_id] for pattern_id in PATTERN_ORDER)


@lru_cache(maxsize=None)
def stage_patterns(stage: str) -> Tuple[Pattern, ...]:
    return tuple(PATTERNS[pattern_id] for pattern_id in STAGE_PATTERN_IDS.get(stage, ()))


@lru_cache(maxsize=None)
def pattern_ids_for_stage(stage: str) -> Tuple[PatternId, ...]:
    return STAGE_PATTERN_IDS.get(stage, ())


@lru_cache(maxsize=None)
def product_pattern_ids(product: int) -> Tuple[PatternId, ...]:
    found = {
        "product_hub",
        "route_in_route_out",
        "commutative_switch",
        "boundary_belonging",
        "same_product_different_routes",
        "route_multiplicity",
    }

    families = factor_families(product)
    routes = ways_in(product)
    route_count = len(families)

    if len(routes) > 1:
        found.add("same_product_different_routes")

    if route_count > 1:
        found.add("product_family_overlap")

    if any(a == b for a, b in families):
        found.add("square_pattern")

    stage = stage_of(product)

    for pattern_id in STAGE_PATTERN_IDS.get(stage, ()):
        found.add(pattern_id)

    if structural_role(product) == "closure_hub":
        found.add("closure_with_7x7")

    found.add("parity_structure")

    if product % 2 == 0:
        if any(a % 2 == 0 and b % 2 == 0 for a, b in families):
            found.add("even_times_even_is_even")
        if any((a % 2 == 0 and b % 2 == 1) or (a % 2 == 1 and b % 2 == 0) for a, b in families):
            found.add("odd_times_even_is_even")
    else:
        found.add("odd_times_odd_is_odd")
        found.add("odd_product_excludes_even_route")

    found.add("use_one_product_for_another")

    ordered = [pattern_id for pattern_id in PATTERN_ORDER if pattern_id in found]
    return tuple(ordered)


@lru_cache(maxsize=None)
def product_patterns(product: int):

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

    return tuple(PATTERNS[p] for p in patterns)
