from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

import streamlit as st


# ============================================================
# EXISTING TMK SERVICE HOOKS
# ============================================================
# Replace these imports with your real service functions.
# They must return already-prepared view data.
#
# Example expected functions:
# - get_planner_view(selected_stage: str | None = None) -> dict
# - get_product_lab_view(
#       selected_product_label: str | None = None,
#       selected_compare_label: str | None = None
#   ) -> dict
#
# The UI below does not compute TMK structure. It only renders
# whatever your services provide.

try:
    from services.planner_service import get_planner_view  # type: ignore
except Exception:
    get_planner_view = None

try:
    from services.product_service import get_product_lab_view  # type: ignore
except Exception:
    get_product_lab_view = None


# ============================================================
# THEME
# ============================================================

PALETTE = {
    "ink": "#1B1F3B",         # Midnight Ink
    "sand": "#E6D8C3",        # Sandstone
    "mist": "#D8DADF",        # Mist Grey
    "sage": "#7FA58A",        # Sage Green
    "coral": "#E76F51",       # Burnt Coral
    "lavender": "#8A7CFF",    # Electric Lavender
    "white": "#FFFFFF",
    "text": "#1F2430",
    "muted": "#5E6472",
    "border": "rgba(27, 31, 59, 0.12)",
    "shadow": "0 10px 30px rgba(27, 31, 59, 0.08)",
}


