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

    # Stats bar — from actual data
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Unique Names", f"{unique_names:,}")
    with col2:
        st.metric("Countries", str(num_countries))
    with col3:
        st.metric("Time Span", f"{year_min}–{year_max}")
    with col4:
        st.metric("Records", f"{total_records:,}")

       # ─── The Anglosphere — Globe ──────────────────────────────────
    st.markdown("### 🌍 The Anglosphere")
    st.markdown(
        "Eight countries united by one language — English. "
        "Connected through colonization, migration, and shared media. "
        "But each carries its **own cultural currents** beneath the surface."
    )

    import plotly.graph_objects as go

    # Show custom map image instead of interactive globe
    st.image("assets/world_map.png", use_container_width=True)

    # Country detail cards below the globe
    countries = {
        "🇺🇸 USA": "Hispanic heritage, melting pot",
        "🇬🇧 England & Wales": "Commonwealth hub, trend bridge",
        "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland": "Celtic identity",
        "🏴 Northern Ireland": "Gaelic revival (political)",
        "🇮🇪 Ireland": "Gaelic heritage",
        "🇨🇦 Canada": "Francophone Quebec",
        "🇦🇺 Australia": "Early adopter, exporter",
        "🇳🇿 New Zealand": "Pacific connections",
    }

    cols = st.columns(4)
    for i, (country, desc) in enumerate(countries.items()):
        with cols[i % 4]:
            st.markdown(
                f"""
                <div style="background:#f5f5fa; border:1px solid #e5e7eb; 
                            border-radius:8px; padding:12px; margin-bottom:10px; text-align:center;">
                    <div style="font-size:1.1em; font-weight:600;">{country}</div>
                    <div style="font-size:0.8em; color:#6b7280;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("---")

    # ─── Core Question ────────────────────────────────────────────
    st.markdown("### 🔬 Language vs Culture")
    st.markdown(
        """
        > *"These 8 countries share a language. Does that mean they share a culture?
        > Baby names — the most personal choice a family makes — give us the answer."*
        """
    )

    st.markdown(
        """
        We measured cultural distinctness using a **"countryness" score**:
        - **Low** (1–2) → Name used equally everywhere (e.g. Noah, Olivia)
        - **High** (500+) → Name locked to one culture (e.g. Sadhbh, Frédérique)
        """
    )

    # ─── Two Truths ───────────────────────────────────────────────
    st.markdown("#### The Answer: Both Are True")

    col_yes, col_no = st.columns(2)
    with col_yes:
        st.markdown(
            """
            <div style="background:#f0fdf4; border-left:4px solid #06d6a0; 
                        border-radius:8px; padding:20px;">
                <div style="font-weight:700; color:#06d6a0; font-size:1.1em;">
                    ✅ YES — Names ARE Converging
                </div>
                <div style="font-size:2em; font-weight:800; color:#06d6a0; margin:8px 0;">
                    −50%
                </div>
                <div style="color:#4b5563;">
                    Countryness dropped from 22 (1997) to 11 (2023).
                    Countries are naming babies more similarly than ever.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_no:
        st.markdown(
            """
            <div style="background:#fef2f2; border-left:4px solid #e63946; 
                        border-radius:8px; padding:20px;">
                <div style="font-weight:700; color:#e63946; font-size:1.1em;">
                    ❌ BUT — Cultural Borders Persist
                </div>
                <div style="font-size:2em; font-weight:800; color:#e63946; margin:8px 0;">
                    39%
                </div>
                <div style="color:#4b5563;">
                    of names remain culturally distinct — locked to specific countries.
                    N. Ireland is getting MORE distinct, not less.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")

    # ─── Key Chart ────────────────────────────────────────────────
    st.markdown("#### Cultural Distinctness Over Time (1997–2023)")
    st.caption("Lower = more converged across countries")

    df = load_metrics()
    fig = countryness_over_time(df)
    st.plotly_chart(fig, use_container_width=True)

    # ─── Transition ───────────────────────────────────────────────
    st.info(
        "💡 **Two opposite truths coexist.** "
        "Use the sidebar to explore both sides: "
        "**Convergence** (coming together) and **Invisible Borders** (staying apart)."
    )

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
