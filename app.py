import streamlit as st
import sys
import os

# Add the project root to Python path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Now Playing: The Name Playlist",
    page_icon="🎶",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Hide default Streamlit UI clutter ─────────────────────────────
st.markdown("""
<style>
    /* Hide hamburger menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Chapter dividers */
    .chapter-divider {
        margin: 4rem 0 3rem 0;
        padding: 2rem 0;
        text-align: center;
        position: relative;
    }
    .chapter-divider::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 10%;
        right: 10%;
        height: 1px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }
    .chapter-number {
        display: inline-block;
        background: white;
        padding: 0 1.5rem;
        position: relative;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #667eea;
    }
    
    /* Floating chapter nav */
    .chapter-nav {
        position: fixed;
        right: 1.5rem;
        top: 50%;
        transform: translateY(-50%);
        z-index: 1000;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        align-items: center;
    }
    .chapter-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #ddd;
        border: 2px solid #667eea;
        transition: all 0.3s;
        cursor: pointer;
    }
    .chapter-dot:hover {
        background: #667eea;
        transform: scale(1.3);
    }
    .chapter-dot.active {
        background: #667eea;
    }
    
    /* Scroll progress bar */
    .scroll-progress {
        position: fixed;
        top: 0;
        left: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        z-index: 9999;
        transition: width 0.1s;
    }
    
    /* Container max width */
    .block-container {
        max-width: 1200px;
        padding-left: 2rem;
        padding-right: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# ─── Chapter Divider Helper ────────────────────────────────────────
def chapter_break(number, title):
    """Render a styled chapter divider between sections."""
    st.markdown(f"""
    <div class="chapter-divider" id="chapter-{number}">
        <span class="chapter-number">Chapter {number} — {title}</span>
    </div>
    """, unsafe_allow_html=True)


# ─── THE STORY (scroll format) ─────────────────────────────────────

# ═══ CHAPTER 1: The Opening (Home) ═══
try:
    from views.home import render as render_home
    render_home()
except Exception as e:
    st.error(f"Error loading Home: {e}")


# ═══ CHAPTER 2: The Global Playlist ═══
chapter_break(2, "The Global Playlist")
try:
    from views.convergence import render as render_convergence
    render_convergence()
except Exception as e:
    st.error(f"Error loading Global Playlist: {e}")


# ═══ CHAPTER 3: The Local Vinyl ═══
chapter_break(3, "The Local Vinyl")
try:
    from views.borders import render as render_borders
    render_borders()
except Exception as e:
    st.error(f"Error loading Local Vinyl: {e}")


# ═══ CHAPTER 4: Discoveries ═══
chapter_break(4, "Discoveries")
try:
    from views.discoveries import render as render_discoveries
    render_discoveries()
except Exception as e:
    st.error(f"Error loading Discoveries: {e}")


# ═══ CHAPTER 5: Methods ═══
chapter_break(5, "Methods")
try:
    from views.methods import render as render_methods
    render_methods()
except Exception as e:
    st.error(f"Error loading Methods: {e}")


# ═══ FOOTER ═══
st.markdown("""
<div style="margin-top:5rem; padding:3rem 2rem; text-align:center; 
            background: linear-gradient(135deg, #0d1117, #1a1a2e); 
            border-radius: 16px; color: white;">
    <h2 style="font-size:1.8rem; margin:0 0 0.5rem 0;">🎶 End of the Playlist</h2>
    <p style="color: rgba(255,255,255,0.7); font-size:0.9rem; margin:0 0 1rem 0;">
        27 years. 8 countries. 117 million babies. 17,575 unique names.
    </p>
    <p style="color: rgba(255,255,255,0.5); font-size:0.75rem;">
        Now Playing: The Name Playlist — A data storytelling project by Yukta Dhankhar
    </p>
</div>
""", unsafe_allow_html=True)
