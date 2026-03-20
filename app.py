import math
from typing import Dict, List, Tuple

import streamlit as st

try:
    from patterns import PATTERNS, product_patterns
    PATTERNS_AVAILABLE = True
    PATTERN_IMPORT_ERROR = ""
except Exception as exc:
    PATTERNS_AVAILABLE = False
    PATTERN_IMPORT_ERROR = str(exc)
    PATTERNS = {}

    def product_patterns(product: int):
        return tuple()

try:
    from memory_cues import memory_cues_for_product
    MEMORY_CUES_AVAILABLE = True
    MEMORY_CUES_IMPORT_ERROR = ""
except Exception as exc:
    MEMORY_CUES_AVAILABLE = False
    MEMORY_CUES_IMPORT_ERROR = str(exc)

    def memory_cues_for_product(product: int):
        return tuple()


Route = Tuple[int, int]

st.set_page_config(page_title="TMK Structural Planner", page_icon="✳️", layout="wide")

STAGE_ORDER = ["0", "A", "B", "C", "D", "E", "F", "G"]

STAGE_META = {
    "0": {"label": "Stage 0 · Foundation", "products": [4, 6, 8, 9, 10], "color": "#475569"},
    "A": {"label": "Stage A · Identity Anchors", "products": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "color": "#94a3b8"},
    "B": {"label": "Stage B · Ten Scaling", "products": [20, 30, 40, 50, 60, 70, 80, 90, 100], "color": "#2563eb"},
    "C": {"label": "Stage C · Five Midpoints", "products": [15, 25, 35, 45], "color": "#0ea5e9"},
    "D": {"label": "Stage D · Nine Structure", "products": [18, 27, 36, 54, 63, 72, 81], "color": "#0284c7"},
    "E": {"label": "Stage E · Doubling Chain", "products": [12, 14, 16, 24, 28, 32, 48, 56, 64], "color": "#0f766e"},
    "F": {"label": "Stage F · Interleaving", "products": [21, 42], "color": "#7c3aed"},
    "G": {"label": "Stage G · Closure", "products": [49], "color": "#ca8a04"},
}

INTRO_ROUTES = {
    1: (1, 1),
    2: (1, 2),
    3: (1, 3),
    4: (1, 4),
    5: (1, 5),
    6: (1, 6),
    7: (1, 7),
    8: (1, 8),
    9: (1, 9),
    10: (1, 10),
    12: (2, 6),
    14: (2, 7),
    15: (3, 5),
    16: (2, 8),
    18: (2, 9),
    20: (2, 10),
    21: (3, 7),
    24: (4, 6),
    25: (5, 5),
    27: (3, 9),
    28: (4, 7),
    30: (3, 10),
    32: (4, 8),
    35: (5, 7),
    36: (4, 9),
    40: (4, 10),
    42: (6, 7),
    45: (5, 9),
    48: (6, 8),
    49: (7, 7),
    50: (5, 10),
    54: (6, 9),
    56: (7, 8),
    60: (6, 10),
    63: (7, 9),
    64: (8, 8),
    70: (7, 10),
    72: (8, 9),
    80: (8, 10),
    81: (9, 9),
    90: (9, 10),
    100: (10, 10),
}

WORLD_LABELS = {
    "0": "Foundation",
    "A": "Identity",
    "B": "Ten Scaling",
    "C": "Five Midpoints",
    "D": "Nine Structure",
    "E": "Doubling Chain",
    "F": "Interleaving",
    "G": "Closure",
}

BAND_COLOR = {
    "0": "#f8fafc",
    "A": "#f8fafc",
    "B": "#eff6ff",
    "C": "#ecfeff",
    "D": "#f0f9ff",
    "E": "#f0fdfa",
    "F": "#f5f3ff",
    "G": "#fffbeb",
}

PRODUCT_STAGE: Dict[int, str] = {
    product: stage for stage, meta in STAGE_META.items() for product in meta["products"]
}


