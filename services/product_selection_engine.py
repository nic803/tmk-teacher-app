from __future__ import annotations

from itertools import combinations
from typing import Final, Iterable

from domain.product_banks import (
    CLOSURE_PRODUCTS,
    COMPARISON_READY_PRODUCTS,
    CURATED_STAGE_TRIPLES,
    DOUBLING_CHAIN_PRODUCTS,
    DOUBLING_CHAIN_TRIPLES,
    MULTI_ROUTE_PRODUCTS,
    RECAP_FAMILY_BANKS,
    SPECIAL_FOCUS_PRODUCTS,
    SQUARE_PRODUCTS,
    STAGE_BRIDGE_PRODUCTS,
    TMK_ALL_PRODUCTS,
    BENCHMARK_PRODUCTS,
    BOUNDARY_FOCUS_PRODUCTS,
    cumulative_products_for_stage,
    products_for_stage,
    recap_products_for_stage,
    validate_product_banks,
)
from domain.product_metadata import (
    ProductMetadataRecord,
    metadata_summary,
    product_metadata,
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
        "multi_route_hub",
        "square_product",
        "special_focus",
        "doubling_chain_product",
        "stage_bridge",
        "closure_product",
        "boundary_focus",
        "benchmark_product",
        "comparison_ready",
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
        "square_product",
        "special_focus",
        "multi_route_hub",
        "doubling_chain_product",
        "stage_bridge",
        "closure_product",
        "boundary_focus",
        "benchmark_product",
        "comparison_ready",
        "square_or_special_focus",
        "multi_route_compare",
        "interleave_compare",
    ),
    "Core": (
        "single_hub",
        "multi_route_hub",
        "square_product",
        "special_focus",
        "doubling_chain_product",
        "stage_bridge",
        "closure_product",
        "same_factor_family",
        "same_stage_products",
        "multi_route_compare",
        "doubling_chain",
        "interleave_compare",
        "square_or_special_focus",
        "boundary_focus",
        "benchmark_product",
        "comparison_ready",
    ),
    "Extension": (
        "multi_route_hub",
        "comparison_ready",
        "stage_bridge",
        "square_product",
        "special_focus",
        "closure_product",
        "boundary_focus",
        "benchmark_product",
        "single_hub",
        "multi_route_compare",
        "interleave_compare",
        "square_or_special_focus",
        "same_factor_family",
        "same_stage_products",
        "doubling_chain",
        "doubling_chain_product",
    ),
}

_STAGE_COMPATIBLE_MODES: Final[dict[StageId, tuple[ProductSetMode, ...]]] = {
    "A": (
        "single_hub",
        "multi_route_hub",
        "square_product",
        "special_focus",
        "boundary_focus",
        "benchmark_product",
    ),
    "B": (
        "single_hub",
        "multi_route_hub",
        "square_product",
        "special_focus",
        "benchmark_product",
        "same_factor_family",
        "boundary_focus",
    ),
    "C": (
        "single_hub",
        "multi_route_hub",
        "square_product",
        "special_focus",
        "benchmark_product",
        "same_factor_family",
        "same_stage_products",
        "comparison_ready",
    ),
    "D": (
        "single_hub",
        "multi_route_hub",
        "square_product",
        "special_focus",
        "same_factor_family",
        "same_stage_products",
        "multi_route_compare",
        "comparison_ready",
        "benchmark_product",
    ),
    "E": (
        "single_hub",
        "multi_route_hub",
        "square_product",
        "special_focus",
        "doubling_chain_product",
        "stage_bridge",
        "same_stage_products",
        "same_factor_family",
        "multi_route_compare",
        "doubling_chain",
        "square_or_special_focus",
        "comparison_ready",
    ),
    "F": (
        "single_hub",
        "multi_route_hub",
        "square_product",
        "special_focus",
        "stage_bridge",
        "same_stage_products",
        "same_factor_family",
        "multi_route_compare",
        "interleave_compare",
        "square_or_special_focus",
        "comparison_ready",
    ),
    "G": (
        "single_hub",
        "multi_route_hub",
        "square_product",
        "special_focus",
        "stage_bridge",
        "closure_product",
        "same_factor_family",
        "multi_route_compare",
        "interleave_compare",
        "square_or_special_focus",
        "boundary_focus",
        "comparison_ready",
    ),
}


