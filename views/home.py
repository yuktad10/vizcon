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
        <div style="text-align:center; padding: 20px 0 10px;">
            <h1 style="font-size:2.4em; font-weight:800; 
                       background: linear-gradient(135deg, #667eea, #764ba2);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       margin-bottom: 5px;">
                Passport for a Name
            </h1>
            <p style="font-size:1.05em; color:#6b7280; max-width:700px; margin:0 auto;">
                Some names travel the world. Others never leave home.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ─── Story Hook ───────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center; width:100%; margin:1rem auto; padding:18px 30px;
            background: linear-gradient(135deg, #f8f9ff 0%, #eef1ff 100%);
            border: 1px solid rgba(102,126,234,0.2);
            border-radius:10px;
            box-shadow: 0 4px 20px rgba(102,126,234,0.1);">
            <p style="font-size:1.05em; color:#374151; line-height:1.6; margin:0;">
                Eight nations. One language. The tightest alliance in modern history. They share armies. Intelligence. Borders.
                &nbsp;&nbsp;But do they share something as simple as... <strong style="color:#667eea;">a baby name?</strong>
                &nbsp;&nbsp;<span style="font-size:1.1em; font-weight:700; color:#667eea;">This is THAT STORY.</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ─── Anglosphere Context ──────────────────────────────────────
    st.markdown("")
    st.markdown("### 🌍 The Anglosphere")
    st.markdown(
        'The term "Anglosphere" was coined by sci-fi writer **Neal Stephenson** '
        "in his 1995 novel *The Diamond Age*. A fictional concept that became a geopolitical reality. "
        "Today it represents just **6% of the world's population** — but over **30% of its economy**."
    )

    # ─── Map Image (full width) ──────────────────────────────────
    st.image("assets/world_map.png", use_container_width=True)

    # ─── The Two Worlds (integrated baby section) ─────────────────
    st.markdown("")

    # ─── Baby Images with reveal on click ─────────────────────────
    col_pop, col_trad = st.columns(2)

    with col_pop:
        st.image("assets/baby_popculture.png", use_container_width=True)
        if st.button("🎧 Flip to reveal", key="flip_pop", use_container_width=True):
            st.markdown(
                """
                <div style="text-align:center; padding:16px 20px; 
                    background:#f0fdf4; border:2px solid #06d6a0; 
                    border-radius:10px; margin-top:5px;">
                    <p style="font-size:1.1rem; color:#374151; margin:0; line-height:1.6;">
                        🎧 Some names hit #1 in all 8 countries —<br>
                        like a global chart-topper.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_trad:
        st.image("assets/baby_traditional.png", use_container_width=True)
        if st.button("� Flip to reveal", key="flip_trad", use_container_width=True):
            st.markdown(
                """
                <div style="text-align:center; padding:16px 20px;
                    background:#fef2f2; border:2px solid #e63946;
                    border-radius:10px; margin-top:5px;">
                    <p style="font-size:0.95rem; color:#374151; margin:0; line-height:1.6;">
                        Some never leave their homeland —<br>
                        like a vinyl that only plays in one shop.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ─── Countryness Definition ───────────────────────────────────
    st.markdown("")
    st.markdown(
        """
        <div style="text-align:center; margin:1.5rem auto; padding:14px 24px;
            max-width:720px; background:#f8f9ff; border-radius:10px;
            border:1px solid rgba(102,126,234,0.15);">
            <p style="font-size:0.95rem; color:#374151; margin:0; line-height:1.6;">
                We measured cultural distinctness using a <strong style="color:#667eea;">"countryness"</strong> score —
                how geographically concentrated a name is across the Anglosphere.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_low, col_high = st.columns(2)
    with col_low:
        st.markdown(
            """
            <div style="padding:16px 20px; background:#f0fdf4; border:1px solid #06d6a0;
                border-radius:10px;">
                <p style="margin:0 0 4px; color:#06d6a0; font-weight:700;">✅ Low Countryness (1–2)</p>
                <p style="margin:0; font-size:0.9rem; color:#374151;">
                    Name used equally everywhere — a global citizen.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_high:
        st.markdown(
            """
            <div style="padding:16px 20px; background:#fef2f2; border:1px solid #e63946;
                border-radius:10px;">
                <p style="margin:0 0 4px; color:#e63946; font-weight:700;">❌ High Countryness (500+)</p>
                <p style="margin:0; font-size:0.9rem; color:#374151;">
                    Name locked to one culture — a fortress name.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Closing quote
    st.markdown("")
    st.markdown(
        """
        <div style="text-align:center; margin:1.5rem 0; padding:20px;
            background:#f5f5fa; border-radius:10px; border:1px solid #e5e7eb;">
            <p style="font-size:1.05rem; color:#4b5563; font-style:italic; margin:0;">
                "One baby named for the world. One named for home.<br>
                Both are real. Both are happening right now. That's the story."
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
