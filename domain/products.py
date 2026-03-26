from __future__ import annotations


def _validate_product_structure() -> None:
    """
    Validate the canonical TMK product registry.

    Rules:
    - every product must exist exactly once in the canonical stage mapping
    - stages may expose prior products cumulatively elsewhere, but must not
      reintroduce the same product in the canonical registry
    - ALL_PRODUCTS must match the unique canonical stage product set
    """

    duplicates: dict[int, list[str]] = {}
    first_seen_stage: dict[int, str] = {}
    canonical_products_in_stage_order: list[int] = []

    for stage_id in STAGE_ORDER:
        if stage_id not in STAGES:
            raise ValueError(f"Stage '{stage_id}' is missing from STAGES.")

        stage = STAGES[stage_id]

        if not hasattr(stage, "products"):
            raise ValueError(f"Stage '{stage_id}' is missing 'products'.")

        if not isinstance(stage.products, tuple):
            raise ValueError(
                f"Stage '{stage_id}' products must be a tuple. "
                f"Found {type(stage.products).__name__}."
            )

        for product in stage.products:
            if not isinstance(product, int):
                raise ValueError(
                    f"Stage '{stage_id}' contains non-integer product: {product!r}"
                )

            canonical_products_in_stage_order.append(product)

            if product in first_seen_stage:
                duplicates.setdefault(product, [first_seen_stage[product]]).append(stage_id)
            else:
                first_seen_stage[product] = stage_id

    if duplicates:
        duplicate_lines = []
        for product in sorted(duplicates):
            stages = " -> ".join(duplicates[product])
            duplicate_lines.append(f"{product}: {stages}")

        raise ValueError(
            "Duplicate TMK products detected in canonical stage registry:\n"
            + "\n".join(duplicate_lines)
        )

    canonical_unique_products = tuple(canonical_products_in_stage_order)

    if len(canonical_unique_products) != 42:
        raise ValueError(
            f"Canonical TMK registry must contain exactly 42 unique core products. "
            f"Found {len(canonical_unique_products)}."
        )

    if tuple(ALL_PRODUCTS) != canonical_unique_products:
        raise ValueError(
            "ALL_PRODUCTS does not match the canonical unique stage product registry.\n"
            f"Expected: {canonical_unique_products}\n"
            f"Found:    {tuple(ALL_PRODUCTS)}"
        )

    record_products = set()

    for product in ALL_PRODUCTS:
        record = product_record(product)

        if record.product != product:
            raise ValueError(
                f"Product record mismatch for {product}: record.product={record.product}"
            )

        if record.stage not in STAGES:
            raise ValueError(
                f"Product {product} references unknown stage '{record.stage}'."
            )

        if product not in STAGES[record.stage].products:
            raise ValueError(
                f"Product {product} says it belongs to stage '{record.stage}' "
                f"but is not present in that canonical stage product list."
            )

        if product in record_products:
            raise ValueError(
                f"Duplicate product record emitted by product_record(): {product}"
            )

        record_products.add(product)

    if record_products != set(ALL_PRODUCTS):
        missing = set(ALL_PRODUCTS) - record_products
        extra = record_products - set(ALL_PRODUCTS)
        raise ValueError(
            "Mismatch between ALL_PRODUCTS and product_record registry.\n"
            f"Missing: {sorted(missing)}\n"
            f"Extra: {sorted(extra)}"
        )
