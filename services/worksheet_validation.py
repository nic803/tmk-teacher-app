from __future__ import annotations

from typing import Any


def validate_worksheet_bundle(bundle: Any) -> None:
    if not isinstance(bundle, dict):
        raise ValueError("Worksheet bundle must be a dict.")

    for key in ("selection", "student", "teacher"):
        if key not in bundle:
            raise ValueError(f"Worksheet bundle missing '{key}'.")

    student = bundle["student"]
    teacher = bundle["teacher"]

    if not isinstance(student, dict):
        raise ValueError("Student worksheet must be a dict.")
    if not isinstance(teacher, dict):
        raise ValueError("Teacher key must be a dict.")

    questions = student.get("questions", [])
    answers = teacher.get("answers", [])

    if not isinstance(questions, list):
        raise ValueError("Student questions must be a list.")
    if not isinstance(answers, list):
        raise ValueError("Teacher answers must be a list.")

    if len(questions) != len(answers):
        raise ValueError("Student/teacher item count mismatch.")


__all__ = ["validate_worksheet_bundle"]