def stage_rank(stage: str) -> int:
    return STAGE_ORDER.index(stage)


def visible_products(stage: str) -> List[int]:
    visible = set()
    for s in STAGE_ORDER:
        if stage_rank(s) <= stage_rank(stage):
            visible.update(STAGE_META[s]["products"])
    return sorted(visible)


def routes(product: int) -> List[Route]:
    return [(a, b) for a in range(1, 11) for b in range(1, 11) if a * b == product]


def exits(product: int) -> List[Route]:
    return [(d, product // d) for d in range(1, 11) if product % d == 0 and 1 <= product // d <= 10]


def factor_families(product: int) -> List[Route]:
    return sorted({tuple(sorted((a, b))) for a, b in routes(product)})


def routes_flat(product: int) -> List[int]:
    return [n for route in routes(product) for n in route]


def related_products(product: int, stage: str) -> List[int]:
    visible = set(visible_products(stage))
    factors = {n for route in routes(product) for n in route}
    return sorted(p for p in visible if p != product and factors.intersection(routes_flat(p)))


def structural_role(product: int) -> str:
    family_count = len(factor_families(product))
    if product == 49:
        return "closure_hub"
    if product in {21, 42}:
        return "bridge_hub"
    if family_count >= 3:
        return "compression_hub"
    if family_count == 1:
        return "single_route_hub"
    return "anchor_hub"


def product_summary(product: int) -> Dict[str, str]:
    intro = INTRO_ROUTES.get(product)
    return {
        "stage": STAGE_META[PRODUCT_STAGE[product]]["label"],
        "intro": f"{intro[0]} × {intro[1]}" if intro else "—",
        "entry_routes": str(len(routes(product))),
        "exit_routes": str(len(exits(product))),
        "families": str(len(factor_families(product))),
        "role": structural_role(product),
    }


def distribute(left: float, right: float, count: int) -> List[float]:
    if count <= 0:
        return []
    if count == 1:
        return [(left + right) / 2]
    step = (right - left) / (count - 1)
    return [left + i * step for i in range(count)]


def build_world_positions(stage: str) -> Dict[int, Tuple[float, float]]:
    width = 1120
    y_map = {"0": 90, "A": 230, "B": 370, "C": 510, "D": 650, "E": 790, "F": 930, "G": 1070}
    visible = visible_products(stage)
    positions: Dict[int, Tuple[float, float]] = {}

    for s in STAGE_ORDER:
        if stage_rank(s) > stage_rank(stage):
            continue
        stage_products = [p for p in STAGE_META[s]["products"] if p in visible]
        xs = distribute(130, width - 130, len(stage_products))
        y = y_map[s]
        for product, x in zip(stage_products, xs):
            positions[product] = (x, y)

    return positions


def hub_radius(product: int, selected: int) -> int:
    if product == selected:
        return 35
    family_count = len(factor_families(product))
    if family_count >= 3:
        return 28
    if family_count == 2:
        return 25
    return 23


def pattern_glow_color(product: int) -> str | None:
    role = structural_role(product)
    if role == "compression_hub":
        return "#8b5cf6"
    if role == "bridge_hub":
        return "#22c55e"
    if any(a == b for a, b in factor_families(product)):
        return "#f59e0b"
    return None


def build_world_svg(stage: str, selected: int, highlighted: List[int] | None = None) -> str:
    width = 1120
    height = 1160
    positions = build_world_positions(stage)
    visible = visible_products(stage)
    highlighted_set = set(highlighted or [])

    svg: List[str] = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" xmlns="http://www.w3.org/2000/svg">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        """
        <defs>
          <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
            <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.14"/>
          </filter>
        </defs>
        """,
    ]

    y_map = {"0": 90, "A": 230, "B": 370, "C": 510, "D": 650, "E": 790, "F": 930, "G": 1070}
    heights = {stage_key: 118 for stage_key in STAGE_ORDER}
    stage_label_svg: List[str] = []

    for s in STAGE_ORDER:
        if stage_rank(s) > stage_rank(stage):
            continue

        y = y_map[s]
        h = heights[s]
        top = y - (h / 2)

        svg.append(
            f'<rect x="24" y="{top:.1f}" width="{width - 48}" height="{h}" rx="18" '
            f'fill="{BAND_COLOR[s]}" stroke="#e2e8f0" stroke-width="1.5"/>'
        )

        label_x = 34
        label_width = 205
        label_height = 24
        label_y = top + 10
        label_text_y = label_y + 16

        stage_label_svg.append(
            f'<rect x="{label_x}" y="{label_y:.1f}" width="{label_width}" height="{label_height}" rx="12" '
            f'fill="#ffffff" fill-opacity="0.96" stroke="#cbd5e1" stroke-width="1.2"/>'
        )
        stage_label_svg.append(
            f'<text x="{label_x + 10}" y="{label_text_y:.1f}" font-size="13" font-weight="800" fill="#334155">'
            f'{STAGE_META[s]["label"]}</text>'
        )

    for product in visible:
        intro = INTRO_ROUTES.get(product)
        if not intro or product not in positions:
            continue

        px, py = positions[product]
        for src in intro:
            if src not in positions:
                continue
            sx, sy = positions[src]
            stroke = "#fb923c" if selected in {product, src} else "#94a3b8"
            opacity = "0.85" if selected in {product, src} else "0.28"
            svg.append(
                f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{px:.1f}" y2="{py:.1f}" '
                f'stroke="{stroke}" stroke-width="2.8" opacity="{opacity}"/>'
            )

    if selected in positions:
        px, py = positions[selected]
        for route in routes(selected):
            if route == INTRO_ROUTES.get(selected):
                continue
            for src in route:
                if src not in positions:
                    continue
                sx, sy = positions[src]
                svg.append(
                    f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{px:.1f}" y2="{py:.1f}" '
                    f'stroke="#8b5cf6" stroke-width="2.8" opacity="0.65" stroke-dasharray="5 5"/>'
                )

    for product in visible:
        x, y = positions[product]
        color = STAGE_META[PRODUCT_STAGE[product]]["color"]
        radius = hub_radius(product, selected)
        role = structural_role(product)
        selected_state = product == selected
        glow = pattern_glow_color(product)

        if product in highlighted_set and product != selected:
            svg.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius + 11}" fill="#f59e0b" opacity="0.18"/>'
            )

        if glow is not None:
            svg.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius + 8}" fill="{glow}" opacity="0.16"/>'
            )

        if role == "compression_hub":
            svg.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius + 8}" fill="#8b5cf6" opacity="0.08"/>'
            )
        if role == "bridge_hub":
            svg.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius + 7}" fill="#22c55e" opacity="0.08"/>'
            )
        if role == "closure_hub":
            svg.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius + 8}" fill="#f59e0b" opacity="0.14"/>'
            )

        stroke = "#fb923c" if selected_state else "#ffffff"
        stroke_width = 5 if selected_state else 3

        svg.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="{color}" '
            f'stroke="{stroke}" stroke-width="{stroke_width}" filter="url(#softShadow)"/>'
        )
        svg.append(
            f'<text x="{x:.1f}" y="{y + 7:.1f}" text-anchor="middle" font-size="19" '
            f'font-weight="800" fill="#ffffff">{product}</text>'
        )

    svg.extend(stage_label_svg)
    svg.append("</svg>")
    return "".join(svg)


def radial_angles(count: int, start_deg: float, end_deg: float) -> List[float]:
    if count <= 0:
        return []
    if count == 1:
        return [(start_deg + end_deg) / 2]
    step = (end_deg - start_deg) / (count - 1)
    return [start_deg + i * step for i in range(count)]


def arrowhead_polygon(x: float, y: float, angle_deg: float, size: float = 10.0) -> str:
    left = math.radians(angle_deg + 145)
    right = math.radians(angle_deg - 145)
    x1 = x + size * math.cos(left)
    y1 = y + size * math.sin(left)
    x2 = x + size * math.cos(right)
    y2 = y + size * math.sin(right)
    return f"{x:.1f},{y:.1f} {x1:.1f},{y1:.1f} {x2:.1f},{y2:.1f}"


def anchor_for_angle(angle_deg: float) -> str:
    c = math.cos(math.radians(angle_deg))
    if c > 0.30:
        return "start"
    if c < -0.30:
        return "end"
    return "middle"


def text_shift(anchor: str) -> int:
    if anchor == "start":
        return 7
    if anchor == "end":
        return -7
    return 0


def build_radial_svg(product: int) -> str:
    routes_list = routes(product)
    exits_list = exits(product)
    color = STAGE_META[PRODUCT_STAGE[product]]["color"]

    width = 760
    height = 540
    cx = width / 2
    cy = 275
    hub_r = 78

    entry_count = len(routes_list)
    exit_count = len(exits_list)
    max_count = max(entry_count, exit_count)

    if max_count <= 3:
        entry_outer = 152
        exit_outer = 164
        label_push = 16
        entry_angles = [-150, -90, -30][:entry_count]
        exit_angles = [150, 90, 30][:exit_count]
    elif max_count == 4:
        entry_outer = 162
        exit_outer = 174
        label_push = 16
        entry_angles = [-155, -110, -70, -25]
        exit_angles = [155, 110, 70, 25]
    else:
        entry_outer = 175
        exit_outer = 188
        label_push = 16
        entry_angles = radial_angles(entry_count, -155, -25)
        exit_angles = radial_angles(exit_count, 155, 25)

    entry_inner = hub_r + 10
    exit_inner = hub_r + 12

    svg: List[str] = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" xmlns="http://www.w3.org/2000/svg">',
        '<rect width="100%" height="100%" rx="18" fill="#020617"/>',
        '<text x="22" y="34" font-size="27" font-weight="800" fill="#e2e8f0">Radial Hub View</text>',
        '<text x="22" y="60" font-size="15" fill="#cbd5e1">Multiplication enters · Division exits</text>',
    ]

    for angle_deg, route in zip(entry_angles, routes_list):
        angle = math.radians(angle_deg)
        ox = cx + entry_outer * math.cos(angle)
        oy = cy + entry_outer * math.sin(angle)
        ix = cx + entry_inner * math.cos(angle)
        iy = cy + entry_inner * math.sin(angle)
        tx = cx + (entry_outer + label_push) * math.cos(angle)
        ty = cy + (entry_outer + label_push) * math.sin(angle)
        anchor = anchor_for_angle(angle_deg)

        svg.append(
            f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{ix:.1f}" y2="{iy:.1f}" stroke="#e2e8f0" stroke-width="3.5"/>'
        )
        svg.append(f'<polygon points="{arrowhead_polygon(ix, iy, angle_deg)}" fill="#e2e8f0"/>')
        svg.append(
            f'<text x="{tx + text_shift(anchor):.1f}" y="{ty:.1f}" text-anchor="{anchor}" '
            f'font-size="22" font-weight="700" fill="#ffffff">{route[0]}×{route[1]}</text>'
        )

    for angle_deg, route in zip(exit_angles, exits_list):
        angle = math.radians(angle_deg)
        ix = cx + exit_inner * math.cos(angle)
        iy = cy + exit_inner * math.sin(angle)
        ox = cx + exit_outer * math.cos(angle)
        oy = cy + exit_outer * math.sin(angle)
        tx = cx + (exit_outer + label_push) * math.cos(angle)
        ty = cy + (exit_outer + label_push) * math.sin(angle)
        anchor = anchor_for_angle(angle_deg)

        svg.append(
            f'<line x1="{ix:.1f}" y1="{iy:.1f}" x2="{ox:.1f}" y2="{oy:.1f}" stroke="#a78bfa" stroke-width="3.5"/>'
        )
        svg.append(f'<polygon points="{arrowhead_polygon(ox, oy, angle_deg)}" fill="#a78bfa"/>')
        svg.append(
            f'<text x="{tx + text_shift(anchor):.1f}" y="{ty + 4:.1f}" text-anchor="{anchor}" '
            f'font-size="22" font-weight="700" fill="#ddd6fe">{product}÷{route[0]}</text>'
        )

    if structural_role(product) == "compression_hub":
        svg.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{hub_r + 16}" fill="#8b5cf6" opacity="0.18"/>')

    svg.append(
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{hub_r}" fill="{color}" stroke="#ffffff" stroke-width="4.5"/>'
    )
    svg.append(
        f'<text x="{cx:.1f}" y="{cy + 16:.1f}" text-anchor="middle" font-size="46" font-weight="800" fill="#ffffff">{product}</text>'
    )
    svg.append("</svg>")
    return "".join(svg)


def card_html(title: str, value: str, accent: str) -> str:
    return f"""
    <div style="
        background:#ffffff;
        border:1px solid #e2e8f0;
        border-radius:16px;
        padding:14px 16px;
        min-height:92px;
    ">
        <div style="font-size:13px;color:#64748b;font-weight:700;margin-bottom:8px;">{title}</div>
        <div style="font-size:28px;line-height:1.1;font-weight:800;color:{accent};">{value}</div>
    </div>
    """


def pattern_badge_html(title: str, body: str) -> str:
    return f"""
    <div style="
        background:#ffffff;
        border:1px solid #e2e8f0;
        border-radius:14px;
        padding:12px 14px;
        margin-bottom:10px;
    ">
        <div style="font-size:13px;font-weight:800;color:#0f172a;margin-bottom:6px;">{title}</div>
        <div style="font-size:13px;line-height:1.5;color:#475569;">{body}</div>
    </div>
    """


def cue_badge_html(title: str, cue_text: str, cue_type: str, note: str) -> str:
    note_block = f'<div style="font-size:13px;line-height:1.5;color:#7c2d12;">{note}</div>' if note else ""
    return f"""
    <div style="
        background:#fff7ed;
        border:1px solid #fdba74;
        border-radius:14px;
        padding:12px 14px;
        margin-bottom:10px;
    ">
        <div style="font-size:13px;font-weight:800;color:#9a3412;margin-bottom:6px;">{title}</div>
        <div style="font-size:18px;line-height:1.35;font-weight:800;color:#7c2d12;margin-bottom:8px;">{cue_text}</div>
        <div style="font-size:12px;font-weight:700;color:#c2410c;margin-bottom:6px;">Type: {cue_type}</div>
        {note_block}
    </div>
    """


def render_world_map(stage: str, selected: int, highlighted: List[int] | None = None) -> None:
    svg = build_world_svg(stage, selected, highlighted)
    st.markdown(svg, unsafe_allow_html=True)


def render_radial_map(product: int) -> None:
    svg = build_radial_svg(product)
    st.markdown(svg, unsafe_allow_html=True)


def product_button_label(product: int) -> str:
    intro = INTRO_ROUTES.get(product)
    if not intro:
        return str(product)
    return f"{product} · {intro[0]}×{intro[1]}"


def visible_products_for_pattern(stage: str, pattern_id: str) -> List[int]:
    matches: List[int] = []
    for product in visible_products(stage):
        pattern_ids = {pattern.id for pattern in product_patterns(product)}
        if pattern_id in pattern_ids:
            matches.append(product)
    return matches


st.title("TMK Structural Planner")
st.caption("A deploy-safe teacher surface for product hubs, stage growth, routes in, and routes out.")

if not PATTERNS_AVAILABLE:
    st.warning(f"Pattern panel unavailable. Check patterns.py. Import error: {PATTERN_IMPORT_ERROR}")

if not MEMORY_CUES_AVAILABLE:
    st.warning(f"Memory cues unavailable. Check memory_cues.py. Import error: {MEMORY_CUES_IMPORT_ERROR}")

with st.sidebar:
    st.header("Teacher Controls")

    stage = st.radio(
        "Unlock stage",
        STAGE_ORDER,
        index=STAGE_ORDER.index(st.session_state.get("selected_stage", "0")),
        format_func=lambda s: STAGE_META[s]["label"],
    )
    st.session_state.selected_stage = stage

    st.markdown("---")
    language_mode = st.radio(
        "Language mode",
        ["Teacher", "Child"],
        key="language_mode",
    )

    st.markdown("---")
    st.markdown("**World rules**")
    st.caption("Product first")
    st.caption("Multiplication = way in")
    st.caption("Division = way out")
    st.caption("Belonging = both factors at or below 10")

selected_stage = st.session_state.selected_stage
visible = visible_products(selected_stage)

if "selected_product" not in st.session_state or st.session_state.selected_product not in visible:
    st.session_state.selected_product = visible[0]

chosen_product = st.selectbox(
    "Choose product",
    visible,
    index=visible.index(st.session_state.selected_product),
    format_func=product_button_label,
)

st.session_state.selected_product = chosen_product
selected_product = chosen_product

summary = product_summary(selected_product)
accent = STAGE_META[PRODUCT_STAGE[selected_product]]["color"]

pattern_options = sorted(PATTERNS.keys(), key=lambda pid: PATTERNS[pid].name) if PATTERNS_AVAILABLE else []
selected_pattern_id = None
selected_pattern = None
matching_products: List[int] = []

if PATTERNS_AVAILABLE and pattern_options:
    selected_pattern_id = st.selectbox(
        "Choose a pattern to inspect",
        pattern_options,
        index=0,
        format_func=lambda pid: PATTERNS[pid].name,
        key="pattern-lens-select",
    )
    selected_pattern = PATTERNS[selected_pattern_id]
    matching_products = visible_products_for_pattern(selected_stage, selected_pattern_id)

card_1, card_2, card_3, card_4 = st.columns(4)
with card_1:
    st.markdown(card_html("Selected hub", str(selected_product), accent), unsafe_allow_html=True)
with card_2:
    st.markdown(card_html("Stage", PRODUCT_STAGE[selected_product], accent), unsafe_allow_html=True)
with card_3:
    st.markdown(card_html("Intro route", summary["intro"], accent), unsafe_allow_html=True)
with card_4:
    st.markdown(card_html("Structural role", summary["role"], accent), unsafe_allow_html=True)

st.subheader("Product World Map")
render_world_map(selected_stage, selected_product, matching_products)

st.subheader("Visible products")
product_columns = st.columns(min(6, len(visible)))
for index, product in enumerate(visible):
    with product_columns[index % len(product_columns)]:
        button_type = "primary" if product == selected_product else "secondary"
        if st.button(str(product), use_container_width=True, type=button_type, key=f"product-{product}"):
            st.session_state.selected_product = product
            st.rerun()

left, right = st.columns([0.95, 1.25])

with left:
    st.subheader("Hub Detail")

    st.markdown(
        card_html(
            "Hub summary",
            f"{summary['entry_routes']} ways in · {summary['exit_routes']} ways out · {summary['families']} factor families",
            accent,
        ),
        unsafe_allow_html=True,
    )

    st.markdown(f"**Stage label:** {summary['stage']}")
    st.markdown(f"**Pedagogical intro route:** `{summary['intro']} = {selected_product}`")

    st.markdown("**Ways in**")
    for a, b in routes(selected_product):
        intro_marker = " ← intro" if INTRO_ROUTES.get(selected_product) == (a, b) else ""
        st.write(f"{a} × {b} = {selected_product}{intro_marker}")

    st.markdown("**Ways out**")
    for d, q in exits(selected_product):
        st.write(f"{selected_product} ÷ {d} = {q}")

    st.markdown("**Factor families**")
    for a, b in factor_families(selected_product):
        st.write(f"({a}, {b})")

with right:
    st.subheader("Selected Product Map")
    render_radial_map(selected_product)

st.subheader("Pattern Panel")
patterns = product_patterns(selected_product)

if not patterns:
    st.info("No active patterns found for this product.")
else:
    pattern_columns = st.columns(2)
    for index, pattern in enumerate(patterns):
        with pattern_columns[index % 2]:
            body = pattern.child_text if st.session_state.get("language_mode", "Teacher") == "Child" else pattern.teacher_note
            st.markdown(
                pattern_badge_html(
                    pattern.name,
                    body,
                ),
                unsafe_allow_html=True,
            )

st.subheader("Memory Cues")
cues = memory_cues_for_product(selected_product)

if not cues:
    st.caption("No memory cues attached to this product.")
else:
    for cue in cues:
        if st.session_state.get("language_mode", "Teacher") == "Child":
            text = cue.child_text
            note = ""
        else:
            text = cue.cue_text
            note = cue.teacher_note

        st.markdown(
            cue_badge_html(
                cue.id.replace("_", " ").title(),
                text,
                cue.cue_type,
                note,
            ),
            unsafe_allow_html=True,
        )

st.subheader("Structural neighbours")
neighbours = related_products(selected_product, selected_stage)

if not neighbours:
    st.caption("No related products visible at this stage.")
else:
    cols = st.columns(min(6, len(neighbours)))
    for i, p in enumerate(neighbours):
        with cols[i % len(cols)]:
            if st.button(f"Explore {p}", use_container_width=True, key=f"rel-{p}"):
                st.session_state.selected_product = p
                st.rerun()

st.subheader("Pattern Lens")

if not PATTERNS_AVAILABLE or not pattern_options or selected_pattern is None:
    st.caption("Pattern lens unavailable.")
else:
    lens_body = selected_pattern.child_text if st.session_state.get("language_mode", "Teacher") == "Child" else selected_pattern.teacher_note
    st.markdown(
        pattern_badge_html(
            selected_pattern.name,
            lens_body,
        ),
        unsafe_allow_html=True,
    )

    if not matching_products:
        st.caption("No visible products match this pattern at the current stage.")
    else:
        st.markdown("**Products showing this pattern**")
        pattern_cols = st.columns(min(6, len(matching_products)))
        for i, product in enumerate(matching_products):
            with pattern_cols[i % len(pattern_cols)]:
                if st.button(
                    f"Open {product}",
                    use_container_width=True,
                    key=f"pattern-open-{selected_pattern_id}-{product}",
                ):
                    st.session_state.selected_product = product
                    st.rerun()

st.subheader("Stage Overview")
overview_columns = st.columns(len(STAGE_ORDER))
for idx, stage_key in enumerate(STAGE_ORDER):
    with overview_columns[idx]:
        unlocked = stage_rank(stage_key) <= stage_rank(selected_stage)
        products = STAGE_META[stage_key]["products"]
        fill = STAGE_META[stage_key]["color"] if unlocked else "#e5e7eb"
        label_color = "#ffffff" if unlocked else "#6b7280"
        st.markdown(
            f"""
            <div style="
                background:{fill};
                border-radius:16px;
                padding:12px 10px;
                min-height:148px;
                border:1px solid #e5e7eb;
            ">
                <div style="font-size:14px;font-weight:800;color:{label_color};margin-bottom:8px;">
                    {stage_key}
                </div>
                <div style="font-size:12px;font-weight:700;color:{label_color};margin-bottom:8px;">
                    {WORLD_LABELS[stage_key]}
                </div>
                <div style="font-size:12px;line-height:1.5;color:{label_color};">
                    {", ".join(str(p) for p in products)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
