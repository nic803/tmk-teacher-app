from __future__ import annotations

from typing import Final

from domain.product_metadata import (
    ProductMetadataRecord,
    available_products,
    metadata_summary,
    multi_route_products,
    new_products,
    product_metadata,
    products_for_family_tag,
    products_for_structural_tag,
    products_supporting_vocab,
    recommended_multi_route_compare_products,
    recommended_single_hub_products,
    square_products,
)
from domain.stage_vocabulary import available_vocab as stage_available_vocab
from domain.stage_vocabulary import required_vocab_focus as stage_required_vocab_focus
from domain.worksheet_formats import product_count_for_format
from models.worksheet_models import (
    ProductSelectionRequest,
    ProductSelectionResult,
    ProductSetMode,
    SelectionScope,
    StageId,
    WorksheetFormatId,
    WorksheetTier,
    validate_product_set_mode,
    validate_selection_request,
    validate_selection_result,
)


_ALLOWED_MODES_BY_FORMAT: Final[dict[WorksheetFormatId, tuple[ProductSetMode, ...]]] = {
    "one_product_10": (
        "single_hub",
        "square_or_special_focus",
    ),
    "three_product_12": (
        "same_factor_family",
        "same_stage_products",
        "multi_route_compare",
        "doubling_chain",
        "interleave_compare",
        "square_or_special_focus",
    ),
}


_TIER_PREFERRED_MODES: Final[dict[WorksheetTier, tuple[ProductSetMode, ...]]] = {
    "Support": (
        "single_hub",
        "same_factor_family",
        "same_stage_products",
        "doubling_chain",
        "square_or_special_focus",
    ),
    "Core": (
        "single_hub",
        "same_factor_family",
        "multi_route_compare",
        "same_stage_products",
        "square_or_special_focus",
        "interleave_compare",
        "doubling_chain",
    ),
    "Extension": (
        "multi_route_compare",
        "interleave_compare",
        "square_or_special_focus",
        "same_factor_family",
        "same_stage_products",
        "doubling_chain",
        "single_hub",
    ),
}


_STAGE_COMPATIBLE_MODES: Final[dict[StageId, tuple[ProductSetMode, ...]]] = {
    "A": ("single_hub", "square_or_special_focus"),
    "B": ("single_hub", "same_factor_family", "square_or_special_focus"),
    "C": ("single_hub", "same_stage_products", "same_factor_family", "square_or_special_focus"),
    "D": ("single_hub", "same_stage_products", "same_factor_family", "multi_route_compare", "square_or_special_focus"),
    "E": ("single_hub", "same_stage_products", "doubling_chain", "multi_route_compare", "square_or_special_focus"),
    "F": ("single_hub", "same_stage_products", "interleave_compare", "multi_route_compare", "square_or_special_focus"),
    "G": ("single_hub", "square_or_special_focus", "multi_route_compare", "interleave_compare"),
}


def select_product_set(request: ProductSelectionRequest) -> ProductSelectionResult:
    validate_selection_request(request)

    mode = request.selection_mode or _choose_default_mode(
        tier=request.tier,
        format_id=request.format_id,
        stage=request.stage,
    )
    validate_product_set_mode(mode)

    _validate_mode_allowed_for_request(
        mode=mode,
        stage=request.stage,
        format_id=request.format_id,
    )

    base_candidates = _base_candidates_for_scope(
        stage=request.stage,
        selection_scope=request.selection_scope,
    )

    selected_products = _select_primary_products(
        stage=request.stage,
        format_id=request.format_id,
        tier=request.tier,
        selection_scope=request.selection_scope,
        mode=mode,
        base_candidates=base_candidates,
    )

    recap_products = _select_recap_products(
        stage=request.stage,
        selected_products=selected_products,
        include_recap=request.include_recap,
        recap_count=request.recap_count,
    )

    reasons = _selection_reasons(
        stage=request.stage,
        format_id=request.format_id,
        tier=request.tier,
        selection_scope=request.selection_scope,
        mode=mode,
        selected_products=selected_products,
        recap_products=recap_products,
    )

    vocab_supported = _vocab_supported_for_products(
        stage=request.stage,
        selected_products=selected_products,
        recap_products=recap_products,
    )

    structural_tags = _combined_structural_tags(
        selected_products=selected_products,
        recap_products=recap_products,
    )

    result = ProductSelectionResult(
        stage=request.stage,
        format_id=request.format_id,
        tier=request.tier,
        selection_scope=request.selection_scope,
        selection_mode=mode,
        selected_products=selected_products,
        recap_products=recap_products,
        selection_reasons=reasons,
        vocab_supported=vocab_supported,
        structural_tags=structural_tags,
    )
    validate_selection_result(result)
    return result


