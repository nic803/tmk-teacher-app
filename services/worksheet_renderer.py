from __future__ import annotations

from typing import Any


def _get(value: Any, *names: str, default: Any = None) -> Any:
    if value is None:
        return default

    if isinstance(value, dict):
        for name in names:
            if name in value:
                return value[name]
        return default

    for name in names:
        if hasattr(value, name):
            return getattr(value, name)

    return default


def _question_prompt(item: dict[str, Any]) -> str:
    product = int(item["product"])
    q_id = int(item["q_id"])
    tier = str(item["tier"])
    source = str(item["source"])

    prompts = [
        f"Make {product} with a multiplication you know.",
        f"Complete: __ × __ = {product}",
        f"Write a division fact that matches {product}.",
        f"Which factors can make {product}?",
        f"Finish this: {product} ÷ __ = __",
        f"Show one route into {product}.",
        f"Tell a multiplication story for {product}.",
        f"What is the missing number? __ × __ = {product}",
        f"Circle a true fact for {product}.",
        f"Use what you know to explain {product}.",
        f"Write another fact family sentence for {product}.",
        f"Say how {product} is built.",
    ]

    prompt = prompts[(q_id - 1) % len(prompts)]

    if tier == "Support":
        prompt = f"{prompt} Use words or pictures."
    elif tier == "Extension":
        prompt = f"{prompt} Then explain your thinking."

    if source == "recap":
        prompt = f"Recap: {prompt}"

    return prompt


def render_student_worksheet(plan: Any) -> dict[str, Any]:
    items = _get(plan, "items", default=()) or ()

    questions: list[dict[str, Any]] = []
    for item in items:
        row = item if isinstance(item, dict) else dict(item)
        questions.append(
            {
                "q_id": int(row["q_id"]),
                "prompt": _question_prompt(row),
            }
        )

    return {
        "questions": questions,
    }


__all__ = ["render_student_worksheet"]
