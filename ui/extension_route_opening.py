from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple


FactorRoute = Tuple[int, int]


@dataclass(frozen=True)
class TwelveRouteOpeningProduct:
    product: int
    intro_route: Optional[FactorRoute]
    core_routes: List[FactorRoute] = field(default_factory=list)
    extension_routes: List[FactorRoute] = field(default_factory=list)
    teacher_focus: str = ""


TWELVE_ROUTE_OPENING_PRODUCTS: List[TwelveRouteOpeningProduct] = [
    TwelveRouteOpeningProduct(
        product=24,
        intro_route=(4, 6),
        core_routes=[(3, 8), (4, 6)],
        extension_routes=[(2, 12)],
        teacher_focus="24 already has two core routes. Extension adds 2 × 12 as a further true route.",
    ),
    TwelveRouteOpeningProduct(
        product=36,
        intro_route=(4, 9),
        core_routes=[(4, 9), (6, 6)],
        extension_routes=[(3, 12)],
        teacher_focus="36 already has two core routes. Extension adds 3 × 12 as a further true route.",
    ),
    TwelveRouteOpeningProduct(
        product=48,
        intro_route=(8, 6),
        core_routes=[(6, 8)],
        extension_routes=[(4, 12)],
        teacher_focus="48 gains a second lawful route when 12× is opened.",
    ),
    TwelveRouteOpeningProduct(
        product=60,
        intro_route=(6, 10),
        core_routes=[(6, 10)],
        extension_routes=[(5, 12)],
        teacher_focus="60 gains a second lawful route when 12× is opened.",
    ),
    TwelveRouteOpeningProduct(
        product=72,
        intro_route=(9, 8),
        core_routes=[(8, 9)],
        extension_routes=[(6, 12)],
        teacher_focus="72 gains a second lawful route when 12× is opened.",
    ),
]


TWELVE_ROUTE_PRODUCT_BY_VALUE = {
    item.product: item for item in TWELVE_ROUTE_OPENING_PRODUCTS
}


def get_twelve_route_opening_product(product: int) -> Optional[TwelveRouteOpeningProduct]:
    return TWELVE_ROUTE_PRODUCT_BY_VALUE.get(product)


@dataclass
class RouteOpeningActivityCard:
    product: int
    title: str
    focus: str
    teacher_explanation: str
    teacher_prompt: str
    pupil_tasks: List[str] = field(default_factory=list)
    example_questions: List[str] = field(default_factory=list)
    key_noticing: List[str] = field(default_factory=list)
    teaching_note: str = ""
    print_text: str = ""


def format_route(route: FactorRoute) -> str:
    return f"{route[0]} × {route[1]}"


def join_routes(routes: List[FactorRoute]) -> str:
    return ", ".join(format_route(route) for route in routes)


def build_route_opening_print_text(card: RouteOpeningActivityCard) -> str:
    lines = [
        f"Title: {card.title}",
        "",
        f"Focus product: {card.product}",
        "",
        "Teacher explanation:",
        card.teacher_explanation,
        "",
        "Teacher prompt:",
        card.teacher_prompt,
        "",
        "Pupil tasks:",
    ]

    for task in card.pupil_tasks:
        lines.append(f"- {task}")

    lines.extend(["", "Example questions:"])
    for question in card.example_questions:
        lines.append(f"- {question}")

    lines.extend(["", "Key noticing:"])
    for noticing in card.key_noticing:
        lines.append(f"- {noticing}")

    lines.extend(["", "Teaching note:", card.teaching_note])
    return "\n".join(lines)


def build_twelve_route_opening_activity(product: int) -> Optional[RouteOpeningActivityCard]:
    item = get_twelve_route_opening_product(product)
    if item is None:
        return None

    core_route_text = join_routes(item.core_routes)
    extension_route_text = join_routes(item.extension_routes)

    if len(item.core_routes) >= 2:
        teacher_explanation = (
            f"{item.product} already has more than one true route in core TMK: "
            f"{core_route_text}. In the extension layer, a further true route appears: "
            f"{extension_route_text}."
        )
        teacher_prompt = (
            f"{item.product} was already known in core TMK. What new route becomes possible "
            f"when the 12× extension is opened?"
        )
        pupil_tasks = [
            f"Read the core routes into {item.product}.",
            f"Read the new extension route into {item.product}.",
            "Say what stays the same across all the routes.",
            "Explain why the new route belongs to extension, not core.",
        ]
        example_questions = [
            f"Which core routes make {item.product}?",
            f"What new route appears when 12× is opened?",
            f"What product does {extension_route_text} make?",
            "Why was this route not used in core TMK?",
        ]
        key_noticing = [
            "The product stays the same.",
            "The factors change.",
            "Extension can reveal a new true route into a product that was already known.",
        ]
    else:
        teacher_explanation = (
            f"{item.product} has one core TMK route: {core_route_text}. "
            f"When the 12× extension is opened, a new lawful route appears: "
            f"{extension_route_text}."
        )
        teacher_prompt = (
            f"What new route into {item.product} becomes possible when 12× is allowed?"
        )
        pupil_tasks = [
            f"Read the core route into {item.product}.",
            f"Read the new extension route into {item.product}.",
            "Compare the two routes.",
            "Explain why the new route belongs to extension.",
        ]
        example_questions = [
            f"What is the core route into {item.product}?",
            f"What new route appears when 12× is opened?",
            f"What product does {extension_route_text} make?",
            "What stays the same when the route changes?",
        ]
        key_noticing = [
            "The product stays the same.",
            "The route changes.",
            "Extension can add a new lawful route to a product that had only one core route.",
        ]

    title = "12× route opening"
    teaching_note = (
        "Secure the core route or routes first. Reveal the 12× route afterwards as an extension route, not as a replacement."
    )

    card = RouteOpeningActivityCard(
        product=item.product,
        title=title,
        focus=item.teacher_focus,
        teacher_explanation=teacher_explanation,
        teacher_prompt=teacher_prompt,
        pupil_tasks=pupil_tasks,
        example_questions=example_questions,
        key_noticing=key_noticing,
        teaching_note=teaching_note,
    )
    card.print_text = build_route_opening_print_text(card)
    return card
