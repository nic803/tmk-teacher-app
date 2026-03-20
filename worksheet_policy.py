from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal, Tuple

from tier_policy import Tier


WorksheetTierMode = Literal["single"]
WorksheetOutputMode = Literal["python_data_first"]
WorksheetMemoryCueMode = Literal["teacher_key_only"]


@dataclass(frozen=True)
class WorksheetPolicy:
    question_count: int
    tier_mode: WorksheetTierMode
    output_mode: WorksheetOutputMode
    memory_cue_mode: WorksheetMemoryCueMode
    supported_tiers: Tuple[Tier, ...]
    product_based_only: bool


WORKSHEET_POLICY: Final[WorksheetPolicy] = WorksheetPolicy(
    question_count=10,
    tier_mode="single",
    output_mode="python_data_first",
    memory_cue_mode="teacher_key_only",
    supported_tiers=("Support", "Core", "Extension"),
    product_based_only=True,
)


def worksheet_question_count() -> int:
    return WORKSHEET_POLICY.question_count


def worksheet_tier_mode() -> WorksheetTierMode:
    return WORKSHEET_POLICY.tier_mode


def worksheet_output_mode() -> WorksheetOutputMode:
    return WORKSHEET_POLICY.output_mode


def worksheet_memory_cue_mode() -> WorksheetMemoryCueMode:
    return WORKSHEET_POLICY.memory_cue_mode


def worksheet_supported_tiers() -> Tuple[Tier, ...]:
    return WORKSHEET_POLICY.supported_tiers


def worksheet_is_product_based_only() -> bool:
    return WORKSHEET_POLICY.product_based_only


def validate_supported_tier(tier: str) -> None:
    if tier not in WORKSHEET_POLICY.supported_tiers:
        raise ValueError(
            f"Unsupported worksheet tier '{tier}'. "
            f"Supported tiers: {WORKSHEET_POLICY.supported_tiers}"
        )


def validate_question_count(count: int) -> None:
    if count != WORKSHEET_POLICY.question_count:
        raise ValueError(
            f"Worksheet must contain exactly {WORKSHEET_POLICY.question_count} questions. "
            f"Found {count}."
        )
