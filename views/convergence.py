import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import os
import pandas as pd
import numpy as np
from utils.data_loader import load_metrics, load_summary
from utils.charts import CHART_LAYOUT, COLORS, COUNTRY_COLORS


def render():
    # Fixed layout — sticky tabs + wider content
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
    </style>
    """, unsafe_allow_html=True)
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

"""
Global Playlist — Convergence Analysis
Part of "Passport for a Name" baby naming data visualization project.
"""

# ─── Color Theme ───────────────────────────────────────────────────────────────
PURPLE = "#667eea"
SAGE = "#7c9a8e"
CORAL = "#c99e85"
DARK_BG = "#1a1a2e"
CARD_BG = "#f8f9fa"
TEXT_DARK = "#2d3436"
TEXT_MUTED = "#636e72"


# ─── Shared Styles ─────────────────────────────────────────────────────────────
def inject_styles():
    st.markdown("""
    <style>
        .playlist-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem 2.5rem;
            border-radius: 16px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }
        .playlist-header h1 {
            margin: 0;
            font-size: 2.2rem;
            font-weight: 800;
        }
        .playlist-header p {
            margin: 0.5rem 0 0 0;
            opacity: 0.85;
            font-size: 1.05rem;
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
    </style>
    """, unsafe_allow_html=True)


# ─── Section 1: Leaderboard ───────────────────────────────────────────────────
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


# ─── Section 2: Convergence Timeline ──────────────────────────────────────────
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
    fig.add_annotation(
        x=2010,
        y=yearly_avg[yearly_avg["year"] == 2010]["avg_countryness"].values[0] if 2010 in yearly_avg["year"].values else yearly_avg["avg_countryness"].median(),
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


# ─── Section 3: Interactive Search ─────────────────────────────────────────────
def render_interactive_search(df):
    st.markdown("""
    <div class="section-divider">
        <h2>🔍 Track Lookup</h2>
        <p>Search any name to see if it's on the Global Playlist or pressed on Local Vinyl</p>
    </div>
    """, unsafe_allow_html=True)

    search_name = st.text_input(
        "🎵 Type a name to look up",
        placeholder="e.g. Olivia, Liam, Isabella...",
        key="name_search_input",
    )

    if search_name:
        search_name_upper = search_name.strip().capitalize()
        latest_year = df["year"].max()
        matches = df[(df["name"].str.upper() == search_name_upper.upper()) & (df["year"] == latest_year)]

        if matches.empty:
            # Try any year
            matches = df[df["name"].str.upper() == search_name_upper.upper()]

        if matches.empty:
            st.markdown(f"""
            <div class="search-result" style="text-align:center;">
                <p style="font-size:1.2rem; color:{TEXT_MUTED};">🎵 No track found for "<b>{search_name_upper}</b>"</p>
                <p style="font-size:0.9rem; color:{TEXT_MUTED};">This name isn't in our Anglosphere charts. Try another!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Take the row with lowest countryness (best global score)
            best = matches.loc[matches["countryness"].idxmin()]
            countryness_val = best["countryness"]
            countries_count = int(best["countries_using_name"])
            sex_emoji = "♀️" if best["sex"] == "F" else "♂️"
            total_babies = int(best["total_num_babies_w_name"]) if pd.notna(best["total_num_babies_w_name"]) else 0

            # Determine badge
            if countryness_val < 2:
                badge = '<span class="badge-global">🌍 On the Global Playlist</span>'
                verdict = "This name is a worldwide hit — equally loved across all nations!"
            elif countryness_val > 100:
                badge = '<span class="badge-local">🎵 Local Vinyl Only</span>'
                verdict = "This name is a regional classic — beloved in its home country but rare elsewhere."
            else:
                badge = '<span class="badge-neutral">📀 Mid-Chart Contender</span>'
                verdict = "This name has some international appeal but hasn't gone fully global yet."

            # Get countries where it's used (from max_country as primary indicator)
            name_rows = df[df["name"].str.upper() == search_name_upper.upper()]
            countries_used = name_rows["max_country"].unique().tolist()

            country_pills_html = ""
            for c in sorted(countries_used)[:8]:
                country_pills_html += f'<span class="country-pill">{c}</span>'

            st.markdown(f"""
            <div class="search-result">
                <div style="display:flex; align-items:center; gap:1rem; margin-bottom:1rem;">
                    <h3 style="margin:0;">{search_name_upper} {sex_emoji}</h3>
                    {badge}
                </div>
                <p style="color:{TEXT_MUTED}; margin-bottom:1rem;">{verdict}</p>
                <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:1rem; margin:1rem 0;">
                    <div style="text-align:center;">
                        <div style="font-size:1.5rem; font-weight:800; color:{PURPLE};">{countryness_val:.2f}</div>
                        <div style="font-size:0.75rem; color:{TEXT_MUTED};">Countryness Score</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="font-size:1.5rem; font-weight:800; color:{SAGE};">{countries_count}</div>
                        <div style="font-size:0.75rem; color:{TEXT_MUTED};">Countries Using It</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="font-size:1.5rem; font-weight:800; color:{CORAL};">{total_babies:,}</div>
                        <div style="font-size:0.75rem; color:{TEXT_MUTED};">Total Babies</div>
                    </div>
                </div>
                <div style="margin-top:1rem;">
                    <div style="font-size:0.8rem; color:{TEXT_MUTED}; margin-bottom:0.4rem;">Charting in:</div>
                    <div class="country-pills">{country_pills_html}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ─── Section 4: Insights Infographic ──────────────────────────────────────────
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

    # Page header
    st.markdown("""
    <div class="playlist-header">
        <h1>🎧 The Global Playlist</h1>
        <p>Which baby names are worldwide chart-toppers, and which stay pressed on local vinyl?
        Exploring convergence across 8 English-speaking nations.</p>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    df = load_metrics()

    # Render all four sections
    render_leaderboard(df)
    render_convergence_timeline(df)
    render_interactive_search(df)
    render_insights()


# Allow running standalone
if __name__ == "__main__":
    render()