def available_selection_modes(
    stage: StageId,
    format_id: WorksheetFormatId,
    tier: WorksheetTier,
) -> tuple[ProductSetMode, ...]:
    allowed_for_format = set(_ALLOWED_MODES_BY_FORMAT[format_id])
    allowed_for_stage = set(_STAGE_COMPATIBLE_MODES[stage])
    preferred_for_tier = _TIER_PREFERRED_MODES[tier]

    return tuple(
        mode
        for mode in preferred_for_tier
        if mode in allowed_for_format and mode in allowed_for_stage
    )


def explain_selection_request(request: ProductSelectionRequest) -> dict[str, object]:
    result = select_product_set(request)
    return {
        "stage": result.stage,
        "format_id": result.format_id,
        "tier": result.tier,
        "selection_scope": result.selection_scope,
        "selection_mode": result.selection_mode,
        "selected_products": result.selected_products,
        "recap_products": result.recap_products,
        "selection_reasons": result.selection_reasons,
        "vocab_supported": result.vocab_supported,
        "structural_tags": result.structural_tags,
        "selected_product_metadata": tuple(
            metadata_summary(product) for product in result.selected_products
        ),
    }


def recommended_request(
    stage: StageId,
    format_id: WorksheetFormatId,
    tier: WorksheetTier,
    selection_scope: SelectionScope,
    include_recap: bool = False,
    recap_count: int = 0,
) -> ProductSelectionRequest:
    return ProductSelectionRequest(
        stage=stage,
        format_id=format_id,
        tier=tier,
        selection_scope=selection_scope,
        include_recap=include_recap,
        recap_count=recap_count,
        selection_mode=None,
    )


def _choose_default_mode(
    tier: WorksheetTier,
    format_id: WorksheetFormatId,
    stage: StageId,
) -> ProductSetMode:
    allowed = available_selection_modes(stage=stage, format_id=format_id, tier=tier)
    if not allowed:
        raise ValueError(
            f"No selection modes available for stage '{stage}', format '{format_id}', tier '{tier}'."
        )
    return allowed[0]


def _validate_mode_allowed_for_request(
    mode: ProductSetMode,
    stage: StageId,
    format_id: WorksheetFormatId,
) -> None:
    if mode not in _ALLOWED_MODES_BY_FORMAT[format_id]:
        raise ValueError(
            f"Mode '{mode}' is not allowed for format '{format_id}'."
        )
    if mode not in _STAGE_COMPATIBLE_MODES[stage]:
        raise ValueError(
            f"Mode '{mode}' is not compatible with stage '{stage}'."
        )


def _base_candidates_for_scope(
    stage: StageId,
    selection_scope: SelectionScope,
) -> tuple[int, ...]:
    if selection_scope == "new_only":
        return new_products(stage)
    if selection_scope == "available_mixed":
        return available_products(stage)
    if selection_scope == "hybrid":
        return available_products(stage)
    raise ValueError(f"Unsupported selection_scope '{selection_scope}'.")


def _select_primary_products(
    stage: StageId,
    format_id: WorksheetFormatId,
    tier: WorksheetTier,
    selection_scope: SelectionScope,
    mode: ProductSetMode,
    base_candidates: tuple[int, ...],
) -> tuple[int, ...]:
    if format_id == "one_product_10":
        product = _select_single_product(
            stage=stage,
            tier=tier,
            selection_scope=selection_scope,
            mode=mode,
            base_candidates=base_candidates,
        )
        return (product,)

    target_count = product_count_for_format(format_id)
    triple = _select_three_products(
        stage=stage,
        tier=tier,
        selection_scope=selection_scope,
        mode=mode,
        base_candidates=base_candidates,
        target_count=target_count,
    )
    return triple


def _select_single_product(
    stage: StageId,
    tier: WorksheetTier,
    selection_scope: SelectionScope,
    mode: ProductSetMode,
    base_candidates: tuple[int, ...],
) -> int:
    candidates = _single_mode_candidates(
        stage=stage,
        mode=mode,
        base_candidates=base_candidates,
    )

    if selection_scope == "hybrid":
        preferred_new = [p for p in candidates if p in set(new_products(stage))]
        if preferred_new:
            candidates = preferred_new

    ranked = sorted(
        candidates,
        key=lambda p: _single_hub_score(
            product=p,
            stage=stage,
            tier=tier,
            selection_scope=selection_scope,
        ),
        reverse=True,
    )

    if not ranked:
        raise ValueError(
            f"No valid single-product candidates for stage '{stage}', mode '{mode}', scope '{selection_scope}'."
        )

    return ranked[0]


