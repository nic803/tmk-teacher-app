from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

import streamlit as st


# ============================================================
# OPTIONAL SERVICE IMPORTS
# Replace these with your real service/view builders.
# UI only consumes prepared data.
# ============================================================

try:
    from services.planner_service import get_planner_view  # type: ignore
except Exception:
    get_planner_view = None

try:
    from services.product_service import get_product_lab_view  # type: ignore
except Exception:
    get_product_lab_view = None

try:
    from services.worksheet_service import get_worksheet_studio_view  # type: ignore
except Exception:
    get_worksheet_studio_view = None


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
                    padding-top: 1.3rem;
                    padding-left: 1.2rem;
                    padding-right: 1.2rem;
                }}
            }}

            h1, h2, h3 {{
                color: var(--ink);
                letter-spacing: -0.02em;
            }}

            div[data-testid="stSelectbox"] > label,
            div[data-testid="stRadio"] > label,
            div[data-testid="stMultiSelect"] > label {{
                color: var(--ink);
                font-weight: 700;
            }}

            div[data-baseweb="select"] > div {{
                border-radius: 14px !important;
                border-color: rgba(27,31,59,0.12) !important;
                background: rgba(255,255,255,0.86) !important;
            }}

            .tmk-card {{
                background: rgba(255,255,255,0.86);
                border: 1px solid var(--border);
                border-radius: 22px;
                padding: 1rem;
                box-shadow: var(--shadow);
            }}

            .tmk-muted {{
                color: var(--muted);
                font-size: 0.93rem;
                line-height: 1.45;
            }}

            .tmk-chip {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-height: 38px;
                padding: 0.45rem 0.75rem;
                border-radius: 999px;
                font-size: 0.9rem;
                font-weight: 600;
                color: var(--ink);
                background: rgba(216, 218, 223, 0.28);
                border: 1px solid rgba(27,31,59,0.10);
                margin: 0.2rem 0.25rem 0.2rem 0;
            }}

            .tmk-chip-new {{
                background: rgba(138, 124, 255, 0.10);
                border-color: rgba(138, 124, 255, 0.25);
            }}

            .tmk-chip-active {{
                background: rgba(231, 111, 81, 0.12);
                border-color: rgba(231, 111, 81, 0.30);
            }}

            .tmk-chip-soft {{
                background: rgba(127, 165, 138, 0.10);
                border-color: rgba(127, 165, 138, 0.25);
            }}

            .tmk-hub-wrap {{
                background: linear-gradient(180deg, rgba(27,31,59,0.98), rgba(37,48,78,0.98));
                border-radius: 26px;
                padding: 1rem;
                color: white;
            }}

            .tmk-hub-title {{
                font-size: 1.3rem;
                font-weight: 800;
                margin-bottom: 0.2rem;
            }}

            .tmk-hub-sub {{
                color: rgba(255,255,255,0.82);
                font-size: 0.92rem;
                margin-bottom: 1rem;
            }}

            .tmk-hub-routes {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 0.65rem;
            }}

            .tmk-route-pill {{
                background: rgba(255,255,255,0.95);
                color: var(--ink);
                min-height: 46px;
                padding: 0.7rem 1rem;
                border-radius: 16px;
                font-size: 1rem;
                font-weight: 700;
                border: 1px solid rgba(255,255,255,0.65);
            }}

            .tmk-arrow-row {{
                text-align: center;
                color: rgba(255,255,255,0.75);
                font-size: 1.35rem;
                margin: 0.5rem 0;
            }}

            .tmk-core {{
                width: 170px;
                height: 170px;
                max-width: 52vw;
                max-height: 52vw;
                margin: 0.2rem auto 0.4rem auto;
                border-radius: 999px;
                background: linear-gradient(180deg, #657F9D 0%, #56728F 100%);
                border: 8px solid rgba(255,255,255,0.92);
                display: grid;
                place-items: center;
                box-shadow: 0 15px 35px rgba(0,0,0,0.16);
            }}

            .tmk-core span {{
                font-size: 3.2rem;
                line-height: 1;
                font-weight: 800;
                letter-spacing: -0.04em;
                color: white;
            }}

            .tmk-section-title {{
                display: flex;
                justify-content: space-between;
                align-items: baseline;
                gap: 0.75rem;
                margin-bottom: 0.75rem;
            }}

            .tmk-section-title h3 {{
                margin: 0;
                font-size: 1.05rem;
            }}

            .tmk-section-title small {{
                color: var(--muted);
                font-size: 0.84rem;
            }}

            .tmk-divider {{
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(27,31,59,0.12), transparent);
                margin: 0.9rem 0;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SMALL HELPERS
# ============================================================

@dataclass(frozen=True)
class StatItem:
    label: str
    value: str


def card_title(title: str, subtitle: str | None = None) -> None:
    subtitle_html = f"<small>{subtitle}</small>" if subtitle else ""
    st.markdown(
        f"""
        <div class="tmk-section-title">
            <h3>{title}</h3>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def chip_html(label: str, variant: str = "") -> str:
    classes = "tmk-chip"
    if variant:
        classes += f" {variant}"
    return f'<span class="{classes}">{label}</span>'


def render_chip_row(labels: Sequence[str], variant: str = "") -> None:
    html = "".join(chip_html(str(label), variant) for label in labels)
    st.markdown(html, unsafe_allow_html=True)


def render_stats(items: Sequence[StatItem], columns: int = 4) -> None:
    cols = st.columns(columns)
    for i, item in enumerate(items):
        with cols[i % columns]:
            st.markdown(
                f"""
                <div class="tmk-card" style="padding:0.9rem;">
                    <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em; color:{PALETTE['muted']}; margin-bottom:0.25rem;">
                        {item.label}
                    </div>
                    <div style="font-size:1.15rem; font-weight:800; color:{PALETTE['ink']};">
                        {item.value}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# NAV
# ============================================================

def render_top_nav() -> str:
    return st.radio(
        "Navigate",
        ["Structural Planner", "Product Lab", "Worksheet Studio"],
        horizontal=True,
        key="tmk_top_nav",
        label_visibility="collapsed",
    )


# ============================================================
# PAGE HEADERS
# ============================================================

def render_page_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="tmk-card" style="margin-bottom:1rem;">
            <h1 style="margin:0; font-size:2rem;">{title}</h1>
            <p class="tmk-muted" style="margin:0.45rem 0 0 0;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# STRUCTURAL PLANNER
# ============================================================

def render_cumulative_map(stage_products: Mapping[str, Sequence[Mapping[str, Any]]], active_product: str | None) -> None:
    with st.container():
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        card_title("Cumulative product map", "System view")

        for stage, products in stage_products.items():
            left, right = st.columns([0.08, 0.92])
            with left:
                st.markdown(
                    f"<div style='font-weight:800; color:{PALETTE['ink']}; padding-top:0.45rem;'>{stage}</div>",
                    unsafe_allow_html=True,
                )
            with right:
                html = ""
                for item in products:
                    label = str(item.get("label", ""))
                    cls = ""
                    if item.get("is_new"):
                        cls = "tmk-chip-new"
                    if active_product is not None and label == str(active_product):
                        cls = "tmk-chip-active"
                    html += chip_html(label, cls)
                st.markdown(html, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


def render_stage_summary(summary: Mapping[str, Any]) -> None:
    with st.container():
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        card_title("Stage summary", "Calm, cumulative, readable")

        render_stats(
            [
                StatItem("Stage", str(summary.get("stage", "—"))),
                StatItem("Role", str(summary.get("role", "—"))),
                StatItem("New products", str(summary.get("new_count", "—"))),
                StatItem("Available", str(summary.get("available_count", "—"))),
            ]
        )

        st.markdown('<div class="tmk-divider"></div>', unsafe_allow_html=True)

        new_products = [str(x) for x in summary.get("new_products", [])]
        available_products = [str(x) for x in summary.get("available_products", [])]

        if new_products:
            st.caption("New products")
            render_chip_row(new_products, "tmk-chip-new")

        if available_products:
            st.caption("Available products")
            render_chip_row(available_products)

        st.markdown("</div>", unsafe_allow_html=True)


def render_structural_planner_page(view_model: Mapping[str, Any]) -> None:
    render_page_header(
        str(view_model.get("title", "Structural Planner")),
        str(view_model.get("subtitle", "See cumulative products without repeating product-hub detail.")),
    )

    stage_options = list(view_model.get("stage_options", [])) or ["A"]
    selected_stage = str(view_model.get("selected_stage", stage_options[0]))
    selected_stage = st.selectbox(
        "Stage",
        stage_options,
        index=stage_options.index(selected_stage) if selected_stage in stage_options else 0,
        key="planner_stage_selector",
    )

    if get_planner_view is not None:
        refreshed = get_planner_view(selected_stage=selected_stage)
        if isinstance(refreshed, Mapping):
            view_model = refreshed

    render_cumulative_map(
        stage_products=view_model.get("cumulative_map", {}),
        active_product=view_model.get("active_product"),
    )

    st.markdown(
        f"<p class='tmk-muted'>Selected stage: {view_model.get('selected_stage', selected_stage)}. "
        f"New products are highlighted. This view stays cumulative and does not repeat product-hub detail.</p>",
        unsafe_allow_html=True,
    )

    render_stage_summary(view_model.get("stage_summary", {}))


# ============================================================
# PRODUCT LAB
# ============================================================

def render_product_hub(product_label: str, entry_routes: Sequence[str], exit_routes: Sequence[str]) -> None:
    with st.container():
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="tmk-hub-wrap">
                <div class="tmk-hub-title">Radial Hub View</div>
                <div class="tmk-hub-sub">
                    Entry routes point inward. Exit routes point outward. Distinct pairings only.
                </div>
                <div class="tmk-hub-routes">
                    {''.join(f'<span class="tmk-route-pill">{r}</span>' for r in entry_routes)}
                </div>
                <div class="tmk-arrow-row">↓ &nbsp;&nbsp; ↓ &nbsp;&nbsp; ↓</div>
                <div class="tmk-core"><span>{product_label}</span></div>
                <div class="tmk-arrow-row">↓ &nbsp;&nbsp; ↓ &nbsp;&nbsp; ↓</div>
                <div class="tmk-hub-routes">
                    {''.join(f'<span class="tmk-route-pill">{r}</span>' for r in exit_routes)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)


def render_product_identity(product_meta: Mapping[str, Any]) -> None:
    with st.container():
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        card_title("Product identity", "One product, one view")

        render_stats(
            [
                StatItem("Product", str(product_meta.get("product", "—"))),
                StatItem("Stage", str(product_meta.get("stage", "—"))),
                StatItem("Role", str(product_meta.get("role", "—"))),
                StatItem("Distinct routes", str(product_meta.get("route_count", "—"))),
            ]
        )

        description = product_meta.get("description")
        if description:
            st.markdown('<div class="tmk-divider"></div>', unsafe_allow_html=True)
            st.markdown(f"<p class='tmk-muted'>{description}</p>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


def render_simple_relationship_card(title: str, subtitle: str, values: Sequence[str]) -> None:
    with st.container():
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        card_title(title, subtitle)
        render_chip_row([str(v) for v in values], "tmk-chip-soft")
        st.markdown("</div>", unsafe_allow_html=True)


def render_compare_card(compare: Mapping[str, Any] | None) -> None:
    if not compare:
        return

    with st.container():
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        card_title("Comparison", "Optional, compact, non-repetitive")

        render_stats(
            [
                StatItem("Compare with", str(compare.get("product", "—"))),
                StatItem("Stage", str(compare.get("stage", "—"))),
                StatItem("Shared factors", str(compare.get("shared_factors", "—"))),
                StatItem("Shared patterns", str(compare.get("shared_patterns", "—"))),
            ]
        )

        routes = [str(x) for x in compare.get("routes", [])]
        if routes:
            st.markdown('<div class="tmk-divider"></div>', unsafe_allow_html=True)
            st.caption("Compare product routes")
            render_chip_row(routes)

        st.markdown("</div>", unsafe_allow_html=True)


def render_product_lab_page(view_model: Mapping[str, Any]) -> None:
    render_page_header(
        str(view_model.get("title", "Product Lab")),
        str(view_model.get("subtitle", "Explore one product as a structural hub.")),
    )

    product_options = list(view_model.get("product_options", [])) or ["—"]
    selected_product = str(view_model.get("selected_product_label", product_options[0]))
    if selected_product not in product_options:
        selected_product = product_options[0]

    compare_options = list(view_model.get("compare_options", []))
    compare_current = view_model.get("selected_compare_label")
    compare_choices = ["None", *compare_options]
    compare_current = compare_current if compare_current in compare_options else "None"

    col1, col2 = st.columns(2)
    with col1:
        selected_product = st.selectbox(
            "Selected product",
            product_options,
            index=product_options.index(selected_product),
            key="lab_product_selector",
        )
    with col2:
        selected_compare = st.selectbox(
            "Compare with",
            compare_choices,
            index=compare_choices.index(compare_current),
            key="lab_compare_selector",
        )

    selected_compare_value = None if selected_compare == "None" else selected_compare

    if get_product_lab_view is not None:
        refreshed = get_product_lab_view(
            selected_product_label=selected_product,
            selected_compare_label=selected_compare_value,
        )
        if isinstance(refreshed, Mapping):
            view_model = refreshed

    product_meta = view_model.get("product_meta", {})

    render_product_hub(
        product_label=str(product_meta.get("product", selected_product)),
        entry_routes=[str(v) for v in view_model.get("entry_routes", [])],
        exit_routes=[str(v) for v in view_model.get("exit_routes", [])],
    )

    render_product_identity(product_meta)

    representations = [str(v) for v in view_model.get("representations", [])]
    inverse_links = [str(v) for v in view_model.get("inverse_links", [])]
    derived_chains = [str(v) for v in view_model.get("derived_chains", [])]

    if representations:
        render_simple_relationship_card("Representations", "Canonical product forms", representations)

    if inverse_links:
        render_simple_relationship_card("Inverse links", "Linked division relationships", inverse_links)

    if derived_chains:
        render_simple_relationship_card("Derived chains", "Stage-appropriate structural chains", derived_chains)

    mini_map = view_model.get("mini_map")
    if mini_map:
        render_cumulative_map(
            stage_products=mini_map,
            active_product=str(product_meta.get("product", "")),
        )

    render_compare_card(view_model.get("compare"))


# ============================================================
# WORKSHEET STUDIO
# ============================================================

def render_worksheet_studio_page(view_model: Mapping[str, Any]) -> None:
    render_page_header(
        str(view_model.get("title", "Worksheet Studio")),
        str(view_model.get("subtitle", "Generate worksheets from TMK service outputs.")),
    )

    controls = view_model.get("controls", {})
    summary = view_model.get("summary", {})
    preview = view_model.get("preview", {})

    stage_options = list(controls.get("stage_options", [])) or ["A"]
    format_options = list(controls.get("format_options", [])) or ["Standard"]
    tier_options = list(controls.get("tier_options", [])) or ["Core"]

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_stage = st.selectbox(
            "Stage",
            stage_options,
            index=stage_options.index(controls.get("selected_stage", stage_options[0]))
            if controls.get("selected_stage", stage_options[0]) in stage_options else 0,
            key="worksheet_stage_selector",
        )
    with col2:
        selected_format = st.selectbox(
            "Format",
            format_options,
            index=format_options.index(controls.get("selected_format", format_options[0]))
            if controls.get("selected_format", format_options[0]) in format_options else 0,
            key="worksheet_format_selector",
        )
    with col3:
        selected_tier = st.selectbox(
            "Tier",
            tier_options,
            index=tier_options.index(controls.get("selected_tier", tier_options[0]))
            if controls.get("selected_tier", tier_options[0]) in tier_options else 0,
            key="worksheet_tier_selector",
        )

    if get_worksheet_studio_view is not None:
        refreshed = get_worksheet_studio_view(
            selected_stage=selected_stage,
            selected_format=selected_format,
            selected_tier=selected_tier,
        )
        if isinstance(refreshed, Mapping):
            view_model = refreshed
            summary = view_model.get("summary", {})
            preview = view_model.get("preview", {})

    with st.container():
        st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
        card_title("Worksheet summary", "Service-fed only")

        render_stats(
            [
                StatItem("Stage", str(summary.get("stage", "—"))),
                StatItem("Format", str(summary.get("format", "—"))),
                StatItem("Tier", str(summary.get("tier", "—"))),
                StatItem("Products", str(summary.get("product_count", "—"))),
            ]
        )

        st.markdown("</div>", unsafe_allow_html=True)

    if preview:
        with st.container():
            st.markdown('<div class="tmk-card">', unsafe_allow_html=True)
            card_title("Worksheet preview", "Read-only preview")

            title = preview.get("title")
            if title:
                st.subheader(str(title))

            lines = preview.get("lines", [])
            for line in lines:
                st.write(str(line))

            st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FALLBACK VIEWS
# ============================================================

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


def fallback_worksheet_studio_view(
    selected_stage: str | None = None,
    selected_format: str | None = None,
    selected_tier: str | None = None,
) -> Mapping[str, Any]:
    return {
        "title": "Worksheet Studio",
        "subtitle": "Generate worksheets from TMK service outputs.",
        "controls": {
            "stage_options": ["A", "B", "C", "D", "E", "F", "G"],
            "selected_stage": selected_stage or "D",
            "format_options": ["Standard", "Mixed", "Practice"],
            "selected_format": selected_format or "Standard",
            "tier_options": ["Core", "Stretch", "Support"],
            "selected_tier": selected_tier or "Core",
        },
        "summary": {
            "stage": selected_stage or "D",
            "format": selected_format or "Standard",
            "tier": selected_tier or "Core",
            "product_count": "8",
        },
        "preview": {
            "title": "Worksheet preview",
            "lines": [
                "Bundle prepared by service layer.",
                "Preview lines only.",
                "Use your existing worksheet generator output here.",
            ],
        },
    }


# ============================================================
# APP
# ============================================================

def main() -> None:
    inject_theme()
    page = render_top_nav()

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
        compare_value = st.session_state.get("lab_compare_selector")
        compare_value = None if compare_value in (None, "None") else compare_value

        if get_product_lab_view is not None:
            view_model = get_product_lab_view(
                selected_product_label=st.session_state.get("lab_product_selector"),
                selected_compare_label=compare_value,
            )
        else:
            view_model = fallback_product_lab_view(
                selected_product_label=st.session_state.get("lab_product_selector"),
                selected_compare_label=compare_value,
            )
        render_product_lab_page(view_model)

    elif page == "Worksheet Studio":
        if get_worksheet_studio_view is not None:
            view_model = get_worksheet_studio_view(
                selected_stage=st.session_state.get("worksheet_stage_selector"),
                selected_format=st.session_state.get("worksheet_format_selector"),
                selected_tier=st.session_state.get("worksheet_tier_selector"),
            )
        else:
            view_model = fallback_worksheet_studio_view(
                selected_stage=st.session_state.get("worksheet_stage_selector"),
                selected_format=st.session_state.get("worksheet_format_selector"),
                selected_tier=st.session_state.get("worksheet_tier_selector"),
            )
        render_worksheet_studio_page(view_model)


if __name__ == "__main__":
    main()
