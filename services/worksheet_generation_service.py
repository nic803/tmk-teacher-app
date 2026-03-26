from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any


def _load_attr(module_name: str, *names: str) -> Any:
    module = __import__(module_name, fromlist=["*"])
    for name in names:
        if hasattr(module, name):
            return getattr(module, name)
    available = ", ".join(sorted(dir(module)))
    raise ImportError(
        f"Could not find any of {names} in {module_name}. "
        f"Available names: {available}"
    )


def _as_plain_data(value: Any) -> Any:
    if value is None:
        return None
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, dict):
        return {k: _as_plain_data(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_as_plain_data(v) for v in value]
    return value


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


def _as_tuple(value: Any) -> tuple[Any, ...]:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    if isinstance(value, set):
        return tuple(value)
    return (value,)


def _normalise_selection(selection: Any) -> dict[str, Any]:
    selection = _as_plain_data(selection) or {}

    return {
        "selected_products": tuple(
            _get(selection, "selected_products", "products", default=()) or ()
        ),
        "recap_products": tuple(
            _get(selection, "recap_products", default=()) or ()
        ),
        "selection_reasons": tuple(
            _get(selection, "selection_reasons", "reasons", default=()) or ()
        ),
        "vocab_supported": tuple(
            _get(selection, "vocab_supported", "supported_vocabulary", default=()) or ()
        ),
        "structural_tags": tuple(
            _get(selection, "structural_tags", "tags", default=()) or ()
        ),
    }


def _normalise_student(student: Any) -> dict[str, Any]:
    student = _as_plain_data(student) or {}
    questions = _get(student, "questions", "items", default=()) or ()

    normalised_questions = []
    for index, item in enumerate(_as_tuple(questions), start=1):
        item = _as_plain_data(item) or {}
        normalised_questions.append(
            {
                "q_id": _get(item, "q_id", "id", default=index),
                "prompt": _get(item, "prompt", "question", "text", default=""),
            }
        )

    return {"questions": normalised_questions}


def _normalise_teacher(teacher: Any) -> dict[str, Any]:
    teacher = _as_plain_data(teacher) or {}
    answers = _get(teacher, "answers", "items", default=()) or ()

    normalised_answers = []
    for index, item in enumerate(_as_tuple(answers), start=1):
        item = _as_plain_data(item) or {}
        normalised_answers.append(
            {
                "q_id": _get(item, "q_id", "id", default=index),
                "answer": _get(item, "answer", "correct_answer", default=""),
                "msvwa_tags": tuple(_get(item, "msvwa_tags", "msvwa", default=()) or ()),
                "teacher_note": _get(item, "teacher_note", "note", default=""),
                "vocab": tuple(_get(item, "vocab", "vocabulary_words", default=()) or ()),
            }
        )

    return {"answers": normalised_answers}


def generate_worksheet_bundle(request: Any) -> dict[str, Any]:
    select_products = _load_attr(
        "services.product_selection_engine",
        "select_product_set",
        "select_products",
        "build_product_selection",
        "run_product_selection",
    )
    build_plan = _load_attr(
        "services.worksheet_planner",
        "build_worksheet_plan",
        "plan_worksheet",
        "create_worksheet_plan",
    )
    render_student = _load_attr(
        "services.worksheet_renderer",
        "render_student_worksheet",
        "render_worksheet",
        "render_student_sheet",
    )
    build_teacher = _load_attr(
        "services.teacher_key_builder",
        "build_teacher_key",
        "render_teacher_key",
        "create_teacher_key",
    )

    try:
        validate_bundle = _load_attr(
            "services.worksheet_validation",
            "validate_worksheet_bundle",
            "validate_bundle",
            "validate_worksheet_output",
        )
    except Exception:
        validate_bundle = None

    selection = select_products(request)
    plan = build_plan(request, selection)
    student = render_student(plan)
    teacher = build_teacher(plan)

    bundle = {
        "selection": _normalise_selection(selection),
        "student": _normalise_student(student),
        "teacher": _normalise_teacher(teacher),
    }

    if validate_bundle is not None:
        validate_bundle(bundle)

    return bundle


__all__ = ["generate_worksheet_bundle"]