def _select_three_products(
    stage: StageId,
    tier: WorksheetTier,
    selection_scope: SelectionScope,
    mode: ProductSetMode,
    base_candidates: tuple[int, ...],
    target_count: int,
) -> tuple[int, ...]:
    triples = _three_product_mode_candidates(
        stage=stage,
        mode=mode,
        base_candidates=base_candidates,
    )

    if selection_scope == "hybrid":
        stage_new = set(new_products(stage))
        triples = [
            triple for triple in triples
            if any(product in stage_new for product in triple)
            and any(product not in stage_new for product in triple)
        ]

    if selection_scope == "new_only":
        stage_new = set(new_products(stage))
        triples = [
            triple for triple in triples
            if all(product in stage_new for product in triple)
        ]

    triples = [triple for triple in triples if len(triple) == target_count]

    ranked = sorted(
        triples,
        key=lambda triple: _coherence_score(
            products=triple,
            stage=stage,
            tier=tier,
            mode=mode,
            selection_scope=selection_scope,
        ),
        reverse=True,
    )

    if not ranked:
        raise ValueError(
            f"No valid three-product candidates for stage '{stage}', mode '{mode}', scope '{selection_scope}'."
        )

    return ranked[0]


def _single_mode_candidates(
    stage: StageId,
    mode: ProductSetMode,
    base_candidates: tuple[int, ...],
) -> list[int]:
    candidate_set = set(base_candidates)

    if mode == "single_hub":
        ranked = recommended_single_hub_products(stage)
        return [product for product in ranked if product in candidate_set]

    if mode == "square_or_special_focus":
        squares = square_products(stage)
        preferred = [product for product in squares if product in candidate_set]
        if preferred:
            return list(preferred)

        ranked = recommended_single_hub_products(stage)
        return [product for product in ranked if product in candidate_set]

    raise ValueError(
        f"Mode '{mode}' is not a valid one-product selection mode."
    )


def _three_product_mode_candidates(
    stage: StageId,
    mode: ProductSetMode,
    base_candidates: tuple[int, ...],
) -> list[tuple[int, ...]]:
    candidate_set = set(base_candidates)

    if mode == "same_stage_products":
        stage_products = tuple(
            product for product in new_products(stage) if product in candidate_set
        )
        return _sliding_triples(stage_products)

    if mode == "same_factor_family":
        triples: list[tuple[int, ...]] = []
        family_preferences = (
            "times_9",
            "times_8",
            "times_5",
            "times_7",
            "times_4",
            "times_3",
            "times_2",
        )
        for family_tag in family_preferences:
            products = tuple(
                p for p in products_for_family_tag(family_tag, stage) if p in candidate_set
            )
            triples.extend(_sliding_triples(products))
        return _dedupe_triples(triples)

    if mode == "multi_route_compare":
        multi_route = tuple(
            product for product in recommended_multi_route_compare_products(stage)
            if product in candidate_set
        )
        triples = _sliding_triples(multi_route)
        if triples:
            return triples

        squares_and_multi = tuple(
            product for product in available_products(stage)
            if product in candidate_set
            and (
                product_metadata(product).has_multiple_routes
                or product_metadata(product).is_square
            )
        )
        return _sliding_triples(squares_and_multi)

    if mode == "doubling_chain":
        candidates = [
            triple for triple in (
                (12, 24, 48),
                (16, 32, 64),
            )
            if all(product in candidate_set for product in triple)
        ]
        return candidates

    if mode == "interleave_compare":
        preferred = [
            triple for triple in (
                (21, 24, 42),
                (21, 36, 42),
                (21, 42, 49),
            )
            if all(product in candidate_set for product in triple)
        ]
        return preferred

    if mode == "square_or_special_focus":
        candidates = [
            triple for triple in (
                (25, 36, 49),
                (16, 25, 36),
                (36, 49, 64),
            )
            if all(product in candidate_set for product in triple)
        ]
        if candidates:
            return candidates

        squares = tuple(product for product in square_products(stage) if product in candidate_set)
        return _sliding_triples(squares)

    raise ValueError(f"Unsupported three-product selection mode '{mode}'.")


