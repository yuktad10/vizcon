import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import os
from utils.data_loader import load_metrics, load_summary
from utils.charts import CHART_LAYOUT, COLORS, COUNTRY_COLORS


def render():
    # ─── Header ───────────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center; padding: 20px 0 10px;">
            <h1 style="font-size: 2.4em; color: #4A5568;">
                💿 The Local Vinyl
            </h1>
            <p style="font-size: 1.15em; color: #718096; max-width: 700px; margin: 0 auto;">
                Not every name makes it to the global playlist.<br>
                Some are pressed on vinyl that only plays in one country.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    df = load_metrics()
    summary = load_summary()
    data_2023 = df[df["year"] == 2023]

    # ══════════════════════════════════════════════════════════════
    # SECTION 1: QUIZ FIRST (Hook immediately)
    # ══════════════════════════════════════════════════════════════

    st.markdown("### 🎤 Can You Say This?")
    st.markdown(
        "Before we explain why some names never leave — **try reading these aloud.** "
        "These are real baby names from the Anglosphere. Can you pronounce them?"
    )

    # Pronunciation challenge data
    challenges = [
        {
            "name": "Sadhbh",
            "country": "🇮🇪 Ireland",
            "language": "Irish Gaelic",
            "countryness": 8171,
            "actual": "SIVE (just one syllable!)",
            "hint": "Rhymes with a number between four and six.",
        },
        {
            "name": "Seumas",
            "country": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland",
            "language": "Scottish Gaelic",
            "countryness": 4629,
            "actual": "SHAY-mus",
            "hint": "A king's name in disguise — think Bond, not bible.",
        },
        {
            "name": "Ffion",
            "country": "🏴󠁧󠁢󠁷󠁬󠁳󠁿 Wales",
            "language": "Welsh",
            "countryness": 1761,
            "actual": "FEE-on",
            "hint": "In Welsh, one of these letters is lying to you.",
        },
        {
            "name": "Frédérique",
            "country": "🇨🇦 Canada",
            "language": "French",
            "countryness": 10588,
            "actual": "fray-day-REEK",
            "audio_file": "frederique",
            "hint": "The accents aren't decorative — each one changes a vowel.",
        },
        {
            "name": "Ophélie",
            "country": "🇨🇦 Canada",
            "language": "French",
            "countryness": 3786,
            "actual": "oh-fay-LEE",
            "audio_file": "ophelie",
            "hint": "Shakespeare knew her, but the French say her name differently.",
        },
        {
            "name": "Ngaire",
            "country": "🇳🇿 New Zealand",
            "language": "Māori",
            "countryness": 11270,
            "actual": "NY-ree",
            "hint": "The first two letters are actually one sound you already know.",
        },
        {
            "name": "Aroha",
            "country": "🇳🇿 New Zealand",
            "language": "Māori",
            "countryness": 13713,
            "actual": "ah-ROH-ha",
            "hint": "What you say at the end of a Hawaiian greeting — but at the start.",
        },
        {
            "name": "Narelle",
            "country": "🇦🇺 Australia",
            "language": "Aboriginal Australian",
            "countryness": 4738,
            "actual": "nah-RELL",
            "hint": "Stress the ending — think of a bell, not a fairy tale.",
        },
        {
            "name": "Caoimhín",
            "country": "🏴 N. Ireland",
            "language": "Irish Gaelic",
            "countryness": 465,
            "actual": "KEE-veen",
            "audio_file": "caoimhin",
            "hint": "You already know this name — just not in this spelling.",
        },
        {
            "name": "Nikau",
            "country": "🇳🇿 New Zealand",
            "language": "Māori",
            "countryness": 29620,
            "actual": "NEE-kow",
            "hint": "Named after a tree. Rhymes with 'free cow'.",
        },
    ]

    # Challenge selector
    if "challenge_idx" not in st.session_state:
        st.session_state.challenge_idx = 0
    if "revealed" not in st.session_state:
        st.session_state.revealed = False

    challenge = challenges[st.session_state.challenge_idx]

    # Display the challenge card
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #F0F8FF, #E8F4FD); 
                    border: 2px solid #7C9FD6; border-radius: 16px; 
                    padding: 30px; text-align: center; margin: 20px 0;">
            <div style="font-size: 0.85em; color: #718096; text-transform: uppercase; 
                        letter-spacing: 2px;">How do you pronounce...</div>
            <div style="font-size: 3em; font-weight: 800; color: #4A5568; 
                        margin: 15px 0; font-family: Georgia, serif;">
                {challenge['name']}
            </div>
            <div style="font-size: 0.9em; color: #718096;">
                {challenge['country']} · Countryness: <b>{challenge['countryness']:,}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Buttons row
    col_hint, col_reveal, col_next = st.columns([1, 1, 1])

    with col_hint:
        if st.button("💡 Hint", use_container_width=True):
            st.info(f"💡 {challenge['hint']}")

    with col_reveal:
        if st.button("🔊 Reveal Pronunciation", use_container_width=True):
            st.session_state.revealed = True

    with col_next:
        if st.button("➡️ Next Name", use_container_width=True):
            st.session_state.challenge_idx = (st.session_state.challenge_idx + 1) % len(challenges)
            st.session_state.revealed = False
            st.rerun()

    # Reveal section
    if st.session_state.revealed:
        st.markdown(
            f"""
            <div style="background: #F0FFF4; border: 2px solid #A8E6C8; border-radius: 12px;
                        padding: 20px; text-align: center; margin-top: 16px;">
                <div style="font-size: 0.85em; color: #059669; text-transform: uppercase; 
                            letter-spacing: 2px;">It's pronounced:</div>
                <div style="font-size: 2.2em; font-weight: 700; color: #059669; margin: 8px 0;">
                    "{challenge['actual']}"
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Audio playback
        audio_key = challenge.get("audio_file", challenge["name"].lower())
        audio_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets", "audio", f"{audio_key}.wav"
        )
        if os.path.exists(audio_path):
            st.audio(audio_path)
        else:
            st.caption("🔈 Audio clip coming soon!")

        # Why it matters
        st.markdown(
            f"""
            <div style="background: #FFF5F5; border-radius: 8px; padding: 12px; 
                        margin-top: 12px; text-align: center;">
                <span style="color: #e63946; font-weight: 600;">
                    Countryness: {challenge['countryness']:,}
                </span>
                <span style="color: #718096;"> — This is why </span>
                <span style="font-weight: 600;">{challenge['name']}</span>
                <span style="color: #718096;"> never left {challenge['country']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Progress dots
    dots = ""
    for i in range(len(challenges)):
        if i == st.session_state.challenge_idx:
            dots += "● "
        else:
            dots += "○ "
    st.caption(f"Name {st.session_state.challenge_idx + 1} of {len(challenges)}:  {dots}")

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # SECTION 2: INTRO — Why Some Names Never Left
    # ══════════════════════════════════════════════════════════════

    st.markdown("### 🏠 Why Some Names Never Left")
    st.markdown(
        """
        Could you pronounce all of those? Probably not — and that's the point.
        
        In 2023, **41% of all baby names** in the Anglosphere are at least 5x more 
        popular in one country than anywhere else. They're culturally locked — 
        and some countries lock harder than others.
        """
    )

    # Bar chart: % of locked names per country
    st.markdown("#### Which Countries Keep Their Names the Most?")

    country_pct = []
    for country in data_2023["max_country"].unique():
        country_data = data_2023[data_2023["max_country"] == country]
        total = country_data["name"].nunique()
        locked = country_data[country_data["countryness"] >= 5]["name"].nunique()
        if total > 0:
            country_pct.append({"Country": country, "% Locked": round(locked / total * 100, 1)})

    country_pct_df = sorted(country_pct, key=lambda x: x["% Locked"], reverse=True)

    fig_locked = go.Figure()
    fig_locked.add_trace(go.Bar(
        x=[c["Country"] for c in country_pct_df],
        y=[c["% Locked"] for c in country_pct_df],
        marker_color=[COUNTRY_COLORS.get(c["Country"], "#7C9FD6") for c in country_pct_df],
        text=[f"{c['% Locked']}%" for c in country_pct_df],
        textposition="outside",
        textfont=dict(size=13, color="#4A5568"),
    ))
    fig_locked.update_layout(
        **CHART_LAYOUT,
        title=None,
        yaxis_title="% of Names Culturally Locked (countryness ≥ 5)",
        height=400,
        showlegend=False,
    )
    st.plotly_chart(fig_locked, use_container_width=True)

    # Example names per country
    st.markdown("#### 🎵 The Local Collection")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div style="background: #F0FFF4; border-radius: 10px; padding: 14px; margin-bottom: 10px;">
                <div style="font-weight: 700;">🏴 Northern Ireland (65% locked)</div>
                <div style="color: #718096; font-size: 0.9em;">Eireann · Roisé · Dáithí · Ruadhán · Cianan</div>
            </div>
            <div style="background: #F0FFF4; border-radius: 10px; padding: 14px; margin-bottom: 10px;">
                <div style="font-weight: 700;">🇮🇪 Ireland (55% locked)</div>
                <div style="color: #718096; font-size: 0.9em;">Naoise · Sadhbh · Iarla · Laoise · Aoibhínn</div>
            </div>
            <div style="background: #F0FFF4; border-radius: 10px; padding: 14px; margin-bottom: 10px;">
                <div style="font-weight: 700;">🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland (52% locked)</div>
                <div style="color: #718096; font-size: 0.9em;">Innes · Ruairidh · Munro · Murdo</div>
            </div>
            <div style="background: #F0FFF4; border-radius: 10px; padding: 14px; margin-bottom: 10px;">
                <div style="font-weight: 700;">🇳🇿 New Zealand (36% locked)</div>
                <div style="color: #718096; font-size: 0.9em;">Kauri · Manaia · Ardie · Nikau</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div style="background: #EEF2FF; border-radius: 10px; padding: 14px; margin-bottom: 10px;">
                <div style="font-weight: 700;">🇨🇦 Canada (36% locked)</div>
                <div style="color: #718096; font-size: 0.9em;">Édouard · Éloi · Ludovic · Frédérique</div>
            </div>
            <div style="background: #EEF2FF; border-radius: 10px; padding: 14px; margin-bottom: 10px;">
                <div style="font-weight: 700;">🇺🇸 USA (44% locked)</div>
                <div style="color: #718096; font-size: 0.9em;">Kaylani · Anahi · Tadeo · Itzel</div>
            </div>
            <div style="background: #EEF2FF; border-radius: 10px; padding: 14px; margin-bottom: 10px;">
                <div style="font-weight: 700;">🏴󠁧󠁢󠁷󠁬󠁳󠁿 England & Wales (35% locked)</div>
                <div style="color: #718096; font-size: 0.9em;">Ffion · Barney · Isla-rose · Tommy-lee</div>
            </div>
            <div style="background: #EEF2FF; border-radius: 10px; padding: 14px; margin-bottom: 10px;">
                <div style="font-weight: 700;">🇦🇺 Australia (23% locked)</div>
                <div style="color: #718096; font-size: 0.9em;">Narelle · Zali · Bronte</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        "So **why** do these names stay locked? We found three main reasons:"
    )

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # SECTION 3: REASONS WHY
    # ══════════════════════════════════════════════════════════════

    # ─── Reason 1: Pronunciation Wall ─────────────────────────────
    st.markdown("### 🗣️ Reason 1: The Pronunciation Wall")
    st.markdown(
        "The most powerful predictor of whether a name stays locked is simple: "
        "**can outsiders read it?**"
    )

    # Declan vs Niamh
    st.markdown("#### Two Irish Names. Two Fates.")

    col_dec, col_niamh = st.columns(2)
    with col_dec:
        st.markdown(
            """
            <div style="background: #E8F4FD; border: 2px solid #A8E6C8; border-radius: 12px;
                        padding: 20px; text-align: center;">
                <div style="font-size: 2em; font-weight: 800; color: #4A5568;">Declan</div>
                <div style="font-size: 0.9em; color: #718096; margin: 4px 0;">"DECK-lin" ✅ Easy to read</div>
                <div style="font-size: 2.5em; font-weight: 800; color: #A8E6C8; margin: 8px 0;">2.5</div>
                <div style="font-size: 0.85em; color: #718096;">countryness → Gone global</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_niamh:
        st.markdown(
            """
            <div style="background: #FFF5F5; border: 2px solid #F5B7C5; border-radius: 12px;
                        padding: 20px; text-align: center;">
                <div style="font-size: 2em; font-weight: 800; color: #4A5568;">Niamh</div>
                <div style="font-size: 0.9em; color: #718096; margin: 4px 0;">"NEEV" ❌ Impossible to guess</div>
                <div style="font-size: 2.5em; font-weight: 800; color: #F5B7C5; margin: 8px 0;">28</div>
                <div style="font-size: 0.85em; color: #718096;">countryness → Stayed home</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")

    # Orthographic complexity
    st.markdown("#### It's Not Just Sound — It's How It LOOKS")
    st.markdown(
        "If a name *looks* impossible on paper, parents in other countries won't even attempt it. "
        "The letter-to-sound mismatch creates a visual wall:"
    )

    complexity_data = {
        "Name": ["Liam", "Declan", "Niamh", "Sadhbh", "Caoilfhionn"],
        "Letters": [4, 6, 5, 6, 11],
        "Actual Sounds": [4, 6, 3, 3, 5],
        "Mismatch": ["None — what you see is what you say", "None — readable", "5 letters → 3 sounds", "6 letters → 3 sounds!", "11 letters → 5 sounds!!"],
        "Countryness": [1.5, 2.5, 28, 905, 2974],
        "Fate": ["🌍 Global", "🌍 Global", "🏠 Locked", "🔒 Very locked", "🔒 Extremely locked"],
    }
    st.dataframe(complexity_data, use_container_width=True, hide_index=True)

    st.markdown(
        """
        **The pattern:** Names where letters = sounds (Liam, Declan) go global.
        Names where letters ≠ sounds (Sadhbh, Caoilfhionn) stay locked.
        The bigger the mismatch, the higher the countryness.
        """
    )

    # Name length vs countryness
    st.markdown("#### Longer Names = More Locked")

    fig_length = go.Figure()
    fig_length.add_trace(go.Bar(
        x=["3-4 letters", "5-6 letters", "7-8 letters", "9-10 letters", "11+ letters"],
        y=[64, 81, 82, 122, 205],
        marker_color=["#A8E6C8", "#A8D8F0", "#F5D68A", "#F5C878", "#F5B7C5"],
        text=["64", "81", "82", "122", "205"],
        textposition="outside",
        textfont=dict(size=13, color="#4A5568"),
    ))
    fig_length.update_layout(
        **CHART_LAYOUT,
        title=None,
        yaxis_title="Avg Countryness Score",
        xaxis_title="Name Length",
        height=350,
        showlegend=False,
    )
    st.plotly_chart(fig_length, use_container_width=True)

    st.info(
        "💡 Names with 11+ letters have **3x higher countryness** than short names. "
        "Complexity = barrier."
    )

    st.markdown("---")

    # ─── Reason 2: Culture & Tradition ────────────────────────────
    st.markdown("### ✝️ Reason 2: Culture & Tradition")
    st.markdown(
        "Even when a name has a perfectly pronounceable equivalent in English, "
        "communities choose the **local form** — because the form IS the identity."
    )

    # Patrick vs Pádraig
    st.markdown("#### Same Saint. Different Name. Different Fate.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div style="background: #F0F8FF; border-radius: 10px; padding: 16px; text-align: center;">
                <div style="color: #A8E6C8; font-size: 0.8em; font-weight: 600;">GLOBAL VERSION</div>
                <div style="font-size: 1.4em; font-weight: 700; margin: 6px 0;">Patrick</div>
                <div style="font-size: 1.8em; font-weight: 800; color: #A8E6C8;">~2</div>
                <div style="color: #718096; font-size: 0.8em;">countryness — everywhere</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div style="text-align: center; padding-top: 25px;">
                <div style="font-size: 2.5em;">⚡</div>
                <div style="font-size: 0.85em; color: #718096; margin-top: 4px;">Same person.<br>Same meaning.<br>Different identity.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div style="background: #FFF5F5; border-radius: 10px; padding: 16px; text-align: center;">
                <div style="color: #F5B7C5; font-size: 0.8em; font-weight: 600;">LOCAL VERSION</div>
                <div style="font-size: 1.4em; font-weight: 700; margin: 6px 0;">Pádraig</div>
                <div style="font-size: 1.8em; font-weight: 800; color: #F5B7C5;">343</div>
                <div style="color: #718096; font-size: 0.8em;">countryness — locked in Ireland</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")

    more_saints = {
        "English (Global)": ["Patrick (~2)", "Kieran (1.4)", "Brendan (4.7)", "Bridget (~3)"],
        "Gaelic (Locked)": ["Pádraig (343)", "Ciarán (24)", "Breandán (—)", "Brigid (6)"],
    }
    st.dataframe(more_saints, use_container_width=True, hide_index=True)

    st.markdown(
        "**Choosing Pádraig over Patrick is a cultural statement.** "
        "It says: *I belong to this place, this language, this tradition.* "
        "The pronunciation wall is real — but sometimes staying locked is a **choice**."
    )

    st.markdown("---")

    # ─── Reason 3: Political Identity ─────────────────────────────
    st.markdown("### 🏴 Reason 3: Political Identity")
    st.markdown(
        "If pronunciation and tradition were the only factors, all Celtic countries "
        "would behave the same. But they don't. Look at **Northern Ireland vs Ireland**:"
    )

    # NI vs Ireland divergence chart
    ni_data = df[
        (df["max_country"].isin(["Northern Ireland", "Ireland"]))
        & (df["countryness"] > 100)
    ].groupby(["year", "max_country"])["name"].nunique().reset_index()
    ni_data.columns = ["year", "country", "high_identity_names"]

    fig_ni = px.line(
        ni_data,
        x="year",
        y="high_identity_names",
        color="country",
        color_discrete_map={
            "Northern Ireland": "#9FE6C8",
            "Ireland": "#F5B7C5",
        },
        markers=True,
    )
    fig_ni.update_layout(
        **CHART_LAYOUT,
        title="High-Identity Names (countryness > 100) Over Time",
        xaxis_title="Year",
        yaxis_title="Number of Highly Distinct Names",
        legend_title=None,
        height=400,
    )
    st.plotly_chart(fig_ni, use_container_width=True)

    col_ni, col_irl = st.columns(2)
    with col_ni:
        st.markdown(
            """
            <div style="background: #E6FFF5; border-left: 4px solid #A8E6C8; 
                        border-radius: 8px; padding: 16px;">
                <div style="font-weight: 700; color: #059669;">🏴 Northern Ireland</div>
                <div style="font-size: 1.8em; font-weight: 800; color: #059669;">+38%</div>
                <div style="color: #718096; font-size: 0.9em;">
                    47 → 65 high-identity names (1997–2021)<br>
                    Getting MORE distinct while everyone converges
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_irl:
        st.markdown(
            """
            <div style="background: #FFF5F5; border-left: 4px solid #F5B7C5; 
                        border-radius: 8px; padding: 16px;">
                <div style="font-weight: 700; color: #e63946;">🇮🇪 Ireland</div>
                <div style="font-size: 1.8em; font-weight: 800; color: #e63946;">−52%</div>
                <div style="color: #718096; font-size: 0.9em;">
                    71 → 34 high-identity names (1997–2021)<br>
                    Same heritage — opposite response
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.info(
        "💡 **Same Gaelic heritage. Opposite response.** In Northern Ireland, "
        "naming a child in Gaelic is tied to the Irish language movement and "
        "post-Troubles cultural identity. It's not just tradition — it's a political act."
    )

    st.markdown("---")

    # ─── Reason 3b: Active Cultural Revival ───────────────────────
    st.markdown("### 📜 Reason 4: Active Cultural Revival")
    st.markdown(
        "It's not just old names surviving — communities are actively **inventing** "
        "brand-new names designed to never leave."
    )

    revival_data = {
        "Name": ["Iarla", "Siún", "Cadain", "Siomha", "Caragh", "Aibhlinn", "Bradan", "Breagha", "Doireann", "Saorla"],
        "First Appeared": [2015, 2013, 2017, 2017, 2021, 2018, 2016, 2018, 2020, 2012],
        "Country": ["Ireland", "Ireland", "N. Ireland", "Ireland", "Ireland", "N. Ireland", "N. Ireland", "Scotland", "Ireland", "N. Ireland"],
        "Countryness": [815, 713, 702, 547, 532, 465, 458, 446, 422, 374],
    }
    st.dataframe(revival_data, use_container_width=True, hide_index=True)

    st.markdown(
        "**85 brand-new high-identity Celtic names** created since 2010. "
        "None of these existed in the data before — they're freshly minted "
        "cultural markers, designed with Gaelic orthography that outsiders can't read."
    )

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # SECTION 4: DATA FACTS
    # ══════════════════════════════════════════════════════════════

    st.markdown("### 📊 The Numbers Behind the Wall")

    # 3.2% vs 30.2% chart
    st.markdown("#### Gaelic Spelling = Cultural Lock")

    fig_gaelic = go.Figure()
    fig_gaelic.add_trace(go.Bar(
        x=["Names that ESCAPED Ireland", "Names that STAYED"],
        y=[3.2, 30.2],
        marker_color=["#A8E6C8", "#F5B7C5"],
        text=["3.2%", "30.2%"],
        textposition="outside",
        textfont=dict(size=16, color="#4A5568"),
    ))
    fig_gaelic.update_layout(
        **CHART_LAYOUT,
        title="% of Names with Gaelic Orthography (bh, dh, gh, mh, aoi)",
        yaxis_title="Percentage",
        height=350,
        showlegend=False,
    )
    st.plotly_chart(fig_gaelic, use_container_width=True)

    st.markdown(
        "Of **126** Irish names that escaped to other countries, only **3.2%** had Gaelic spelling. "
        "Of **86** that stayed locked, **30.2%** did. A **10x difference** — and a **7.4x cultural lock factor**."
    )

    # Three borders table
    st.markdown("#### Three Linguistic Borders Within One Language")
    border_data = {
        "Border": ["🟣 Gaelic ↔ Anglophone", "🔵 Francophone ↔ Anglophone", "🟢 Hispanic ↔ Anglophone"],
        "Locked (can't cross)": ["Sadhbh, Caoilfhionn, Niamh, Aoife", "Frédérique, Océanne, Laurianne", "Almost none!"],
        "Escaped (crossed)": ["Declan, Ronan, Connor, Liam", "Very few escape", "Santiago, Diego, Carlos, Isabella"],
        "Wall Strength": ["Hard wall 🧱 (7.4x lock)", "Hard wall but fading 📉 (−79% since 1997)", "No wall! 🌍 (phonetically accessible)"],
    }
    st.dataframe(border_data, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Culture > Geography
    st.markdown("#### Culture > Geography")
    st.markdown(
        "If distance were the barrier, Australia would be the most distinct. "
        "It's not. **Cultural tradition trumps physical isolation.**"
    )

    country_cn = data_2023.groupby("max_country")["countryness"].mean().sort_values(ascending=True).reset_index()

    fig_geo = go.Figure()
    fig_geo.add_trace(go.Bar(
        x=country_cn["countryness"],
        y=country_cn["max_country"],
        orientation="h",
        marker_color=[COUNTRY_COLORS.get(c, "#7C9FD6") for c in country_cn["max_country"]],
        text=[f"{v:.1f}" for v in country_cn["countryness"]],
        textposition="outside",
    ))
    fig_geo.update_layout(
        **CHART_LAYOUT,
        title="Avg Countryness by Country (2023)",
        height=350,
        xaxis_title="Avg Countryness Score (Higher = More Distinct)",
    )
    st.plotly_chart(fig_geo, use_container_width=True)

    st.info(
        "💡 **Ireland** (right next to the UK) remains 5x more distinct than **Australia** "
        "(on the other side of the planet but culturally connected via media). "
        "A non-English linguistic tradition matters more than distance."
    )
