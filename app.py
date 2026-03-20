from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from typing import Any

import streamlit as st

from products import ALL_PRODUCTS, product_record, stage_label
from worksheet_engine import generate_worksheet

APP_TITLE = "TMK Teacher App"
APP_CAPTION = "TMK World and product hubs"
TIERS = ("Support", "Core", "Extension")


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="✳️",
    layout="wide",
)


def main() -> None:
    st.title(APP_TITLE)
    st.caption(APP_CAPTION)

    product, tier, view = _render_sidebar()

    if view == "TMK World":
        _render_world_home(selected_product=product)
        return

    if view == "Product Hubs":
        _render_hubs_home(selected_product=product)
        return

    if view == "Product Detail":
        _render_product_detail(selected_product=product)
        return

    if view == "Worksheets":
        _render_worksheet_view(product=product, tier=tier)
        return


def _render_sidebar() -> tuple[int, str, str]:
    with st.sidebar:
        st.header("Teacher Controls")

        view = st.radio(
            "View",
            options=("TMK World", "Product Hubs", "Product Detail", "Worksheets"),
            index=0,
        )

        default_product = 36 if 36 in ALL_PRODUCTS else ALL_PRODUCTS[0]

        product = st.selectbox(
            "Selected product",
            options=ALL_PRODUCTS,
            index=ALL_PRODUCTS.index(default_product),
            format_func=_product_option_label,
        )

        tier = st.radio(
            "Worksheet tier",
            options=TIERS,
            index=1,
            horizontal=True,
        )

        record = product_record(product)

        st.divider()
        st.markdown("**Current Product**")
        st.write(f"Product: {record.product}")
        st.write(f"Stage: {stage_label(record.stage)}")
        st.write(f"Intro route: {_format_route(record.intro_route)}")
        st.write(f"Routes: {len(record.factor_families)}")
        st.write(f"Structural role: {record.structural_role}")

    return product, tier, view


def _render_world_home(selected_product: int) -> None:
    st.subheader("TMK World")

    selected = product_record(selected_product)

    hero_left, hero_right = st.columns([1.3, 1])

    with hero_left:
        st.markdown("### World Overview")
        st.write(
            "This is the teacher-facing TMK front face. It shows the bounded multiplication world "
            "through stages and products, with the selected product highlighted."
        )

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Products", str(len(ALL_PRODUCTS)))
        col2.metric("Selected", str(selected.product))
        col3.metric("Stage", str(stage_label(selected.stage)))
        col4.metric("Routes", str(len(selected.factor_families)))

    with hero_right:
        st.markdown("### Selected Product")
        st.write(f"Product: {selected.product}")
        st.write(f"Intro route: {_format_route(selected.intro_route)}")
        st.write(f"Role: {selected.structural_role}")
        st.write(f"Ways in: {_format_routes(selected.ways_in)}")

    st.divider()

    stage_groups = _products_by_stage()

    for stage in _sorted_stage_keys(stage_groups):
        products = stage_groups[stage]
        label = stage_label(stage)

        st.markdown(f"### {label}")
        cols = st.columns(6)

        for index, product in enumerate(products):
            record = product_record(product)
            marker = "⬅ selected" if product == selected_product else ""

            with cols[index % 6]:
                with st.container(border=True):
                    st.markdown(f"**{product}**")
                    st.write(f"Intro: {_format_route(record.intro_route)}")
                    st.write(f"Routes: {len(record.factor_families)}")
                    st.write(f"Role: {record.structural_role}")
                    if marker:
                        st.write(marker)


def _render_hubs_home(selected_product: int) -> None:
    st.subheader("Product Hubs")
    st.write(
        "Products grouped by structural role, so the teacher can inspect the hub structure of the TMK world."
    )

    selected = product_record(selected_product)

    top1, top2, top3, top4 = st.columns(4)
    top1.metric("Selected Product", str(selected.product))
    top2.metric("Stage", str(stage_label(selected.stage)))
    top3.metric("Routes", str(len(selected.factor_families)))
    top4.metric("Role", str(selected.structural_role))

    st.divider()

    role_groups = _products_by_role()

    for role in sorted(role_groups):
        products = role_groups[role]
        st.markdown(f"### {role}")
        cols = st.columns(4)

        for index, product in enumerate(products):
            record = product_record(product)
            marker = "⬅ selected" if product == selected_product else ""

            with cols[index % 4]:
                with st.container(border=True):
                    st.markdown(f"**{product}**")
                    st.write(f"Stage: {stage_label(record.stage)}")
                    st.write(f"Hub route: {_format_route(record.intro_route)}")
                    st.write(f"Routes: {len(record.factor_families)}")
                    if marker:
                        st.write(marker)