def select_product_set(request: ProductSelectionRequest) -> ProductSelectionResult:
    validate_product_banks()
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
    validate_product_banks()

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
            "A": "same_stage_products",
            "B": "same_factor_family",
            "C": "same_factor_family",
            "D": "same_stage_products",
            "E": "doubling_chain",
            "F": "interleave_compare",
            "G": "interleave_compare",
        }
        preferred = stage_defaults[stage]
        if preferred in _ALLOWED_MODES_BY_FORMAT[format_id] and preferred in _STAGE_COMPATIBLE_MODES[stage]:
            return preferred

    if format_id == "one_product_10":
        stage_defaults: dict[StageId, ProductSetMode] = {
            "A": "single_hub",
            "B": "benchmark_product",
            "C": "special_focus",
            "D": "multi_route_hub",
            "E": "doubling_chain_product",
            "F": "stage_bridge",
            "G": "closure_product",
        }
        preferred = stage_defaults[stage]
        if preferred in _ALLOWED_MODES_BY_FORMAT[format_id] and preferred in _STAGE_COMPATIBLE_MODES[stage]:
            return preferred

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
    pool = _primary_scope_pool(stage, selection_scope)
    candidates = _single_mode_candidates(stage, mode, pool)

    if not candidates:
        raise ValueError(
            f"No valid single-product candidates for stage '{stage}', mode '{mode}', scope '{selection_scope}'."
        )

    stage_new = set(products_for_stage(stage))
    stage_recap = set(recap_products_for_stage(stage))

    ranked = sorted(
        _ordered_unique(candidates),
        key=lambda p: _single_hub_score(
            product=p,
            stage=stage,
            tier=tier,
            selection_scope=selection_scope,
            is_stage_new=(p in stage_new),
            is_stage_recap=(p in stage_recap),
            mode=mode,
        ),
        reverse=True,
    )

    return ranked[rotation_index % len(ranked)]


def _single_mode_candidates(
    stage: StageId,
    mode: ProductSetMode,
    pool: list[int],
) -> list[int]:
    cumulative = set(cumulative_products_for_stage(stage))

    if mode == "single_hub":
        return list(pool)

    if mode == "multi_route_hub":
        return [p for p in pool if p in MULTI_ROUTE_PRODUCTS]

    if mode == "square_product":
        return [p for p in pool if p in SQUARE_PRODUCTS]

    if mode == "special_focus":
        return [p for p in pool if p in SPECIAL_FOCUS_PRODUCTS]

    if mode == "doubling_chain_product":
        return [p for p in pool if p in DOUBLING_CHAIN_PRODUCTS]

    if mode == "stage_bridge":
        return [p for p in pool if p in STAGE_BRIDGE_PRODUCTS]

    if mode == "closure_product":
        return [p for p in pool if p in CLOSURE_PRODUCTS]

    if mode == "boundary_focus":
        return [p for p in pool if p in BOUNDARY_FOCUS_PRODUCTS]

    if mode == "benchmark_product":
        return [p for p in pool if p in BENCHMARK_PRODUCTS]

    if mode == "comparison_ready":
        return [p for p in pool if p in COMPARISON_READY_PRODUCTS]

    raise ValueError(f"Unsupported single-product selection mode '{mode}'.")


