from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class ActivityExample:
    prompt: str
    answer: Optional[str] = None


@dataclass(frozen=True)
class ExtensionActivity:
    activity_id: str
    family: str  # "11x", "12x", or "11x_12x"
    title: str
    activity_type: str  # e.g. "derive", "spot_pattern", "new_route", "core_or_extension"
    focus: str
    teacher_explanation: str
    teacher_prompt: str
    pupil_tasks: List[str] = field(default_factory=list)
    example_questions: List[str] = field(default_factory=list)
    examples: List[ActivityExample] = field(default_factory=list)
    teaching_note: str = ""
    related_pattern_ids: List[str] = field(default_factory=list)
    print_text: str = ""


def build_extension_activity_print_text(activity: ExtensionActivity) -> str:
    lines = [
        f"Title: {activity.title}",
        "",
        f"Focus: {activity.focus}",
        "",
        "Teacher explanation:",
        activity.teacher_explanation,
        "",
        "Teacher prompt:",
        activity.teacher_prompt,
        "",
        "Pupil tasks:",
    ]

    for task in activity.pupil_tasks:
        lines.append(f"- {task}")

    lines.extend(["", "Example questions:"])
    for question in activity.example_questions:
        lines.append(f"- {question}")

    if activity.examples:
        lines.extend(["", "Examples:"])
        for example in activity.examples:
            if example.answer:
                lines.append(f"- {example.prompt}: {example.answer}")
            else:
                lines.append(f"- {example.prompt}")

    if activity.teaching_note:
        lines.extend(["", "Teaching note:", activity.teaching_note])

    return "\n".join(lines)


_EXTENSIONS_ACTIVITY_SEED: List[ExtensionActivity] = [
    ExtensionActivity(
        activity_id="11x_derive_from_10_plus_1",
        family="11x",
        title="Build 11× from 10× and 1×",
        activity_type="derive",
        focus="Use the ten-plus-one rule to derive 11× facts.",
        teacher_explanation="11× facts should be built from known structure: 10× plus 1×.",
        teacher_prompt="How can we build this 11× fact from 10× and 1×?",
        pupil_tasks=[
            "Find the matching 10× fact.",
            "Find the matching 1× fact.",
            "Combine the two results.",
            "State the full 11× fact.",
        ],
        example_questions=[
            "What is 10 × 4?",
            "What is 1 × 4?",
            "So what is 11 × 4?",
            "How did you build 11 × 7?",
        ],
        examples=[
            ActivityExample("11 × 4", "10 × 4 + 1 × 4 = 40 + 4 = 44"),
            ActivityExample("11 × 7", "10 × 7 + 1 × 7 = 70 + 7 = 77"),
        ],
        teaching_note="Lead with derivation first. Use repeated digits only as a noticing pattern afterwards.",
        related_pattern_ids=[
            "eleven_ten_plus_one",
            "eleven_repeated_digit",
        ],
    ),
    ExtensionActivity(
        activity_id="11x_repeat_or_build",
        family="11x",
        title="Repeat or build?",
        activity_type="spot_pattern",
        focus="Notice repeated-digit products, but keep the structure visible.",
        teacher_explanation="Many 11× facts show repeated digits, but the secure method remains 10× plus 1×.",
        teacher_prompt="Can you see the repeated-digit pattern, and can you still explain it by building?",
        pupil_tasks=[
            "Read the 11× facts.",
            "Spot which products repeat digits.",
            "Explain each one using 10× plus 1×.",
            "Check what happens after 11 × 9.",
        ],
        example_questions=[
            "What do you notice about 11 × 5 = 55?",
            "Why does 11 × 10 not fit the repeated-digit pattern?",
            "How can you build 11 × 11?",
            "Is repeated-digit noticing enough on its own?",
        ],
        examples=[
            ActivityExample("11 × 5 = 55", "10 × 5 + 1 × 5 = 50 + 5 = 55"),
            ActivityExample("11 × 10 = 110", "10 × 10 + 1 × 10 = 100 + 10 = 110"),
            ActivityExample("11 × 11 = 121", "10 × 11 + 1 × 11 = 110 + 11 = 121"),
        ],
        teaching_note="Use this to prevent 11× from becoming a trick-only topic.",
        related_pattern_ids=[
            "eleven_repeated_digit",
            "eleven_beyond_repeated_digit",
        ],
    ),
    ExtensionActivity(
        activity_id="12x_derive_from_10_plus_2",
        family="12x",
        title="Build 12× from 10× and 2×",
        activity_type="derive",
        focus="Use the ten-plus-two rule to derive 12× facts.",
        teacher_explanation="12× facts should be built from known structure: 10× plus 2×.",
        teacher_prompt="How can we build this 12× fact from 10× and 2×?",
        pupil_tasks=[
            "Find the matching 10× fact.",
            "Find the matching 2× fact.",
            "Combine the two results.",
            "State the full 12× fact.",
        ],
        example_questions=[
            "What is 10 × 5?",
            "What is 2 × 5?",
            "So what is 12 × 5?",
            "How did you build 12 × 7?",
        ],
        examples=[
            ActivityExample("12 × 5", "10 × 5 + 2 × 5 = 50 + 10 = 60"),
            ActivityExample("12 × 7", "10 × 7 + 2 × 7 = 70 + 14 = 84"),
        ],
        teaching_note="This should be the main derivation route for 12×.",
        related_pattern_ids=[
            "twelve_ten_plus_two",
        ],
    ),
    ExtensionActivity(
        activity_id="12x_clock_cue",
        family="12x",
        title="Clock to product",
        activity_type="spot_pattern",
        focus="Use the clock as a real-world cue for 12 × 5 = 60.",
        teacher_explanation=(
            "A clock has 12 equal sections, and each section is 5 minutes. "
            "This gives a memorable anchor for 12 × 5 = 60."
        ),
        teacher_prompt="How does the clock help us know that 12 × 5 = 60?",
        pupil_tasks=[
            "Count around the clock in steps of 5.",
            "Say how many sections the clock has.",
            "Say how many minutes are in each section.",
            "State the matching multiplication fact.",
        ],
        example_questions=[
            "How many 5-minute sections are there in one hour?",
            "What is 12 × 5?",
            "How does the clock show this?",
            "How can we also build it from 10 × 5 and 2 × 5?",
        ],
        examples=[
            ActivityExample("12 × 5", "5 minutes × 12 sections = 60 minutes"),
            ActivityExample("12 × 5", "10 × 5 + 2 × 5 = 50 + 10 = 60"),
        ],
        teaching_note="Use the clock cue to support the structure, not replace it.",
        related_pattern_ids=[
            "twelve_clock_cue",
            "twelve_ten_plus_two",
        ],
    ),
    ExtensionActivity(
        activity_id="12x_new_routes",
        family="12x",
        title="New routes opened by 12×",
        activity_type="new_route",
        focus="See how 12× reveals new lawful routes into known products.",
        teacher_explanation="Opening 12× can reveal a new true route into a product that was already known in core TMK.",
        teacher_prompt="Which new route becomes possible when 12× is allowed?",
        pupil_tasks=[
            "Read the known core routes into the product.",
            "Find the added 12× route.",
            "Say what stays the same across all routes.",
            "Explain why the new route belongs to extension.",
        ],
        example_questions=[
            "What new route does 12 add to 24?",
            "What new route does 12 add to 36?",
            "Why is 3 × 12 extension, not core?",
            "What stays the same when the route changes?",
        ],
        examples=[
            ActivityExample("24", "2 × 12 = 3 × 8 = 4 × 6"),
            ActivityExample("36", "3 × 12 = 4 × 9 = 6 × 6"),
            ActivityExample("60", "5 × 12 = 6 × 10"),
        ],
        teaching_note="Secure the core routes first, then reveal the extension route.",
        related_pattern_ids=[
            "twelve_new_route_opening",
        ],
    ),
    ExtensionActivity(
        activity_id="11x_12x_core_or_extension",
        family="11x_12x",
        title="Core or extension?",
        activity_type="core_or_extension",
        focus="Classify routes and products as core or extension.",
        teacher_explanation="This helps learners see that extension adds lawful routes and products without replacing the core.",
        teacher_prompt="Does this route belong to the core TMK world or to the extension layer?",
        pupil_tasks=[
            "Read each route.",
            "Decide whether it belongs to core or extension.",
            "Explain your choice.",
            "Sort the routes into two groups.",
        ],
        example_questions=[
            "Is 4 × 9 core or extension?",
            "Is 3 × 12 core or extension?",
            "Is 2 × 10 core or extension?",
            "Why is 5 × 12 an extension route?",
        ],
        examples=[
            ActivityExample("4 × 9", "core"),
            ActivityExample("3 × 12", "extension"),
            ActivityExample("2 × 10", "core"),
            ActivityExample("5 × 12", "extension"),
        ],
        teaching_note="Keep the boundary clear: core uses factors up to 10; extension opens 11 and 12.",
        related_pattern_ids=[
            "eleven_new_route_opening",
            "twelve_new_route_opening",
        ],
    ),
]