def _render_product_detail(selected_product: int) -> None:
    record = product_record(selected_product)

    st.subheader(f"Product Detail · {selected_product}")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### Core Structure")
            st.write(f"Stage: {stage_label(record.stage)}")
            st.write(f"Intro route: {_format_route(record.intro_route)}")
            st.write(f"Ways in: {_format_routes(record.ways_in)}")
            st.write(f"Ways out: {_format_routes(record.ways_out)}")
            st.write(f"Routes: {_format_routes(record.factor_families)}")
            st.write(f"Related products: {_format_scalar_sequence(record.related_products)}")
            st.write(f"Structural role: {record.structural_role}")

    with col2:
        with st.container(border=True):
            st.markdown("### Teacher Reading")
            st.write(_teacher_reading_for_product(record))

    st.divider()
    st.markdown("### Route Cards")

    route_cols = st.columns(max(1, min(4, len(record.factor_families))))

    for index, route in enumerate(record.factor_families):
        with route_cols[index % len(route_cols)]:
            with st.container(border=True):
                st.markdown(f"**Route {index + 1}**")
                st.write(_format_route(route))
                st.write(f"This route makes {record.product}.")

    st.divider()
    st.markdown("### Related Product Cards")

    related_products = [p for p in record.related_products if p in ALL_PRODUCTS]

    if not related_products:
        st.write("No related products attached.")
        return

    related_cols = st.columns(4)
    for index, related in enumerate(related_products):
        related_record = product_record(related)
        with related_cols[index % 4]:
            with st.container(border=True):
                st.markdown(f"**{related}**")
                st.write(f"Stage: {stage_label(related_record.stage)}")
                st.write(f"Intro: {_format_route(related_record.intro_route)}")
                st.write(f"Role: {related_record.structural_role}")


def _render_worksheet_view(product: int, tier: str) -> None:
    st.subheader("Worksheets")

    worksheet = generate_worksheet(product, tier)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Product", str(worksheet.product))
    col2.metric("Stage", str(worksheet.stage))
    col3.metric("Tier", str(worksheet.tier))
    col4.metric("Questions", str(len(worksheet.questions)))

    st.divider()

    left, right = st.columns([1.5, 1])

    with left:
        st.markdown("### Pupil Worksheet")
        for index, question in enumerate(worksheet.questions, start=1):
            with st.container(border=True):
                st.markdown(f"**Q{_question_number(question, index)}**")
                st.write(_render_question_text(question))

    with right:
        st.markdown("### Teacher Key")
        answers = _coerce_sequence(_get_attr(worksheet.teacher_key, "answers"))
        notes = _coerce_sequence(_get_attr(worksheet.teacher_key, "notes"))

        st.markdown("**Answers**")
        for index, answer in enumerate(answers, start=1):
            st.write(f"Q{index}. {_stringify(answer)}")

        st.markdown("**Notes**")
        for note in notes:
            st.write(f"- {_stringify(note)}")


def _products_by_stage() -> dict[str, list[int]]:
    grouped: dict[str, list[int]] = defaultdict(list)

    for product in ALL_PRODUCTS:
        grouped[product_record(product).stage].append(product)

    for stage in grouped:
        grouped[stage].sort()

    return dict(grouped)


def _products_by_role() -> dict[str, list[int]]:
    grouped: dict[str, list[int]] = defaultdict(list)

    for product in ALL_PRODUCTS:
        grouped[product_record(product).structural_role].append(product)

    for role in grouped:
        grouped[role].sort()

    return dict(grouped)


def _sorted_stage_keys(stage_groups: dict[str, list[int]]) -> list[str]:
    return sorted(stage_groups.keys())


def _product_option_label(product: int) -> str:
    record = product_record(product)
    return f"{product} · {record.stage}"


def _teacher_reading_for_product(record: Any) -> str:
    route_count = len(record.factor_families)

    if route_count == 1:
        return (
            f"{record.product} is a single-route product in the current TMK world. "
            f"The teacher focus is to secure {_format_route(record.intro_route)} as the stable route in."
        )

    return (
        f"{record.product} is a multi-route product. "
        f"The teacher focus is to keep the product as the hub while connecting "
        f"{_format_route(record.intro_route)} to the other routes."
    )


def _render_question_text(question: Any) -> str:
    for field_name in ("pupil_prompt", "prompt", "display_text", "text", "question_text", "body"):
        value = _get_attr(question, field_name)
        if value not in (None, ""):
            return _stringify(value)

    return _stringify(question)


def _question_number(question: Any, fallback: int) -> int:
    value = _get_attr(question, "id")
    if isinstance(value, int):
        return value
    return fallback


def _format_route(route: tuple[int, int]) -> str:
    return f"{route[0]} × {route[1]}"


def _format_routes(routes: Iterable[Any]) -> str:
    items = []
    for route in routes:
        if isinstance(route, tuple) and len(route) == 2:
            items.append(_format_route(route))
        else:
            items.append(_stringify(route))
    return ", ".join(items) if items else "—"


def _format_scalar_sequence(values: Iterable[Any]) -> str:
    items = [_stringify(value) for value in values]
    return ", ".join(items) if items else "—"


def _coerce_sequence(value: Any) -> tuple[Any, ...]:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Iterable):
        return tuple(value)
    return (value,)


def _get_attr(obj: Any, name: str) -> Any:
    return getattr(obj, name, None)


def _stringify(value: Any) -> str:
    if isinstance(value, tuple) and len(value) == 2:
        return _format_route(value)
    return str(value)


if __name__ == "__main__":
    main()
