from __future__ import annotations

from models.worksheet_models import ProductSelectionRequest
from services.worksheet_generation_service import (
    generate_teacher_key,
    generate_student_worksheet,
    generate_worksheet_bundle,
)


def generate_worksheet_bundle_from_request(
    request: ProductSelectionRequest,
):
    return generate_worksheet_bundle(request)


def generate_student_worksheet_from_request(
    request: ProductSelectionRequest,
):
    return generate_student_worksheet(request)


def generate_teacher_key_from_request(
    request: ProductSelectionRequest,
):
    return generate_teacher_key(request)