def _select_recap_products(
    stage: StageId,
    selected_products: tuple[int, ...],
    include_recap: bool,
    recap_count: int,
) -> tuple[int, ...]:
    if not include_recap or recap_count == 0:
        return ()

    stage_new = set(new_products(stage))
    recap_pool = [
        product for product in available_products(stage)
        if product not in stage_new and product not in set(selected_products)
    ]

    ranked = sorted(
        recap_pool,
        key=lambda p: (
            -_hub_band_rank(product_metadata(p).hub_band),
            -int(product_metadata(p).has_multiple_routes),
            product_metadata(p).product,
        ),
    )

    return tuple(ranked[:recap_count])


def _single_hub_score(
    product: int,
    stage: StageId,
    tier: WorksheetTier,
    selection_scope: SelectionScope,
) -> int:
    record = product_metadata(product)
    score = 0

    score += _hub_band_rank(record.hub_band) * 10
    score += _route_profile_rank(record.route_profile) * 5
    score += len(record.known_routes_at_stage) * 3
    score += len(set(record.vocab_tags).intersection(stage_required_vocab_focus(stage))) * 4

    if record.is_square:
        score += 4
    if record.has_factor_7 and stage in ("F", "G"):
        score += 3
    if record.stage_introduced == stage:
        score += 6
    if selection_scope == "hybrid" and record.stage_introduced != stage:
        score += 1

    if tier == "Support":
        if record.has_multiple_routes:
            score -= 1
        if record.hub_band == "high":
            score += 1
    elif tier == "Core":
        if record.has_multiple_routes:
            score += 2
    elif tier == "Extension":
        if record.has_multiple_routes:
            score += 4
        if record.is_square:
            score += 2

    return score


def _coherence_score(
    products: tuple[int, ...],
    stage: StageId,
    tier: WorksheetTier,
    mode: ProductSetMode,
    selection_scope: SelectionScope,
) -> int:
    records = tuple(product_metadata(product) for product in products)
    score = 0

    score += len(_shared_family_tags(records)) * 8
    score += len(_shared_structural_tags(records)) * 8
    score += len(_supported_required_vocab(records, stage)) * 5
    score += sum(_hub_band_rank(record.hub_band) for record in records)
    score += sum(int(record.has_multiple_routes) for record in records) * 4
    score += sum(int(record.is_square) for record in records) * 3
    score += sum(int(record.has_factor_7) for record in records) * 2

    if selection_scope == "new_only":
        score += sum(int(record.stage_introduced == stage) for record in records) * 5
    elif selection_scope == "hybrid":
        stage_new = {record.product for record in records if record.stage_introduced == stage}
        stage_old = {record.product for record in records if record.stage_introduced != stage}
        if stage_new and stage_old:
            score += 10

    if mode == "same_stage_products":
        if all(record.stage_introduced == stage for record in records):
            score += 20

    if mode == "same_factor_family" and _shared_family_tags(records):
        score += 18

    if mode == "multi_route_compare":
        score += sum(int(record.has_multiple_routes) for record in records) * 5

    if mode == "doubling_chain":
        if _matches_known_doubling_chain(products):
            score += 25

    if mode == "interleave_compare":
        if any(record.stage_introduced == "F" for record in records):
            score += 20

    if mode == "square_or_special_focus":
        if any(record.is_square for record in records):
            score += 20

    if tier == "Support":
        score -= sum(int(record.has_multiple_routes) for record in records)
        if mode in ("same_factor_family", "same_stage_products", "doubling_chain"):
            score += 8

    if tier == "Core":
        if any(record.has_multiple_routes for record in records):
            score += 6

    if tier == "Extension":
        if any(record.is_square for record in records):
            score += 6
        if len(_shared_structural_tags(records)) > 0:
            score += 6
        if any(record.has_multiple_routes for record in records):
            score += 8

    return score