def _select_three_products(
    stage: StageId,
    tier: WorksheetTier,
    selection_scope: SelectionScope,
    mode: ProductSetMode,
    target_count: int,
    rotation_index: int,
) -> tuple[int, ...]:
    candidates = _three_product_candidates(
        stage=stage,
        mode=mode,
        selection_scope=selection_scope,
        target_count=target_count,
    )

    ranked = sorted(
        candidates,
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

    return ranked[rotation_index % len(ranked)]


def _three_product_candidates(
    stage: StageId,
    mode: ProductSetMode,
    selection_scope: SelectionScope,
    target_count: int,
) -> list[tuple[int, ...]]:
    if target_count != 3:
        raise ValueError(f"Only 3-product selection is supported here, got {target_count}.")

    pool = _primary_scope_pool(stage, selection_scope)
    stage_new = set(products_for_stage(stage))
    stage_recap = set(recap_products_for_stage(stage))
    cumulative = set(cumulative_products_for_stage(stage))

    if mode == "same_stage_products":
        base = products_for_stage(stage)
        triples = _generate_combinations(base, 3)

        if triples:
            return _rank_preserving_dedupe(triples)

        triples = _generate_combinations(pool, 3)
        return _filter_scope_triples(
            triples=triples,
            selection_scope=selection_scope,
            stage_new=stage_new,
            stage_recap=stage_recap,
        )

    if mode == "same_factor_family":
        family_pool = _same_factor_family_pool(stage)
        triples = _generate_combinations(family_pool, 3)
        return _filter_scope_triples(
            triples=triples,
            selection_scope=selection_scope,
            stage_new=stage_new,
            stage_recap=stage_recap,
        )

    if mode == "multi_route_compare":
        base = [p for p in pool if p in MULTI_ROUTE_PRODUCTS]
        if len(base) < 3:
            base = [p for p in cumulative if p in MULTI_ROUTE_PRODUCTS]
        triples = _generate_combinations(base, 3)
        return _filter_scope_triples(
            triples=triples,
            selection_scope=selection_scope,
            stage_new=stage_new,
            stage_recap=stage_recap,
        )

    if mode == "doubling_chain":
        if stage not in ("E", "F", "G"):
            return []
        triples = [
            tuple(sorted(triple))
            for triple in DOUBLING_CHAIN_TRIPLES
            if all(p in cumulative for p in triple)
        ]
        return _filter_scope_triples(
            triples=triples,
            selection_scope=selection_scope,
            stage_new=stage_new,
            stage_recap=stage_recap,
        )

    if mode == "interleave_compare":
        triples = [
            tuple(sorted(triple))
            for triple in CURATED_STAGE_TRIPLES.get(stage, [])
            if all(p in cumulative for p in triple)
        ]
        return _filter_scope_triples(
            triples=triples,
            selection_scope=selection_scope,
            stage_new=stage_new,
            stage_recap=stage_recap,
        )

    if mode == "square_or_special_focus":
        focus_bank = set(SQUARE_PRODUCTS) | set(SPECIAL_FOCUS_PRODUCTS)
        focus_pool = [p for p in pool if p in focus_bank]
        if len(focus_pool) < 3:
            focus_pool = [p for p in cumulative if p in focus_bank]
        triples = _generate_combinations(focus_pool, 3)
        return _filter_scope_triples(
            triples=triples,
            selection_scope=selection_scope,
            stage_new=stage_new,
            stage_recap=stage_recap,
        )

    raise ValueError(f"Unsupported three-product selection mode '{mode}'.")


def _primary_scope_pool(stage: StageId, selection_scope: SelectionScope) -> list[int]:
    stage_new = list(products_for_stage(stage))
    stage_focus = _stage_focus_pool(stage)
    cumulative = list(cumulative_products_for_stage(stage))

    if selection_scope == "new_only":
        return _ordered_unique(stage_new)

    if selection_scope == "available_mixed":
        return _ordered_unique(stage_focus + cumulative)

    if selection_scope == "hybrid":
        return _ordered_unique(stage_new + stage_focus)

    raise ValueError(f"Unsupported selection scope '{selection_scope}'.")


def _stage_focus_pool(stage: StageId) -> list[int]:
    stage_new = list(products_for_stage(stage))
    recap_family = list(recap_products_for_stage(stage))
    cumulative = set(cumulative_products_for_stage(stage))

    if stage == "A":
        return _ordered_unique(stage_new)

    if stage == "B":
        return _ordered_unique(stage_new + [10])

    if stage == "C":
        return _ordered_unique(stage_new + recap_family)

    if stage == "D":
        return _ordered_unique(stage_new + recap_family)

    if stage == "E":
        return _ordered_unique(stage_new + list(DOUBLING_CHAIN_PRODUCTS) + recap_family)

    if stage == "F":
        base = stage_new + recap_family + [24, 27, 30, 36, 45, 54]
        return _ordered_unique([p for p in base if p in cumulative])

    if stage == "G":
        base = stage_new + recap_family + [36, 42, 56]
        return _ordered_unique([p for p in base if p in cumulative])

    raise ValueError(f"Unknown stage '{stage}'.")


def _same_factor_family_pool(stage: StageId) -> list[int]:
    if stage == "A":
        return list(products_for_stage("A"))

    if stage == "B":
        return [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    if stage in RECAP_FAMILY_BANKS:
        return [
            p for p in recap_products_for_stage(stage)
            if p in TMK_ALL_PRODUCTS
        ]

    return list(products_for_stage(stage))


def _filter_scope_triples(
    triples: Iterable[tuple[int, ...]],
    selection_scope: SelectionScope,
    stage_new: set[int],
    stage_recap: set[int],
) -> list[tuple[int, ...]]:
    filtered: list[tuple[int, ...]] = []

    for triple in triples:
        triple_set = set(triple)

        if selection_scope == "new_only":
            if triple_set.issubset(stage_new):
                filtered.append(tuple(sorted(triple)))
            continue

        if selection_scope == "hybrid":
            has_new = bool(triple_set & stage_new)
            has_support = bool((triple_set & stage_recap) or (triple_set - stage_new))
            if has_new and has_support:
                filtered.append(tuple(sorted(triple)))
            continue

        if selection_scope == "available_mixed":
            filtered.append(tuple(sorted(triple)))
            continue

    return _rank_preserving_dedupe(filtered)


def _select_recap_products(
    stage: StageId,
    selected_products: tuple[int, ...],
    include_recap: bool,
) -> tuple[int, ...]:
    if not include_recap:
        return ()

    recap_pool = [p for p in recap_products_for_stage(stage) if p not in selected_products]
    return tuple(recap_pool)


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
        f"Selected products: {', '.join(str(p) for p in selected_products)}.",
    ]

    single_mode_reason_map: dict[str, str] = {
        "single_hub": "Single-hub mode chooses a normal stage-shaped product.",
        "multi_route_hub": "Multi-route-hub mode chooses from the canonical multiple-route bank.",
        "square_product": "Square-product mode chooses from the canonical square bank.",
        "special_focus": "Special-focus mode chooses from the canonical landmark bank.",
        "doubling_chain_product": "Doubling-chain-product mode chooses from the canonical Stage E doubling bank.",
        "stage_bridge": "Stage-bridge mode chooses from products that strongly connect stages or families.",
        "closure_product": "Closure-product mode foregrounds Stage G closure.",
        "boundary_focus": "Boundary-focus mode foregrounds strong in-world structural boundary products.",
        "benchmark_product": "Benchmark-product mode foregrounds benchmark anchors such as 10, 25, 50, 90, and 100.",
        "comparison_ready": "Comparison-ready mode foregrounds products that support route comparison.",
    }

    if mode in single_mode_reason_map:
        reasons.append(single_mode_reason_map[mode])

    if stage == "C":
        reasons.append("Stage C recap is family-driven from the 5× structure, not arbitrary earlier products.")
    if stage == "D":
        reasons.append("Stage D recap is family-driven from the 9× structure.")
    if stage == "E":
        reasons.append("Stage E selection and recap foreground the 2× / 4× / 8× doubling structure.")
    if stage == "F":
        reasons.append("Stage F selection foregrounds interleaving around the 3× / 6× structure and the bridge products 21 and 42.")
    if stage == "G":
        reasons.append("Stage G selection foregrounds closure and 7× structure, including lawful cross-stage comparison products.")

    if mode == "same_stage_products":
        reasons.append("Same-stage mode is built from the canonical stage product bank and stage-shaped support when a stage has fewer than three new products.")
    if mode == "same_factor_family":
        reasons.append("Same-factor-family mode is built from explicit family banks, not generic cumulative pools.")
    if mode == "multi_route_compare":
        reasons.append("Multi-route mode is built from the canonical multi-route product bank.")
    if mode == "doubling_chain":
        reasons.append("Doubling-chain mode is built from the canonical doubling-chain triples.")
    if mode == "interleave_compare":
        reasons.append("Interleave mode is built from curated stage triples in the canonical bank module.")
    if mode == "square_or_special_focus":
        reasons.append("Square/special mode is built from the square and special-focus banks.")

    if recap_products:
        reasons.append(
            "Recap products are drawn from the explicit recap family bank for this stage and are intended for a recap box or separate recap worksheet."
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


def _single_hub_score(
    product: int,
    stage: StageId,
    tier: WorksheetTier,
    selection_scope: SelectionScope,
    is_stage_new: bool,
    is_stage_recap: bool,
    mode: ProductSetMode,
) -> int:
    record = product_metadata(product)
    score = 0

    score += _hub_band_rank(record.hub_band) * 10
    score += _route_profile_rank(record.route_profile) * 5
    score += len(record.known_routes_at_stage) * 3
    score += len(set(record.vocab_tags).intersection(stage_required_vocab_focus(stage))) * 4

    if is_stage_new:
        score += 14
    if is_stage_recap:
        score += 8
    if record.is_square:
        score += 4
    if product in SPECIAL_FOCUS_PRODUCTS:
        score += 4

    mode_bonus_map: dict[str, int] = {
        "multi_route_hub": 10 if product in MULTI_ROUTE_PRODUCTS else -20,
        "square_product": 12 if product in SQUARE_PRODUCTS else -20,
        "special_focus": 10 if product in SPECIAL_FOCUS_PRODUCTS else -20,
        "doubling_chain_product": 12 if product in DOUBLING_CHAIN_PRODUCTS else -20,
        "stage_bridge": 12 if product in STAGE_BRIDGE_PRODUCTS else -20,
        "closure_product": 20 if product in CLOSURE_PRODUCTS else -40,
        "boundary_focus": 10 if product in BOUNDARY_FOCUS_PRODUCTS else -20,
        "benchmark_product": 10 if product in BENCHMARK_PRODUCTS else -20,
        "comparison_ready": 10 if product in COMPARISON_READY_PRODUCTS else -20,
    }
    score += mode_bonus_map.get(mode, 0)

    if stage == "F" and product in (21, 42, 24, 27, 30, 36, 45, 54):
        score += 12
    if stage == "G" and product in (49, 42, 56, 35, 63, 70, 36):
        score += 12

    if selection_scope == "new_only" and not is_stage_new:
        score -= 20
    if selection_scope == "hybrid" and (is_stage_new or is_stage_recap):
        score += 4

    if tier == "Support":
        if record.has_multiple_routes:
            score -= 1
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
    records = tuple(product_metadata(p) for p in products)
    product_set = set(products)
    stage_new = set(products_for_stage(stage))
    stage_recap = set(recap_products_for_stage(stage))
    score = 0

    score += len(_shared_family_tags(records)) * 8
    score += len(_shared_structural_tags(records)) * 8
    score += len(_supported_required_vocab(records, stage)) * 5
    score += sum(_hub_band_rank(record.hub_band) for record in records)
    score += sum(int(record.has_multiple_routes) for record in records) * 4
    score += sum(int(record.is_square) for record in records) * 3
    score += sum(int(record.product in SPECIAL_FOCUS_PRODUCTS) for record in records) * 2

    if selection_scope == "new_only":
        score += sum(int(record.product in stage_new) for record in records) * 10
    elif selection_scope == "hybrid":
        has_new = bool(product_set & stage_new)
        has_support = bool((product_set & stage_recap) or (product_set - stage_new))
        if has_new and has_support:
            score += 18
    elif selection_scope == "available_mixed":
        score += sum(int(record.product in stage_new) for record in records) * 4

    if mode == "same_stage_products":
        score += sum(int(record.product in stage_new) for record in records) * 8
        if stage in ("F", "G"):
            score += sum(int(record.product in stage_recap) for record in records) * 4

    if mode == "same_factor_family":
        score += sum(int(record.product in stage_recap) for record in records) * 8

    if mode == "multi_route_compare":
        score += sum(int(record.product in MULTI_ROUTE_PRODUCTS) for record in records) * 8

    if mode == "doubling_chain":
        if tuple(sorted(products)) in {tuple(sorted(t)) for t in DOUBLING_CHAIN_TRIPLES}:
            score += 35
        score += sum(int(record.product in DOUBLING_CHAIN_PRODUCTS) for record in records) * 8

    if mode == "interleave_compare":
        if tuple(sorted(products)) in {tuple(sorted(t)) for t in CURATED_STAGE_TRIPLES.get(stage, [])}:
            score += 28

    if mode == "square_or_special_focus":
        score += sum(int(record.product in SQUARE_PRODUCTS) for record in records) * 8
        score += sum(int(record.product in SPECIAL_FOCUS_PRODUCTS) for record in records) * 6

    if stage == "C":
        score += sum(int(record.product in recap_products_for_stage("C")) for record in records) * 6
    if stage == "D":
        score += sum(int(record.product in recap_products_for_stage("D")) for record in records) * 6
    if stage == "E":
        score += sum(int(record.product in DOUBLING_CHAIN_PRODUCTS) for record in records) * 6
    if stage == "F":
        score += sum(int(record.product in recap_products_for_stage("F")) for record in records) * 7
        if {21, 42}.issubset(product_set):
            score += 14
    if stage == "G":
        score += sum(int(record.product in recap_products_for_stage("G")) for record in records) * 7
        if 49 in product_set:
            score += 20
        if {42, 49}.issubset(product_set):
            score += 12
        if {35, 49}.issubset(product_set):
            score += 8

    if tier == "Support":
        if mode in ("same_factor_family", "same_stage_products", "doubling_chain"):
            score += 8
    elif tier == "Core":
        if any(record.has_multiple_routes for record in records):
            score += 6
    elif tier == "Extension":
        if any(record.has_multiple_routes for record in records):
            score += 8
        if any(record.is_square for record in records):
            score += 6

    return score


def _generate_combinations(pool: Iterable[int], count: int) -> list[tuple[int, ...]]:
    unique_pool = _ordered_unique(pool)
    if len(unique_pool) < count:
        return []
    return [tuple(sorted(combo)) for combo in combinations(unique_pool, count)]


def _rank_preserving_dedupe(triples: Iterable[tuple[int, ...]]) -> list[tuple[int, ...]]:
    seen: set[tuple[int, ...]] = set()
    ordered: list[tuple[int, ...]] = []
    for triple in triples:
        normalized = tuple(sorted(triple))
        if normalized not in seen:
            seen.add(normalized)
            ordered.append(normalized)
    return ordered


def _ordered_unique(values: Iterable[int]) -> list[int]:
    seen: set[int] = set()
    ordered: list[int] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


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