def inject_theme() -> None:
    st.set_page_config(
        page_title="TMK",
        page_icon="✦",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    st.markdown(
        f"""
        <style>
            :root {{
                --ink: {PALETTE['ink']};
                --sand: {PALETTE['sand']};
                --mist: {PALETTE['mist']};
                --sage: {PALETTE['sage']};
                --coral: {PALETTE['coral']};
                --lavender: {PALETTE['lavender']};
                --white: {PALETTE['white']};
                --text: {PALETTE['text']};
                --muted: {PALETTE['muted']};
                --border: {PALETTE['border']};
                --shadow: {PALETTE['shadow']};
                --radius-lg: 22px;
                --radius-md: 16px;
                --radius-sm: 12px;
            }}

            .stApp {{
                background: linear-gradient(180deg, #F7F5F1 0%, #FBFAF8 100%);
                color: var(--text);
            }}

            .block-container {{
                max-width: 920px;
                padding-top: 1rem;
                padding-bottom: 3rem;
                padding-left: 0.9rem;
                padding-right: 0.9rem;
            }}

            @media (min-width: 768px) {{
                .block-container {{
                    padding-top: 1.35rem;
                    padding-left: 1.3rem;
                    padding-right: 1.3rem;
                }}
            }}

            h1, h2, h3 {{
                color: var(--ink);
                letter-spacing: -0.02em;
            }}

            .tmk-page-header {{
                background: rgba(255,255,255,0.84);
                border: 1px solid var(--border);
                border-radius: var(--radius-lg);
                padding: 1.1rem 1rem;
                box-shadow: var(--shadow);
                backdrop-filter: blur(8px);
                margin-bottom: 1rem;
            }}

            .tmk-page-header h1 {{
                margin: 0;
                font-size: 1.8rem;
                line-height: 1.1;
            }}

            .tmk-page-header p {{
                margin: 0.45rem 0 0 0;
                color: var(--muted);
                font-size: 0.98rem;
                line-height: 1.45;
            }}

            .tmk-section {{
                background: rgba(255,255,255,0.84);
                border: 1px solid var(--border);
                border-radius: var(--radius-lg);
                padding: 1rem;
                box-shadow: var(--shadow);
                margin-bottom: 1rem;
            }}

            .tmk-section-title {{
                display: flex;
                align-items: baseline;
                justify-content: space-between;
                gap: 0.75rem;
                margin-bottom: 0.8rem;
            }}

            .tmk-section-title h3 {{
                margin: 0;
                font-size: 1.08rem;
            }}

            .tmk-section-title span {{
                color: var(--muted);
                font-size: 0.86rem;
            }}

            .tmk-stat-grid {{
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 0.75rem;
            }}

            @media (min-width: 760px) {{
                .tmk-stat-grid {{
                    grid-template-columns: repeat(4, minmax(0, 1fr));
                }}
            }}

            .tmk-stat-card {{
                background: linear-gradient(180deg, #FFFDF9 0%, #F7F3EC 100%);
                border: 1px solid rgba(230, 216, 195, 0.95);
                border-radius: var(--radius-md);
                padding: 0.9rem;
            }}

            .tmk-stat-label {{
                color: var(--muted);
                font-size: 0.78rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-bottom: 0.3rem;
            }}

            .tmk-stat-value {{
                color: var(--ink);
                font-size: 1.12rem;
                font-weight: 700;
                line-height: 1.15;
            }}

            .tmk-chip-row {{
                display: flex;
                flex-wrap: wrap;
                gap: 0.55rem;
            }}

            .tmk-chip {{
                display: inline-flex;
                align-items: center;
                min-height: 40px;
                padding: 0.52rem 0.8rem;
                border-radius: 999px;
                background: rgba(216, 218, 223, 0.28);
                border: 1px solid rgba(27, 31, 59, 0.10);
                color: var(--ink);
                font-weight: 600;
                font-size: 0.92rem;
            }}

            .tmk-chip.is-new {{
                background: rgba(138, 124, 255, 0.10);
                border-color: rgba(138, 124, 255, 0.25);
            }}

            .tmk-chip.is-active {{
                background: rgba(231, 111, 81, 0.12);
                border-color: rgba(231, 111, 81, 0.30);
            }}

            .tmk-chip.is-soft {{
                background: rgba(127, 165, 138, 0.10);
                border-color: rgba(127, 165, 138, 0.25);
            }}

            .tmk-muted {{
                color: var(--muted);
                font-size: 0.93rem;
                line-height: 1.45;
            }}

            .tmk-divider {{
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(27,31,59,0.12), transparent);
                margin: 0.8rem 0 0.9rem;
            }}

            .tmk-hub-zone {{
                background: linear-gradient(180deg, rgba(27,31,59,0.98), rgba(37,48,78,0.98));
                border-radius: 26px;
                padding: 1rem;
                color: white;
                overflow: hidden;
            }}

            .tmk-hub-title {{
                font-size: 1.25rem;
                font-weight: 700;
                margin-bottom: 0.2rem;
            }}

            .tmk-hub-subtitle {{
                color: rgba(255,255,255,0.82);
                font-size: 0.92rem;
                margin-bottom: 1rem;
            }}

            .tmk-hub-mobile {{
                display: grid;
                gap: 0.85rem;
            }}

            .tmk-hub-route-group {{
                display: flex;
                flex-wrap: wrap;
                gap: 0.65rem;
                justify-content: center;
            }}

            .tmk-route-pill {{
                background: rgba(255,255,255,0.94);
                color: var(--ink);
                min-height: 48px;
                border-radius: 16px;
                padding: 0.75rem 1rem;
                font-size: 1rem;
                font-weight: 700;
                border: 1px solid rgba(255,255,255,0.65);
                box-shadow: 0 6px 16px rgba(0,0,0,0.10);
            }}

            .tmk-arrow-row {{
                display: flex;
                justify-content: center;
                gap: 1rem;
                color: rgba(255,255,255,0.78);
                font-size: 1.35rem;
                line-height: 1;
            }}

            .tmk-product-core {{
                width: 170px;
                height: 170px;
                max-width: 52vw;
                max-height: 52vw;
                margin: 0 auto;
                border-radius: 999px;
                background: linear-gradient(180deg, #657F9D 0%, #56728F 100%);
                border: 8px solid rgba(255,255,255,0.92);
                display: grid;
                place-items: center;
                box-shadow: 0 15px 35px rgba(0,0,0,0.16);
            }}

            .tmk-product-core span {{
                font-size: 3.2rem;
                line-height: 1;
                font-weight: 800;
                letter-spacing: -0.04em;
                color: white;
            }}

            .tmk-mini-map {{
                display: grid;
                gap: 0.6rem;
            }}

            .tmk-stage-row {{
                display: grid;
                grid-template-columns: 30px 1fr;
                gap: 0.6rem;
                align-items: start;
            }}

            .tmk-stage-label {{
                font-weight: 800;
                color: var(--ink);
                font-size: 0.9rem;
                padding-top: 0.25rem;
            }}

            .tmk-scroll-x {{
                overflow-x: auto;
                padding-bottom: 0.15rem;
            }}

            .tmk-compare-card {{
                background: linear-gradient(180deg, rgba(127,165,138,0.10), rgba(127,165,138,0.04));
                border: 1px solid rgba(127,165,138,0.20);
                border-radius: var(--radius-md);
                padding: 0.9rem;
            }}

            div[data-testid="stSelectbox"] > label {{
                color: var(--ink);
                font-weight: 700;
            }}

            div[data-baseweb="select"] > div {{
                border-radius: 14px !important;
                border-color: rgba(27,31,59,0.12) !important;
                background: rgba(255,255,255,0.86) !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# UI PRIMITIVES
# ============================================================

@dataclass(frozen=True)
class StatItem:
    label: str
    value: str


def page_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="tmk-page-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def start_section(title: str, subtitle: str | None = None) -> None:
    subtitle_html = f"<span>{subtitle}</span>" if subtitle else ""
    st.markdown(
        f"""
        <div class="tmk-section">
            <div class="tmk-section-title">
                <h3>{title}</h3>
                {subtitle_html}
            </div>
        """,
        unsafe_allow_html=True,
    )


def end_section() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def stat_grid(items: Sequence[StatItem]) -> None:
    cards = "".join(
        f"""
        <div class="tmk-stat-card">
            <div class="tmk-stat-label">{item.label}</div>
            <div class="tmk-stat-value">{item.value}</div>
        </div>
        """
        for item in items
    )
    st.markdown(f'<div class="tmk-stat-grid">{cards}</div>', unsafe_allow_html=True)


def chip_row(labels: Sequence[str], variant: str = "") -> None:
    chips = "".join(
        f'<span class="tmk-chip {variant}">{label}</span>' for label in labels
    )
    st.markdown(f'<div class="tmk-chip-row">{chips}</div>', unsafe_allow_html=True)


def muted(text: str) -> None:
    st.markdown(f'<div class="tmk-muted">{text}</div>', unsafe_allow_html=True)


def divider() -> None:
    st.markdown('<div class="tmk-divider"></div>', unsafe_allow_html=True)


# ============================================================
# COMMON CONTROLS
# ============================================================

def render_nav() -> str:
    return st.radio(
        "Navigate",
        ["Structural Planner", "Product Lab"],
        horizontal=True,
        key="tmk_page_nav",
    )


def render_stage_selector(stages: Sequence[str], selected_stage: str | None) -> str:
    safe_stages = list(stages) if stages else ["A"]
    current = selected_stage if selected_stage in safe_stages else safe_stages[0]
    index = safe_stages.index(current)
    return st.selectbox("Stage", safe_stages, index=index, key="planner_stage_selector")


def render_product_selector(
    product_labels: Sequence[str],
    selected_label: str | None,
    key: str,
    label: str,
) -> str:
    safe_products = list(product_labels) if product_labels else ["—"]
    current = selected_label if selected_label in safe_products else safe_products[0]
    index = safe_products.index(current)
    return st.selectbox(label, safe_products, index=index, key=key)


def render_compare_selector(
    product_labels: Sequence[str],
    selected_label: str | None,
) -> str | None:
    safe_products = list(product_labels)
    options = ["None", *safe_products]
    current = selected_label if selected_label in safe_products else "None"
    index = options.index(current)
    result = st.selectbox("Compare with", options, index=index, key="lab_compare_selector")
    return None if result == "None" else result


# ============================================================
# STRUCTURAL PLANNER UI
# ============================================================

def render_cumulative_product_map(
    stage_products: Mapping[str, Sequence[Mapping[str, Any]]],
    active_stage: str,
    active_product: str | None = None,
) -> None:
    start_section("Cumulative product map", "System view")

    st.markdown('<div class="tmk-mini-map">', unsafe_allow_html=True)
    for stage, products in stage_products.items():
        chips = []
        for item in products:
            classes: list[str] = []
            if item.get("is_new"):
                classes.append("is-new")
            if active_product is not None and str(item.get("label")) == str(active_product):
                classes.append("is-active")
            class_text = " ".join(classes)
            chips.append(f'<span class="tmk-chip {class_text}">{item.get("label", "")}</span>')

        stage_html = "".join(chips)
        st.markdown(
            f"""
            <div class="tmk-stage-row">
                <div class="tmk-stage-label">{stage}</div>
                <div class="tmk-scroll-x">
                    <div class="tmk-chip-row">{stage_html}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    muted(
        f"Selected stage: {active_stage}. New products are highlighted. "
        f"This view stays cumulative and does not repeat product-hub detail."
    )
    end_section()


def render_stage_summary(summary: Mapping[str, Any]) -> None:
    start_section("Stage summary", "Calm, cumulative, readable")

    stat_grid(
        [
            StatItem("Stage", str(summary.get("stage", "—"))),
            StatItem("Stage role", str(summary.get("role", "—"))),
            StatItem("New products", str(summary.get("new_count", "0"))),
            StatItem("Available", str(summary.get("available_count", "0"))),
        ]
    )

    divider()

    new_products = [str(v) for v in summary.get("new_products", [])]
    available_products = [str(v) for v in summary.get("available_products", [])]

    if new_products:
        st.caption("New products")
        chip_row(new_products, "is-new")

    if available_products:
        st.caption("Available products")
        chip_row(available_products)

    end_section()


def render_structural_planner_page(view_model: Mapping[str, Any]) -> None:
    page_header(
        str(view_model.get("title", "Structural Planner")),
        str(view_model.get("subtitle", "See cumulative products across the TMK system.")),
    )

    selected_stage = render_stage_selector(
        stages=view_model.get("stage_options", []),
        selected_stage=view_model.get("selected_stage"),
    )

    # If your service supports reloading by stage, this preserves controller simplicity.
    if get_planner_view is not None:
        refreshed = get_planner_view(selected_stage=selected_stage)
        if isinstance(refreshed, Mapping):
            view_model = refreshed

    render_cumulative_product_map(
        stage_products=view_model.get("cumulative_map", {}),
        active_stage=str(view_model.get("selected_stage", selected_stage)),
        active_product=view_model.get("active_product"),
    )

    render_stage_summary(view_model.get("stage_summary", {}))


# ============================================================
# PRODUCT LAB UI
# ============================================================

def render_product_hub(
    product_label: str,
    entry_routes: Sequence[str],
    exit_routes: Sequence[str],
) -> None:
    start_section("Product hub", "Routes in and out")

    entry_html = "".join(
        f'<span class="tmk-route-pill">{route}</span>' for route in entry_routes
    )
    exit_html = "".join(
        f'<span class="tmk-route-pill">{route}</span>' for route in exit_routes
    )

    st.markdown(
        f"""
        <div class="tmk-hub-zone">
            <div class="tmk-hub-title">Hub view</div>
            <div class="tmk-hub-subtitle">
                Entry routes move inward to the product. Exit routes move outward from it.
            </div>
            <div class="tmk-hub-mobile">
                <div class="tmk-hub-route-group">{entry_html}</div>
                <div class="tmk-arrow-row"><span>↓</span><span>↓</span><span>↓</span></div>
                <div class="tmk-product-core"><span>{product_label}</span></div>
                <div class="tmk-arrow-row"><span>↓</span><span>↓</span><span>↓</span></div>
                <div class="tmk-hub-route-group">{exit_html}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    end_section()


def render_product_identity(product_meta: Mapping[str, Any]) -> None:
    start_section("Product identity", "One product, one view")

    stat_grid(
        [
            StatItem("Product", str(product_meta.get("product", "—"))),
            StatItem("Stage", str(product_meta.get("stage", "—"))),
            StatItem("Role", str(product_meta.get("role", "—"))),
            StatItem("Distinct routes", str(product_meta.get("route_count", "—"))),
        ]
    )

    description = product_meta.get("description")
    if description:
        divider()
        muted(str(description))

    end_section()


def render_relationships_card(title: str, values: Sequence[str], subtitle: str) -> None:
    start_section(title, subtitle)
    chip_row([str(v) for v in values], "is-soft")
    end_section()


def render_compare_card(compare: Mapping[str, Any] | None) -> None:
    if not compare:
        return

    start_section("Comparison", "Optional, compact, non-repetitive")

    st.markdown('<div class="tmk-compare-card">', unsafe_allow_html=True)

    stat_grid(
        [
            StatItem("Compare with", str(compare.get("product", "—"))),
            StatItem("Stage", str(compare.get("stage", "—"))),
            StatItem("Shared factors", str(compare.get("shared_factors", "—"))),
            StatItem("Shared patterns", str(compare.get("shared_patterns", "—"))),
        ]
    )

    routes = [str(v) for v in compare.get("routes", [])]
    if routes:
        divider()
        st.caption("Compare product routes")
        chip_row(routes)

    st.markdown("</div>", unsafe_allow_html=True)
    end_section()


def render_product_lab_page(view_model: Mapping[str, Any]) -> None:
    page_header(
        str(view_model.get("title", "Product Lab")),
        str(view_model.get("subtitle", "Explore one product as a structural hub.")),
    )

    selected_product = render_product_selector(
        product_labels=view_model.get("product_options", []),
        selected_label=view_model.get("selected_product_label"),
        key="lab_product_selector",
        label="Selected product",
    )

    selected_compare = render_compare_selector(
        product_labels=view_model.get("compare_options", []),
        selected_label=view_model.get("selected_compare_label"),
    )

    if get_product_lab_view is not None:
        refreshed = get_product_lab_view(
            selected_product_label=selected_product,
            selected_compare_label=selected_compare,
        )
        if isinstance(refreshed, Mapping):
            view_model = refreshed

    product_meta = view_model.get("product_meta", {})

    render_product_hub(
        product_label=str(product_meta.get("product", selected_product or "—")),
        entry_routes=[str(v) for v in view_model.get("entry_routes", [])],
        exit_routes=[str(v) for v in view_model.get("exit_routes", [])],
    )

    render_product_identity(product_meta)

    representations = [str(v) for v in view_model.get("representations", [])]
    inverse_links = [str(v) for v in view_model.get("inverse_links", [])]
    derived_chains = [str(v) for v in view_model.get("derived_chains", [])]

    if representations:
        render_relationships_card(
            "Representations",
            representations,
            "Canonical product forms",
        )

    if inverse_links:
        render_relationships_card(
            "Inverse links",
            inverse_links,
            "Linked division relationships",
        )

    if derived_chains:
        render_relationships_card(
            "Derived chains",
            derived_chains,
            "Stage-appropriate structural chains",
        )

    mini_map = view_model.get("mini_map")
    if mini_map:
        render_cumulative_product_map(
            stage_products=mini_map,
            active_stage=str(product_meta.get("stage", "")),
            active_product=str(product_meta.get("product", "")),
        )

    render_compare_card(view_model.get("compare"))


# ============================================================
# FALLBACK DEMO DATA
# ============================================================
# These are only used if your real services are not imported yet.

def fallback_planner_view(selected_stage: str | None = None) -> Mapping[str, Any]:
    stage = selected_stage or "D"
    return {
        "title": "Structural Planner",
        "subtitle": "See cumulative products without repeating product-hub detail.",
        "selected_stage": stage,
        "stage_options": ["A", "B", "C", "D", "E", "F", "G"],
        "active_product": "36",
        "cumulative_map": {
            "A": [{"label": x, "is_new": False} for x in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]],
            "B": [{"label": x, "is_new": False} for x in ["20", "30", "40", "50", "60", "70", "80", "90", "100"]],
            "C": [{"label": x, "is_new": False} for x in ["15", "25", "35", "45"]],
            "D": [{"label": x, "is_new": True} for x in ["18", "27", "36", "54", "63", "72", "81"]],
            "E": [{"label": x, "is_new": False} for x in ["12", "24", "48"]],
            "F": [{"label": x, "is_new": False} for x in ["21", "42"]],
            "G": [{"label": x, "is_new": False} for x in ["49"]],
        },
        "stage_summary": {
            "stage": stage,
            "role": "Near-ten logic" if stage == "D" else "TMK structure",
            "new_count": "7" if stage == "D" else "—",
            "available_count": "30" if stage == "D" else "—",
            "new_products": ["18", "27", "36", "54", "63", "72", "81"] if stage == "D" else [],
            "available_products": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "20", "30"],
        },
    }


def fallback_product_lab_view(
    selected_product_label: str | None = None,
    selected_compare_label: str | None = None,
) -> Mapping[str, Any]:
    product = selected_product_label or "36"
    compare = selected_compare_label or "24"
    return {
        "title": "Product Lab",
        "subtitle": "A single hub view with routes in and out.",
        "selected_product_label": product,
        "selected_compare_label": compare,
        "product_options": ["12", "24", "36", "42", "48"],
        "compare_options": ["12", "24", "36", "42", "48"],
        "entry_routes": ["4×9", "6×6", "9×4"],
        "exit_routes": ["36÷4→9", "36÷6→6", "36÷9→4"],
        "representations": ["4×9", "6×6", "9×4"],
        "inverse_links": ["36÷4=9", "36÷6=6", "36÷9=4"],
        "derived_chains": ["9→18→36→72", "6→12→24→48"],
        "product_meta": {
            "product": product,
            "stage": "D",
            "role": "Complement / Near-Ten Logic (9×)",
            "route_count": "3",
            "description": "Single product hub view with canonical representations and linked inverse relationships.",
        },
        "mini_map": {
            "A": [{"label": x, "is_new": False} for x in ["1", "2", "3", "4", "5"]],
            "B": [{"label": x, "is_new": False} for x in ["20", "30"]],
            "C": [{"label": x, "is_new": False} for x in ["15", "25", "35"]],
            "D": [
                {"label": "18", "is_new": True},
                {"label": "27", "is_new": True},
                {"label": "36", "is_new": True},
                {"label": "54", "is_new": True},
            ],
        },
        "compare": {
            "product": compare,
            "stage": "E",
            "shared_factors": "4, 6",
            "shared_patterns": "doubling / even structure",
            "routes": ["3×8", "4×6"],
        },
    }


# ============================================================
# APP ENTRY
# ============================================================

def main() -> None:
    inject_theme()

    page = render_nav()

    if page == "Structural Planner":
        if get_planner_view is not None:
            view_model = get_planner_view(
                selected_stage=st.session_state.get("planner_stage_selector")
            )
        else:
            view_model = fallback_planner_view(
                selected_stage=st.session_state.get("planner_stage_selector")
            )

        render_structural_planner_page(view_model)

    elif page == "Product Lab":
        if get_product_lab_view is not None:
            view_model = get_product_lab_view(
                selected_product_label=st.session_state.get("lab_product_selector"),
                selected_compare_label=st.session_state.get("lab_compare_selector"),
            )
        else:
            compare_value = st.session_state.get("lab_compare_selector")
            view_model = fallback_product_lab_view(
                selected_product_label=st.session_state.get("lab_product_selector"),
                selected_compare_label=None if compare_value in (None, "None") else compare_value,
            )

        render_product_lab_page(view_model)


if __name__ == "__main__":
    main()
