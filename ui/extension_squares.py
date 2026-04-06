from dataclasses import dataclass
from typing import Dict, List, Tuple


Route = Tuple[int, int]


@dataclass(frozen=True)
class SquareExample:
    id: str
    product: int
    root: int
    square_route: Route
    is_core: bool
    other_core_routes: List[Route]
    notes: str


@dataclass(frozen=True)
class SquarePattern:
    id: str
    title: str
    summary: str
    teacher_note: str
    examples: List[str]


@dataclass(frozen=True)
class SquareSection:
    id: str
    title: str
    subtitle: str
    pattern_ids: List[str]


@dataclass(frozen=True)
class SquareActivity:
    id: str
    title: str
    focus: str
    teacher_explanation: str
    teacher_prompt: str
    pupil_tasks: List[str]
    example_questions: List[str]
    teaching_note: str


SQUARE_EXAMPLES: List[SquareExample] = [
    SquareExample(
        id="sq_1",
        product=1,
        root=1,
        square_route=(1, 1),
        is_core=True,
        other_core_routes=[],
        notes="Identity square.",
    ),
    SquareExample(
        id="sq_4",
        product=4,
        root=2,
        square_route=(2, 2),
        is_core=True,
        other_core_routes=[(1, 4)],
        notes="Square with more than one core route.",
    ),
    SquareExample(
        id="sq_9",
        product=9,
        root=3,
        square_route=(3, 3),
        is_core=True,
        other_core_routes=[(1, 9)],
        notes="Square with more than one core route.",
    ),
    SquareExample(
        id="sq_16",
        product=16,
        root=4,
        square_route=(4, 4),
        is_core=True,
        other_core_routes=[(2, 8)],
        notes="Square with more than one core route.",
    ),
    SquareExample(
        id="sq_25",
        product=25,
        root=5,
        square_route=(5, 5),
        is_core=True,
        other_core_routes=[],
        notes="Single-route square in the core world.",
    ),
    SquareExample(
        id="sq_36",
        product=36,
        root=6,
        square_route=(6, 6),
        is_core=True,
        other_core_routes=[(4, 9)],
        notes="Core square and bridge product.",
    ),
    SquareExample(
        id="sq_49",
        product=49,
        root=7,
        square_route=(7, 7),
        is_core=True,
        other_core_routes=[],
        notes="Closure square in the core world.",
    ),
    SquareExample(
        id="sq_64",
        product=64,
        root=8,
        square_route=(8, 8),
        is_core=True,
        other_core_routes=[],
        notes="Single-route square in the core world.",
    ),
    SquareExample(
        id="sq_81",
        product=81,
        root=9,
        square_route=(9, 9),
        is_core=True,
        other_core_routes=[],
        notes="Single-route square in the core world.",
    ),
    SquareExample(
        id="sq_100",
        product=100,
        root=10,
        square_route=(10, 10),
        is_core=True,
        other_core_routes=[],
        notes="Largest core square.",
    ),
    SquareExample(
        id="sq_121",
        product=121,
        root=11,
        square_route=(11, 11),
        is_core=False,
        other_core_routes=[],
        notes="Extension square.",
    ),
    SquareExample(
        id="sq_144",
        product=144,
        root=12,
        square_route=(12, 12),
        is_core=False,
        other_core_routes=[],
        notes="Extension square.",
    ),
]


SQUARE_PATTERNS: List[SquarePattern] = [
    SquarePattern(
        id="same_factor_square",
        title="Same-factor pattern",
        summary="A square number has a route of the form n × n.",
        teacher_note=(
            "Lead with multiplication structure first. The product is square because "
            "the same factor is used twice."
        ),
        examples=[
            "4 = 2 × 2",
            "25 = 5 × 5",
            "36 = 6 × 6",
            "121 = 11 × 11",
        ],
    ),
    SquarePattern(
        id="square_ladder",
        title="Square ladder",
        summary="Square numbers rise in order along the ladder 1², 2², 3², ...",
        teacher_note=(
            "Show core squares first, then extend naturally to 11² and 12²."
        ),
        examples=[
            "1, 4, 9, 16, 25, 36, 49, 64, 81, 100",
            "Extension continuation: 121, 144",
        ],
    ),
    SquarePattern(
        id="single_vs_multi_route_squares",
        title="Single-route and multi-route squares",
        summary=(
            "Some square numbers have only the square route in the bounded world, "
            "while others also have another route."
        ),
        teacher_note=(
            "This keeps the work product-first: square structure is a route property "
            "of the product."
        ),
        examples=[
            "25 = 5 × 5",
            "49 = 7 × 7",
            "9 = 3 × 3 = 1 × 9",
            "36 = 6 × 6 = 4 × 9",
        ],
    ),
]


