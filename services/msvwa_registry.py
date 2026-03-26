from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from models.worksheet_models import (
    MSVWATag,
    QuizFormat,
    WorksheetItemFamily,
    WorksheetTier,
    validate_item_family,
    validate_msvwa_tags,
    validate_quiz_format,
    validate_tier,
)


@dataclass(frozen=True)
class MSVWAProfile:
    primary: tuple[MSVWATag, ...]
    secondary: tuple[MSVWATag, ...] = ()
    light: tuple[MSVWATag, ...] = ()


@dataclass(frozen=True)
class ItemFamilyMSVWADefinition:
    family: WorksheetItemFamily
    default_tags: tuple[MSVWATag, ...]
    reason: str


@dataclass(frozen=True)
class FormatMSVWABoost:
    quiz_format: QuizFormat
    boost_tags: tuple[MSVWATag, ...]
    reason: str


ITEM_FAMILY_TO_MSVWA: Final[dict[WorksheetItemFamily, ItemFamilyMSVWADefinition]] = {
    "product_recognition": ItemFamilyMSVWADefinition(
        family="product_recognition",
        default_tags=("A", "M"),
        reason=(
            "The learner notices the correct signal and marks the target product."
        ),
    ),
    "route_in": ItemFamilyMSVWADefinition(
        family="route_in",
        default_tags=("S", "W"),
        reason=(
            "The learner follows a multiplication sequence into the product and holds the relation."
        ),
    ),
    "missing_factor": ItemFamilyMSVWADefinition(
        family="missing_factor",
        default_tags=("S", "W"),
        reason=(
            "The learner reconstructs a partial route and holds the factor-product relation."
        ),
    ),
    "another_way": ItemFamilyMSVWADefinition(
        family="another_way",
        default_tags=("V", "W"),
        reason=(
            "The learner shows variation while keeping the same product in view."
        ),
    ),
    "compare_routes": ItemFamilyMSVWADefinition(
        family="compare_routes",
        default_tags=("V", "M", "W"),
        reason=(
            "The learner compares sameness and difference across routes, checks what matches, "
            "and holds the compared relations."
        ),
    ),
    "route_out": ItemFamilyMSVWADefinition(
        family="route_out",
        default_tags=("S", "W"),
        reason=(
            "The learner uses inverse sequence from the product and holds the linked relation."
        ),
    ),
    "check_match": ItemFamilyMSVWADefinition(
        family="check_match",
        default_tags=("A", "M"),
        reason=(
            "The learner attends to the target and marks the matching route, fact, or product."
        ),
    ),
    "correct_incorrect": ItemFamilyMSVWADefinition(
        family="correct_incorrect",
        default_tags=("M", "W"),
        reason=(
            "The learner checks mathematical status and verifies the relation against the known structure."
        ),
    ),
    "error_repair": ItemFamilyMSVWADefinition(
        family="error_repair",
        default_tags=("M", "S", "W"),
        reason=(
            "The learner detects an error, restores the correct sequence, and holds the repaired relation."
        ),
    ),
    "structural_grouping": ItemFamilyMSVWADefinition(
        family="structural_grouping",
        default_tags=("A", "V", "M"),
        reason=(
            "The learner selects signals, compares structure, and classifies mathematical status."
        ),
    ),
    "final_explanation": ItemFamilyMSVWADefinition(
        family="final_explanation",
        default_tags=("W",),
        reason=(
            "Explanation requires holding mathematical relations together; a secondary tag is added from context."
        ),
    ),
}


