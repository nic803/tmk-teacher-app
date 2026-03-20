from __future__ import annotations

from typing import Final

from blueprint_rotation import register_blueprint_set
from worksheet_blueprints import WorksheetBlueprint, WorksheetSlot


SUPPORT_BLUEPRINT_A: Final[WorksheetBlueprint] = WorksheetBlueprint(
    tier="Support",
    slots=(
        WorksheetSlot(1, "product_notice", ("circle",)),
        WorksheetSlot(2, "intro_way_in", ("fill_blank",)),
        WorksheetSlot(3, "reverse_factor", ("match",)),
        WorksheetSlot(4, "way_out", ("fill_blank",)),
        WorksheetSlot(5, "truth_check", ("tick_yes_no",)),
        WorksheetSlot(6, "compare_routes", ("match",)),
        WorksheetSlot(7, "world_membership", ("tick_yes_no",)),
        WorksheetSlot(8, "error_repair", ("fill_blank",)),
        WorksheetSlot(9, "sorting", ("match",)),
        WorksheetSlot(10, "explanation", ("fill_blank",)),
    ),
)

SUPPORT_BLUEPRINT_B: Final[WorksheetBlueprint] = WorksheetBlueprint(
    tier="Support",
    slots=(
        WorksheetSlot(1, "product_notice", ("circle",)),
        WorksheetSlot(2, "intro_way_in", ("fill_blank",)),
        WorksheetSlot(3, "way_out", ("fill_blank",)),
        WorksheetSlot(4, "truth_check", ("tick_yes_no",)),
        WorksheetSlot(5, "reverse_factor", ("match",)),
        WorksheetSlot(6, "world_membership", ("tick_yes_no",)),
        WorksheetSlot(7, "compare_routes", ("match",)),
        WorksheetSlot(8, "error_repair", ("fill_blank",)),
        WorksheetSlot(9, "sorting", ("match",)),
        WorksheetSlot(10, "explanation", ("fill_blank",)),
    ),
)

CORE_BLUEPRINT_A: Final[WorksheetBlueprint] = WorksheetBlueprint(
    tier="Core",
    slots=(
        WorksheetSlot(1, "product_notice", ("find",)),
        WorksheetSlot(2, "intro_way_in", ("complete",)),
        WorksheetSlot(3, "reverse_factor", ("find",)),
        WorksheetSlot(4, "way_out", ("complete",)),
        WorksheetSlot(5, "truth_check", ("true_false",)),
        WorksheetSlot(6, "compare_routes", ("compare",)),
        WorksheetSlot(7, "world_membership", ("choose_one",)),
        WorksheetSlot(8, "error_repair", ("complete",)),
        WorksheetSlot(9, "sorting", ("simple_sort",)),
        WorksheetSlot(10, "explanation", ("find",)),
    ),
)

CORE_BLUEPRINT_B: Final[WorksheetBlueprint] = WorksheetBlueprint(
    tier="Core",
    slots=(
        WorksheetSlot(1, "product_notice", ("find",)),
        WorksheetSlot(2, "truth_check", ("true_false",)),
        WorksheetSlot(3, "intro_way_in", ("complete",)),
        WorksheetSlot(4, "compare_routes", ("compare",)),
        WorksheetSlot(5, "way_out", ("complete",)),
        WorksheetSlot(6, "world_membership", ("true_false",)),
        WorksheetSlot(7, "reverse_factor", ("find",)),
        WorksheetSlot(8, "error_repair", ("complete",)),
        WorksheetSlot(9, "sorting", ("simple_sort",)),
        WorksheetSlot(10, "explanation", ("compare",)),
    ),
)

CORE_BLUEPRINT_C: Final[WorksheetBlueprint] = WorksheetBlueprint(
    tier="Core",
    slots=(
        WorksheetSlot(1, "product_notice", ("find",)),
        WorksheetSlot(2, "intro_way_in", ("complete",)),
        WorksheetSlot(3, "way_out", ("complete",)),
        WorksheetSlot(4, "reverse_factor", ("find",)),
        WorksheetSlot(5, "world_membership", ("choose_one",)),
        WorksheetSlot(6, "truth_check", ("true_false",)),
        WorksheetSlot(7, "compare_routes", ("compare",)),
        WorksheetSlot(8, "error_repair", ("complete",)),
        WorksheetSlot(9, "sorting", ("simple_sort",)),
        WorksheetSlot(10, "explanation", ("find",)),
    ),
)

EXTENSION_BLUEPRINT_A: Final[WorksheetBlueprint] = WorksheetBlueprint(
    tier="Extension",
    slots=(
        WorksheetSlot(1, "product_notice", ("compare_routes",)),
        WorksheetSlot(2, "intro_way_in", ("rebuild_and_explain",)),
        WorksheetSlot(3, "reverse_factor", ("odd_one_out",)),
        WorksheetSlot(4, "way_out", ("compare_routes",)),
        WorksheetSlot(5, "truth_check", ("true_outside_false",)),
        WorksheetSlot(6, "compare_routes", ("compare_routes",)),
        WorksheetSlot(7, "world_membership", ("true_outside_false",)),
        WorksheetSlot(8, "error_repair", ("sort_and_justify",)),
        WorksheetSlot(9, "sorting", ("sort_and_justify",)),
        WorksheetSlot(10, "explanation", ("one_sentence_explain",)),
    ),
)

EXTENSION_BLUEPRINT_B: Final[WorksheetBlueprint] = WorksheetBlueprint(
    tier="Extension",
    slots=(
        WorksheetSlot(1, "product_notice", ("compare_routes",)),
        WorksheetSlot(2, "truth_check", ("true_outside_false",)),
        WorksheetSlot(3, "compare_routes", ("compare_routes",)),
        WorksheetSlot(4, "world_membership", ("true_outside_false",)),
        WorksheetSlot(5, "reverse_factor", ("odd_one_out",)),
        WorksheetSlot(6, "intro_way_in", ("rebuild_and_explain",)),
        WorksheetSlot(7, "way_out", ("compare_routes",)),
        WorksheetSlot(8, "sorting", ("sort_and_justify",)),
        WorksheetSlot(9, "error_repair", ("sort_and_justify",)),
        WorksheetSlot(10, "explanation", ("one_sentence_explain",)),
    ),
)


def register_all_blueprint_variants() -> None:
    register_blueprint_set(
        tier="Support",
        variant_a=SUPPORT_BLUEPRINT_A,
        variant_b=SUPPORT_BLUEPRINT_B,
    )
    register_blueprint_set(
        tier="Core",
        variant_a=CORE_BLUEPRINT_A,
        variant_b=CORE_BLUEPRINT_B,
        variant_c=CORE_BLUEPRINT_C,
    )
    register_blueprint_set(
        tier="Extension",
        variant_a=EXTENSION_BLUEPRINT_A,
        variant_b=EXTENSION_BLUEPRINT_B,
    )


register_all_blueprint_variants()