SQUARE_SECTIONS: List[SquareSection] = [
    SquareSection(
        id="square_numbers_recap",
        title="Square Numbers Recap",
        subtitle="Known products with a same-factor route",
        pattern_ids=[
            "same_factor_square",
            "square_ladder",
            "single_vs_multi_route_squares",
        ],
    )
]


SQUARE_ACTIVITIES: List[SquareActivity] = [
    SquareActivity(
        id="find_the_square_route",
        title="Find the square route",
        focus="Recognise square numbers as products with a same-factor route.",
        teacher_explanation=(
            "A product is a square if one of its routes uses the same factor twice."
        ),
        teacher_prompt=(
            "Look at each product. Can you find a route of the form n × n?"
        ),
        pupil_tasks=[
            "Circle the products that are square numbers.",
            "Write the square route for each square number.",
            "Decide whether each square has only one route or more than one route.",
        ],
        example_questions=[
            "Is 16 a square number? Which route shows this?",
            "Why is 25 a square number?",
            "36 is a square number. Can you find another route into 36?",
            "Is 72 a square number? Explain why not.",
            "Which extension squares appear after 100?",
        ],
        teaching_note=(
            "Keep core and extension visible as separate labels. "
            "121 and 144 are extension squares, not core TMK products."
        ),
    )
]


SQUARE_BY_ID: Dict[str, SquareExample] = {item.id: item for item in SQUARE_EXAMPLES}
SQUARE_PATTERN_BY_ID: Dict[str, SquarePattern] = {item.id: item for item in SQUARE_PATTERNS}
SQUARE_SECTION_BY_ID: Dict[str, SquareSection] = {item.id: item for item in SQUARE_SECTIONS}
SQUARE_ACTIVITY_BY_ID: Dict[str, SquareActivity] = {item.id: item for item in SQUARE_ACTIVITIES}


def get_core_square_examples() -> List[SquareExample]:
    return [item for item in SQUARE_EXAMPLES if item.is_core]


def get_extension_square_examples() -> List[SquareExample]:
    return [item for item in SQUARE_EXAMPLES if not item.is_core]


def get_square_section(section_id: str) -> SquareSection:
    return SQUARE_SECTION_BY_ID[section_id]


def get_square_patterns_for_section(section_id: str) -> List[SquarePattern]:
    section = get_square_section(section_id)
    return [SQUARE_PATTERN_BY_ID[pattern_id] for pattern_id in section.pattern_ids]


def format_square_route(route: Route) -> str:
    a, b = route
    return f"{a} × {b}"


def format_square_example(example: SquareExample) -> str:
    main_line = f"{example.product} = {format_square_route(example.square_route)}"
    if example.other_core_routes:
        other = " = ".join(format_square_route(route) for route in example.other_core_routes)
        return f"{main_line} = {other}"
    return main_line


def build_square_activity_print_text(activity_id: str) -> str:
    activity = SQUARE_ACTIVITY_BY_ID[activity_id]
    lines = [
        activity.title,
        "",
        f"Focus: {activity.focus}",
        "",
        f"Teacher explanation: {activity.teacher_explanation}",
        f"Teacher prompt: {activity.teacher_prompt}",
        "",
        "Pupil tasks:",
    ]
    lines.extend(f"- {task}" for task in activity.pupil_tasks)
    lines.append("")
    lines.append("Example questions:")
    lines.extend(f"- {question}" for question in activity.example_questions)
    lines.append("")
    lines.append(f"Teaching note: {activity.teaching_note}")
    return "\n".join(lines)
