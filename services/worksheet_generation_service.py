from __future__ import annotations

from models.worksheet_models import (
    ProductSelectionRequest,
    WorksheetBundle,
)

from services.product_selection_engine import (
    select_product_set,
)

from services.worksheet_planner import (
    build_worksheet_plan,
)

from services.worksheet_renderer import (
    render_student_worksheet,
)

from services.teacher_key_builder import (
    build_teacher_key,
)

from services.worksheet_validation import (
    validate_bundle,
)


def generate_worksheet_bundle(
    request: ProductSelectionRequest,
) -> WorksheetBundle:
    """
    Generate a full worksheet bundle.

    Pipeline:

    1. Select products
    2. Build worksheet plan
    3. Render student worksheet
    4. Build teacher key
    5. Validate entire bundle
    """

    # -----------------------------
    # STEP 1 — PRODUCT SELECTION
    # -----------------------------

    selection = select_product_set(request)

    # -----------------------------
    # STEP 2 — PLAN WORKSHEET
    # -----------------------------

    plan = build_worksheet_plan(selection)

    # -----------------------------
    # STEP 3 — RENDER STUDENT WORKSHEET
    # -----------------------------

    student_worksheet = render_student_worksheet(plan)

    # -----------------------------
    # STEP 4 — BUILD TEACHER KEY
    # -----------------------------

    teacher_key = build_teacher_key(plan)

    # -----------------------------
    # STEP 5 — VALIDATE
    # -----------------------------

    validation = validate_bundle(
        selection=selection,
        plan=plan,
        student_worksheet=student_worksheet,
        teacher_key=teacher_key,
    )

    if not validation.is_valid:
        raise ValueError(
            "Worksheet generation failed validation:\n"
            + "\n".join(validation.errors)
        )

    # -----------------------------
    # FINAL BUNDLE
    # -----------------------------

    return WorksheetBundle(
        selection=selection,
        plan=plan,
        student_worksheet=student_worksheet,
        teacher_key=teacher_key,
        validation=validation,
    )


def generate_student_worksheet(
    request: ProductSelectionRequest,
) -> dict:
    """
    Convenience helper.

    Returns only the student worksheet.
    """

    bundle = generate_worksheet_bundle(request)

    return bundle.student_worksheet


def generate_teacher_key(
    request: ProductSelectionRequest,
) -> dict:
    """
    Convenience helper.

    Returns only the teacher key.
    """

    bundle = generate_worksheet_bundle(request)

    return bundle.teacher_key
