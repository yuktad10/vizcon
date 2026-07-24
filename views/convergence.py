"""
Global Playlist — The Global Playlist Tab
Part of "Now Playing: The Name Playlist" baby naming data visualization project.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import os
import pandas as pd
import numpy as np
from utils.data_loader import load_metrics, load_summary
from utils.charts import CHART_LAYOUT, COLORS, COUNTRY_COLORS


# ─── Color Theme ─────────────────────────────────────────────────────────────
PURPLE = "#667eea"
SAGE = "#7c9a8e"
CORAL = "#c99e85"
DARK_BG = "#1a1a2e"
CARD_BG = "#f8f9fa"
TEXT_DARK = "#2d3436"
TEXT_MUTED = "#636e72"


# ─── Load the detailed per-country data for sparklines ────────────────────────
@st.cache_data
def load_all_names():
    """Load the full per-country yearly dataset for the Track Lookup sparklines."""
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "all-names-long.csv.gz")
    if not os.path.exists(path):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "all-names-long.csv.gz")
    return pd.read_csv(path)


# ─── Shared Styles ────────────────────────────────────────────────────────────
def inject_styles():
    st.markdown("""
    <style>
        .stTabs [data-baseweb="tab-list"] {
            position: sticky;
            top: 0;
            z-index: 999;
            background: #F0F8FF;
        }
        .block-container {
            max-width: 1200px;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        .chart-entry {
            display: flex;
            align-items: center;
            padding: 0.75rem 1.2rem;
            margin: 0.35rem 0;
            border-radius: 12px;
            background: white;
            border: 1px solid #eee;
            transition: all 0.2s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }
        .chart-entry:hover {
            transform: translateX(4px);
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.15);
            border-color: #667eea;
        }
        .chart-rank {
            font-size: 1.3rem;
            font-weight: 800;
            color: #667eea;
            min-width: 40px;
            text-align: center;
        }
        .chart-rank.top3 {
            color: white;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 50%;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
        }
        .chart-info {
            flex: 1;
            margin-left: 1rem;
        }
        .chart-name {
            font-size: 1.1rem;
            font-weight: 700;
            color: #2d3436;
        }
        .chart-meta {
            font-size: 0.8rem;
            color: #636e72;
            margin-top: 2px;
        }
        .chart-score {
            text-align: right;
            padding-left: 1rem;
        }
        .chart-score .value {
            font-size: 1.1rem;
            font-weight: 700;
            color: #7c9a8e;
        }
        .chart-score .label {
            font-size: 0.7rem;
            color: #636e72;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .insight-card {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 0.75rem 0;
            border: 1px solid #eee;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            transition: transform 0.2s ease;
        }
        .insight-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        }
        .insight-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        .insight-title {
            font-size: 1rem;
            font-weight: 700;
            color: #2d3436;
            margin-bottom: 0.4rem;
        }
        .insight-detail {
            font-size: 0.85rem;
            color: #636e72;
            line-height: 1.5;
        }
        .insight-stat {
            font-size: 1.5rem;
            font-weight: 800;
            color: #667eea;
            margin: 0.3rem 0;
        }
        .search-result {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            border: 1px solid #eee;
            box-shadow: 0 4px 16px rgba(0,0,0,0.06);
            margin-top: 1rem;
        }
        .search-result h3 {
            margin: 0 0 0.5rem 0;
            color: #2d3436;
        }
        .badge-global {
            display: inline-block;
            background: linear-gradient(135deg, #7c9a8e, #5a7d6f);
            color: white;
            padding: 0.3rem 0.9rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        .badge-local {
            display: inline-block;
            background: linear-gradient(135deg, #c99e85, #b8876d);
            color: white;
            padding: 0.3rem 0.9rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        .badge-neutral {
            display: inline-block;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 0.3rem 0.9rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        .section-divider {
            margin: 3rem 0 2rem 0;
            padding: 1.2rem 1.5rem;
            background: linear-gradient(90deg, #f8f9fa, white);
            border-left: 4px solid #667eea;
            border-radius: 0 12px 12px 0;
        }
        .section-divider h2 {
            margin: 0;
            font-size: 1.4rem;
            color: #2d3436;
        }
        .section-divider p {
            margin: 0.3rem 0 0 0;
            color: #636e72;
            font-size: 0.9rem;
        }
        .country-pills {
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
            margin-top: 0.5rem;
        }
        .country-pill {
            background: #f0f2f5;
            color: #2d3436;
            padding: 0.25rem 0.7rem;
            border-radius: 12px;
            font-size: 0.78rem;
            font-weight: 500;
        }
        .track-lookup-box {
            background: linear-gradient(135deg, #EEF2FF, #F0FFF4);
            border-radius: 16px;
            padding: 2rem;
            border: 1px solid #E2E8F0;
            margin-bottom: 1rem;
        }
        .vinyl-spin {
            display: inline-block;
            animation: spin 3s linear infinite;
        }
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        /* Override Streamlit input focus border */
        .stTextInput > div > div > input:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 1px #667eea !important;
        }
        .stTextInput > div > div {
            border-color: #ddd !important;
        }
        .stTextInput > div > div:focus-within {
            border-color: #667eea !important;
            box-shadow: 0 0 0 1px #667eea !important;
        }
    </style>
    """, unsafe_allow_html=True)


# ─── Section: Track Lookup (Song-Themed) ─────────────────────────────────────
def render_track_lookup(df_metrics):
    """Track Lookup — styled like a music streaming track page. Data from summary-1997-2023.csv."""
    
    # Load the summary dataset (pre-aggregated 1997-2023)
    df_summary = load_summary()
    
    # Section heading — plain text, no box
    st.markdown("""
    <h2 style="margin: 0 0 4px 0;">🔍 Track Lookup</h2>
    <p style="font-size: 1.1em; font-weight: 600; color: #2D3748; margin: 0 0 4px 0;">
        🎵 Every name is a track. What are you listening to?
    </p>
    <p style="font-size: 0.85em; color: #636e72; margin: 0 0 1rem 0;">
        Search any name to see its streaming stats, chart history, and which nations have it on repeat.
    </p>
    """, unsafe_allow_html=True)

    search_name = st.text_input(
        "Search a track",
        placeholder="e.g. Olivia, Liam, Isabella, Nevaeh...",
        key="name_search_input",
        label_visibility="collapsed",
    )

    if search_name:
        search_name_clean = search_name.strip().capitalize()

        # ─── Look up in summary (aggregated 1997-2023) ─────────────
        match = df_summary[df_summary["name"].str.upper() == search_name_clean.upper()]

        if match.empty:
            st.markdown(f"""
            <div style="background: white; border-radius: 16px; padding: 3rem; border: 1px solid #eee;
                        box-shadow: 0 4px 16px rgba(0,0,0,0.06); margin-top: 1rem; text-align:center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎵</div>
                <p style="font-size:1.2rem; color:#2d3436; font-weight: 600;">
                    No track found for "<b>{search_name_clean}</b>"
                </p>
                <p style="font-size:0.9rem; color:#636e72;">
                    This track isn't in our Anglosphere charts (1997-2023). Try another!
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            row = match.iloc[0]

            # ─── Stats from summary sheet ──────────────────────────
            total_streams = int(row["total_babies_with_name"])
            countryness_val = row["countryness"]
            max_countries = int(row["countries_using_name"])
            peak_country = row["max_country"]
            sex_emoji = "♀️" if row["sex"] == "F" else "♂️"
            freq_in_max = int(row["freq_in_max_country"])
            prop_in_max = row["prop_in_max_country"]
            avg_outside = row["average_usage_outside_country"]

            # Chart rank (rank by countryness — lower = more global)
            df_summary["_rank"] = df_summary["countryness"].rank(method="min")
            rank_val = int(df_summary[df_summary["name"].str.upper() == search_name_clean.upper()]["_rank"].iloc[0])
            total_names = len(df_summary)

            # ─── Countries list from all-names-long ─────────────────
            try:
                df_all = load_all_names()
                name_detail = df_all[df_all["name"].str.upper() == search_name_clean.upper()]
                if not name_detail.empty:
                    countries_list = sorted(name_detail["country"].unique().tolist())
                else:
                    countries_list = [peak_country]
            except Exception:
                countries_list = [peak_country]

            # ─── Classification (from summary countryness) ─────────
            if countryness_val < 5:
                badge_text = "🎧 Global Hit"
                badge_class = "badge-global"
                verdict = "This track topped charts worldwide — a cross-border anthem with no single home country."
                verdict_emoji = "🔥"
                genre_tag = "Genre: Global Pop"
            elif countryness_val < 10:
                badge_text = "🌍 Leaning Global"
                badge_class = "badge-global"
                verdict = "This track is concentrating in one market but still gets play across borders."
                verdict_emoji = "📈"
                genre_tag = "Genre: Crossover"
            elif countryness_val < 100:
                badge_text = "📻 Regional Radio Hit"
                badge_class = "badge-neutral"
                verdict = "This track clearly belongs to one country — it gets some airplay abroad but home is where the heart is."
                verdict_emoji = "📡"
                genre_tag = "Genre: Regional"
            elif countryness_val < 1000:
                badge_text = "💿 Underground Classic"
                badge_class = "badge-local"
                verdict = "A cult favorite that barely exists outside its home country — deep local roots."
                verdict_emoji = "🎸"
                genre_tag = "Genre: Indie Local"
            else:
                badge_text = "🚫 Cultural Exclusive"
                badge_class = "badge-local"
                verdict = "This track is a one-country anthem — it exists almost exclusively in one nation's playlist."
                verdict_emoji = "🏠"
                genre_tag = "Genre: Heritage"

            # ─── Track title + badge + verdict ─────────────────────
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f9f5ff, #f3eeff); border-radius: 16px; padding: 2rem; border: 1px solid #e8ddf5;
                        box-shadow: 0 4px 16px rgba(102,126,234,0.08); margin-top: 1rem;">
                <div style="margin-bottom:0.5rem;">
                    <span style="font-size: 2rem; font-weight: 800; letter-spacing: -0.5px;">{search_name_clean} {sex_emoji}</span>
                    <span class="{badge_class}" style="margin-left: 0.8rem;">{badge_text}</span>
                </div>
                <p style="color:#636e72; margin: 0 0 0.3rem 0; font-size: 0.85rem; font-style: italic;">{genre_tag}</p>
                <p style="color:#2d3436; margin-bottom:0; font-size: 1.05rem;">
                    {verdict_emoji} {verdict}
                </p>
            </div>
            """, unsafe_allow_html=True)

            # ─── Stats grid using st.columns ───────────────────────
            st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""
                <div style="text-align:center; padding:1rem; background:#fff0f3; border-radius:12px; border:1px solid #fcd5df;">
                    <div style="font-size:0.65rem; color:#636e72; text-transform:uppercase; letter-spacing:1px;">🎧 Total Streams</div>
                    <div style="font-size:1.6rem; font-weight:800; color:#667eea; margin:0.3rem 0;">{total_streams:,}</div>
                    <div style="font-size:0.7rem; color:#636e72;">babies (1997-2023)</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div style="text-align:center; padding:1rem; background:#fff0f3; border-radius:12px; border:1px solid #fcd5df;">
                    <div style="font-size:0.65rem; color:#636e72; text-transform:uppercase; letter-spacing:1px;">🌍 Listeners</div>
                    <div style="font-size:1.6rem; font-weight:800; color:#7c9a8e; margin:0.3rem 0;">{max_countries}/8</div>
                    <div style="font-size:0.7rem; color:#636e72;">countries charting</div>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div style="text-align:center; padding:1rem; background:#fff0f3; border-radius:12px; border:1px solid #fcd5df;">
                    <div style="font-size:0.65rem; color:#636e72; text-transform:uppercase; letter-spacing:1px;">📊 Chart Rank</div>
                    <div style="font-size:1.6rem; font-weight:800; color:#2d3436; margin:0.3rem 0;">#{rank_val:,}</div>
                    <div style="font-size:0.7rem; color:#636e72;">of {total_names:,} tracks</div>
                </div>
                """, unsafe_allow_html=True)

            # ─── Extra stats row ───────────────────────────────────
            st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:#eef6ff; border-radius:10px; padding:0.8rem 1.2rem; margin:0.5rem 0; border:1px solid #d4e8fc;">
                <span style="font-size:0.78rem; color:#636e72;">🎯 Countryness: </span><span style="font-weight:700;">{countryness_val:.2f}</span>
                <span style="margin:0 1rem; color:#ddd;">|</span>
                <span style="font-size:0.78rem; color:#636e72;">🏠 Home Market: </span><span style="font-weight:700;">{peak_country}</span>
            </div>
            """, unsafe_allow_html=True)

            # ─── Countries list ────────────────────────────────────
            country_pills_html = " ".join(
                f'<span style="background:#e8edf3; color:#2d3436; padding:0.3rem 0.8rem; border-radius:12px; font-size:0.78rem; font-weight:500; margin:0.2rem; display:inline-block;">{c}{" 👑" if c == peak_country else ""}</span>'
                for c in countries_list[:8]
            )
            st.markdown(f"""
            <div style="margin-top:0.8rem; background:#eef6ff; border-radius:12px; padding:1rem 1.2rem; border:1px solid #d4e8fc;">
                <div style="font-size:0.8rem; color:#636e72; margin-bottom:0.5rem;">
                    🔊 Streaming in {len(countries_list)} markets <span style="font-size:0.7rem;">(👑 = #1 market)</span>
                </div>
                <div>{country_pills_html}</div>
            </div>
            """, unsafe_allow_html=True)



    else:
        # Empty state
        st.markdown("""
        <div style="text-align: center; padding: 2.5rem 1rem; color: #636e72;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎤</div>
            <p style="font-size: 1.05rem; margin: 0 0 0.5rem 0; font-weight: 500;">Drop a name in the search bar above</p>
            <p style="font-size: 0.85rem; margin: 0; color: #636e72;">
                Try <b>Isabella</b> (global #1 hit), <b>Raewyn</b> (underground NZ classic), or <b>your own name</b>
            </p>
        </div>
        """, unsafe_allow_html=True)


# ─── Section: Media Eras ──────────────────────────────────────────────────────
def render_media_eras(df):
    st.markdown("---")
    st.markdown("""
    <h2 style="margin: 0 0 4px 0;">🔊 Turning Up The Volume</h2>
    <p style="font-size: 0.95em; color: #636e72; margin: 0 0 1.5rem 0;">
        From silent films to TikTok, each media revolution amplified names across borders. The louder the shared signal, the more our playlists sync up.
    </p>
    """, unsafe_allow_html=True)

    # Define media eras
    eras = [
        {"era": "Radio", "years": "1997–2000", "start": 1997, "end": 2000, "icon": "📻", "note": "Local DJs ruled"},
        {"era": "Early TV", "years": "2001–2005", "start": 2001, "end": 2005, "icon": "📺", "note": "Friends & soaps"},
        {"era": "Cable & DVD", "years": "2006–2009", "start": 2006, "end": 2009, "icon": "📀", "note": "Global franchises"},
        {"era": "Internet", "years": "2010–2014", "start": 2010, "end": 2014, "icon": "💻", "note": "YouTube era"},
        {"era": "Social Media", "years": "2015–2019", "start": 2015, "end": 2019, "icon": "📱", "note": "Viral culture"},
        {"era": "Streaming", "years": "2020–2023", "start": 2020, "end": 2023, "icon": "🎧", "note": "Same playlist"},
    ]

    # Calculate avg countryness per era
    era_stats = []
    for era in eras:
        era_data = df[(df["year"] >= era["start"]) & (df["year"] <= era["end"])]
        avg_c = era_data["countryness"].mean() if not era_data.empty else 0
        era_stats.append({**era, "avg_countryness": avg_c})

    first_val = era_stats[0]["avg_countryness"]
    last_val = era_stats[-1]["avg_countryness"]
    drop_pct = ((first_val - last_val) / first_val) * 100

    # Build clean timeline using components.html
    from streamlit.components.v1 import html as st_html

    era_cards = ""
    for i, era in enumerate(era_stats):
        # Color: coral for high (distinct) → sage for low (synced)
        if era["avg_countryness"] > 20:
            color = "#c99e85"
        elif era["avg_countryness"] > 16:
            color = "#667eea"
        else:
            color = "#7c9a8e"

        era_cards += f"""
        <div style="text-align:center; flex:1; min-width:100px; background:#fefefe; border-radius:12px; padding:1.2rem 0.5rem; border:1px solid #f0ebe3;">
            <div style="font-size:1.8rem; margin-bottom:0.4rem;">{era['icon']}</div>
            <div style="font-size:0.82rem; font-weight:700; color:#2d3436;">{era['era']}</div>
            <div style="font-size:0.7rem; color:#999; margin:0.2rem 0 0.6rem 0;">{era['years']}</div>
            <div style="font-size:1.5rem; font-weight:800; color:{color};">{era['avg_countryness']:.1f}</div>
            <div style="font-size:0.65rem; color:#999; font-style:italic; margin-top:0.2rem;">{era['note']}</div>
        </div>
        """

    timeline_html = f"""
    <html>
    <body style="margin:0; padding:0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
        <div style="background: linear-gradient(135deg, #fffbf0, #fff8e8); border-radius:16px; padding:1.5rem; border:1px solid #f0e6d0;">
            <!-- Era cards -->
            <div style="display:flex; align-items:stretch; justify-content:space-between; gap:0.6rem;">
                {era_cards}
            </div>

            <!-- Summary line -->
            <div style="text-align:center; margin-top:1.2rem; padding:0.8rem 1rem; background:#fefefe; border-radius:10px; border:1px solid #f0ebe3;">
                <p style="font-size:0.88rem; color:#2d3436; margin:0;">
                    📉 Cultural distinctness dropped from <b>{first_val:.1f}</b> to <b>{last_val:.1f}</b> — 
                    a <span style="color:#667eea; font-weight:800;">{drop_pct:.0f}%</span> sync-up across the Anglosphere.
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    st_html(timeline_html, height=330)


# ─── Section: Global Top 6 ────────────────────────────────────────────────────
def render_leaderboard(df):
    st.markdown("---")
    st.markdown("""
    <h2 style="margin: 0 0 4px 0;">🎧 Now Streaming Worldwide</h2>
    <p style="font-size: 0.95em; color: #636e72; margin: 0 0 1.5rem 0;">
        The six biggest cross-border anthems — names that charted equally in all 8 nations. No single home country. Pure global hits.
    </p>
    """, unsafe_allow_html=True)

    # Load summary for aggregated data
    df_summary = load_summary()
    
    # Top 6 from summary (used in all 8 countries, lowest countryness)
    top6 = (
        df_summary[df_summary["countries_using_name"] == 8]
        .nsmallest(6, "countryness")
        .reset_index(drop=True)
    )

    from streamlit.components.v1 import html as st_html

    # Light/pastel poster themes — easy on eyes, text clearly visible
    poster_themes = [
        {"bg": "linear-gradient(135deg, #3d2c5e, #5b3f8f)", "accent": "#f0c040", "icon": "🎤", "label": "#1 HIT"},
        {"bg": "linear-gradient(135deg, #1e3a5f, #2c5282)", "accent": "#63b3ed", "icon": "🎸", "label": "CHART BREAKER"},
        {"bg": "linear-gradient(135deg, #1a4a42, #276b5d)", "accent": "#68d391", "icon": "🎹", "label": "GLOBAL SOUND"},
        {"bg": "linear-gradient(135deg, #4a2040, #6b3060)", "accent": "#f687b3", "icon": "🎧", "label": "ON REPEAT"},
        {"bg": "linear-gradient(135deg, #3d3020, #5c4a2a)", "accent": "#ecc94b", "icon": "🎷", "label": "CLASSIC"},
        {"bg": "linear-gradient(135deg, #1a3650, #2a5070)", "accent": "#90cdf4", "icon": "🎵", "label": "RISING STAR"},
    ]

    taglines = [
        "The #1 hit everywhere, all the time",
        "Breaking borders at record speed",
        "Strength in every single market",
        "Quietly conquering the charts",
        "A timeless classic on repeat",
        "The smoothest global groove",
    ]

    # Build poster data as JSON for the interactive component
    poster_data = []
    for i, row in top6.iterrows():
        poster_data.append({
            "name": row["name"],
            "sex": row["sex"],
            "total": int(row["total_babies_with_name"]),
            "score": f"{row['countryness']:.3f}",
            "country": row["max_country"],
            "theme": poster_themes[i],
            "tagline": taglines[i],
            "rank": i + 1,
        })

    # Build the full interactive HTML — posters + now playing bar
    posters_html = ""
    for p in poster_data:
        theme = p["theme"]
        sex_emoji = "♀️" if p["sex"] == "F" else "♂️"
        total_fmt = f"{p['total']:,}"

        posters_html += f"""
        <div class="poster" onclick="playTrack('{p['name']}', '{total_fmt}', '{p['country']}', '{p['score']}', '{theme['bg']}', '{theme['accent']}')" 
             style="flex:1; min-width:150px; max-width:185px; cursor:pointer; transition:transform 0.2s;"
             onmouseover="this.style.transform='translateY(-4px)'"
             onmouseout="this.style.transform='none'">
            <div style="background:{theme['bg']}; border-radius:14px; padding:1.2rem 0.8rem; text-align:center; box-shadow:0 4px 16px rgba(0,0,0,0.12); position:relative; overflow:hidden; height:250px;">
                <div style="position:absolute; top:8px; left:8px; background:rgba(255,255,255,0.15); border-radius:6px; padding:2px 7px;">
                    <span style="font-size:0.55rem; color:rgba(255,255,255,0.9); font-weight:700; letter-spacing:1px;">{theme['label']}</span>
                </div>
                <div style="position:absolute; top:8px; right:8px; background:rgba(0,0,0,0.2); border-radius:6px; padding:2px 7px;">
                    <span style="font-size:0.7rem; color:white; font-weight:700;">#{p['rank']}</span>
                </div>
                <div style="font-size:2rem; margin:0.8rem 0 0.3rem 0;">{theme['icon']}</div>
                <div style="font-size:1.4rem; font-weight:900; color:white; letter-spacing:-0.5px; margin:0.2rem 0;">{p['name']}</div>
                <div style="font-size:0.6rem; color:rgba(255,255,255,0.65); font-style:italic; margin-bottom:0.7rem;">"{p['tagline']}"</div>
                <div style="background:rgba(0,0,0,0.2); border-radius:8px; padding:0.5rem 0.4rem; margin:0 0.2rem;">
                    <div style="font-size:1.05rem; font-weight:800; color:{theme['accent']};">{total_fmt}</div>
                    <div style="font-size:0.55rem; color:rgba(255,255,255,0.5); text-transform:uppercase; letter-spacing:0.5px;">total plays • 8 countries</div>
                </div>
                <div style="margin-top:0.5rem;">
                    <span style="background:rgba(255,255,255,0.15); padding:0.2rem 0.6rem; border-radius:10px; font-size:0.68rem; color:white; font-weight:600;">Score: {p['score']}</span>
                </div>
            </div>
        </div>
        """

    # First track data for initial state
    first = poster_data[0]
    first_total = f"{first['total']:,}"

    full_html = f"""
    <html>
    <head>
        <style>
            .poster {{ user-select: none; }}
            .poster:active {{ transform: scale(0.97) !important; }}
        </style>
    </head>
    <body style="margin:0; padding:0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
        <!-- Posters -->
        <div style="display:flex; gap:0.7rem; flex-wrap:wrap; justify-content:center;">
            {posters_html}
        </div>

        <!-- Now Playing Bar -->
        <div id="now-playing" style="background:linear-gradient(90deg, #1a1a2e, #2d2d44); border-radius:12px; padding:0.8rem 1.2rem; margin-top:1.2rem; display:flex; align-items:center; gap:1rem; box-shadow:0 4px 16px rgba(0,0,0,0.2);">
            <!-- Album art -->
            <div id="np-art" style="width:44px; height:44px; border-radius:8px; background:linear-gradient(135deg, #3d2c5e, #5b3f8f); display:flex; align-items:center; justify-content:center; flex-shrink:0; transition:background 0.4s;">
                <span id="np-letter" style="color:white; font-size:1.2rem; font-weight:800;">{first['name'][0]}</span>
            </div>
            <!-- Track info -->
            <div style="flex:1; min-width:0;">
                <div style="display:flex; align-items:center; gap:0.4rem;">
                    <span id="np-name" style="font-size:0.85rem; font-weight:700; color:white;">{first['name']}</span>
                    <span id="np-country" style="color:rgba(255,255,255,0.5); font-weight:400; font-size:0.75rem;">• {first['country']}</span>
                </div>
                <div id="np-stats" style="font-size:0.68rem; color:rgba(255,255,255,0.5);">{first_total} plays • 8 countries</div>
                <!-- Progress bar -->
                <div style="margin-top:0.4rem; height:4px; background:rgba(255,255,255,0.1); border-radius:2px; overflow:hidden;">
                    <div id="np-progress" style="height:100%; width:0%; background:linear-gradient(90deg, #667eea, #7c9a8e); border-radius:2px; transition:width 3s linear;"></div>
                </div>
            </div>
            <!-- Play controls -->
            <div style="display:flex; align-items:center; gap:0.8rem; flex-shrink:0;">
                <span style="color:rgba(255,255,255,0.4); font-size:0.9rem;">⏮</span>
                <span id="np-play-btn" style="color:white; font-size:1.4rem; cursor:pointer;" onclick="togglePlay()">▶</span>
                <span style="color:rgba(255,255,255,0.4); font-size:0.9rem;">⏭</span>
            </div>
            <!-- Now Playing label -->
            <div style="flex-shrink:0; text-align:right;">
                <div style="font-size:0.55rem; color:#667eea; text-transform:uppercase; letter-spacing:1.5px; font-weight:600;">Now Playing</div>
                <div id="np-rank" style="font-size:0.6rem; color:rgba(255,255,255,0.4);">Global #1</div>
            </div>
        </div>

        <!-- Hidden audio element -->
        <audio id="np-audio" loop>
            <source src="data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAIA+AAACABAAZGdOaQ==" type="audio/wav">
        </audio>

        <script>
            let isPlaying = false;
            
            function playTrack(name, total, country, score, bg, accent) {{
                // Update Now Playing bar
                document.getElementById('np-name').textContent = name;
                document.getElementById('np-letter').textContent = name[0];
                document.getElementById('np-country').textContent = '• ' + country;
                document.getElementById('np-stats').textContent = total + ' plays • 8 countries';
                document.getElementById('np-rank').textContent = 'Score: ' + score;
                
                // Reset and animate progress bar
                const progress = document.getElementById('np-progress');
                progress.style.transition = 'none';
                progress.style.width = '0%';
                setTimeout(() => {{
                    progress.style.transition = 'width 8s linear';
                    progress.style.width = '100%';
                }}, 50);
                
                // Update play button
                document.getElementById('np-play-btn').textContent = '⏸';
                isPlaying = true;
            }}
            
            function togglePlay() {{
                const btn = document.getElementById('np-play-btn');
                const progress = document.getElementById('np-progress');
                if (isPlaying) {{
                    btn.textContent = '▶';
                    progress.style.animationPlayState = 'paused';
                    isPlaying = false;
                }} else {{
                    btn.textContent = '⏸';
                    progress.style.transition = 'width 8s linear';
                    progress.style.width = '100%';
                    isPlaying = true;
                }}
            }}

            // Auto-play first track animation on load
            setTimeout(() => {{
                document.getElementById('np-progress').style.transition = 'width 8s linear';
                document.getElementById('np-progress').style.width = '100%';
                document.getElementById('np-play-btn').textContent = '⏸';
                isPlaying = true;
            }}, 500);
        </script>
    </body>
    </html>
    """

    st_html(full_html, height=450)

    # Explanation below — plain text, no box
    st.markdown("""
    <p style="font-size:0.85rem; color:#2d3436; margin-top:1rem; margin-bottom:0.3rem; line-height:1.7;">
        Ranked by countryness score (lower = more equally spread across nations). A name with fewer total babies can rank higher 
        if it's perfectly balanced — being a small hit <i>everywhere</i> beats being a massive hit in just one place.
    </p>
    <p style="font-size:0.82rem; color:#2d3436; line-height:1.6; margin-top:0.3rem;">
        Think of it like a song that charts at #20 in every country simultaneously vs one that's #1 in one country but unknown elsewhere — 
        the first one is the true global anthem. A score of 1.0 means perfectly equal usage across all 8 nations.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("---")


# ─── Section: One-Hit Wonders ──────────────────────────────────────────────────
def render_convergence_timeline(df):
    st.markdown("""
    <h2 style="margin: 0 0 4px 0;">💥 One-Hit Wonders</h2>
    <p style="font-size: 0.95em; color: #2d3436; margin: 0 0 0.3rem 0;">
        The fastest rise, the shortest life. Pop culture creates instant global sync — but these names burn bright and fade fast.
    </p>
    <p style="font-size: 0.85em; color: #636e72; margin: 0 0 1.5rem 0;">
        👇 Click on any emoji to reveal the story behind each name
    </p>
    """, unsafe_allow_html=True)

    from streamlit.components.v1 import html as st_html

    # Interactive horizontal timeline + quiz
    timeline_quiz_html = """
    <html>
    <head>
    <style>
        body { margin:0; padding:1rem 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
        
        .timeline-container {
            position: relative;
            padding: 2rem 1rem;
        }
        
        .timeline-line {
            position: absolute;
            top: 35px;
            left: 5%;
            right: 5%;
            height: 3px;
            background: linear-gradient(90deg, #667eea, #c99e85);
            border-radius: 2px;
        }
        
        .timeline-markers {
            display: flex;
            justify-content: space-between;
            padding: 0 3%;
            position: relative;
        }
        
        .marker {
            display: flex;
            flex-direction: column;
            align-items: center;
            cursor: pointer;
            transition: transform 0.2s;
            z-index: 2;
        }
        
        .marker:hover { transform: scale(1.2); }
        .marker.active { transform: scale(1.3); }
        
        .marker-emoji {
            font-size: 2rem;
            background: white;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 12px rgba(0,0,0,0.1);
            border: 3px solid #eee;
            transition: border-color 0.3s, box-shadow 0.3s;
        }
        
        .marker.active .marker-emoji {
            border-color: #667eea;
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        }
        
        .marker-year {
            font-size: 0.7rem;
            color: #999;
            margin-top: 0.4rem;
            font-weight: 600;
        }
        
        .marker-name {
            font-size: 0.75rem;
            color: #2d3436;
            font-weight: 700;
            margin-top: 0.2rem;
        }
        
        .info-box {
            margin-top: 1.5rem;
            padding: 1.5rem;
            background: linear-gradient(135deg, #f9f5ff, #f3eeff);
            border-radius: 14px;
            border: 1px solid #e8ddf5;
            display: none;
            animation: fadeIn 0.3s ease;
        }
        
        .info-box.visible { display: block; }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .info-title { font-size: 1.1rem; font-weight: 800; color: #2d3436; margin-bottom: 0.3rem; }
        .info-trigger { font-size: 0.85rem; color: #4a5568; font-style: italic; margin-bottom: 0.8rem; }
        .info-stats { display: flex; gap: 2rem; flex-wrap: wrap; }
        .info-stat { text-align: center; }
        .info-stat-value { font-size: 1.3rem; font-weight: 800; }
        .info-stat-label { font-size: 0.65rem; color: #999; text-transform: uppercase; letter-spacing: 0.5px; }
        .status-badge { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 8px; font-size: 0.72rem; font-weight: 600; margin-top: 0.8rem; }
        
        .quiz-section {
            margin-top: 2.5rem;
            padding: 1.5rem;
            background: linear-gradient(135deg, #f0f4f8, #e8ecf0);
            border-radius: 14px;
            border: 1px solid #d8dee4;
        }
        
        .quiz-title { font-size: 1rem; font-weight: 700; color: #2d3436; margin-bottom: 0.5rem; }
        .quiz-subtitle { font-size: 0.82rem; color: #636e72; margin-bottom: 1rem; }
        
        .quiz-options {
            display: flex;
            gap: 0.6rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
        }
        
        .quiz-btn {
            padding: 0.5rem 1.2rem;
            border-radius: 10px;
            border: 2px solid #ddd;
            background: white;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.2s;
        }
        
        .quiz-btn:hover { border-color: #667eea; background: #f5f0ff; }
        .quiz-btn.correct { border-color: #7c9a8e; background: #e8f5e9; color: #2e7d32; }
        .quiz-btn.wrong { border-color: #e63946; background: #ffebee; color: #c62828; }
        
        .quiz-result {
            display: none;
            padding: 1rem;
            border-radius: 10px;
            font-size: 0.85rem;
            line-height: 1.6;
        }
        .quiz-result.visible { display: block; }
    </style>
    </head>
    <body>
        <div class="timeline-container">
            <div class="timeline-line"></div>
            <div class="timeline-markers">
                <div class="marker" onclick="showInfo(0)">
                    <div class="marker-emoji">🎤</div>
                    <div class="marker-year">1999</div>
                    <div class="marker-name">Britney</div>
                </div>
                <div class="marker" onclick="showInfo(1)">
                    <div class="marker-emoji">💥</div>
                    <div class="marker-year">2001</div>
                    <div class="marker-name">Nevaeh</div>
                </div>
                <div class="marker" onclick="showInfo(2)">
                    <div class="marker-emoji">🐉</div>
                    <div class="marker-year">2011</div>
                    <div class="marker-name">Khaleesi</div>
                </div>
                <div class="marker" onclick="showInfo(3)">
                    <div class="marker-emoji">⚔️</div>
                    <div class="marker-year">2011</div>
                    <div class="marker-name">Arya</div>
                </div>
                <div class="marker" onclick="showInfo(4)">
                    <div class="marker-emoji">❄️</div>
                    <div class="marker-year">2013</div>
                    <div class="marker-name">Elsa</div>
                </div>
            </div>
        </div>
        
        <div id="info-box" class="info-box">
            <div id="info-content"></div>
        </div>
        
        <div class="quiz-section">
            <div class="quiz-title">🎯 Can You Guess Who Survived?</div>
            <div class="quiz-subtitle">Two names were triggered by the same show (Game of Thrones). One dropped 81% from peak. The other only 31%. Which one is still charting strong?</div>
            <div class="quiz-options">
                <div class="quiz-btn" id="q1-a" onclick="checkQuiz('q1', 'a')">Khaleesi</div>
                <div class="quiz-btn" id="q1-b" onclick="checkQuiz('q1', 'b')">Arya</div>
            </div>
            <div id="q1-result" class="quiz-result"></div>
            
            <div style="margin-top:1.5rem; padding-top:1rem; border-top:1px solid #d8dee4;">
                <div class="quiz-title">🎵 Evergreen or One-Hit?</div>
                <div class="quiz-subtitle">James has been a top name since 1997. In 27 years, how much did it drop from its peak?</div>
                <div class="quiz-options">
                    <div class="quiz-btn" id="q2-a" onclick="checkQuiz('q2', 'a')">↓55% (lost half)</div>
                    <div class="quiz-btn" id="q2-b" onclick="checkQuiz('q2', 'b')">↓35% (steady decline)</div>
                    <div class="quiz-btn" id="q2-c" onclick="checkQuiz('q2', 'c')">↓15% (barely moved)</div>
                </div>
                <div id="q2-result" class="quiz-result"></div>
            </div>
        </div>
        
        <script>
            const data = [
                {
                    name: "Britney", emoji: "🎤",
                    trigger: "Britney Spears drops '...Baby One More Time' — every girl wants to be Britney",
                    peak: "3,083", peakYear: "2000", now: "217", fall: "93",
                    status: "❌ Basically gone", statusColor: "#e63946", statusBg: "#ffebee"
                },
                {
                    name: "Nevaeh", emoji: "💥",
                    trigger: "'Heaven' spelled backwards goes viral after an MTV interview",
                    peak: "7,455", peakYear: "2007", now: "3,053", fall: "59",
                    status: "📉 Fading slowly", statusColor: "#c99e85", statusBg: "#fff3e0"
                },
                {
                    name: "Khaleesi", emoji: "🐉",
                    trigger: "Game of Thrones S1 — parents name babies after a fictional dragon queen",
                    peak: "606", peakYear: "2018", now: "422", fall: "30",
                    status: "⚠️ Fading with the show", statusColor: "#e9c46a", statusBg: "#fffde7"
                },
                {
                    name: "Arya", emoji: "⚔️",
                    trigger: "GoT's fierce warrior + real Sanskrit/Persian roots (meaning noble)",
                    peak: "3,913", peakYear: "2019", now: "2,691", fall: "31",
                    status: "✅ Still charting", statusColor: "#7c9a8e", statusBg: "#e8f5e9"
                },
                {
                    name: "Elsa", emoji: "❄️",
                    trigger: "Frozen is released — 'Let It Go' is inescapable",
                    peak: "1,999", peakYear: "2014", now: "373", fall: "81",
                    status: "❌ Frozen out", statusColor: "#e63946", statusBg: "#ffebee"
                }
            ];
            
            function showInfo(idx) {
                document.querySelectorAll('.marker').forEach(m => m.classList.remove('active'));
                document.querySelectorAll('.marker')[idx].classList.add('active');
                
                const d = data[idx];
                const box = document.getElementById('info-box');
                box.className = 'info-box visible';
                
                document.getElementById('info-content').innerHTML =
                    '<div class="info-title">' + d.emoji + ' ' + d.name + '</div>' +
                    '<div class="info-trigger">"' + d.trigger + '"</div>' +
                    '<div class="info-stats">' +
                        '<div class="info-stat"><div class="info-stat-value" style="color:#667eea;">' + d.peak + '</div><div class="info-stat-label">Peak (' + d.peakYear + ')</div></div>' +
                        '<div style="display:flex; align-items:center; font-size:1.2rem; color:#ccc;">→</div>' +
                        '<div class="info-stat"><div class="info-stat-value" style="color:#2d3436;">' + d.now + '</div><div class="info-stat-label">Now (2023)</div></div>' +
                        '<div class="info-stat"><div class="info-stat-value" style="color:' + d.statusColor + ';">↓' + d.fall + '%</div><div class="info-stat-label">Drop</div></div>' +
                    '</div>' +
                    '<div class="status-badge" style="background:' + d.statusBg + '; color:' + d.statusColor + ';">' + d.status + '</div>';
            }
            
            function checkQuiz(quiz, answer) {
                const resultDiv = document.getElementById(quiz + '-result');
                
                if (quiz === 'q1') {
                    const btnA = document.getElementById('q1-a');
                    const btnB = document.getElementById('q1-b');
                    
                    if (answer === 'b') {
                        btnB.className = 'quiz-btn correct';
                        btnA.className = 'quiz-btn wrong';
                        resultDiv.innerHTML = '<b>✅ Arya</b> is still going strong (↓31%)! Unlike "Khaleesi" which is purely a TV reference, "Arya" has real linguistic roots in Sanskrit (meaning noble) and Persian — it sounds like a natural name, so it outlived its source material.';
                        resultDiv.style.background = '#e8f5e9';
                        resultDiv.style.color = '#2e7d32';
                    } else {
                        btnA.className = 'quiz-btn wrong';
                        btnB.className = 'quiz-btn correct';
                        resultDiv.innerHTML = '❌ Actually, <b>Arya</b> survived better! Khaleesi is fading because it only references GoT. Arya has real Sanskrit/Persian roots — names that <i>sound</i> natural outlast names that only <i>reference</i> something.';
                        resultDiv.style.background = '#ffebee';
                        resultDiv.style.color = '#c62828';
                    }
                    resultDiv.className = 'quiz-result visible';
                }
                
                if (quiz === 'q2') {
                    const btnA = document.getElementById('q2-a');
                    const btnB = document.getElementById('q2-b');
                    const btnC = document.getElementById('q2-c');
                    
                    btnA.className = 'quiz-btn wrong';
                    btnB.className = 'quiz-btn wrong';
                    btnC.className = 'quiz-btn wrong';
                    
                    if (answer === 'c') {
                        btnC.className = 'quiz-btn correct';
                        resultDiv.innerHTML = '✅ Correct! <b>James</b> only dropped ~15% in 27 years — from 35,413 to 15,918. That is an evergreen classic. Compare that to Britney (↓93%) or Elsa (↓81%). Classic names do not ride trends — they ARE the trend.';
                        resultDiv.style.background = '#e8f5e9';
                        resultDiv.style.color = '#2e7d32';
                    } else {
                        btnC.className = 'quiz-btn correct';
                        resultDiv.innerHTML = '❌ Nope! James barely budged — only ↓15% over 27 years (35,413 → 15,918). Evergreen classics do not ride cultural waves. They ARE the baseline. Britney fell 93% but James just keeps going.';
                        resultDiv.style.background = '#ffebee';
                        resultDiv.style.color = '#c62828';
                    }
                    resultDiv.className = 'quiz-result visible';
                }
            }
            
            // Don't show anything until user clicks
        </script>
    </body>
    </html>
    """

    st_html(timeline_quiz_html, height=900)

    st.markdown("""
    <p style="font-size:0.85rem; color:#2d3436; margin-top:1rem; line-height:1.7;">
        Pop culture is the fastest way to make a name sync across countries — a single movie, show, or song can put a name on every nation's playlist overnight. 
        But the same force that creates instant global recognition also creates disposable names. The louder the debut, the faster the fade.
    </p>
    <p style="font-size:0.82rem; color:#2d3436; line-height:1.6; margin-top:0.3rem;">
        The exception? Names like Arya that tap into deeper phonetic appeal and outlast their source material.
        A name that <i>sounds</i> right survives. A name that only <i>references</i> something fades with it.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("---")


# ─── Section: Import/Export Economy ─────────────────────────────────────────────
def render_import_export(df):
    """The Record Label Map — animated particle flow (proportion-based)."""
    
    st.markdown("""
    <h2 style="margin: 0 0 4px 0;">💿 The Record Label Map</h2>
    <p style="font-size: 0.95em; color: #2d3436; margin: 0 0 0.3rem 0;">
        Every hit has a label behind it. We mapped which countries <b>produce</b> the names and which ones <b>play</b> them.
    </p>
    <p style="font-size: 0.82em; color: #636e72; margin: 0 0 1.5rem 0;">
        Origin = where a name is most concentrated (proportion-adjusted). More particles = more names exported.
    </p>
    """, unsafe_allow_html=True)
    
    from streamlit.components.v1 import html as st_html
    
    # Compute flows using proportion-based max_country from summary
    df_summary = load_summary()
    df_all = load_all_names()
    
    # Names in 5+ countries
    name_countries = df_all.groupby("name")["country"].nunique().reset_index()
    name_countries.columns = ["name", "n_countries"]
    global_names_list = name_countries[name_countries["n_countries"] >= 5]["name"].tolist()
    
    # Get max_country (proportion-based origin)
    df_global_summary = df_summary[df_summary["name"].isin(global_names_list)][["name", "max_country"]].copy()
    
    # Get countries each name appears in
    df_global_long = df_all[df_all["name"].isin(global_names_list)]
    name_country_set = df_global_long.groupby("name")["country"].apply(set).reset_index()
    name_country_set.columns = ["name", "countries"]
    
    df_merged = df_global_summary.merge(name_country_set, on="name")
    
    name_map = {
        "USA": "USA", "England and Wales": "England", "Canada": "Canada",
        "Australia": "Australia", "Scotland": "Scotland", "Ireland": "Ireland",
        "Northern Ireland": "N.Ireland", "New Zealand": "NZ"
    }
    
    flow_rows = []
    for _, row in df_merged.iterrows():
        src = name_map.get(row["max_country"], row["max_country"])
        for country in row["countries"]:
            tgt = name_map.get(country, country)
            if tgt != src:
                flow_rows.append({"source": src, "target": tgt})
    
    import pandas as pd
    flow_df = pd.DataFrame(flow_rows)
    flow_counts = flow_df.groupby(["source", "target"]).size().reset_index(name="n_names")
    flow_counts = flow_counts[flow_counts["n_names"] >= 400].sort_values("n_names", ascending=False)
    
    # Export/import totals
    all_flows = pd.DataFrame(flow_rows)
    all_flow_counts = all_flows.groupby(["source", "target"]).size().reset_index(name="n_names")
    export_totals = all_flow_counts.groupby("source")["n_names"].sum().sort_values(ascending=False)
    import_totals = all_flow_counts.groupby("target")["n_names"].sum().sort_values(ascending=False)
    
    # Build JS data
    js_flows = ", ".join([f"[\'{row.source}\', \'{row.target}\', {row.n_names}]" for _, row in flow_counts.iterrows()])
    
    # Sources for left side (top 5 exporters)
    top_sources = export_totals.head(5)
    js_sources = ", ".join([
        f"{{ name: \'{c}\', exports: {v} }}"
        for c, v in top_sources.items()
    ])
    
    # All targets for right side
    js_targets = ", ".join([
        f"{{ name: \'{c}\', imports: {v} }}"
        for c, v in import_totals.items()
    ])
    
    max_flow = int(flow_counts["n_names"].max())
    
    # Stats
    total_exp = int(export_totals.sum())
    usa_pct = int(round(export_totals.get("USA", 0) / total_exp * 100))
    can_pct = int(round(export_totals.get("Canada", 0) / total_exp * 100))
    eng_pct = int(round(export_totals.get("England", 0) / total_exp * 100))
    top_importer = import_totals.idxmax()
    
    flow_html = f"""
    <html>
    <head>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: transparent; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }}
        .container {{ position: relative; background: linear-gradient(135deg, #f8f9fa, #eef2ff); border-radius: 16px; border: 1px solid #e2e8f0; overflow: hidden; }}
        canvas {{ display: block; }}
        
        .header-row {{
            display: flex;
            justify-content: space-between;
            padding: 14px 20px 0;
            position: absolute;
            top: 0; left: 0; right: 0;
            z-index: 2;
        }}
        .header-label {{
            font-size: 10px; font-weight: 700;
            text-transform: uppercase; letter-spacing: 1.5px;
            padding: 4px 10px; border-radius: 6px;
        }}
        .header-export {{ color: #9b59b6; background: rgba(155,89,182,0.1); }}
        .header-import {{ color: #1abc9c; background: rgba(26,188,156,0.1); }}
        
        .stats-panel {{
            position: absolute;
            bottom: 12px; left: 50%; transform: translateX(-50%);
            display: flex; gap: 18px;
            background: rgba(255,255,255,0.92);
            border-radius: 10px; padding: 8px 18px;
            border: 1px solid #e2e8f0; z-index: 2;
        }}
        .stat-item {{ text-align: center; }}
        .stat-value {{ font-size: 13px; font-weight: 800; }}
        .stat-label {{ font-size: 9px; color: #636e72; text-transform: uppercase; letter-spacing: 0.5px; }}
    </style>
    </head>
    <body>
        <div class="container">
            <div class="header-row">
                <div class="header-label header-export">🎙️ Producers (Origin)</div>
                <div style="font-size:10px; color:#636e72; padding-top:4px;">proportion-based: where names are most concentrated</div>
                <div class="header-label header-import">📻 Players (Absorb)</div>
            </div>
            <canvas id="canvas"></canvas>
            <div class="stats-panel">
                <div class="stat-item">
                    <div class="stat-value" style="color:#3498db;">{usa_pct}%</div>
                    <div class="stat-label">from USA</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" style="color:#9b59b6;">{can_pct}%</div>
                    <div class="stat-label">from Canada</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" style="color:#e74c3c;">{eng_pct}%</div>
                    <div class="stat-label">from England</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" style="color:#1abc9c;">{top_importer}</div>
                    <div class="stat-label">#1 importer</div>
                </div>
            </div>
        </div>
        <script>
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            const W = canvas.width = canvas.parentElement.clientWidth;
            const H = canvas.height = 480;
            
            const nodeColors = {{
                'USA': '#3498db', 'Canada': '#9b59b6', 'England': '#e74c3c',
                'NZ': '#e91e63', 'Scotland': '#1abc9c', 'Ireland': '#f39c12',
                'Australia': '#2ecc71', 'N.Ireland': '#00bcd4'
            }};
            
            // Left side: producers (positioned by export volume)
            const sourceData = [{js_sources}];
            const maxExport = sourceData[0].exports;
            const sources = {{}};
            sourceData.forEach((s, i) => {{
                sources[s.name] = {{
                    x: W * 0.08,
                    y: H * 0.18 + (H * 0.7) * (i / (sourceData.length - 1 || 1)),
                    color: nodeColors[s.name],
                    exports: s.exports
                }};
            }});
            
            // Right side: players (positioned by import volume)
            const targetData = [{js_targets}];
            const maxImport = targetData[0].imports;
            const targets = {{}};
            targetData.forEach((t, i) => {{
                targets[t.name] = {{
                    x: W * 0.92,
                    y: H * 0.14 + (H * 0.76) * (i / (targetData.length - 1 || 1)),
                    color: nodeColors[t.name],
                    imports: t.imports
                }};
            }});
            
            const flows = [{js_flows}];
            const maxFlow = {max_flow};
            
            let particles = [];
            
            function createParticle(srcNode, tgtNode, color) {{
                const mx = (srcNode.x + tgtNode.x) / 2;
                const my = (srcNode.y + tgtNode.y) / 2;
                const dx = tgtNode.x - srcNode.x;
                const dy = tgtNode.y - srcNode.y;
                const len = Math.sqrt(dx*dx + dy*dy) || 1;
                const offset = (Math.random() - 0.5) * 50;
                const nx = -dy / len * offset;
                const ny = dx / len * offset;
                
                return {{
                    sx: srcNode.x, sy: srcNode.y,
                    tx: tgtNode.x, ty: tgtNode.y,
                    cx: mx + nx, cy: my + ny,
                    t: Math.random(),
                    speed: 0.002 + Math.random() * 0.003,
                    color: color,
                    size: 1.5 + Math.random() * 2,
                    alpha: 0.5 + Math.random() * 0.5
                }};
            }}
            
            function initParticles() {{
                particles = [];
                flows.forEach(([src, tgt, vol]) => {{
                    const srcNode = sources[src];
                    const tgtNode = targets[tgt];
                    if (!srcNode || !tgtNode) return;
                    const count = Math.max(1, Math.round((vol / maxFlow) * 10));
                    for (let i = 0; i < count; i++) {{
                        particles.push(createParticle(srcNode, tgtNode, srcNode.color));
                    }}
                }});
            }}
            
            function bezier(t, sx, sy, cx, cy, tx, ty) {{
                return {{
                    x: (1-t)*(1-t)*sx + 2*(1-t)*t*cx + t*t*tx,
                    y: (1-t)*(1-t)*sy + 2*(1-t)*t*cy + t*t*ty
                }};
            }}
            
            function drawNode(node, name, isSource, maxVal) {{
                const val = isSource ? node.exports : node.imports;
                const size = 6 + 16 * (val / maxVal);
                
                const grad = ctx.createRadialGradient(node.x, node.y, 0, node.x, node.y, size + 5);
                grad.addColorStop(0, node.color + '30');
                grad.addColorStop(1, 'transparent');
                ctx.beginPath();
                ctx.arc(node.x, node.y, size + 5, 0, Math.PI * 2);
                ctx.fillStyle = grad;
                ctx.fill();
                
                ctx.beginPath();
                ctx.arc(node.x, node.y, size, 0, Math.PI * 2);
                ctx.fillStyle = node.color;
                ctx.fill();
                ctx.strokeStyle = 'rgba(255,255,255,0.8)';
                ctx.lineWidth = 1.5;
                ctx.stroke();
                
                ctx.fillStyle = '#2d3436';
                ctx.font = 'bold 10px Arial';
                ctx.textAlign = isSource ? 'left' : 'right';
                const lx = isSource ? node.x + size + 8 : node.x - size - 8;
                ctx.fillText(name, lx, node.y);
                
                ctx.fillStyle = '#636e72';
                ctx.font = '9px Arial';
                const valText = isSource ? (val/1000).toFixed(1) + 'k out' : (val/1000).toFixed(1) + 'k in';
                ctx.fillText(valText, lx, node.y + 12);
            }}
            
            function draw() {{
                ctx.clearRect(0, 0, W, H);
                
                // Faint paths
                flows.forEach(([src, tgt, vol]) => {{
                    const s = sources[src]; const t = targets[tgt];
                    if (!s || !t) return;
                    ctx.beginPath();
                    ctx.moveTo(s.x, s.y);
                    ctx.quadraticCurveTo((s.x+t.x)/2, (s.y+t.y)/2, t.x, t.y);
                    ctx.strokeStyle = 'rgba(0,0,0,0.03)';
                    ctx.lineWidth = 1 + 2*(vol/maxFlow);
                    ctx.stroke();
                }});
                
                // Particles
                particles.forEach(p => {{
                    const pos = bezier(p.t, p.sx, p.sy, p.cx, p.cy, p.tx, p.ty);
                    ctx.beginPath();
                    ctx.arc(pos.x, pos.y, p.size, 0, Math.PI * 2);
                    ctx.globalAlpha = p.alpha;
                    ctx.fillStyle = p.color;
                    ctx.fill();
                    ctx.globalAlpha = 1;
                    
                    p.t += p.speed;
                    if (p.t > 1) {{ p.t = 0; p.speed = 0.002 + Math.random() * 0.003; }}
                }});
                
                // Nodes
                Object.entries(sources).forEach(([name, node]) => drawNode(node, name, true, maxExport));
                Object.entries(targets).forEach(([name, node]) => drawNode(node, name, false, maxImport));
                
                requestAnimationFrame(draw);
            }}
            
            initParticles();
            draw();
        </script>
    </body>
    </html>
    """
    
    st_html(flow_html, height=540)
    
    st.markdown("""
    <p style="font-size:0.82rem; color:#2d3436; margin-top:1rem; line-height:1.6;">
        Using proportion-adjusted origin: <b style="color:#3498db;">USA</b> still leads, but <b style="color:#9b59b6;">Canada</b> is the #2 producer — 
        the cultural gateway where global names concentrate most. The import side is highly democratic — every country absorbs roughly equally.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("---")


# ─── Section: Insights Infographic ────────────────────────────────────────────
def render_insights():
    st.markdown("""
    <div class="section-divider">
        <h2>💡 Liner Notes</h2>
        <p>Six key discoveries about what makes a name travel — the science behind the Global Playlist</p>
    </div>
    """, unsafe_allow_html=True)

    insights = [
        {
            "icon": "✂️",
            "title": "Shorter Names Travel Better",
            "stat": "5.8 vs 6.5",
            "detail": "Global names average 5.8 characters vs 6.5 for local names. Compact names cross linguistic borders more easily — they're the pop singles of the naming world.",
            "color": PURPLE,
        },
        {
            "icon": "♀️",
            "title": "Female Names Are More Global",
            "stat": "58%",
            "detail": "58% of the most global names are female. Women's names travel further, possibly because they share more cross-cultural phonetic patterns like soft vowel endings.",
            "color": SAGE,
        },
        {
            "icon": "📉",
            "title": "Names Are Converging",
            "stat": "−27%",
            "detail": "Average countryness dropped 27% from 1997 to 2023. The Anglosphere is slowly syncing its naming playlist — streaming culture may be the DJ.",
            "color": CORAL,
        },
        {
            "icon": "🇨🇦",
            "title": "Canada: The Cultural Gateway",
            "stat": "47%",
            "detail": "47% of global top names peak in Canada first. As the most multicultural Anglosphere nation, Canada acts as the gateway where international names first break through.",
            "color": PURPLE,
        },
        {
            "icon": "🎬",
            "title": "Pop Culture Drives Global Names",
            "stat": "Isabella",
            "detail": "Twilight's Isabella, Frozen's Elsa, Harry Potter's Luna — pop culture creates instant global recognition. These names jumped from local to worldwide in a single media cycle.",
            "color": SAGE,
        },
        {
            "icon": "🔤",
            "title": "Vowel Endings Cross Borders",
            "stat": "-na, -ia, -ah",
            "detail": "The most global names end in soft vowels: -na, -ah, -ia for girls; -on, -en, -an for boys. These phonetic patterns feel natural across English dialects worldwide.",
            "color": CORAL,
        },
    ]

    # Render in 2-column grid
    for i in range(0, len(insights), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(insights):
                ins = insights[i + j]
                with col:
                    st.markdown(f"""
                    <div class="insight-card">
                        <div class="insight-icon">{ins['icon']}</div>
                        <div class="insight-title">{ins['title']}</div>
                        <div class="insight-stat" style="color:{ins['color']};">{ins['stat']}</div>
                        <div class="insight-detail">{ins['detail']}</div>
                    </div>
                    """, unsafe_allow_html=True)


# ─── Main Render Function ─────────────────────────────────────────────────────
def render():
    inject_styles()

    # ─── Header ───────────────────────────────────────────────────
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #EEF2FF, #E8F4FD, #F0FFF4); 
                    border-radius: 16px; padding: 50px 30px; text-align: center; 
                    margin-bottom: 20px; border: 1px solid #E2E8F0;">
            <h1 style="font-size: 2.8em; font-weight: 800; color: #2D3748; margin: 0 0 12px 0;">
                🎧 The Global Playlist
            </h1>
            <p style="font-size: 1.5em; color: #4A5568; max-width: 650px; margin: 0 auto; line-height: 1.7;">
                Featuring the Greatest Hits.<br>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # Load data
    df = load_metrics()

    # Section order: Track Lookup first (interactive), then the rest
    render_track_lookup(df)
    render_media_eras(df)
    render_leaderboard(df)
    render_convergence_timeline(df)
    render_import_export(df)
    render_insights()


# Allow running standalone
if __name__ == "__main__":
    render()