FORMAT_MSVWA_BOOST: Final[dict[QuizFormat, FormatMSVWABoost]] = {
    "circle": FormatMSVWABoost(
        quiz_format="circle",
        boost_tags=("A",),
        reason="Circle tasks foreground attention to the correct signal.",
    ),
    "tick": FormatMSVWABoost(
        quiz_format="tick",
        boost_tags=("A",),
        reason="Tick tasks foreground attention to the correct signal.",
    ),
    "yes_no": FormatMSVWABoost(
        quiz_format="yes_no",
        boost_tags=("M",),
        reason="Yes/no tasks foreground correctness status.",
    ),
    "tick_all": FormatMSVWABoost(
        quiz_format="tick_all",
        boost_tags=("A", "V", "M"),
        reason="Tick-all tasks combine noticing, comparison, and status checking.",
    ),
    "match": FormatMSVWABoost(
        quiz_format="match",
        boost_tags=("A", "W"),
        reason="Match tasks require noticing correspondences and holding linked pairs together.",
    ),
    "sort": FormatMSVWABoost(
        quiz_format="sort",
        boost_tags=("V", "M"),
        reason="Sort tasks foreground comparison and structural status classification.",
    ),
    "choose": FormatMSVWABoost(
        quiz_format="choose",
        boost_tags=("A", "M"),
        reason="Choice tasks emphasise noticing and selecting the correct mathematical status.",
    ),
    "fill_box": FormatMSVWABoost(
        quiz_format="fill_box",
        boost_tags=("S", "W"),
        reason="Fill-box tasks foreground completion of a sequence while holding the relation.",
    ),
    "label_from_options": FormatMSVWABoost(
        quiz_format="label_from_options",
        boost_tags=("A", "W"),
        reason="Label tasks require noticing the right word and attaching it to the structure.",
    ),
}


TIER_PREFERRED_MSVWA: Final[dict[WorksheetTier, MSVWAProfile]] = {
    "Support": MSVWAProfile(
        primary=("A", "S", "W"),
        secondary=("V",),
        light=("M",),
    ),
    "Core": MSVWAProfile(
        primary=("S", "V", "W"),
        secondary=("A",),
        light=("M",),
    ),
    "Extension": MSVWAProfile(
        primary=("V", "M", "W"),
        secondary=("S",),
        light=("A",),
    ),
}


def get_family_msvwa_definition(
    family: WorksheetItemFamily,
) -> ItemFamilyMSVWADefinition:
    validate_item_family(family)
    return ITEM_FAMILY_TO_MSVWA[family]


def get_format_msvwa_boost(
    quiz_format: QuizFormat,
) -> FormatMSVWABoost:
    validate_quiz_format(quiz_format)
    return FORMAT_MSVWA_BOOST[quiz_format]


def get_tier_msvwa_profile(
    tier: WorksheetTier,
) -> MSVWAProfile:
    validate_tier(tier)
    return TIER_PREFERRED_MSVWA[tier]


def family_default_tags(
    family: WorksheetItemFamily,
) -> tuple[MSVWATag, ...]:
    return get_family_msvwa_definition(family).default_tags


def format_boost_tags(
    quiz_format: QuizFormat,
) -> tuple[MSVWATag, ...]:
    return get_format_msvwa_boost(quiz_format).boost_tags


def resolve_item_msvwa(
    family: WorksheetItemFamily,
    quiz_format: QuizFormat,
    tier: WorksheetTier,
    contextual_secondary_tag: MSVWATag | None = None,
) -> tuple[MSVWATag, ...]:
    validate_item_family(family)
    validate_quiz_format(quiz_format)
    validate_tier(tier)

    family_tags = family_default_tags(family)
    format_tags = format_boost_tags(quiz_format)

    merged = _dedupe_tags(family_tags + format_tags)

    if family == "final_explanation" and contextual_secondary_tag is not None:
        merged = _dedupe_tags(merged + (contextual_secondary_tag,))

    profile = get_tier_msvwa_profile(tier)
    ranked = _rank_tags_against_profile(merged, profile)

    final_tags = ranked[:3]
    validate_msvwa_tags(final_tags)
    return final_tags


def resolve_item_msvwa_reason(
    family: WorksheetItemFamily,
    quiz_format: QuizFormat,
    tier: WorksheetTier,
    contextual_secondary_tag: MSVWATag | None = None,
) -> str:
    tags = resolve_item_msvwa(
        family=family,
        quiz_format=quiz_format,
        tier=tier,
        contextual_secondary_tag=contextual_secondary_tag,
    )
    family_reason = get_family_msvwa_definition(family).reason
    format_reason = get_format_msvwa_boost(quiz_format).reason
    profile_reason = tier_profile_summary(tier)

    return (
        f"MSVWA {', '.join(tags)}. {family_reason} {format_reason} "
        f"Tier profile emphasis: {profile_reason}."
    )


def tier_profile_summary(tier: WorksheetTier) -> str:
    profile = get_tier_msvwa_profile(tier)
    return (
        f"primary {', '.join(profile.primary)}; "
        f"secondary {', '.join(profile.secondary) if profile.secondary else 'none'}; "
        f"light {', '.join(profile.light) if profile.light else 'none'}"
    )