EXTENSION_ACTIVITIES: List[ExtensionActivity] = [
    ExtensionActivity(
        activity_id=activity.activity_id,
        family=activity.family,
        title=activity.title,
        activity_type=activity.activity_type,
        focus=activity.focus,
        teacher_explanation=activity.teacher_explanation,
        teacher_prompt=activity.teacher_prompt,
        pupil_tasks=list(activity.pupil_tasks),
        example_questions=list(activity.example_questions),
        examples=list(activity.examples),
        teaching_note=activity.teaching_note,
        related_pattern_ids=list(activity.related_pattern_ids),
        print_text=build_extension_activity_print_text(activity),
    )
    for activity in _EXTENSIONS_ACTIVITY_SEED
]


EXTENSION_ACTIVITY_GROUPS: Dict[str, List[str]] = {
    "11x_resources": [
        "11x_derive_from_10_plus_1",
        "11x_repeat_or_build",
    ],
    "12x_resources": [
        "12x_derive_from_10_plus_2",
        "12x_clock_cue",
        "12x_new_routes",
    ],
    "boundary_resources": [
        "11x_12x_core_or_extension",
    ],
}


ACTIVITY_BY_ID: Dict[str, ExtensionActivity] = {
    activity.activity_id: activity for activity in EXTENSION_ACTIVITIES
}


def get_extension_activity(activity_id: str) -> Optional[ExtensionActivity]:
    return ACTIVITY_BY_ID.get(activity_id)


def get_extension_activities_for_group(group_id: str) -> List[ExtensionActivity]:
    activity_ids = EXTENSION_ACTIVITY_GROUPS.get(group_id, [])
    return [ACTIVITY_BY_ID[activity_id] for activity_id in activity_ids if activity_id in ACTIVITY_BY_ID]


def get_extension_activities_for_family(family: str) -> List[ExtensionActivity]:
    return [activity for activity in EXTENSION_ACTIVITIES if activity.family == family]
