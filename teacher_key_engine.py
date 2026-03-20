from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from memory_cues import memory_cues_for_product
from patterns import product_pattern_ids
from products import product_record
from question_form_engine import QuestionSpec
from worksheet_policy import worksheet_memory_cue_mode


@dataclass(frozen=True)
class TeacherKey:
    answers: Tuple[Dict[str, object], ...]
    pattern_ids: Tuple[str, ...]
    memory_cue_ids: Tuple[str, ...]
    notes: Tuple[str, ...]


def build_teacher_key(
    product: int,
    questions: Tuple[QuestionSpec, ...],
) -> TeacherKey:
    record = product_record(product)
    memory_cues = memory_cues_for_product(product)

    return TeacherKey(
        answers=tuple(question.answer_data for question in questions),
        pattern_ids=product_pattern_ids(product),
        memory_cue_ids=_teacher_memory_cue_ids(memory_cues),
        notes=(
            f"Product: {record.product}",
            f"Stage: {record.stage}",
            f"Intro route: {record.intro_route[0]} × {record.intro_route[1]}",
            f"Structural role: {record.structural_role}",
            f"Factor families: {len(record.factor_families)}",
        ),
    )


def _teacher_memory_cue_ids(memory_cues: Tuple[object, ...]) -> Tuple[str, ...]:
    if worksheet_memory_cue_mode() != "teacher_key_only":
        return ()
    return tuple(cue.id for cue in memory_cues)
