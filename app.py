import streamlit as st
import sys
import os

# Add the project root to Python path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Passport for a Name",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Top Tab Navigation ───────────────────────────────────────────
tab_home, tab_conv, tab_borders, tab_disc, tab_methods = st.tabs(
    ["🏠 Home", "🤝 Convergence", "🧱 Invisible Borders", "🎉 Discoveries", "📋 Methods"]
)

with tab_home:
    try:
        from views.home import render as render_home
        render_home()
    except Exception as e:
        st.error(f"Error loading Home: {e}")

with tab_conv:
    try:
        from views.convergence import render as render_convergence
        render_convergence()
    except Exception as e:
        st.error(f"Error loading Convergence: {e}")

with tab_borders:
    try:
        from views.borders import render as render_borders
        render_borders()
    except Exception as e:
        st.error(f"Error loading Borders: {e}")

with tab_disc:
    try:
        from views.discoveries import render as render_discoveries
        render_discoveries()
    except Exception as e:
        st.error(f"Error loading Discoveries: {e}")

with tab_methods:
    try:
        from views.methods import render as render_methods
        render_methods()
    except Exception as e:
        st.error(f"Error loading Methods: {e}")
