from __future__ import annotations

from typing import Final

from domain.product_metadata import (
    ProductMetadataRecord,
    available_products,
    metadata_summary,
    new_products,
    product_metadata,
    products_for_family_tag,
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

    rotation_index = _request_rotation_index(request)

    selected_products = _select_primary_products(
        stage=request.stage,
        format_id=request.format_id,
        tier=request.tier,
        selection_scope=request.selection_scope,
        mode=mode,
        rotation_index=rotation_index,
    )

    recap_products = _select_recap_products(
        stage=request.stage,
        selected_products=selected_products,
        include_recap=request.include_recap,
        recap_count=request.recap_count,
        rotation_index=rotation_index,
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
            metadata_summary(p) for p in result.selected_products
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
        rotation_index=0,
    )


def _choose_default_mode(
    tier: WorksheetTier,
    format_id: WorksheetFormatId,
    stage: StageId,
) -> ProductSetMode:
    if format_id == "three_product_12":
        stage_defaults: dict[StageId, ProductSetMode] = {
            "A": "square_or_special_focus",
            "B": "same_factor_family",
            "C": "same_stage_products",
            "D": "same_stage_products",
            "E": "doubling_chain",
            "F": "interleave_compare",
            "G": "interleave_compare",
        }

        preferred = stage_defaults[stage]
        if preferred in _ALLOWED_MODES_BY_FORMAT[format_id] and preferred in _STAGE_COMPATIBLE_MODES[stage]:
            return preferred

    if format_id == "one_product_10":
        if stage == "G":
            return "square_or_special_focus"
        return "single_hub"

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
        raise ValueError(f"Mode '{mode}' is not allowed for format '{format_id}'.")
    if mode not in _STAGE_COMPATIBLE_MODES[stage]:
        raise ValueError(f"Mode '{mode}' is not compatible with stage '{stage}'.")


def _request_rotation_index(request: ProductSelectionRequest) -> int:
    raw = getattr(request, "rotation_index", 0)
    if raw is None:
        return 0
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return 0
    return max(0, value)


def _select_primary_products(
    stage: StageId,
    format_id: WorksheetFormatId,
    tier: WorksheetTier,
    selection_scope: SelectionScope,
    mode: ProductSetMode,
    rotation_index: int,
) -> tuple[int, ...]:
    if format_id == "one_product_10":
        selected = _select_single_product(
            stage=stage,
            tier=tier,
            selection_scope=selection_scope,
            mode=mode,
            rotation_index=rotation_index,
        )
        return (selected,)

    target_count = product_count_for_format(format_id)
    return _select_three_products(
        stage=stage,
        tier=tier,
        selection_scope=selection_scope,
        mode=mode,
        target_count=target_count,
        rotation_index=rotation_index,
    )


def _select_single_product(
    stage: StageId,
    tier: WorksheetTier,
    selection_scope: SelectionScope,
    mode: ProductSetMode,
    rotation_index: int,
) -> int:
    primary_candidates, support_candidates = _worksheet_candidate_pools(stage)
    candidates = _single_mode_candidates(
        stage=stage,
        mode=mode,
        primary_candidates=primary_candidates,
        support_candidates=support_candidates,
        selection_scope=selection_scope,
    )

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

    pick_index = _rotating_pick_index(ranked, rotation_index, top_window=12)
    return ranked[pick_index]


def _select_three_products(
    stage: StageId,
    tier: WorksheetTier,
    selection_scope: SelectionScope,
    mode: ProductSetMode,
    target_count: int,
    rotation_index: int,
) -> tuple[int, ...]:
    primary_candidates, support_candidates = _worksheet_candidate_pools(stage)

    triples = _three_product_mode_candidates(
        stage=stage,
        mode=mode,
        primary_candidates=primary_candidates,
        support_candidates=support_candidates,
        selection_scope=selection_scope,
    )

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

    pick_index = _rotating_pick_index(ranked, rotation_index, top_window=16)
    return ranked[pick_index]


def _worksheet_candidate_pools(stage: StageId) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """
    Returns:
        primary_candidates: stage-shaped focus pool
        support_candidates: cumulative lawful support pool
    """
    available = set(available_products(stage))
    stage_new = tuple(p for p in new_products(stage) if p in available)

    if stage == "A":
        primary = stage_new
        support = tuple(p for p in available_products(stage) if p in available)
        return primary, support

    if stage == "B":
        primary = _ordered_unique(
            tuple(p for p in products_for_family_tag("times_10", stage) if p in available) + stage_new
        )
        support = tuple(p for p in available_products(stage) if p in available)
        return primary, support

    if stage == "C":
        primary = _ordered_unique(
            tuple(p for p in products_for_family_tag("times_5", stage) if p in available) + stage_new
        )
        support = tuple(p for p in available_products(stage) if p in available)
        return primary, support

    if stage == "D":
        primary = _ordered_unique(
            tuple(p for p in products_for_family_tag("times_9", stage) if p in available) + stage_new
        )
        support = tuple(p for p in available_products(stage) if p in available)
        return primary, support

    if stage == "E":
        doubling = tuple(p for p in (12, 24, 48, 16, 32, 64) if p in available)
        primary = _ordered_unique(stage_new + doubling)
        support = tuple(p for p in available_products(stage) if p in available)
        return primary, support

    if stage == "F":
        interleave = tuple(p for p in (21, 24, 27, 30, 36, 42, 48, 54) if p in available)
        primary = _ordered_unique(stage_new + interleave)
        support = tuple(
            p for p in available_products(stage)
            if p in available and p not in primary
        )
        return primary, support

    if stage == "G":
        closure = tuple(p for p in (14, 21, 28, 35, 42, 49, 56, 63, 70) if p in available)
        squares = tuple(p for p in (25, 36, 49, 64) if p in available)
        primary = _ordered_unique(stage_new + closure + squares)
        support = tuple(
            p for p in available_products(stage)
            if p in available and p not in primary
        )
        return primary, support

    raise ValueError(f"Unsupported stage '{stage}'.")


def _single_mode_candidates(
    stage: StageId,
    mode: ProductSetMode,
    primary_candidates: tuple[int, ...],
    support_candidates: tuple[int, ...],
    selection_scope: SelectionScope,
) -> list[int]:
    primary_set = set(primary_candidates)
    support_set = set(support_candidates)
    available_set = primary_set | support_set

    if mode == "single_hub":
        ranked = recommended_single_hub_products(stage)
        stage_shaped = [p for p in ranked if p in primary_set]
        if stage_shaped:
            if selection_scope == "available_mixed":
                return stage_shaped + [p for p in ranked if p in support_set and p not in stage_shaped]
            return stage_shaped
        return [p for p in ranked if p in available_set]

    if mode == "square_or_special_focus":
        if stage == "G":
            preferred_g = [p for p in (49, 42, 56, 35, 36, 64, 25) if p in available_set]
            if preferred_g:
                return preferred_g

        stage_squares = [p for p in square_products(stage) if p in available_set]
        stage_shaped = [p for p in stage_squares if p in primary_set]
        if stage_shaped:
            return stage_shaped

        if stage_squares:
            return stage_squares

        ranked = recommended_single_hub_products(stage)
        return [p for p in ranked if p in available_set]

    raise ValueError(f"Mode '{mode}' is not a valid one-product selection mode.")


def _three_product_mode_candidates(
    stage: StageId,
    mode: ProductSetMode,
    primary_candidates: tuple[int, ...],
    support_candidates: tuple[int, ...],
    selection_scope: SelectionScope,
) -> list[tuple[int, ...]]:
    primary_set = set(primary_candidates)
    support_set = set(support_candidates)
    available_set = primary_set | support_set

    if mode == "same_stage_products":
        stage_products = tuple(p for p in new_products(stage) if p in available_set)
        triples = _sliding_triples(stage_products)
        if triples:
            return triples

        if selection_scope == "available_mixed":
            expanded = _ordered_unique(primary_candidates + support_candidates)
            return _sliding_triples(expanded)

        return []

    if mode == "same_factor_family":
        triples: list[tuple[int, ...]] = []
        family_preferences = {
            "A": ("times_1", "times_2"),
            "B": ("times_10", "times_5", "times_2"),
            "C": ("times_5", "times_10", "times_2"),
            "D": ("times_9", "times_3", "times_6"),
            "E": ("times_2", "times_4", "times_8"),
            "F": ("times_3", "times_6", "times_9"),
            "G": ("times_7", "times_8", "times_9"),
        }[stage]

        for family_tag in family_preferences:
            family_products = tuple(
                p for p in products_for_family_tag(family_tag, stage) if p in available_set
            )
            if selection_scope != "available_mixed":
                family_products = tuple(p for p in family_products if p in primary_set)
            triples.extend(_sliding_triples(family_products))

        return _dedupe_triples(triples)

    if mode == "multi_route_compare":
        multi_route = tuple(
            p for p in recommended_multi_route_compare_products(stage)
            if p in available_set
        )

        if selection_scope == "available_mixed":
            triples = _sliding_triples(multi_route)
        else:
            triples = _sliding_triples(tuple(p for p in multi_route if p in primary_set))

        if triples:
            return _dedupe_triples(triples)

        fallback = tuple(
            p for p in _ordered_unique(primary_candidates + support_candidates)
            if p in available_set and (
                product_metadata(p).has_multiple_routes or product_metadata(p).is_square
            )
        )
        return _dedupe_triples(_sliding_triples(fallback))

    if mode == "doubling_chain":
        candidates = [
            triple for triple in (
                (12, 24, 48),
                (16, 32, 64),
                (6, 12, 24),
                (24, 48, 96),
            )
            if all(p in available_set for p in triple)
        ]
        filtered = [triple for triple in candidates if any(p in primary_set for p in triple)]
        return _dedupe_triples(filtered or candidates)

    if mode == "interleave_compare":
        if stage == "F":
            candidates = [
                triple for triple in (
                    (21, 24, 42),
                    (21, 27, 42),
                    (21, 30, 42),
                    (21, 36, 42),
                    (24, 36, 42),
                    (27, 36, 54),
                    (30, 36, 42),
                    (24, 30, 48),
                )
                if all(p in available_set for p in triple)
            ]
            filtered = [triple for triple in candidates if sum(int(p in primary_set) for p in triple) >= 2]
            return _dedupe_triples(filtered or candidates)

        if stage == "G":
            candidates = [
                triple for triple in (
                    (21, 42, 49),
                    (28, 42, 56),
                    (35, 42, 49),
                    (35, 49, 56),
                    (21, 35, 49),
                    (42, 49, 56),
                    (28, 35, 49),
                    (21, 28, 42),
                )
                if all(p in available_set for p in triple)
            ]
            filtered = [triple for triple in candidates if sum(int(p in primary_set) for p in triple) >= 2]
            return _dedupe_triples(filtered or candidates)

        candidates = [
            triple for triple in (
                (21, 24, 42),
                (21, 36, 42),
                (21, 42, 49),
            )
            if all(p in available_set for p in triple)
        ]
        return _dedupe_triples(candidates)

    if mode == "square_or_special_focus":
        candidates: list[tuple[int, ...]] = []

        if stage == "G":
            candidates.extend(
                [
                    triple for triple in (
                        (35, 42, 49),
                        (42, 49, 56),
                        (25, 42, 49),
                        (36, 42, 49),
                        (36, 49, 56),
                        (25, 49, 64),
                    )
                    if all(p in available_set for p in triple)
                ]
            )

        candidates.extend(
            [
                triple for triple in (
                    (16, 25, 36),
                    (25, 36, 49),
                    (36, 49, 64),
                    (25, 49, 64),
                )
                if all(p in available_set for p in triple)
            ]
        )

        if selection_scope != "available_mixed":
            filtered = [triple for triple in candidates if any(p in primary_set for p in triple)]
            if filtered:
                return _dedupe_triples(filtered)

        if candidates:
            return _dedupe_triples(candidates)

        squares = tuple(p for p in square_products(stage) if p in available_set)
        return _dedupe_triples(_sliding_triples(squares))

    raise ValueError(f"Unsupported three-product selection mode '{mode}'.")


def _select_recap_products(
    stage: StageId,
    selected_products: tuple[int, ...],
    include_recap: bool,
    recap_count: int,
    rotation_index: int,
) -> tuple[int, ...]:
    if not include_recap or recap_count == 0:
        return ()

    primary_candidates, support_candidates = _worksheet_candidate_pools(stage)
    selected_set = set(selected_products)
    primary_set = set(primary_candidates)

    recap_pool = [
        p for p in support_candidates
        if p not in selected_set
    ]

    if stage in ("F", "G"):
        preferred_recap = [
            p for p in recap_pool
            if p not in primary_set and not product_metadata(p).has_factor_7
        ]
        if preferred_recap:
            recap_pool = preferred_recap

    ranked = sorted(
        recap_pool,
        key=lambda p: (-_recap_priority_score(p, stage), p),
    )

    if not ranked:
        return ()

    windows = _rotating_windows(
        ranked_items=ranked,
        size=recap_count,
        rotation_index=rotation_index,
        max_windows=12,
    )
    if not windows:
        return tuple(ranked[:recap_count])

    return tuple(windows[0])


def _recap_priority_score(product_value: int, stage: StageId) -> int:
    record = product_metadata(product_value)
    score = 0

    score += _hub_band_rank(record.hub_band) * 10
    score += int(record.has_multiple_routes) * 8
    score += int(record.is_square) * 6

    if stage in ("F", "G") and record.has_factor_7:
        score -= 10

    if record.stage_introduced == stage:
        score -= 20

    return score


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
        score += 12
    if record.stage_introduced == stage:
        score += 8
    if selection_scope == "hybrid" and record.stage_introduced != stage:
        score += 1
    if selection_scope == "available_mixed" and record.stage_introduced == stage:
        score += 4

    if stage == "G":
        if product == 49:
            score += 40
        if record.has_factor_7:
            score += 16
        if product in (35, 42, 56):
            score += 12

    if stage == "F":
        if product in (21, 42, 36, 24, 27, 30):
            score += 12

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
        if stage in ("F", "G") and record.has_factor_7:
            score += 6

    return score


def _coherence_score(
    products: tuple[int, ...],
    stage: StageId,
    tier: WorksheetTier,
    mode: ProductSetMode,
    selection_scope: SelectionScope,
) -> int:
    records = tuple(product_metadata(p) for p in products)
    score = 0

    score += len(_shared_family_tags(records)) * 8
    score += len(_shared_structural_tags(records)) * 8
    score += len(_supported_required_vocab(records, stage)) * 5
    score += sum(_hub_band_rank(record.hub_band) for record in records)
    score += sum(int(record.has_multiple_routes) for record in records) * 4
    score += sum(int(record.is_square) for record in records) * 3
    score += sum(int(record.has_factor_7) for record in records) * 2

    if selection_scope == "new_only":
        score += sum(int(record.stage_introduced == stage) for record in records) * 8
    elif selection_scope == "hybrid":
        stage_new_products = {record.product for record in records if record.stage_introduced == stage}
        stage_old_products = {record.product for record in records if record.stage_introduced != stage}
        if stage_new_products and stage_old_products:
            score += 10
    elif selection_scope == "available_mixed":
        score += sum(int(record.stage_introduced == stage) for record in records) * 4

    if mode == "same_stage_products":
        if all(record.stage_introduced == stage for record in records):
            score += 20

    if mode == "same_factor_family" and _shared_family_tags(records):
        score += 18

    if mode == "multi_route_compare":
        score += sum(int(record.has_multiple_routes) for record in records) * 5

    if mode == "doubling_chain" and _matches_known_doubling_chain(products):
        score += 25

    if mode == "interleave_compare":
        if stage == "F" and any(record.product in (21, 24, 27, 30, 36, 42, 48, 54) for record in records):
            score += 24
        if stage == "G" and any(record.has_factor_7 for record in records):
            score += 24

    if mode == "square_or_special_focus" and any(record.is_square for record in records):
        score += 20

    if stage == "F":
        score += sum(int(record.product in (21, 24, 27, 30, 36, 42, 48, 54)) for record in records) * 10

    if stage == "G":
        score += sum(int(record.has_factor_7) for record in records) * 18
        if any(record.product == 49 for record in records):
            score += 35
        if {42, 49}.issubset({record.product for record in records}):
            score += 16
        if {35, 49}.issubset({record.product for record in records}):
            score += 12
        if {42, 56}.issubset({record.product for record in records}):
            score += 10

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
        if stage in ("F", "G") and any(record.has_factor_7 for record in records):
            score += 10

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

    if stage == "F":
        reasons.append(
            "Stage F selection prioritises interleaving structure around 3× and 6× relationships."
        )

    if stage == "G":
        reasons.append(
            "Stage G selection prioritises closure, 7-times structure, and final-key products."
        )

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
        records = tuple(product_metadata(p) for p in selected_products)
        reasons.append(
            f"Selected products {selected_products} form a structurally coherent set for mode '{mode}'."
        )

        shared_families = _shared_family_tags(records)
        if shared_families:
            reasons.append(f"Shared family tags: {', '.join(shared_families)}.")

        shared_structural = _shared_structural_tags(records)
        if shared_structural:
            reasons.append(f"Shared structural tags: {', '.join(shared_structural)}.")

        required_vocab = _supported_required_vocab(records, stage)
        if required_vocab:
            reasons.append(
                f"Supports stage vocabulary focus: {', '.join(required_vocab)}."
            )

    if recap_products:
        reasons.append(
            f"Recap products included: {', '.join(str(p) for p in recap_products)}."
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
        if any(
            word.lower() in {tag.lower() for tag in product_metadata(p).vocab_tags}
            for p in all_products
        ):
            supported_words.append(word)

    for p in all_products:
        for word in product_metadata(p).vocab_tags:
            if word in available and word not in supported_words:
                supported_words.append(word)

    return tuple(supported_words)


def _combined_structural_tags(
    selected_products: tuple[int, ...],
    recap_products: tuple[int, ...],
) -> tuple[str, ...]:
    ordered: list[str] = []
    for p in selected_products + recap_products:
        for tag in product_metadata(p).structural_tags:
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
        if any(
            word.lower() in {tag.lower() for tag in record.vocab_tags}
            for record in records
        ):
            supported.append(word)
    return tuple(supported)


def _matches_known_doubling_chain(products: tuple[int, ...]) -> bool:
    normalized = tuple(sorted(products))
    return normalized in (
        tuple(sorted((12, 24, 48))),
        tuple(sorted((16, 32, 64))),
    )


def _rotating_pick_index(
    ranked_items: list[object],
    rotation_index: int,
    top_window: int = 8,
) -> int:
    if not ranked_items:
        raise ValueError("Cannot pick from an empty ranked candidate list.")
    usable_window = min(len(ranked_items), max(1, top_window))
    return rotation_index % usable_window


def _rotating_windows(
    ranked_items: list[int],
    size: int,
    rotation_index: int,
    max_windows: int = 12,
) -> list[tuple[int, ...]]:
    if size <= 0 or len(ranked_items) < size:
        return []

    windows: list[tuple[int, ...]] = []
    limit = min(max_windows, len(ranked_items) - size + 1)
    for idx in range(limit):
        start = (rotation_index + idx) % (len(ranked_items) - size + 1)
        window = tuple(ranked_items[start:start + size])
        if len(window) == size and window not in windows:
            windows.append(window)
    return windows


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
            triples.append(tuple(sorted(triple)))
    return _dedupe_triples(triples)


def _ordered_unique(values: tuple[int, ...]) -> tuple[int, ...]:
    seen: set[int] = set()
    ordered: list[int] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return tuple(ordered)


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
