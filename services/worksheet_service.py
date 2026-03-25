try:
    worksheet = generate_worksheet(
        product=st.session_state.selected_product,
        tier=st.session_state.selected_tier,
    )
except TypeError:
    worksheet = generate_worksheet(
        product_id=st.session_state.selected_product,
        tier=st.session_state.selected_tier,
    )