def worksheet_tag_counts(
    tags_by_item: tuple[tuple[MSVWATag, ...], ...],
) -> dict[MSVWATag, int]:
    counts: dict[MSVWATag, int] = {
        "M": 0,
        "S": 0,
        "V": 0,
        "W": 0,
        "A": 0,
    }
    for item_tags in tags_by_item:
        for tag in item_tags:
            counts[tag] += 1
    return counts


def dominant_tags_for_worksheet(
    tags_by_item: tuple[tuple[MSVWATag, ...], ...],
) -> tuple[MSVWATag, ...]:
    counts = worksheet_tag_counts(tags_by_item)
    ranked = sorted(
        counts.items(),
        key=lambda item: (-item[1], _tag_order(item[0])),
    )
    non_zero = [tag for tag, count in ranked if count > 0]
    return tuple(non_zero[:3])


def worksheet_matches_tier_profile(
    tags_by_item: tuple[tuple[MSVWATag, ...], ...],
    tier: WorksheetTier,
) -> bool:
    validate_tier(tier)
    counts = worksheet_tag_counts(tags_by_item)
    profile = get_tier_msvwa_profile(tier)

    primary_total = sum(counts[tag] for tag in profile.primary)
    secondary_total = sum(counts[tag] for tag in profile.secondary)
    light_total = sum(counts[tag] for tag in profile.light)

    if tier == "Support":
        return primary_total >= secondary_total and primary_total >= light_total
    if tier == "Core":
        return primary_total >= secondary_total and primary_total >= light_total
    if tier == "Extension":
        return primary_total >= secondary_total and primary_total >= light_total

    raise ValueError(f"Unsupported tier '{tier}'.")


def tier_profile_alignment_report(
    tags_by_item: tuple[tuple[MSVWATag, ...], ...],
    tier: WorksheetTier,
) -> dict[str, object]:
    validate_tier(tier)
    counts = worksheet_tag_counts(tags_by_item)
    profile = get_tier_msvwa_profile(tier)

    primary_total = sum(counts[tag] for tag in profile.primary)
    secondary_total = sum(counts[tag] for tag in profile.secondary)
    light_total = sum(counts[tag] for tag in profile.light)

    return {
        "tier": tier,
        "counts": counts,
        "primary": {
            "tags": profile.primary,
            "total": primary_total,
        },
        "secondary": {
            "tags": profile.secondary,
            "total": secondary_total,
        },
        "light": {
            "tags": profile.light,
            "total": light_total,
        },
        "dominant_tags": dominant_tags_for_worksheet(tags_by_item),
        "matches_profile": worksheet_matches_tier_profile(tags_by_item, tier),
    }


def validate_item_msvwa_assignment(
    family: WorksheetItemFamily,
    quiz_format: QuizFormat,
    tier: WorksheetTier,
    tags: tuple[MSVWATag, ...],
) -> None:
    validate_item_family(family)
    validate_quiz_format(quiz_format)
    validate_tier(tier)
    validate_msvwa_tags(tags)

    expected = set(
        resolve_item_msvwa(
            family=family,
            quiz_format=quiz_format,
            tier=tier,
        )
    )
    actual = set(tags)

    if not actual.issubset({"M", "S", "V", "W", "A"}):
        raise ValueError("Invalid MSVWA tag in item assignment.")

    if not actual.intersection(expected):
        raise ValueError(
            f"Assigned tags {tags} do not align with expected MSVWA profile "
            f"for family '{family}', format '{quiz_format}', tier '{tier}'."
        )


def validate_worksheet_msvwa_distribution(
    tags_by_item: tuple[tuple[MSVWATag, ...], ...],
    tier: WorksheetTier,
) -> None:
    validate_tier(tier)

    if not tags_by_item:
        raise ValueError("Worksheet must contain at least one item tag set.")

    for item_tags in tags_by_item:
        validate_msvwa_tags(item_tags)

    if not worksheet_matches_tier_profile(tags_by_item, tier):
        report = tier_profile_alignment_report(tags_by_item, tier)
        raise ValueError(
            f"Worksheet MSVWA distribution does not align with tier '{tier}'. "
            f"Report: {report}"
        )


def family_default_reason(
    family: WorksheetItemFamily,
) -> str:
    return get_family_msvwa_definition(family).reason


