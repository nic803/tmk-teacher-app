[tmk_ui_knowledge_doc.md](https://github.com/user-attachments/files/26321390/tmk_ui_knowledge_doc.md)[Uploa# TMK Teacher App --- Current UI Knowledge Doc

## Purpose

This document captures the currently inspected state of the TMK Teacher
App so a coding GPT can reason safely before making changes. It is a
knowledge/reference document, not a code change plan.

------------------------------------------------------------------------

## 1. Current Repository Shape

The project is structured with clear layers:

-   UI/
-   domain/
-   models/
-   services/
-   root worksheet and teacher key files
-   app.py as the application entry point

### UI files observed

-   app.py
-   UI/planner_page.py
-   UI/product_lab_page.py

### Domain files

-   domain/products.py
-   domain/routes.py
-   domain/structure.py
-   domain/product_metadata.py
-   domain/product_banks.py
-   domain/stage_vocabulary.py
-   domain/worksheet_formats.py
-   domain/worksheet_taxonomy.py

### Service files

-   services/product_selection_engine.py
-   services/worksheet_generation_service.py
-   services/worksheet_planner.py
-   services/worksheet_renderer.py
-   services/worksheet_validation.py
-   services/question_form_engine.py
-   services/teacher_key_builder.py
-   services/pupil_prompt_map.py
-   services/wording_guard.py
-   services/wording_policy.py

### Model files

-   models/worksheet_models.py

### Worksheet system files

-   worksheet_engine.py
-   worksheet_service.py
-   worksheet_policy.py
-   worksheet_blueprints.py
-   worksheet_blueprint_library.py
-   teacher_key_engine.py
-   teacher_render_map.py
-   tier_policy.py

------------------------------------------------------------------------

## 2. Current App Entry Structure

app.py currently:

-   sets Streamlit page configuration
-   initializes session state
-   syncs surface from query parameters
-   applies CSS styles
-   renders header
-   renders top navigation
-   renders sidebar
-   routes to one of three UI surfaces

### Surfaces currently implemented

Structural Planner\
Product Lab\
Worksheet Studio

Instruction Planner is not yet implemented.

------------------------------------------------------------------------

## 3. Current Session State Keys

The application initializes the following session state keys:

surface\
selected_product\
selected_tier\
compare_product\
planner_link_mode\
planner_zoom_mode\
route_view_mode\
selected_route_index\
selected_stage\
worksheet_format\
selection_scope\
selection_mode\
include_recap\
recap_count\
worksheet_rotation_index\
last_bundle\
last_request_signature

These should be treated as stable unless deliberately migrated.

------------------------------------------------------------------------

## 4. Query Parameter Behaviour

The app reads a query parameter:

surface

This determines which UI surface is shown.

No product query parameter is currently synchronized.

------------------------------------------------------------------------

## 5. Theme System

Two themes are defined:

LIGHT_THEME\
DARK_THEME

CSS classes used across the UI include:

tmk-shell\
tmk-header\
tmk-panel\
tmk-card\
tmk-answer-box\
tmk-section-title\
tmk-section-subtitle\
tmk-small-label\
tmk-value\
tmk-note\
tmk-pill\
tmk-pill-accent\
tmk-soft-list\
tmk-worksheet-frame

The palette currently used is the older orange‑accent theme.

------------------------------------------------------------------------

## 6. Navigation and Sidebar

### Top Navigation

Navigation buttons correspond to the surfaces tuple.

Clicking a surface updates: - session state surface - query parameter
surface

Then triggers a rerun.

### Sidebar

The sidebar currently shows:

TMK summary: - product - stage - intro route - route count - division
exits - structural role

Optional metadata: - square - factor 7 - multiple routes

Surface‑specific information is also displayed depending on the active
screen.

------------------------------------------------------------------------

## 7. Structural Planner

Rendered by function:

\_render_structural_planner(product)

### Controls

-   selected product selector
-   planner link mode selector
-   planner zoom selector

### Metrics

-   selected stage
-   introduced here
-   full routes
-   division exits

### Left Column

Selected product card\
Stage introduced products\
Cumulative products\
New products at stage\
Admissible routes

### Right Column

Stage sequence cards

Word bank section containing: - new vocabulary - cumulative vocabulary -
required worksheet vocabulary focus - preferred quiz formats - preferred
vocab task types - example child‑friendly questions

Observation: this screen mixes structural planning, instruction support,
and worksheet guidance.

------------------------------------------------------------------------

## 8. Stage Sequence Rendering

Function:

\_render_stage_cards()

Displays each stage with product pills and highlights the selected
product.

------------------------------------------------------------------------

## 9. Product Lab

Rendered by:

\_render_product_lab(product)

### Controls

Selected product\
Compare product\
Route view mode

### Metrics

Product\
Stage\
Distinct routes\
Compare product

### Left Column

Hub overview\
Route inspector\
Inverse labels

### Right Column

Compare products\
Selected product routes\
Compare product routes

Observation: mathematically focused but visually dense.

------------------------------------------------------------------------

## 10. Worksheet Studio

Rendered by:

\_render_worksheet_studio()

### Configuration Controls

Worksheet stage\
Worksheet format\
Tier\
Selection scope\
Selection mode\
Include recap\
Recap count

### Generation Pipeline

\_build_product_selection_request()\
\_worksheet_request_signature()\
generate_worksheet_bundle()

Rotation logic uses worksheet_rotation_index.

### Output Sections

Pupil worksheet\
Selection rationale\
Teacher key\
Supported vocabulary\
Structural tags

This subsystem already contains substantial working logic.

------------------------------------------------------------------------

## 11. Helper Functions in app.py

Helper utilities include:

product selection request builder\
metric card row renderer\
pill list renderer\
word list renderer\
route formatting\
worksheet request signature generation\
worksheet bundle invalidation\
bundle extraction helpers

This means app.py currently handles layout, UI rendering, and helper
orchestration.

------------------------------------------------------------------------

## 12. UI Risk Map

Low risk:

theme variables\
CSS styling\
header presentation\
panel styling

Medium risk:

planner controls\
product lab controls\
sidebar summaries

High risk:

worksheet generation pipeline\
rotation logic\
session state structure

------------------------------------------------------------------------

## 13. Confirmed UI Problems

Structural Planner mixes structure and instruction.

Sidebar duplicates summary information.

Product Lab exposes too many route lists simultaneously.

Worksheet Studio should be treated as stable infrastructure.

------------------------------------------------------------------------

## 14. Safe Refactor Boundaries

Safe UI files:

app.py\
UI/planner_page.py\
UI/product_lab_page.py

Protected files:

domain/\*\
services/\*\
worksheet engines\
teacher key engines\
models

------------------------------------------------------------------------

## 15. Target Screen Model

Planned screens:

Structural Planner\
Product Lab\
Instruction Planner\
Worksheet Studio

### Structural Planner

Stage structure only.

### Product Lab

Product mathematics and relationships.

### Instruction Planner

Vocabulary, prompts, explanation flow, and teacher planning.

### Worksheet Studio

Worksheet generation and preview.

------------------------------------------------------------------------

## 16. Locked Colour Palette

Blue Slate --- #497379\
Mid Blue --- #83B8BE\
Light Blue --- #A9CED2\
Cream Stone --- #E8E1D5\
Soft Paper --- #F7F4EE\
Amber Sand --- #ECA159\
Coral --- #FF5E57\
Mist Grey --- #D9D4C8\
Charcoal Ink --- #2F3A3C\
Slate Grey --- #6C7A7D\
White --- #FFFFFF

------------------------------------------------------------------------

## 17. Coding Safety Rules

1.  Never change a file before inspecting it.
2.  Always return full‑file replacements.
3.  Do not alter domain truth.
4.  Preserve session state keys.
5.  Maintain widget key uniqueness.
6.  Treat worksheet generation as high‑risk.
7.  Separate structure, instruction, product logic, and practice into
    different screens.
8.  Avoid unnecessary query parameter changes.
9.  Refactor one screen at a time.
10. Begin with theme and styling before layout changes.

------------------------------------------------------------------------

## 18. Next Inspection Order

1.  UI/planner_page.py
2.  UI/product_lab_page.py

This confirms whether those files are active or legacy.

------------------------------------------------------------------------

## 19. Summary

The application currently works and is structurally sound.

The main UI issue is screen overload rather than architectural failure.

A safe refactor should be:

incremental\
UI‑first\
file‑by‑file

The worksheet system and domain logic should remain untouched during
early UI cleanup.
ding tmk_ui_knowledge_doc.md…]()