def _selection_reasons(
    stage: StageId,
    format_id: WorksheetFormatId,
    tier: WorksheetTier,
    selection_scope: SelectionScope,
    mode: ProductSetMode,
    selected_products: tuple[int, ...],
    recap_products: tuple[int, ...],
) -> tuple[str, ...]:
    reasons: list[str] = [
        f"Selection mode: {mode}.",
        f"Selection scope: {selection_scope}.",
        f"Format: {format_id}.",
        f"Tier: {tier}.",
    ]

    if format_id == "one_product_10":
        record = product_metadata(selected_products[0])
        reasons.append(
            f"Product {record.product} was chosen as a worksheet hub with hub band '{record.hub_band}'."
        )
        if record.has_multiple_routes:
            reasons.append(
                f"Product {record.product} supports another-way or compare-routes tasks."
            )
        if record.is_square:
            reasons.append(
                f"Product {record.product} supports square-focused vocabulary or recognition."
            )
        if record.has_factor_7:
            reasons.append(
                f"Product {record.product} supports 7-times structure."
            )
    else:
        records = tuple(product_metadata(product) for product in selected_products)
        reasons.append(
            f"Selected products {selected_products} form a structurally coherent set for mode '{mode}'."
        )

        shared_families = _shared_family_tags(records)
        if shared_families:
            reasons.append(
                f"Shared family tags: {', '.join(shared_families)}."
            )

        shared_structural = _shared_structural_tags(records)
        if shared_structural:
            reasons.append(
                f"Shared structural tags: {', '.join(shared_structural)}."
            )

        required_vocab = _supported_required_vocab(records, stage)
        if required_vocab:
            reasons.append(
                f"Supports stage vocabulary focus: {', '.join(required_vocab)}."
            )

    if recap_products:
        reasons.append(
            f"Recap products included: {', '.join(str(product) for product in recap_products)}."
        )

    return tuple(reasons)


def _vocab_supported_for_products(
    stage: StageId,
    selected_products: tuple[int, ...],
    recap_products: tuple[int, ...],
) -> tuple[str, ...]:
    supported_words: list[str] = []
    all_products = selected_products + recap_products
    required = stage_required_vocab_focus(stage)
    available = set(stage_available_vocab(stage))

    for word in required:
        if word not in available:
            continue
        if any(word.lower() in {tag.lower() for tag in product_metadata(product).vocab_tags} for product in all_products):
            supported_words.append(word)

    for product in all_products:
        for word in product_metadata(product).vocab_tags:
            if word in available and word not in supported_words:
                supported_words.append(word)

    return tuple(supported_words)


def _combined_structural_tags(
    selected_products: tuple[int, ...],
    recap_products: tuple[int, ...],
) -> tuple[str, ...]:
    ordered: list[str] = []
    for product in selected_products + recap_products:
        for tag in product_metadata(product).structural_tags:
            if tag not in ordered:
                ordered.append(tag)
    return tuple(ordered)


def _shared_family_tags(records: tuple[ProductMetadataRecord, ...]) -> tuple[str, ...]:
    if not records:
        return ()
    shared = set(records[0].family_tags)
    for record in records[1:]:
        shared &= set(record.family_tags)
    return tuple(sorted(shared))


def _shared_structural_tags(records: tuple[ProductMetadataRecord, ...]) -> tuple[str, ...]:
    if not records:
        return ()
    shared = set(records[0].structural_tags)
    for record in records[1:]:
        shared &= set(record.structural_tags)
    return tuple(sorted(shared))


def _supported_required_vocab(
    records: tuple[ProductMetadataRecord, ...],
    stage: StageId,
) -> tuple[str, ...]:
    required = stage_required_vocab_focus(stage)
    supported: list[str] = []
    for word in required:
        if any(word.lower() in {tag.lower() for tag in record.vocab_tags} for record in records):
            supported.append(word)
    return tuple(supported)


def _matches_known_doubling_chain(products: tuple[int, ...]) -> bool:
    normalized = tuple(sorted(products))
    return normalized in (
        tuple(sorted((12, 24, 48))),
        tuple(sorted((16, 32, 64))),
    )


def _dedupe_triples(
    triples: list[tuple[int, ...]],
) -> list[tuple[int, ...]]:
    seen: set[tuple[int, ...]] = set()
    deduped: list[tuple[int, ...]] = []
    for triple in triples:
        normalized = tuple(sorted(triple))
        if normalized not in seen:
            seen.add(normalized)
            deduped.append(normalized)
    return deduped


def _sliding_triples(products: tuple[int, ...]) -> list[tuple[int, ...]]:
    if len(products) < 3:
        return []
    triples: list[tuple[int, ...]] = []
    for index in range(len(products) - 2):
        triple = (products[index], products[index + 1], products[index + 2])
        if len(set(triple)) == 3:
            triples.append(triple)
    return triples


def _hub_band_rank(hub_band: str) -> int:
    if hub_band == "high":
        return 3
    if hub_band == "medium":
        return 2
    return 1


def _route_profile_rank(route_profile: str) -> int:
    if route_profile == "multi_route":
        return 3
    if route_profile == "square_route":
        return 2
    return 1
