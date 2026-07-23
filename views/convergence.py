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
    </style>
    """, unsafe_allow_html=True)


# ─── Section: Track Lookup (Song-Themed) ─────────────────────────────────────
def render_track_lookup(df_metrics):
    """Track Lookup — styled like a music streaming track page with aggregated 1997-2023 data."""
    st.markdown("""
    <div class="section-divider">
        <h2>🔍 Track Lookup</h2>
        <p>Look up any name — we'll pull up its track info like it's a song on your favourite streaming app</p>
    </div>
    """, unsafe_allow_html=True)

    # Search input with music-themed container
    st.markdown("""
    <div class="track-lookup-box">
        <p style="font-size: 1.1em; font-weight: 600; color: #2D3748; margin: 0 0 4px 0;">
            🎵 Every name is a track. What are you listening to?
        </p>
        <p style="font-size: 0.85em; color: #636e72; margin: 0;">
            Search any name to see its streaming stats, chart history, and which nations have it on repeat.
        </p>
    </div>
    """, unsafe_allow_html=True)

    search_name = st.text_input(
        "Search a track",
        placeholder="e.g. Olivia, Liam, Isabella, Nevaeh...",
        key="name_search_input",
        label_visibility="collapsed",
    )

    if search_name:
        search_name_clean = search_name.strip().capitalize()

        # ─── AGGREGATE across all years (1997–2023) ─────────────────
        name_all_years = df_metrics[df_metrics["name"].str.upper() == search_name_clean.upper()]

        if name_all_years.empty:
            st.markdown(f"""
            <div class="search-result" style="text-align:center; padding: 3rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎵</div>
                <p style="font-size:1.2rem; color:{TEXT_DARK}; font-weight: 600;">
                    No track found for "<b>{search_name_clean}</b>"
                </p>
                <p style="font-size:0.9rem; color:{TEXT_MUTED};">
                    This track isn't in our Anglosphere charts (1997–2023). Try another!
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Aggregated stats across all years
            total_streams = int(name_all_years["total_num_babies_w_name"].sum())
            avg_countryness = name_all_years["countryness"].mean()
            min_countryness = name_all_years["countryness"].min()
            max_countries = int(name_all_years["countries_using_name"].max())
            peak_country = name_all_years.loc[name_all_years["freq_in_max_country"].idxmax(), "max_country"]
            years_on_chart = name_all_years["year"].nunique()
            sex_val = name_all_years["sex"].mode().iloc[0]
            sex_emoji = "♀️" if sex_val == "F" else "♂️"

            # Peak year (highest total babies)
            peak_year_row = name_all_years.loc[name_all_years["total_num_babies_w_name"].idxmax()]
            peak_year = int(peak_year_row["year"])
            peak_streams = int(peak_year_row["total_num_babies_w_name"])

            # Classification based on average countryness across all years
            if avg_countryness < 2:
                badge = '<span class="badge-global">🎧 Global Hit</span>'
                verdict = "This track topped charts worldwide — a cross-border anthem heard in every corner of the Anglosphere."
                verdict_emoji = "🔥"
                genre_tag = "Genre: Global Pop"
                accent = SAGE
            elif avg_countryness > 100:
                badge = '<span class="badge-local">💿 Underground Classic</span>'
                verdict = "A cult favorite with deep roots in its home country — beloved by locals, unknown abroad."
                verdict_emoji = "🎸"
                genre_tag = "Genre: Regional Indie"
                accent = CORAL
            elif avg_countryness > 10:
                badge = '<span class="badge-neutral">📻 Regional Radio Hit</span>'
                verdict = "This track gets airplay in a few markets but hasn't broken through to the global charts yet."
                verdict_emoji = "📡"
                genre_tag = "Genre: Mid-Market"
                accent = PURPLE
            else:
                badge = '<span class="badge-global">🌍 Rising Global Track</span>'
                verdict = "On the verge of worldwide rotation — gaining listeners across multiple nations."
                verdict_emoji = "📈"
                genre_tag = "Genre: Crossover"
                accent = SAGE

            # All countries where it appeared
            countries_used = sorted(name_all_years["max_country"].unique().tolist())

            # Chart position (rank by avg countryness across all names)
            all_names_rank = (
                df_metrics.groupby("name")["countryness"]
                .mean()
                .rank(method="min")
            )
            rank_val = int(all_names_rank.get(search_name_clean, all_names_rank.get(search_name_clean.upper(), 0)))
            total_names = len(all_names_rank)

            # Country pills with peak indicator
            country_pills_html = ""
            for c in countries_used[:8]:
                is_peak = " 👑" if c == peak_country else ""
                country_pills_html += f'<span class="country-pill">{c}{is_peak}</span>'

            # ─── Render: Album Art Style Result Card ──────────────────────
            st.markdown(f"""
            <div class="search-result">
                <!-- Track title + badge -->
                <div style="display:flex; align-items:center; gap:1rem; margin-bottom:0.5rem; flex-wrap: wrap;">
                    <h2 style="margin:0; font-size: 2rem; font-weight: 800; letter-spacing: -0.5px;">{search_name_clean} {sex_emoji}</h2>
                    {badge}
                </div>
                <p style="color:{TEXT_MUTED}; margin: 0 0 0.3rem 0; font-size: 0.85rem; font-style: italic;">{genre_tag}</p>
                <p style="color:{TEXT_DARK}; margin-bottom:1.5rem; font-size: 1.05rem;">
                    {verdict_emoji} {verdict}
                </p>

                <!-- Stats grid — "streaming stats" -->
                <div style="display:grid; grid-template-columns: repeat(2, 1fr) repeat(2, 1fr); gap:1rem; margin:1.5rem 0;
                            background: linear-gradient(135deg, #f8f9fa, #fff); padding: 1.5rem; border-radius: 16px; border: 1px solid #eee;">
                    <div style="text-align:center; padding: 0.5rem;">
                        <div style="font-size:0.7rem; color:{TEXT_MUTED}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">🎧 Total Streams</div>
                        <div style="font-size:1.8rem; font-weight:800; color:{PURPLE};">{total_streams:,}</div>
                        <div style="font-size:0.7rem; color:{TEXT_MUTED};">babies named (1997–2023)</div>
                    </div>
                    <div style="text-align:center; padding: 0.5rem;">
                        <div style="font-size:0.7rem; color:{TEXT_MUTED}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">🌍 Listeners</div>
                        <div style="font-size:1.8rem; font-weight:800; color:{SAGE};">{max_countries}/8</div>
                        <div style="font-size:0.7rem; color:{TEXT_MUTED};">countries charting in</div>
                    </div>
                    <div style="text-align:center; padding: 0.5rem;">
                        <div style="font-size:0.7rem; color:{TEXT_MUTED}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">📈 Peak Year</div>
                        <div style="font-size:1.8rem; font-weight:800; color:{CORAL};">{peak_year}</div>
                        <div style="font-size:0.7rem; color:{TEXT_MUTED};">{peak_streams:,} streams that year</div>
                    </div>
                    <div style="text-align:center; padding: 0.5rem;">
                        <div style="font-size:0.7rem; color:{TEXT_MUTED}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">📊 Chart Position</div>
                        <div style="font-size:1.8rem; font-weight:800; color:{TEXT_DARK};">#{rank_val:,}</div>
                        <div style="font-size:0.7rem; color:{TEXT_MUTED};">of {total_names:,} tracks</div>
                    </div>
                </div>

                <!-- Extra stats row -->
                <div style="display:flex; gap:2rem; margin:1rem 0; padding:0.8rem 1.2rem; background: #fafbfc; border-radius:10px; flex-wrap: wrap;">
                    <div>
                        <span style="font-size:0.75rem; color:{TEXT_MUTED};">⏱️ Years on Chart:</span>
                        <span style="font-weight:700; color:{TEXT_DARK};"> {years_on_chart}</span>
                    </div>
                    <div>
                        <span style="font-size:0.75rem; color:{TEXT_MUTED};">🎯 Avg Countryness:</span>
                        <span style="font-weight:700; color:{TEXT_DARK};"> {avg_countryness:.2f}</span>
                    </div>
                    <div>
                        <span style="font-size:0.75rem; color:{TEXT_MUTED};">🏆 Best Score:</span>
                        <span style="font-weight:700; color:{TEXT_DARK};"> {min_countryness:.2f}</span>
                    </div>
                </div>

                <!-- Countries (listeners) -->
                <div style="margin-top:1rem;">
                    <div style="font-size:0.8rem; color:{TEXT_MUTED}; margin-bottom:0.4rem;">
                        🔊 Streaming in {max_countries} markets <span style="font-size:0.7rem;">(👑 = #1 market)</span>
                    </div>
                    <div class="country-pills">{country_pills_html}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ─── Chart History: Multi-country sparkline ──────────────────
            st.markdown(f"""
            <div style="margin-top: 1.5rem; padding: 0.8rem 0;">
                <p style="font-size: 0.95rem; font-weight: 600; color: {TEXT_DARK}; margin: 0;">
                    📈 Streaming History — <b>{search_name_clean}</b> across nations (1997–2023)
                </p>
                <p style="font-size: 0.78rem; color: {TEXT_MUTED}; margin: 4px 0 0 0;">
                    Each line = one country's yearly "streams" (births per 1,000)
                </p>
            </div>
            """, unsafe_allow_html=True)

            try:
                df_all = load_all_names()
                name_data = df_all[df_all["name"].str.upper() == search_name_clean.upper()]

                if not name_data.empty:
                    # Aggregate by year + country
                    trend = (
                        name_data.groupby(["year", "country"])["proportion"]
                        .sum()
                        .reset_index()
                    )

                    # Plotly multi-line chart
                    fig = go.Figure()

                    countries_in_data = sorted(trend["country"].unique())

                    # Palette
                    color_palette = [
                        "#667eea", "#7c9a8e", "#c99e85", "#e63946",
                        "#457b9d", "#2a9d8f", "#e9c46a", "#264653"
                    ]

                    for idx, country in enumerate(countries_in_data):
                        ct = trend[trend["country"] == country]
                        color = COUNTRY_COLORS.get(country, color_palette[idx % len(color_palette)])
                        fig.add_trace(go.Scatter(
                            x=ct["year"],
                            y=ct["proportion"] * 1000,  # per 1000 births
                            mode="lines",
                            name=country,
                            line=dict(width=2.5, color=color, shape="spline"),
                            hovertemplate=f"<b>{country}</b><br>Year: %{{x}}<br>Streams: %{{y:.2f}} per 1,000<extra></extra>",
                        ))

                    fig.update_layout(
                        plot_bgcolor="white",
                        paper_bgcolor="white",
                        font=dict(family="Inter, sans-serif", color=TEXT_DARK, size=12),
                        xaxis=dict(
                            title="",
                            showgrid=False,
                            dtick=5,
                            tickfont=dict(size=10),
                        ),
                        yaxis=dict(
                            title="Streams per 1,000",
                            showgrid=True,
                            gridcolor="rgba(0,0,0,0.05)",
                            zeroline=False,
                            tickfont=dict(size=10),
                        ),
                        margin=dict(l=50, r=20, t=20, b=40),
                        height=340,
                        hovermode="x unified",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.35,
                            xanchor="center",
                            x=0.5,
                            font=dict(size=10),
                        ),
                    )

                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.caption("📊 Streaming history not available for this track.")
            except Exception:
                st.caption("📊 Streaming history requires the full dataset.")

    else:
        # Empty state — spinning vinyl with suggestions
        st.markdown(f"""
        <div style="text-align: center; padding: 2.5rem 1rem; color: {TEXT_MUTED};">
            <div style="font-size: 3rem; margin-bottom: 1rem;"><span class="vinyl-spin">💿</span></div>
            <p style="font-size: 1.05rem; margin: 0 0 0.5rem 0; font-weight: 500;">Drop a name in the search bar above</p>
            <p style="font-size: 0.85rem; margin: 0; color: {TEXT_MUTED};">
                Try <b>Isabella</b> (global #1 hit), <b>Raewyn</b> (underground NZ classic), or <b>your own name</b>
            </p>
        </div>
        """, unsafe_allow_html=True)


# ─── Section: Leaderboard ─────────────────────────────────────────────────────
def render_leaderboard(df):
    st.markdown("""
    <div class="section-divider">
        <h2>🏆 The Global Top 20</h2>
        <p>Chart-toppers that hit #1 in all 8 nations — the most borderless names on Earth</p>
    </div>
    """, unsafe_allow_html=True)

    # Filter: used in all 8 countries, take most recent year per name
    latest_year = df["year"].max()
    recent = df[df["year"] == latest_year].copy()

    # Names used in all 8 countries
    global_names = recent[recent["countries_using_name"] == 8].copy()

    # Get lowest countryness (most global)
    top20 = (
        global_names.groupby(["name", "sex"])
        .agg(
            countryness=("countryness", "min"),
            total_babies=("total_num_babies_w_name", "max"),
        )
        .reset_index()
        .sort_values("countryness")
        .head(20)
        .reset_index(drop=True)
    )

    # Build HTML chart entries
    entries_html = ""
    for i, row in top20.iterrows():
        rank = i + 1
        sex_emoji = "♀️" if row["sex"] == "F" else "♂️"
        rank_class = "chart-rank top3" if rank <= 3 else "chart-rank"
        total_formatted = f"{int(row['total_babies']):,}"

        entries_html += f"""
        <div class="chart-entry">
            <div class="{rank_class}">{rank}</div>
            <div class="chart-info">
                <div class="chart-name">{row['name']} {sex_emoji}</div>
                <div class="chart-meta">🌍 8 countries • {total_formatted} babies worldwide</div>
            </div>
            <div class="chart-score">
                <div class="value">{row['countryness']:.2f}</div>
                <div class="label">countryness</div>
            </div>
        </div>
        """

    st.markdown(entries_html, unsafe_allow_html=True)


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
        <div style="text-align:center; padding:1rem; background:white; border-radius:12px; border:1px solid #eee;">
            <div style="font-size:2rem; font-weight:800; color:{PURPLE};">{start_val:.1f}</div>
            <div style="font-size:0.8rem; color:{TEXT_MUTED};">1997 Average</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="text-align:center; padding:1rem; background:white; border-radius:12px; border:1px solid #eee;">
            <div style="font-size:2rem; font-weight:800; color:{SAGE};">{end_val:.1f}</div>
            <div style="font-size:0.8rem; color:{TEXT_MUTED};">2023 Average</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="text-align:center; padding:1rem; background:white; border-radius:12px; border:1px solid #eee;">
            <div style="font-size:2rem; font-weight:800; color:{CORAL};">27%</div>
            <div style="font-size:0.8rem; color:{TEXT_MUTED};">Convergence Drop</div>
        </div>
        """, unsafe_allow_html=True)


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
    render_leaderboard(df)
    render_convergence_timeline(df)
    render_insights()


# Allow running standalone
if __name__ == "__main__":
    render()
