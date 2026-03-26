from __future__ import annotations

from typing import Final

from models.worksheet_models import (
    ProductMetadataRecord,
    StageId,
    SUPPORTED_STAGES,
    validate_product_metadata_record,
    validate_stage,
)


TMK_PRODUCT_METADATA: Final[tuple[ProductMetadataRecord, ...]] = (
    ProductMetadataRecord(
        product=1,
        stage_introduced="A",
        intro_family="anchor_1x",
        factor_pairs=((1, 1),),
        family_tags=("times_1", "square"),
        structural_tags=("identity_anchor", "closure_square"),
        vocab_tags=("identity", "factor", "product", "inverse", "square"),
        route_profile="square_route",
        hub_band="medium",
        has_multiple_routes=False,
        known_routes_at_stage=((1, 1),),
        is_square=True,
        has_factor_7=False,
        notes="Identity anchor and first square product.",
    ),
    ProductMetadataRecord(
        product=2,
        stage_introduced="A",
        intro_family="anchor_1x",
        factor_pairs=((1, 2),),
        family_tags=("times_1", "times_2"),
        structural_tags=("identity_anchor", "doubling_seed"),
        vocab_tags=("identity", "factor", "product", "inverse", "double"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((1, 2),),
        is_square=False,
        has_factor_7=False,
        notes="Simple identity product and early doubling seed.",
    ),
    ProductMetadataRecord(
        product=3,
        stage_introduced="A",
        intro_family="anchor_1x",
        factor_pairs=((1, 3),),
        family_tags=("times_1", "times_3"),
        structural_tags=("identity_anchor", "interleave_seed"),
        vocab_tags=("identity", "factor", "product", "inverse"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((1, 3),),
        is_square=False,
        has_factor_7=False,
        notes="Simple identity product and seed for later 3x interleaving.",
    ),
    ProductMetadataRecord(
        product=4,
        stage_introduced="A",
        intro_family="anchor_1x",
        factor_pairs=((1, 4), (2, 2)),
        family_tags=("times_1", "times_2", "times_4", "square"),
        structural_tags=("identity_anchor", "doubling_seed", "closure_square"),
        vocab_tags=("identity", "factor", "product", "inverse", "double", "square"),
        route_profile="multi_route",
        hub_band="medium",
        has_multiple_routes=True,
        known_routes_at_stage=((1, 4), (2, 2)),
        is_square=True,
        has_factor_7=False,
        notes="First product with a useful compare between identity and square routes.",
    ),
    ProductMetadataRecord(
        product=5,
        stage_introduced="A",
        intro_family="anchor_1x",
        factor_pairs=((1, 5),),
        family_tags=("times_1", "times_5"),
        structural_tags=("identity_anchor", "midpoint_seed"),
        vocab_tags=("identity", "factor", "product", "inverse", "half"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((1, 5),),
        is_square=False,
        has_factor_7=False,
        notes="Midpoint seed for later 5x work.",
    ),
    ProductMetadataRecord(
        product=6,
        stage_introduced="A",
        intro_family="anchor_1x",
        factor_pairs=((1, 6), (2, 3)),
        family_tags=("times_1", "times_2", "times_3", "times_6"),
        structural_tags=("identity_anchor", "interleave_seed", "multi_route_product"),
        vocab_tags=("identity", "factor", "product", "inverse", "fact family"),
        route_profile="multi_route",
        hub_band="medium",
        has_multiple_routes=True,
        known_routes_at_stage=((1, 6), (2, 3)),
        is_square=False,
        has_factor_7=False,
        notes="Early fact-family product with two visible core routes.",
    ),
    ProductMetadataRecord(
        product=7,
        stage_introduced="A",
        intro_family="anchor_1x",
        factor_pairs=((1, 7),),
        family_tags=("times_1", "times_7"),
        structural_tags=("identity_anchor", "times7_seed"),
        vocab_tags=("identity", "factor", "product", "inverse"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((1, 7),),
        is_square=False,
        has_factor_7=True,
        notes="7-times seed product.",
    ),
    ProductMetadataRecord(
        product=8,
        stage_introduced="A",
        intro_family="anchor_1x",
        factor_pairs=((1, 8), (2, 4)),
        family_tags=("times_1", "times_2", "times_4", "times_8"),
        structural_tags=("identity_anchor", "doubling_seed", "multi_route_product"),
        vocab_tags=("identity", "factor", "product", "inverse", "double"),
        route_profile="multi_route",
        hub_band="medium",
        has_multiple_routes=True,
        known_routes_at_stage=((1, 8), (2, 4)),
        is_square=False,
        has_factor_7=False,
        notes="Useful doubling seed with two visible routes.",
    ),
    ProductMetadataRecord(
        product=9,
        stage_introduced="A",
        intro_family="anchor_1x",
        factor_pairs=((1, 9), (3, 3)),
        family_tags=("times_1", "times_3", "times_9", "square"),
        structural_tags=("identity_anchor", "near10_seed", "closure_square"),
        vocab_tags=("identity", "factor", "product", "inverse", "square"),
        route_profile="multi_route",
        hub_band="medium",
        has_multiple_routes=True,
        known_routes_at_stage=((1, 9), (3, 3)),
        is_square=True,
        has_factor_7=False,
        notes="Square and 9x seed.",
    ),
    ProductMetadataRecord(
        product=10,
        stage_introduced="A",
        intro_family="anchor_10x",
        factor_pairs=((1, 10), (2, 5)),
        family_tags=("times_1", "times_2", "times_5", "times_10"),
        structural_tags=("base10_anchor", "midpoint_seed", "multi_route_product"),
        vocab_tags=("identity", "factor", "product", "inverse", "half", "place value"),
        route_profile="multi_route",
        hub_band="medium",
        has_multiple_routes=True,
        known_routes_at_stage=((1, 10), (2, 5)),
        is_square=False,
        has_factor_7=False,
        notes="Base-10 anchor with clear 2×5 relation.",
    ),
    ProductMetadataRecord(
        product=20,
        stage_introduced="B",
        intro_family="anchor_10x",
        factor_pairs=((2, 10), (4, 5)),
        family_tags=("times_2", "times_4", "times_5", "times_10"),
        structural_tags=("base10_anchor", "scaling_product", "multi_route_product"),
        vocab_tags=("product", "factor", "inverse", "place value", "half"),
        route_profile="multi_route",
        hub_band="medium",
        has_multiple_routes=True,
        known_routes_at_stage=((2, 10), (4, 5)),
        is_square=False,
        has_factor_7=False,
        notes="Strong 10x scaling product with a second visible route.",
    ),
    ProductMetadataRecord(
        product=30,
        stage_introduced="B",
        intro_family="anchor_10x",
        factor_pairs=((3, 10), (5, 6)),
        family_tags=("times_3", "times_5", "times_6", "times_10"),
        structural_tags=("base10_anchor", "scaling_product", "multi_route_product"),
        vocab_tags=("product", "factor", "inverse", "place value"),
        route_profile="multi_route",
        hub_band="medium",
        has_multiple_routes=True,
        known_routes_at_stage=((3, 10), (5, 6)),
        is_square=False,
        has_factor_7=False,
        notes="Connects 10x scaling to 5x and 6x structure.",
    ),
    ProductMetadataRecord(
        product=40,
        stage_introduced="B",
        intro_family="anchor_10x",
        factor_pairs=((4, 10), (5, 8)),
        family_tags=("times_4", "times_5", "times_8", "times_10"),
        structural_tags=("base10_anchor", "scaling_product", "multi_route_product"),
        vocab_tags=("product", "factor", "inverse", "place value", "double"),
        route_profile="multi_route",
        hub_band="medium",
        has_multiple_routes=True,
        known_routes_at_stage=((4, 10), (5, 8)),
        is_square=False,
        has_factor_7=False,
        notes="Strong 10x anchor linking 4x, 5x, and 8x structure.",
    ),
    ProductMetadataRecord(
        product=50,
        stage_introduced="B",
        intro_family="anchor_10x",
        factor_pairs=((5, 10),),
        family_tags=("times_5", "times_10"),
        structural_tags=("base10_anchor", "scaling_product", "midpoint_product"),
        vocab_tags=("product", "factor", "inverse", "place value", "half"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((5, 10),),
        is_square=False,
        has_factor_7=False,
        notes="Clear midpoint and scaling product.",
    ),
    ProductMetadataRecord(
        product=60,
        stage_introduced="B",
        intro_family="anchor_10x",
        factor_pairs=((6, 10),),
        family_tags=("times_6", "times_10"),
        structural_tags=("base10_anchor", "scaling_product"),
        vocab_tags=("product", "factor", "inverse", "place value"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((6, 10),),
        is_square=False,
        has_factor_7=False,
        notes="Simple scaling product.",
    ),
    ProductMetadataRecord(
        product=70,
        stage_introduced="B",
        intro_family="anchor_10x",
        factor_pairs=((7, 10),),
        family_tags=("times_7", "times_10"),
        structural_tags=("base10_anchor", "scaling_product"),
        vocab_tags=("product", "factor", "inverse", "place value"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((7, 10),),
        is_square=False,
        has_factor_7=True,
        notes="7x scaling anchor.",
    ),
    ProductMetadataRecord(
        product=80,
        stage_introduced="B",
        intro_family="anchor_10x",
        factor_pairs=((8, 10),),
        family_tags=("times_8", "times_10"),
        structural_tags=("base10_anchor", "scaling_product"),
        vocab_tags=("product", "factor", "inverse", "place value", "double"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((8, 10),),
        is_square=False,
        has_factor_7=False,
        notes="Simple 8×10 scaling anchor.",
    ),
    ProductMetadataRecord(
        product=90,
        stage_introduced="B",
        intro_family="anchor_10x",
        factor_pairs=((9, 10),),
        family_tags=("times_9", "times_10"),
        structural_tags=("base10_anchor", "scaling_product", "near10_product"),
        vocab_tags=("product", "factor", "inverse", "place value", "pattern"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((9, 10),),
        is_square=False,
        has_factor_7=False,
        notes="Near-ten scaling anchor.",
    ),
    ProductMetadataRecord(
        product=100,
        stage_introduced="B",
        intro_family="anchor_10x",
        factor_pairs=((10, 10),),
        family_tags=("times_10", "square"),
        structural_tags=("base10_anchor", "closure_square"),
        vocab_tags=("product", "factor", "inverse", "place value", "square"),
        route_profile="square_route",
        hub_band="medium",
        has_multiple_routes=False,
        known_routes_at_stage=((10, 10),),
        is_square=True,
        has_factor_7=False,
        notes="10×10 closure square.",
    ),
    ProductMetadataRecord(
        product=15,
        stage_introduced="C",
        intro_family="times_5",
        factor_pairs=((3, 5),),
        family_tags=("times_3", "times_5"),
        structural_tags=("midpoint_product", "halving_product"),
        vocab_tags=("half", "product", "factor", "inverse", "commutative"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((3, 5),),
        is_square=False,
        has_factor_7=False,
        notes="Clear midpoint 5x product.",
    ),
    ProductMetadataRecord(
        product=25,
        stage_introduced="C",
        intro_family="times_5",
        factor_pairs=((5, 5),),
        family_tags=("times_5", "square"),
        structural_tags=("midpoint_product", "closure_square"),
        vocab_tags=("half", "product", "factor", "inverse", "square"),
        route_profile="square_route",
        hub_band="medium",
        has_multiple_routes=False,
        known_routes_at_stage=((5, 5),),
        is_square=True,
        has_factor_7=False,
        notes="Strong square/midpoint focus product.",
    ),
    ProductMetadataRecord(
        product=35,
        stage_introduced="C",
        intro_family="times_5",
        factor_pairs=((5, 7),),
        family_tags=("times_5", "times_7"),
        structural_tags=("midpoint_product", "times7_bridge"),
        vocab_tags=("half", "product", "factor", "inverse", "commutative"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((5, 7),),
        is_square=False,
        has_factor_7=True,
        notes="Bridge between 5x and 7x structure.",
    ),
    ProductMetadataRecord(
        product=45,
        stage_introduced="C",
        intro_family="times_5",
        factor_pairs=((5, 9),),
        family_tags=("times_5", "times_9"),
        structural_tags=("midpoint_product", "near10_bridge"),
        vocab_tags=("half", "product", "factor", "inverse", "commutative"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((5, 9),),
        is_square=False,
        has_factor_7=False,
        notes="Bridge between 5x and 9x structure.",
    ),
    ProductMetadataRecord(
        product=18,
        stage_introduced="D",
        intro_family="times_9",
        factor_pairs=((2, 9), (3, 6)),
        family_tags=("times_2", "times_3", "times_6", "times_9"),
        structural_tags=("near10_product", "multi_route_product"),
        vocab_tags=("product", "factor", "inverse", "commutative", "fact family", "pattern"),
        route_profile="multi_route",
        hub_band="medium",
        has_multiple_routes=True,
        known_routes_at_stage=((2, 9), (3, 6)),
        is_square=False,
        has_factor_7=False,
        notes="Good compare product in the 9x stage.",
    ),
    ProductMetadataRecord(
        product=27,
        stage_introduced="D",
        intro_family="times_9",
        factor_pairs=((3, 9),),
        family_tags=("times_3", "times_9"),
        structural_tags=("near10_product"),
        vocab_tags=("product", "factor", "inverse", "pattern"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((3, 9),),
        is_square=False,
        has_factor_7=False,
        notes="Clear 9x pattern product.",
    ),
    ProductMetadataRecord(
        product=36,
        stage_introduced="D",
        intro_family="times_9",
        factor_pairs=((4, 9), (6, 6)),
        family_tags=("times_4", "times_6", "times_9", "square"),
        structural_tags=("near10_product", "multi_route_product", "closure_square"),
        vocab_tags=("product", "factor", "inverse", "fact family", "square", "pattern"),
        route_profile="multi_route",
        hub_band="high",
        has_multiple_routes=True,
        known_routes_at_stage=((4, 9), (6, 6)),
        is_square=True,
        has_factor_7=False,
        notes="One of the strongest hub products in the system.",
    ),
    ProductMetadataRecord(
        product=54,
        stage_introduced="D",
        intro_family="times_9",
        factor_pairs=((6, 9),),
        family_tags=("times_6", "times_9"),
        structural_tags=("near10_product"),
        vocab_tags=("product", "factor", "inverse", "pattern"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((6, 9),),
        is_square=False,
        has_factor_7=False,
        notes="Clear upper 9x sequence product.",
    ),
    ProductMetadataRecord(
        product=63,
        stage_introduced="D",
        intro_family="times_9",
        factor_pairs=((7, 9),),
        family_tags=("times_7", "times_9"),
        structural_tags=("near10_product", "times7_bridge"),
        vocab_tags=("product", "factor", "inverse", "pattern"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((7, 9),),
        is_square=False,
        has_factor_7=True,
        notes="9x/7x bridge product.",
    ),
    ProductMetadataRecord(
        product=72,
        stage_introduced="D",
        intro_family="times_9",
        factor_pairs=((8, 9),),
        family_tags=("times_8", "times_9"),
        structural_tags=("near10_product"),
        vocab_tags=("product", "factor", "inverse", "pattern"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((8, 9),),
        is_square=False,
        has_factor_7=False,
        notes="High-end 9x product.",
    ),
    ProductMetadataRecord(
        product=81,
        stage_introduced="D",
        intro_family="times_9",
        factor_pairs=((9, 9),),
        family_tags=("times_9", "square"),
        structural_tags=("near10_product", "closure_square"),
        vocab_tags=("product", "factor", "inverse", "square", "pattern"),
        route_profile="square_route",
        hub_band="medium",
        has_multiple_routes=False,
        known_routes_at_stage=((9, 9),),
        is_square=True,
        has_factor_7=False,
        notes="9×9 closure square.",
    ),
    ProductMetadataRecord(
        product=12,
        stage_introduced="E",
        intro_family="doubling_chain",
        factor_pairs=((2, 6), (3, 4)),
        family_tags=("times_2", "times_3", "times_4", "times_6"),
        structural_tags=("doubling_product", "multi_route_product"),
        vocab_tags=("double", "factor", "product", "inverse", "fact family", "pair"),
        route_profile="multi_route",
        hub_band="medium",
        has_multiple_routes=True,
        known_routes_at_stage=((2, 6), (3, 4)),
        is_square=False,
        has_factor_7=False,
        notes="Strong doubling-chain compare product.",
    ),
    ProductMetadataRecord(
        product=14,
        stage_introduced="E",
        intro_family="doubling_chain",
        factor_pairs=((2, 7),),
        family_tags=("times_2", "times_7"),
        structural_tags=("doubling_product", "times7_bridge"),
        vocab_tags=("double", "factor", "product", "inverse"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((2, 7),),
        is_square=False,
        has_factor_7=True,
        notes="Simple doubled-7 product.",
    ),
    ProductMetadataRecord(
        product=16,
        stage_introduced="E",
        intro_family="doubling_chain",
        factor_pairs=((2, 8), (4, 4)),
        family_tags=("times_2", "times_4", "times_8", "square"),
        structural_tags=("doubling_product", "closure_square", "multi_route_product"),
        vocab_tags=("double", "factor", "product", "inverse", "square"),
        route_profile="multi_route",
        hub_band="medium",
        has_multiple_routes=True,
        known_routes_at_stage=((2, 8), (4, 4)),
        is_square=True,
        has_factor_7=False,
        notes="Doubling and square comparison product.",
    ),
    ProductMetadataRecord(
        product=24,
        stage_introduced="E",
        intro_family="doubling_chain",
        factor_pairs=((3, 8), (4, 6)),
        family_tags=("times_3", "times_4", "times_6", "times_8"),
        structural_tags=("doubling_product", "multi_route_product"),
        vocab_tags=("double", "factor", "product", "inverse", "fact family", "pair"),
        route_profile="multi_route",
        hub_band="high",
        has_multiple_routes=True,
        known_routes_at_stage=((3, 8), (4, 6)),
        is_square=False,
        has_factor_7=False,
        notes="Excellent compare and route product for one-product worksheets.",
    ),
    ProductMetadataRecord(
        product=28,
        stage_introduced="E",
        intro_family="doubling_chain",
        factor_pairs=((4, 7),),
        family_tags=("times_4", "times_7"),
        structural_tags=("doubling_product", "times7_bridge"),
        vocab_tags=("double", "factor", "product", "inverse"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((4, 7),),
        is_square=False,
        has_factor_7=True,
        notes="4x/7x bridge product.",
    ),
    ProductMetadataRecord(
        product=32,
        stage_introduced="E",
        intro_family="doubling_chain",
        factor_pairs=((4, 8),),
        family_tags=("times_4", "times_8"),
        structural_tags=("doubling_product"),
        vocab_tags=("double", "factor", "product", "inverse", "pattern"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((4, 8),),
        is_square=False,
        has_factor_7=False,
        notes="Clear doubling pattern product.",
    ),
    ProductMetadataRecord(
        product=48,
        stage_introduced="E",
        intro_family="doubling_chain",
        factor_pairs=((6, 8),),
        family_tags=("times_6", "times_8"),
        structural_tags=("doubling_product"),
        vocab_tags=("double", "factor", "product", "inverse", "pattern"),
        route_profile="single_route",
        hub_band="medium",
        has_multiple_routes=False,
        known_routes_at_stage=((6, 8),),
        is_square=False,
        has_factor_7=False,
        notes="Important end-of-chain doubling product.",
    ),
    ProductMetadataRecord(
        product=56,
        stage_introduced="E",
        intro_family="doubling_chain",
        factor_pairs=((7, 8),),
        family_tags=("times_7", "times_8"),
        structural_tags=("doubling_product", "times7_bridge"),
        vocab_tags=("double", "factor", "product", "inverse", "pattern"),
        route_profile="single_route",
        hub_band="low",
        has_multiple_routes=False,
        known_routes_at_stage=((7, 8),),
        is_square=False,
        has_factor_7=True,
        notes="7x/8x bridge product.",
    ),
    ProductMetadataRecord(
        product=64,
        stage_introduced="E",
        intro_family="doubling_chain",
        factor_pairs=((8, 8),),
        family_tags=("times_8", "square"),
        structural_tags=("doubling_product", "closure_square"),
        vocab_tags=("double", "factor", "product", "inverse", "square"),
        route_profile="square_route",
        hub_band="medium",
        has_multiple_routes=False,
        known_routes_at_stage=((8, 8),),
        is_square=True,
        has_factor_7=False,
        notes="8×8 closure square.",
    ),
    ProductMetadataRecord(
        product=21,
        stage_introduced="F",
        intro_family="interleave",
        factor_pairs=((3, 7),),
        family_tags=("times_3", "times_7"),
        structural_tags=("interleave_product", "new_product_focus"),
        vocab_tags=("factor", "product", "inverse", "fact family", "link", "new product"),
        route_profile="single_route",
        hub_band="medium",
        has_multiple_routes=False,
        known_routes_at_stage=((3, 7),),
        is_square=False,
        has_factor_7=True,
        notes="One of two genuinely new Stage F products.",
    ),
    ProductMetadataRecord(
        product=42,
        stage_introduced="F",
        intro_family="interleave",
        factor_pairs=((6, 7),),
        family_tags=("times_6", "times_7"),
        structural_tags=("interleave_product", "new_product_focus"),
        vocab_tags=("factor", "product", "inverse", "fact family", "link", "new product"),
        route_profile="single_route",
        hub_band="medium",
        has_multiple_routes=False,
        known_routes_at_stage=((6, 7),),
        is_square=False,
        has_factor_7=True,
        notes="Second genuinely new Stage F product.",
    ),
    ProductMetadataRecord(
        product=49,
        stage_introduced="G",
        intro_family="times_7",
        factor_pairs=((7, 7),),
        family_tags=("times_7", "square"),
        structural_tags=("closure_square", "final_key"),
        vocab_tags=("square", "factor", "product", "inverse", "area", "perimeter", "side length"),
        route_profile="square_route",
        hub_band="high",
        has_multiple_routes=False,
        known_routes_at_stage=((7, 7),),
        is_square=True,
        has_factor_7=True,
        notes="Final key and stage-closure square.",
    ),
)


PRODUCT_METADATA_BY_VALUE: Final[dict[int, ProductMetadataRecord]] = {
    record.product: record for record in TMK_PRODUCT_METADATA
}


INTRODUCED_PRODUCTS_BY_STAGE: Final[dict[StageId, tuple[int, ...]]] = {
    "A": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
    "B": (20, 30, 40, 50, 60, 70, 80, 90, 100),
    "C": (15, 25, 35, 45),
    "D": (18, 27, 36, 54, 63, 72, 81),
    "E": (12, 14, 16, 24, 28, 32, 48, 56, 64),
    "F": (21, 42),
    "G": (49,),
}


_STAGE_ORDER: Final[tuple[StageId, ...]] = ("A", "B", "C", "D", "E", "F", "G")


def product_metadata(product: int) -> ProductMetadataRecord:
    try:
        return PRODUCT_METADATA_BY_VALUE[product]
    except KeyError as exc:
        raise ValueError(f"Unknown TMK product metadata for product {product}.") from exc


def all_product_metadata() -> tuple[ProductMetadataRecord, ...]:
    return TMK_PRODUCT_METADATA


def new_products(stage: StageId) -> tuple[int, ...]:
    validate_stage(stage)
    return INTRODUCED_PRODUCTS_BY_STAGE[stage]


def available_products(stage: StageId) -> tuple[int, ...]:
    validate_stage(stage)
    available: list[int] = []
    for current_stage in _STAGES_UP_TO(stage):
        available.extend(INTRODUCED_PRODUCTS_BY_STAGE[current_stage])
    return tuple(available)


def stage_for_product(product: int) -> StageId:
    return product_metadata(product).stage_introduced


def products_with_factor_7(stage: StageId | None = None) -> tuple[int, ...]:
    records = _records_for_stage_filter(stage)
    return tuple(record.product for record in records if record.has_factor_7)


def square_products(stage: StageId | None = None) -> tuple[int, ...]:
    records = _records_for_stage_filter(stage)
    return tuple(record.product for record in records if record.is_square)


def multi_route_products(stage: StageId | None = None) -> tuple[int, ...]:
    records = _records_for_stage_filter(stage)
    return tuple(record.product for record in records if record.has_multiple_routes)


def products_for_family_tag(
    family_tag: str,
    stage: StageId | None = None,
) -> tuple[int, ...]:
    normalized = family_tag.strip().lower()
    records = _records_for_stage_filter(stage)
    return tuple(
        record.product
        for record in records
        if normalized in {tag.lower() for tag in record.family_tags}
    )


def products_for_structural_tag(
    structural_tag: str,
    stage: StageId | None = None,
) -> tuple[int, ...]:
    normalized = structural_tag.strip().lower()
    records = _records_for_stage_filter(stage)
    return tuple(
        record.product
        for record in records
        if normalized in {tag.lower() for tag in record.structural_tags}
    )


def products_supporting_vocab(
    word: str,
    stage: StageId | None = None,
) -> tuple[int, ...]:
    normalized = word.strip().lower()
    records = _records_for_stage_filter(stage)
    return tuple(
        record.product
        for record in records
        if normalized in {tag.lower() for tag in record.vocab_tags}
    )


def products_by_hub_band(
    hub_band: str,
    stage: StageId | None = None,
) -> tuple[int, ...]:
    normalized = hub_band.strip().lower()
    if normalized not in {"low", "medium", "high"}:
        raise ValueError("hub_band must be one of: low, medium, high.")

    records = _records_for_stage_filter(stage)
    return tuple(record.product for record in records if record.hub_band == normalized)


def known_routes_at_stage(product: int, stage: StageId) -> tuple[tuple[int, int], ...]:
    validate_stage(stage)
    record = product_metadata(product)
    if _stage_index(record.stage_introduced) > _stage_index(stage):
        raise ValueError(
            f"Product {product} is not available at stage {stage}."
        )
    return record.known_routes_at_stage


def has_multiple_routes(product: int, stage: StageId | None = None) -> bool:
    record = product_metadata(product)
    if stage is not None:
        validate_stage(stage)
        if _stage_index(record.stage_introduced) > _stage_index(stage):
            raise ValueError(
                f"Product {product} is not available at stage {stage}."
            )
    return record.has_multiple_routes


def is_square_product(product: int) -> bool:
    return product_metadata(product).is_square


def has_factor_7(product: int) -> bool:
    return product_metadata(product).has_factor_7


def supports_recap_product(stage: StageId, product: int) -> bool:
    validate_stage(stage)
    return product in available_products(stage) and product not in new_products(stage)


def recommended_single_hub_products(stage: StageId) -> tuple[int, ...]:
    validate_stage(stage)
    available = [product_metadata(product) for product in available_products(stage)]
    ranked = sorted(
        available,
        key=_single_hub_sort_key,
    )
    return tuple(record.product for record in ranked)


def recommended_multi_route_compare_products(stage: StageId) -> tuple[int, ...]:
    validate_stage(stage)
    records = [
        product_metadata(product)
        for product in available_products(stage)
        if product_metadata(product).has_multiple_routes
    ]
    ranked = sorted(
        records,
        key=lambda record: (
            -_hub_band_rank(record.hub_band),
            _stage_index(record.stage_introduced),
            record.product,
        ),
    )
    return tuple(record.product for record in ranked)


def metadata_summary(product: int) -> dict[str, object]:
    record = product_metadata(product)
    return {
        "product": record.product,
        "stage_introduced": record.stage_introduced,
        "intro_family": record.intro_family,
        "factor_pairs": record.factor_pairs,
        "family_tags": record.family_tags,
        "structural_tags": record.structural_tags,
        "vocab_tags": record.vocab_tags,
        "route_profile": record.route_profile,
        "hub_band": record.hub_band,
        "has_multiple_routes": record.has_multiple_routes,
        "known_routes_at_stage": record.known_routes_at_stage,
        "is_square": record.is_square,
        "has_factor_7": record.has_factor_7,
        "notes": record.notes,
    }


def validate_product_metadata_system() -> None:
    if len(TMK_PRODUCT_METADATA) != 42:
        raise ValueError(
            f"TMK product metadata must contain exactly 42 core products. "
            f"Found {len(TMK_PRODUCT_METADATA)}."
        )

    seen_products: set[int] = set()
    for record in TMK_PRODUCT_METADATA:
        validate_product_metadata_record(record)
        if record.product in seen_products:
            raise ValueError(f"Duplicate product metadata found for product {record.product}.")
        seen_products.add(record.product)

    actual_stage_keys = set(INTRODUCED_PRODUCTS_BY_STAGE.keys())
    expected_stage_keys = set(SUPPORTED_STAGES)
    if actual_stage_keys != expected_stage_keys:
        raise ValueError(
            f"Introduced-products registry must contain exactly {expected_stage_keys}. "
            f"Found {actual_stage_keys}."
        )

    flattened_stage_products: list[int] = []
    for stage in _STAGE_ORDER:
        stage_products = INTRODUCED_PRODUCTS_BY_STAGE[stage]
        if not stage_products:
            raise ValueError(f"Stage '{stage}' must introduce at least one product.")
        flattened_stage_products.extend(stage_products)

    if len(flattened_stage_products) != 42:
        raise ValueError(
            f"Introduced-products registry must contain exactly 42 products. "
            f"Found {len(flattened_stage_products)}."
        )

    if len(set(flattened_stage_products)) != 42:
        raise ValueError("Introduced-products registry contains duplicate products.")

    metadata_products = {record.product for record in TMK_PRODUCT_METADATA}
    stage_products = set(flattened_stage_products)

    if metadata_products != stage_products:
        missing_in_registry = metadata_products - stage_products
        missing_in_metadata = stage_products - metadata_products
        raise ValueError(
            "Mismatch between TMK_PRODUCT_METADATA and INTRODUCED_PRODUCTS_BY_STAGE. "
            f"Missing in registry: {missing_in_registry}; missing in metadata: {missing_in_metadata}"
        )

    for stage in _STAGE_ORDER:
        for product in INTRODUCED_PRODUCTS_BY_STAGE[stage]:
            record = product_metadata(product)
            if record.stage_introduced != stage:
                raise ValueError(
                    f"Product {product} is listed under stage '{stage}' but metadata says "
                    f"'{record.stage_introduced}'."
                )

    for stage in _STAGE_ORDER:
        available = available_products(stage)
        expected_available_count = sum(
            len(INTRODUCED_PRODUCTS_BY_STAGE[current_stage])
            for current_stage in _STAGES_UP_TO(stage)
        )
        if len(available) != expected_available_count:
            raise ValueError(
                f"available_products('{stage}') returned {len(available)} products but "
                f"expected {expected_available_count}."
            )


def _records_for_stage_filter(stage: StageId | None) -> tuple[ProductMetadataRecord, ...]:
    if stage is None:
        return TMK_PRODUCT_METADATA

    validate_stage(stage)
    allowed = set(available_products(stage))
    return tuple(record for record in TMK_PRODUCT_METADATA if record.product in allowed)


def _stage_index(stage: StageId) -> int:
    return _STAGE_ORDER.index(stage)


def _STAGES_UP_TO(stage: StageId) -> tuple[StageId, ...]:
    validate_stage(stage)
    index = _stage_index(stage)
    return _STAGE_ORDER[: index + 1]


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


def _single_hub_sort_key(record: ProductMetadataRecord) -> tuple[int, int, int, int]:
    return (
        -_hub_band_rank(record.hub_band),
        -_route_profile_rank(record.route_profile),
        -int(record.has_multiple_routes),
        record.product,
    )


validate_product_metadata_system()
