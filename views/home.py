import streamlit as st
from utils.data_loader import load_metrics
from utils.charts import countryness_over_time, COLORS


def render():
    from utils.data_loader import load_metrics

    df = load_metrics()

    # Compute actual stats from data
    unique_names = df["name"].nunique()
    num_countries = df["max_country"].nunique()
    year_min = df["year"].min()
    year_max = df["year"].max()
    total_records = len(df)

    # ─── Hero Section ─────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center; padding: 30px 0 20px;">
            <h1 style="font-size:2.8em; font-weight:800; 
                       background: linear-gradient(135deg, #667eea, #764ba2);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       margin-bottom: 8px;">
                Passport for a Name
            </h1>
            <p style="font-size:1.2em; color:#6b7280; max-width:700px; margin:0 auto;">
                Some names travel the world. Others never leave home.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ─── Story Hook ───────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center; width:100%; margin:2rem auto; padding:25px 40px;
            background: linear-gradient(135deg, #f8f9ff 0%, #eef1ff 100%);
            border: 1px solid rgba(102,126,234,0.2);
            border-radius:12px;
            box-shadow: 0 4px 20px rgba(102,126,234,0.1);">
            <p style="font-size:1.2em; color:#374151; line-height:1.6; margin:0; text-transform:uppercase; letter-spacing:1px;">
                Eight nations. One language. The tightest alliance in modern history. They share armies. Intelligence. Borders.
                &nbsp;&nbsp;But do they share something as simple as... <strong style="color:#667eea;">a baby name?</strong>
                &nbsp;&nbsp;<span style="font-size:1.2em; font-weight:700; color:#667eea;">This is that story.</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ─── Anglosphere Context ──────────────────────────────────────
    st.markdown("")
    st.markdown("### 🌍 The Anglosphere")
    st.markdown(
        "Eight countries united by one language — English. "
        "Connected through colonization, migration, and shared media. "
        "But each carries its **own cultural currents** beneath the surface."
    )

    # ─── Map Image (reduced size) ────────────────────────────────
    col_left, col_center, col_right = st.columns([1, 3, 1])
    with col_center:
        st.image("assets/world_map.png", use_container_width=True)

    st.markdown("---")

    # ─── Baby Images: Two Worlds ─────────────────────────────────
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align:center; margin: 2rem 0 1.5rem;">
            <p style="font-size:0.8rem; color:#667eea; text-transform:uppercase; 
                      letter-spacing:3px; margin-bottom:6px;">
                THE TWO WORLDS OF NAMING
            </p>
            <h2 style="color:#1a1a2e; font-size:1.8rem; margin:0; font-weight:700;">
                Same Language. Different Cultures. One Choice.
            </h2>
            <p style="color:#6b7280; font-size:0.95rem; margin-top:8px;">
                👆 Click on a baby to explore their world
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_pop, col_trad = st.columns(2)

    with col_pop:
        st.image("assets/baby_popculture.png", use_container_width=True)
        st.markdown(
            """
            <div style="text-align:center; padding:14px 20px; 
                background:#f0fdf4; border:1px solid #06d6a0; 
                border-radius:10px; margin-top:10px;">
                <p style="font-size:1.4rem; margin:0; color:#06d6a0; font-weight:700;">
                    🎧 "Maverick"
                </p>
                <p style="font-size:0.88rem; color:#4b5563; margin:6px 0 0;">
                    Pop culture baby — trending in ALL 8 countries.<br>
                    <strong style="color:#06d6a0;">Countryness: 1.2</strong> (global)
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("▶ Explore The Global Playlist", key="btn_playlist", use_container_width=True):
            st.session_state["active_tab"] = 1
            st.markdown(
                """<script>
                var tabs = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
                if (tabs.length > 1) tabs[1].click();
                </script>""",
                unsafe_allow_html=True,
            )

    with col_trad:
        st.image("assets/baby_traditional.png", use_container_width=True)
        st.markdown(
            """
            <div style="text-align:center; padding:14px 20px;
                background:#fef2f2; border:1px solid #e63946;
                border-radius:10px; margin-top:10px;">
                <p style="font-size:1.4rem; margin:0; color:#e63946; font-weight:700;">
                    💿 "Sadhbh"
                </p>
                <p style="font-size:0.88rem; color:#4b5563; margin:6px 0 0;">
                    Gaelic baby — locked to Ireland, unpronounceable elsewhere.<br>
                    <strong style="color:#e63946;">Countryness: 8,171</strong> (fortress)
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("▶ Explore The Local Vinyl", key="btn_vinyl", use_container_width=True):
            st.session_state["active_tab"] = 2
            st.markdown(
                """<script>
                var tabs = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
                if (tabs.length > 2) tabs[2].click();
                </script>""",
                unsafe_allow_html=True,
            )

    # Closing quote
    st.markdown("")
    st.markdown(
        """
        <div style="text-align:center; margin:1.5rem 0; padding:20px;
            background:#f5f5fa; border-radius:10px; border:1px solid #e5e7eb;">
            <p style="font-size:1.1rem; color:#4b5563; font-style:italic; margin:0;">
                "One baby named for the world. One named for home.<br>
                Both are real. Both are happening right now. That's the story."
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
