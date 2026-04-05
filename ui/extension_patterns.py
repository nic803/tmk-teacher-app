from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class PatternExample:
    expression: str
    working: Optional[str] = None


@dataclass(frozen=True)
class ExtensionPattern:
    pattern_id: str
    family: str  # "11x" or "12x"
    title: str
    rule: str
    teacher_explanation: str
    teaching_use: str
    examples: List[PatternExample] = field(default_factory=list)
    cue: Optional[str] = None
    cue_explanation: Optional[str] = None


EXTENSION_PATTERNS = [
    ExtensionPattern(
        pattern_id="eleven_ten_plus_one",
        family="11x",
        title="Ten-plus-one rule",
        rule="11 × n = 10 × n + 1 × n",
        teacher_explanation="11 times a number is ten times the number, plus one more group of the same number.",
        teaching_use="Main teaching rule for 11×.",
        examples=[
            PatternExample("11 × 4 = 44", "10 × 4 + 1 × 4 = 40 + 4 = 44"),
            PatternExample("11 × 7 = 77", "10 × 7 + 1 × 7 = 70 + 7 = 77"),
        ],
    ),
    ExtensionPattern(
        pattern_id="eleven_repeated_digit",
        family="11x",
        title="Repeated-digit pattern",
        rule="11 × 2 = 22, 11 × 3 = 33, ..., 11 × 9 = 99",
        teacher_explanation="Many 11× products repeat the digit, but the secure method is still 10× plus 1×.",
        teaching_use="Useful noticing pattern, not the first explanation.",
        examples=[
            PatternExample("11 × 2 = 22"),
            PatternExample("11 × 5 = 55"),
            PatternExample("11 × 9 = 99"),
        ],
    ),
    ExtensionPattern(
        pattern_id="eleven_beyond_repeated_digit",
        family="11x",
        title="Beyond the repeated-digit pattern",
        rule="11 × 10 = 110, 11 × 11 = 121, 11 × 12 = 132",
        teacher_explanation="The repeated-digit pattern is helpful for some facts, but the deeper structure is still 10×n + 1×n.",
        teaching_use="Prevents 11× from being taught as a trick only.",
        examples=[
            PatternExample("11 × 10 = 110", "10 × 10 + 1 × 10 = 100 + 10 = 110"),
            PatternExample("11 × 11 = 121", "10 × 11 + 1 × 11 = 110 + 11 = 121"),
            PatternExample("11 × 12 = 132", "10 × 12 + 1 × 12 = 120 + 12 = 132"),
        ],
    ),
    ExtensionPattern(
        pattern_id="eleven_new_route_opening",
        family="11x",
        title="New-route opening through 11×",
        rule="11× creates new products and new lawful routes in the extension layer.",
        teacher_explanation="Opening 11× adds new lawful routes and new products to the multiplication world.",
        teaching_use="Use when moving from pattern teaching to extension routes.",
        examples=[
            PatternExample("22 = 2 × 11"),
            PatternExample("33 = 3 × 11"),
            PatternExample("44 = 4 × 11"),
            PatternExample("55 = 5 × 11"),
        ],
    ),
    ExtensionPattern(
        pattern_id="twelve_ten_plus_two",
        family="12x",
        title="Ten-plus-two rule",
        rule="12 × n = 10 × n + 2 × n",
        teacher_explanation="12 times a number is ten times the number, plus two more groups of the same number.",
        teaching_use="Main teaching rule for 12×.",
        examples=[
            PatternExample("12 × 4 = 48", "10 × 4 + 2 × 4 = 40 + 8 = 48"),
            PatternExample("12 × 5 = 60", "10 × 5 + 2 × 5 = 50 + 10 = 60"),
        ],
    ),
    ExtensionPattern(
        pattern_id="twelve_double_six",
        family="12x",
        title="Double-the-6× rule",
        rule="12 × n = 2(6 × n)",
        teacher_explanation="If the 6× fact is known, the 12× fact can be found by doubling it.",
        teaching_use="Secondary derivation route after the ten-plus-two rule.",
        examples=[
            PatternExample("12 × 7 = 84", "2(6 × 7) = 2(42) = 84"),
            PatternExample("12 × 6 = 72", "2(6 × 6) = 2(36) = 72"),
        ],
    ),
    ExtensionPattern(
        pattern_id="twelve_even_products",
        family="12x",
        title="Even-product pattern",
        rule="All 12× products are even.",
        teacher_explanation="Because 12 is even, every 12× product is even.",
        teaching_use="Useful checking pattern.",
        examples=[
            PatternExample("12, 24, 36, 48, 60, 72"),
        ],
    ),
    ExtensionPattern(
        pattern_id="twelve_growth_by_twelve",
        family="12x",
        title="Growth-by-12 pattern",
        rule="Each new 12× product is 12 more than the one before it.",
        teacher_explanation="The 12× sequence grows by 12 each time.",
        teaching_use="Useful for sequence work and missing-number questions.",
        examples=[
            PatternExample("12, 24, 36, 48, 60, 72"),
        ],
    ),
    ExtensionPattern(
        pattern_id="twelve_clock_cue",
        family="12x",
        title="Clock cue",
        rule="12 × 5 = 60",
        teacher_explanation="A clock has 12 equal sections, and each section is 5 minutes. So 12 lots of 5 minutes make 60 minutes.",
        teaching_use="Memorable real-world anchor for 12×, especially for 12 × 5.",
        cue="5 minutes × 12 clock sections = 60 minutes",
        cue_explanation="Use this to anchor 12 × 5 = 60, but keep the structure visible: 10 × 5 + 2 × 5 = 50 + 10 = 60.",
        examples=[
            PatternExample("12 × 5 = 60", "10 × 5 + 2 × 5 = 50 + 10 = 60"),
        ],
    ),
    ExtensionPattern(
        pattern_id="twelve_new_route_opening",
        family="12x",
        title="New-route opening through 12×",
        rule="12× creates additional lawful routes into known products and introduces new products in the extension layer.",
        teacher_explanation="Opening 12× can reveal new true routes into products that were already known, and can also introduce new products in the extension layer.",
        teaching_use="Use when moving from pattern teaching to route overlap and extension products.",
        examples=[
            PatternExample("24 = 2 × 12 = 3 × 8 = 4 × 6"),
            PatternExample("36 = 3 × 12 = 4 × 9 = 6 × 6"),
            PatternExample("48 = 4 × 12 = 6 × 8"),
            PatternExample("60 = 5 × 12 = 6 × 10"),
            PatternExample("72 = 6 × 12 = 8 × 9"),
        ],
    ),
]


EXTENSION_PATTERN_GROUPS = {
    "11x_foundations": [
        "eleven_ten_plus_one",
        "eleven_repeated_digit",
        "eleven_beyond_repeated_digit",
        "eleven_new_route_opening",
    ],
    "12x_foundations": [
        "twelve_ten_plus_two",
        "twelve_double_six",
        "twelve_even_products",
        "twelve_growth_by_twelve",
        "twelve_clock_cue",
        "twelve_new_route_opening",
    ],
}


@dataclass(frozen=True)
class ExtensionSection:
    section_id: str
    title: str
    subtitle: str
    pattern_ids: List[str] = field(default_factory=list)


EXTENSION_PAGE_SECTIONS = [
    ExtensionSection(
        section_id="foundations_11x",
        title="11× Foundations",
        subtitle="Teach 11× through derivation, visible patterns, and new routes.",
        pattern_ids=EXTENSION_PATTERN_GROUPS["11x_foundations"],
    ),
    ExtensionSection(
        section_id="foundations_12x",
        title="12× Foundations",
        subtitle="Teach 12× through derivation, clock structure, and new routes.",
        pattern_ids=EXTENSION_PATTERN_GROUPS["12x_foundations"],
    ),
]
