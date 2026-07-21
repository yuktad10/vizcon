import streamlit as st

st.set_page_config(
    page_title="What's in a Name? | VizCon 2026",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="collapsed",  # hide sidebar
)

# ─── Top Tab Navigation ───────────────────────────────────────────
tab_home, tab_conv, tab_borders, tab_disc, tab_methods = st.tabs(
    ["🏠 Home", "🤝 Convergence", "🧱 Invisible Borders", "🎉 Discoveries", "📋 Methods"]
)

with tab_home:
    from views.home import render as render_home
    render_home()

with tab_conv:
    from views.convergence import render as render_convergence
    render_convergence()

with tab_borders:
    from views.borders import render as render_borders
    render_borders()

with tab_disc:
    from views.discoveries import render as render_discoveries
    render_discoveries()

with tab_methods:
    from views.methods import render as render_methods
    render_methods()
