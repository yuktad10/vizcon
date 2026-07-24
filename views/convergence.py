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


# ─── Section: Global Top 6 ────────────────────────────────────────────────────
def render_leaderboard(df):
    st.markdown("---")
    st.markdown("""
    <h2 style="margin: 0 0 4px 0;">🏆 The Global 6</h2>
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

    # Render as a vertical countdown strip using components.html
    from streamlit.components.v1 import html as st_html

    tracks_html = ""
    for i, row in top6.iterrows():
        rank = i + 1
        sex_emoji = "♀️" if row["sex"] == "F" else "♂️"
        total = f"{int(row['total_babies_with_name']):,}"
        score = f"{row['countryness']:.3f}"
        
        # Alternating subtle backgrounds
        bg = "#fafbfc" if rank % 2 == 0 else "white"
        
        # Rank colors
        if rank == 1:
            rank_color = "#FFD700"
            rank_icon = "🥇"
        elif rank == 2:
            rank_color = "#C0C0C0"
            rank_icon = "🥈"
        elif rank == 3:
            rank_color = "#CD7F32"
            rank_icon = "🥉"
        else:
            rank_color = "#667eea"
            rank_icon = f"#{rank}"

        # Album art square — using first letter as a stylized "cover"
        letter = row['name'][0]
        art_colors = ["#667eea", "#7c9a8e", "#c99e85", "#457b9d", "#2a9d8f", "#e9c46a"]
        art_bg = art_colors[i % len(art_colors)]

        tracks_html += f"""
        <div style="display:flex; align-items:center; padding:1rem 1.2rem; background:{bg}; border-bottom:1px solid #f0f0f0;">
            <!-- Album art square -->
            <div style="width:52px; height:52px; border-radius:8px; background:linear-gradient(135deg, {art_bg}, {art_bg}dd); display:flex; align-items:center; justify-content:center; flex-shrink:0; box-shadow:0 2px 8px {art_bg}44;">
                <span style="color:white; font-size:1.6rem; font-weight:800;">{letter}</span>
            </div>
            <!-- Track info -->
            <div style="flex:1; margin-left:1rem;">
                <div style="font-size:1.1rem; font-weight:700; color:#2d3436;">{rank_icon} {row['name']} <span style="font-weight:400; font-size:0.85rem;">{sex_emoji}</span></div>
                <div style="font-size:0.75rem; color:#636e72; margin-top:3px;">
                    {total} streams • 8 countries • Peak: {row['max_country']}
                </div>
            </div>
            <!-- Countryness score -->
            <div style="text-align:right; flex-shrink:0;">
                <div style="font-size:1.2rem; font-weight:800; color:#7c9a8e;">{score}</div>
                <div style="font-size:0.6rem; color:#999; text-transform:uppercase; letter-spacing:0.5px;">score</div>
            </div>
        </div>
        """

    countdown_html = f"""
    <html>
    <body style="margin:0; padding:0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
        <div style="border-radius:16px; overflow:hidden; border:1px solid #eee; box-shadow:0 4px 16px rgba(0,0,0,0.06);">
            <!-- Header bar -->
            <div style="background:linear-gradient(135deg, #667eea, #764ba2); padding:0.8rem 1.2rem; display:flex; align-items:center; justify-content:space-between;">
                <span style="color:white; font-weight:700; font-size:0.9rem;">🎧 TOP 6 COUNTDOWN</span>
                <span style="color:rgba(255,255,255,0.7); font-size:0.75rem;">All-Time Global Chart</span>
            </div>
            <!-- Tracks -->
            {tracks_html}
        </div>
    </body>
    </html>
    """
    st_html(countdown_html, height=460)


# ─── Section: Convergence Timeline ───────────────────────────────────────────
def render_convergence_timeline(df):
    st.markdown("""
    <div class="section-divider">
        <h2>📉 The Convergence Timeline</h2>
        <p>How naming trends across 8 nations have been syncing up like a global playlist on shuffle</p>
    </div>
    """, unsafe_allow_html=True)

    # Calculate average countryness per year
    yearly_avg = (
        df.groupby("year")["countryness"]
        .mean()
        .reset_index()
        .rename(columns={"countryness": "avg_countryness"})
    )
    yearly_avg = yearly_avg[(yearly_avg["year"] >= 1997) & (yearly_avg["year"] <= 2023)]

    # Calculate % drop
    start_val = yearly_avg["avg_countryness"].iloc[0]
    end_val = yearly_avg["avg_countryness"].iloc[-1]
    pct_drop = ((start_val - end_val) / start_val) * 100

    fig = go.Figure()

    # Main line
    fig.add_trace(go.Scatter(
        x=yearly_avg["year"],
        y=yearly_avg["avg_countryness"],
        mode="lines+markers",
        line=dict(color=PURPLE, width=3, shape="spline"),
        marker=dict(size=6, color=PURPLE),
        fill="tozeroy",
        fillcolor="rgba(102, 126, 234, 0.08)",
        name="Avg Countryness",
        hovertemplate="<b>%{x}</b><br>Avg Countryness: %{y:.2f}<extra></extra>",
    ))

    # Annotation
    mid_year = 2010
    mid_val = yearly_avg[yearly_avg["year"] == mid_year]["avg_countryness"].values
    mid_val = mid_val[0] if len(mid_val) > 0 else yearly_avg["avg_countryness"].median()

    fig.add_annotation(
        x=mid_year,
        y=mid_val,
        text=f"↓ {pct_drop:.0f}% drop in countryness<br><i>Names are converging globally</i>",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowcolor=PURPLE,
        ax=60,
        ay=-60,
        font=dict(size=12, color=PURPLE),
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor=PURPLE,
        borderwidth=1,
        borderpad=8,
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif", color=TEXT_DARK),
        xaxis=dict(
            title="Year",
            showgrid=False,
            dtick=2,
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            title="Average Countryness Score",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)",
            zeroline=False,
            tickfont=dict(size=11),
        ),
        margin=dict(l=60, r=30, t=40, b=50),
        height=420,
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True)

    # Key stats below the chart
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="text-align:center; padding:1rem; background:#fff0f3; border-radius:12px; border:1px solid #fcd5df;">
            <div style="font-size:2rem; font-weight:800; color:{PURPLE};">{start_val:.1f}</div>
            <div style="font-size:0.8rem; color:{TEXT_MUTED};">1997 Average</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="text-align:center; padding:1rem; background:#fff0f3; border-radius:12px; border:1px solid #fcd5df;">
            <div style="font-size:2rem; font-weight:800; color:{SAGE};">{end_val:.1f}</div>
            <div style="font-size:0.8rem; color:{TEXT_MUTED};">2023 Average</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="text-align:center; padding:1rem; background:#fff0f3; border-radius:12px; border:1px solid #fcd5df;">
            <div style="font-size:2rem; font-weight:800; color:{CORAL};">27%</div>
            <div style="font-size:0.8rem; color:{TEXT_MUTED};">Convergence Drop</div>
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
    render_insights()


# Allow running standalone
if __name__ == "__main__":
    render()
