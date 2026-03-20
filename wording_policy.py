from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Final, Tuple

from worlds import TMK_WORLD, BEYOND_10_WORLD, validate_world_name_usage


@dataclass(frozen=True)
class WordingPolicy:
    tmk_world_phrase: str
    beyond_10_world_phrase: str
    belong_phrase: str
    inside_phrase: str
    outside_phrase: str


WORDING_POLICY: Final[WordingPolicy] = WordingPolicy(
    tmk_world_phrase=TMK_WORLD,
    beyond_10_world_phrase=BEYOND_10_WORLD,
    belong_phrase="belong in",
    inside_phrase="inside",
    outside_phrase="outside",
)


def world_membership_prompt(number: int) -> str:
    text = f"Does {number} belong in {WORDING_POLICY.tmk_world_phrase}?"
    validate_world_name_usage(text)
    return text


def world_inside_statement(number: int) -> str:
    text = f"{number} is inside {WORDING_POLICY.tmk_world_phrase}."
    validate_world_name_usage(text)
    return text


def world_outside_statement(number: int) -> str:
    text = f"{number} is outside {WORDING_POLICY.tmk_world_phrase}."
    validate_world_name_usage(text)
    return text


def beyond_world_statement(number: int) -> str:
    text = f"{number} belongs in {WORDING_POLICY.beyond_10_world_phrase}."
    validate_world_name_usage(text)
    return text


PROMPT_TEMPLATES: Final[Dict[str, str]] = {
    "product_notice": "Find {product}.",
    "complete_way_in": "Complete: {left} × __ = {product}",
    "reverse_factor": "__ × {right} = {product}",
    "way_out": "{product} ÷ {divisor} = __",
    "truth_check": "Check: {left} × {right} = {product}. True or false?",
    "compare_routes": "Compare these ways in to {product}: {route_a} and {route_b}.",
    "error_repair": "Fix this: {left} × {right} = {product}",
    "sorting": "Which of these make {product}? {choices}",
    "explanation": "Explain something true about {product}.",
}


def render_prompt(template_key: str, data: Dict[str, object]) -> str:
    template = PROMPT_TEMPLATES[template_key]

    rendered = template.format(**data)

    validate_world_name_usage(rendered)

    return rendered
