from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, List, Tuple

from domain.structure import get_product_structure


Tier = str

QuestionSection = Literal[
    "product_first",
    "ways_in",
    "ways_out",
    "structure",
    "belongs",
    "error_repair",
    "sorting",
    "final_explanation",
]


@dataclass(frozen=True)
class QuestionSpec:
    id: int
    tier: Tier
    section: QuestionSection
    prompt: str
    answer: str


@dataclass(frozen=True)
class _QuestionRecord:
    product: int
    intro_route: Tuple[int, int]
    alternate_routes: Tuple[Tuple[int, int], ...]
    stage: str | None = None


def _as_tuple_pair(value: Any) -> Tuple[int, int] | None:
    if isinstance(value, (list, tuple)) and len(value) == 2:
        try:
            return int(value[0]), int(value[1])
        except (TypeError, ValueError):
            return None
    return None


def _normalise_routes(structure: dict[str, Any]) -> Tuple[Tuple[int, int], Tuple[Tuple[int, int], ...]]:
    intro_route_raw = structure.get("intro_route")
    intro_route = _as_tuple_pair(intro_route_raw)

    factor_pairs = structure.get("factor_pairs") or structure.get("routes") or ()
    parsed_pairs: list[Tuple[int, int]] = []

    for item in factor_pairs:
        pair = _as_tuple_pair(item)
        if pair is not None and pair not in parsed_pairs:
            parsed_pairs.append(pair)

    if intro_route is None:
        if parsed_pairs:
            intro_route = parsed_pairs[0]
        else:
            raise ValueError("Structure must include either 'intro_route' or at least one valid factor pair.")

    alternates = tuple(pair for pair in parsed_pairs if pair != intro_route)
    return intro_route, alternates


def _build_record(product: int) -> _QuestionRecord:
    structure = get_product_structure(product)
    if not isinstance(structure, dict):
        raise ValueError("get_product_structure(product) must return a dictionary.")

    if "product" not in structure:
        raise ValueError("Structure dictionary must include 'product'.")

    structure_product = int(structure["product"])
    intro_route, alternate_routes = _normalise_routes(structure)

    return _QuestionRecord(
        product=structure_product,
        intro_route=intro_route,
        alternate_routes=alternate_routes,
        stage=structure.get("stage"),
    )


def _product_first_question(record: _QuestionRecord, tier: Tier, qid: int) -> QuestionSpec:
    left, right = record.intro_route
    return QuestionSpec(
        id=qid,
        tier=tier,
        section="product_first",
        prompt=f"What product is made by {left} × {right}?",
        answer=str(record.product),
    )


def _ways_in_question(record: _QuestionRecord, tier: Tier, qid: int) -> QuestionSpec:
    left, right = record.intro_route
    return QuestionSpec(
        id=qid,
        tier=tier,
        section="ways_in",
        prompt=f"{left} × ? = {record.product}",
        answer=str(right),
    )


def _ways_out_question(record: _QuestionRecord, tier: Tier, qid: int) -> QuestionSpec:
    left, right = record.intro_route
    return QuestionSpec(
        id=qid,
        tier=tier,
        section="ways_out",
        prompt=f"{record.product} ÷ {left} = ?",
        answer=str(right),
    )


def _structure_question(record: _QuestionRecord, tier: Tier, qid: int) -> QuestionSpec:
    if record.alternate_routes:
        alt_left, alt_right = record.alternate_routes[0]
        return QuestionSpec(
            id=qid,
            tier=tier,
            section="structure",
            prompt=f"Give another way into {record.product}. Complete: {alt_left} × ? = {record.product}",
            answer=str(alt_right),
        )

    left, right = record.intro_route
    return QuestionSpec(
        id=qid,
        tier=tier,
        section="structure",
        prompt=f"Complete the structure sentence: {record.product} is made by {left} groups of ?",
        answer=str(right),
    )


def _error_repair_question(record: _QuestionRecord, tier: Tier, qid: int) -> QuestionSpec:
    left, right = record.intro_route

    wrong_right = right + 1
    if wrong_right == right:
        wrong_right += 1

    return QuestionSpec(
        id=qid,
        tier=tier,
        section="error_repair",
        prompt=f"A child says {left} × {wrong_right} = {record.product}. What should it be?",
        answer=f"{left} × {right} = {record.product}",
    )


def _final_explanation_question(record: _QuestionRecord, tier: Tier, qid: int) -> QuestionSpec:
    left, right = record.intro_route
    return QuestionSpec(
        id=qid,
        tier=tier,
        section="final_explanation",
        prompt=f"Explain {record.product} using its route {left} × {right}.",
        answer=f"{left} groups of {right} make {record.product}.",
    )


def _support_sequence(record: _QuestionRecord, tier: Tier) -> List[QuestionSpec]:
    return [
        _product_first_question(record, tier, 1),
        _ways_in_question(record, tier, 2),
        _ways_out_question(record, tier, 3),
        _error_repair_question(record, tier, 4),
        _final_explanation_question(record, tier, 5),
    ]


def _core_sequence(record: _QuestionRecord, tier: Tier) -> List[QuestionSpec]:
    return [
        _product_first_question(record, tier, 1),
        _ways_in_question(record, tier, 2),
        _ways_out_question(record, tier, 3),
        _structure_question(record, tier, 4),
        _final_explanation_question(record, tier, 5),
    ]


def _extension_sequence(record: _QuestionRecord, tier: Tier) -> List[QuestionSpec]:
    return [
        _product_first_question(record, tier, 1),
        _structure_question(record, tier, 2),
        _ways_out_question(record, tier, 3),
        _error_repair_question(record, tier, 4),
        _final_explanation_question(record, tier, 5),
    ]


def generate_worksheet(product: int, tier: Tier) -> List[QuestionSpec]:
    """
    Minimal but properly varied worksheet generator.

    Improvements over the previous version:
    - does not repeat the same question form five times
    - includes both multiplication and inverse division
    - uses alternate routes when available
    - keeps dependencies minimal and robust
    """
    record = _build_record(product)

    if tier == "Support":
        return _support_sequence(record, tier)

    if tier == "Extension":
        return _extension_sequence(record, tier)

    return _core_sequence(record, tier)
