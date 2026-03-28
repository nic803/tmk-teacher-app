TMK Curriculum & MSVWA Framework

(Knowledge Document)

Purpose

This document explains the curriculum structure behind The Multiplication Key (TMK) and the MSVWA diagnostic framework used in the TMK Teacher App.

It provides context for developers, designers, and AI coding assistants working on the system so that the mathematical structure and instructional logic are preserved during development.

TMK is not a traditional multiplication table system.
It is a product-centred structural curriculum.

1. The Multiplication Key (TMK)
Core Definition

TMK is a structured multiplication curriculum organised around products, not multiplication facts.

Traditional teaching often focuses on:

3 × 4 = 12

TMK instead treats:

12

as the primary mathematical object, with multiplication and division routes acting as representations of that product.

2. TMK Domain Boundaries

TMK operates within a bounded multiplication domain:

1 × 1  →  10 × 10

Within this domain there are:

42 distinct products

Each product is represented by:

multiplication routes
inverse division relationships
structural role in the multiplication system

This bounded domain prevents the system from becoming an unlimited multiplication table and allows deep structural understanding.

3. Product-Centred Structure

In TMK:

Product = primary mathematical object

Each product contains:

Multiplication routes

Example for product 36

4 × 9
6 × 6
3 × 12 (outside TMK core domain but structurally relevant)
Division exits
36 ÷ 4 = 9
36 ÷ 9 = 4
36 ÷ 6 = 6
Structural role

Examples:

square
doubling chain
near-ten complement
scaling anchor

The teacher app visualises these relationships in Product Lab.

4. TMK Stage Curriculum

The TMK curriculum introduces products in fixed stages.

The stage order is canonical and must not be changed.

A
B
C
D
E
F
G

Each stage introduces a specific structural idea.

Earlier products remain available in later stages because the system is cumulative.

Stage A — Anchors

Purpose:

Establish fundamental multiplication anchors.

Examples of ideas:

1× structure
10× structure
core anchors

These products act as entry points for later derivations.

Stage B — Scaling

Focus:

doubling
scaling patterns

Learners begin seeing multiplication as growth of quantities, not isolated facts.

Stage C — Midpoint Products

Focus:

balanced products
intermediate structures

Students begin identifying relationships between product families.

Stage D — Complement / Near-Ten Logic

This is a major conceptual stage.

Example:

9 × n = (10 × n) − n

Example:

9 × 4
= 10 × 4 − 4
= 40 − 4
= 36

This stage introduces compensating structure.

Stage E — Doubling Chains

Products are derived through doubling relationships:

6 → 12 → 24 → 48

Students begin to see multiplication as transformations along chains.

Stage F — Interleaving Structures

Products interact across multiple structural families.

Learners must coordinate multiple strategies.

Stage G — Closure

Final stage consolidates the complete TMK system.

Learners understand:

all product relationships
inverse links
multiple lawful routes

The multiplication system becomes a connected network, not a set of tables.

5. Cumulative Structure Law

TMK structure is always cumulative.

For any stage S:

available_products = union(Stage A → S)

and

new_products = products introduced in S only

Earlier products never disappear.

This rule is fundamental to the curriculum and must not be violated in software.

6. Routes

Each product contains routes.

Routes represent valid mathematical transformations.

Two types exist.

Canonical Routes

These are the direct multiplication relationships.

Example:

4 × 9
6 × 6

They represent multiplication truth.

Derived Routes

Derived routes are structural transformations based on other products.

Example chain:

6 → 12 → 24 → 48

Derived routes must preserve source products.

7. TMK in the Teacher App

The app exposes TMK structure through different screens.

Structural Planner

Shows:

stage order
stage products
cumulative structure
Product Lab

Shows:

product hub
routes
inverse relationships
comparisons
Worksheet Studio

Generates practice tasks based on:

stage
product set
tier
selection scope
Instruction Planner (future)

Provides teacher explanation tools.

8. MSVWA Diagnostic Framework

MSVWA is a diagnostic model used in TMK assessments.

It is not part of the mathematical structure itself.

It is used to analyse how a learner interacts with the multiplication system.

MSVWA Components
M — Marker
S — Sequence
V — Variation
W — Working Memory
A — Attention
Marker

Markers indicate recognition signals in a task.

Examples:

square number recognition
doubling pattern
near-ten adjustment

Markers show whether a learner detects key structural cues.

Sequence

Sequence refers to the order of reasoning steps.

Example for 9× strategy:

10 × 4
minus 4

Correct sequencing shows the learner understands the structural derivation.

Variation

Variation measures the ability to apply a structure in different contexts.

Example:

9 × 3
9 × 4
9 × 7

A learner must recognise the same underlying idea across problems.

Working Memory

Working memory measures the ability to hold and manipulate intermediate values.

Example:

10 × 7 = 70
70 − 7

If a learner loses track of the intermediate value, the reasoning chain breaks.

Attention

Attention measures whether learners focus on structural cues rather than surface features.

For example:

recognising

6 × 6

as a square rather than treating it as unrelated facts.

9. MSVWA in the Teacher App

MSVWA appears only in:

teacher key outputs
diagnostic tagging
assessment analysis

It must never modify:

products
routes
stages
structure

MSVWA is a diagnostic layer, not a mathematical one.

10. Relationship Between TMK and MSVWA
TMK = mathematical structure
MSVWA = diagnostic interpretation

The app must keep these layers separate.

TMK defines what mathematics exists.

MSVWA describes how learners interact with it.

11. Development Implications

Any software development must respect:

Structural invariants

Products are unique and cumulative.

Domain purity

Domain modules define mathematics.

UI must not redefine mathematical logic.

Diagnostic isolation

MSVWA logic must remain separate from structure generation.

Summary

The TMK Teacher App implements a product-centred multiplication curriculum built on:

42 products
stage progression
route relationships
inverse links

MSVWA provides a diagnostic lens that helps teachers interpret learner reasoning.

Together they allow multiplication to be taught as a structured mathematical network, rather than a memorised table.
