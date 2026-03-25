import inspect

if "product" in params:
    worksheet = generate_worksheet(
        product=st.session_state.selected_product,
        tier=st.session_state.selected_tier,
    )
elif "product_id" in params:
    worksheet = generate_worksheet(
        product_id=st.session_state.selected_product,
        tier=st.session_state.selected_tier,
    )
else:
    raise TypeError("generate_worksheet must accept either 'product' or 'product_id'")
