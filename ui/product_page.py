def _render_product_lab(product: int) -> None:
    from services.product_lab_service import get_product_lab_view
    import ui.product_page as product_page_module

    compare_product = st.session_state.get("compare_product")

    view_model = get_product_lab_view(
        selected_product=product,
        compare_product=compare_product,
    )

    render_fn = getattr(product_page_module, "render_product_lab_page", None)
    if render_fn is None:
        render_fn = getattr(product_page_module, "render_product_page", None)

    if render_fn is None:
        st.error("Product page renderer not found in ui.product_page.")
        return

    render_fn(view_model)