def format_boost_reason(
    quiz_format: QuizFormat,
) -> str:
    return get_format_msvwa_boost(quiz_format).reason


def all_family_default_tags() -> tuple[tuple[WorksheetItemFamily, tuple[MSVWATag, ...]], ...]:
    return tuple(
        (family, definition.default_tags)
        for family, definition in ITEM_FAMILY_TO_MSVWA.items()
    )


def all_format_boost_tags() -> tuple[tuple[QuizFormat, tuple[MSVWATag, ...]], ...]:
    return tuple(
        (quiz_format, definition.boost_tags)
        for quiz_format, definition in FORMAT_MSVWA_BOOST.items()
    )


def all_tier_profiles() -> tuple[tuple[WorksheetTier, MSVWAProfile], ...]:
    return tuple(TIER_PREFERRED_MSVWA.items())


def validate_msvwa_registry() -> None:
    expected_families = {
        "product_recognition",
        "route_in",
        "missing_factor",
        "another_way",
        "compare_routes",
        "route_out",
        "check_match",
        "correct_incorrect",
        "error_repair",
        "structural_grouping",
        "final_explanation",
    }
    actual_families = set(ITEM_FAMILY_TO_MSVWA.keys())
    if actual_families != expected_families:
        raise ValueError(
            f"ITEM_FAMILY_TO_MSVWA must contain exactly {expected_families}. "
            f"Found {actual_families}."
        )

    expected_formats = {
        "circle",
        "tick",
        "yes_no",
        "tick_all",
        "match",
        "sort",
        "choose",
        "fill_box",
        "label_from_options",
    }
    actual_formats = set(FORMAT_MSVWA_BOOST.keys())
    if actual_formats != expected_formats:
        raise ValueError(
            f"FORMAT_MSVWA_BOOST must contain exactly {expected_formats}. "
            f"Found {actual_formats}."
        )

    expected_tiers = {"Support", "Core", "Extension"}
    actual_tiers = set(TIER_PREFERRED_MSVWA.keys())
    if actual_tiers != expected_tiers:
        raise ValueError(
            f"TIER_PREFERRED_MSVWA must contain exactly {expected_tiers}. "
            f"Found {actual_tiers}."
        )

    for definition in ITEM_FAMILY_TO_MSVWA.values():
        validate_item_family(definition.family)
        validate_msvwa_tags(definition.default_tags)

    for definition in FORMAT_MSVWA_BOOST.values():
        validate_quiz_format(definition.quiz_format)
        validate_msvwa_tags(definition.boost_tags)

    for tier, profile in TIER_PREFERRED_MSVWA.items():
        validate_tier(tier)
        validate_msvwa_tags(profile.primary)
        if profile.secondary:
            validate_msvwa_tags(profile.secondary)
        if profile.light:
            validate_msvwa_tags(profile.light)

        overlap = set(profile.primary) & set(profile.secondary)
        overlap |= set(profile.primary) & set(profile.light)
        overlap |= set(profile.secondary) & set(profile.light)
        if overlap:
            raise ValueError(
                f"Tier profile '{tier}' has overlapping MSVWA categories: {overlap}"
            )


def _dedupe_tags(tags: tuple[MSVWATag, ...]) -> tuple[MSVWATag, ...]:
    ordered: list[MSVWATag] = []
    for tag in tags:
        if tag not in ordered:
            ordered.append(tag)
    return tuple(ordered)


def _rank_tags_against_profile(
    tags: tuple[MSVWATag, ...],
    profile: MSVWAProfile,
) -> tuple[MSVWATag, ...]:
    unique_tags = _dedupe_tags(tags)

    def score(tag: MSVWATag) -> tuple[int, int]:
        if tag in profile.primary:
            return (3, -profile.primary.index(tag))
        if tag in profile.secondary:
            return (2, -profile.secondary.index(tag))
        if tag in profile.light:
            return (1, -profile.light.index(tag))
        return (0, -_tag_order(tag))

    ranked = sorted(
        unique_tags,
        key=lambda tag: (-score(tag)[0], score(tag)[1], _tag_order(tag)),
    )
    return tuple(ranked)


def _tag_order(tag: MSVWATag) -> int:
    order = {"M": 0, "S": 1, "V": 2, "W": 3, "A": 4}
    return order[tag]


validate_msvwa_registry()
