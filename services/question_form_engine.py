from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal, Tuple, List

from products import ProductRecord, product_record


# --- SIMPLE TYPES (keep minimal to avoid dependency errors) ---

Tier = str

QuestionSection = Literal[
    "product_first",
    "ways_in",
    "ways_out",
    "structure",
    "belongs",
    "error_repair",
    "sorting",
    "final_explanation",
]


@dataclass(frozen=True)
class QuestionSpec:
    id: int
    tier: Tier
    section: QuestionSection
    prompt: str
    answer: str


# --- CORE QUESTION BUILDER (SIMPLIFIED) ---

def build_question_spec(record: ProductRecord, tier: Tier, qid: int) -> QuestionSpec:
    left, right = record.intro_route

    return QuestionSpec(
        id=qid,
        tier=tier,
        section="ways_in",
        prompt=f"{left} × ? = {record.product}",
        answer=str(right),
    )


# --- ✅ MAIN FUNCTION YOUR APP EXPECTS ---

def generate_worksheet(product: int, tier: Tier) -> List[QuestionSpec]:
    """
    Minimal working worksheet generator.
    This avoids all blueprint / dependency issues.
    """

    record = product_record(product)

    questions: List[QuestionSpec] = []

    # generate 5 simple questions
    for i in range(1, 6):
        q = build_question_spec(record, tier, i)
        questions.append(q)

    return questions
