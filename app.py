"""
VizCon 2026: "What's in a Name?"
Streamlit Multi-Page App — Main Entry Point (Intro Page)

Run: streamlit run app.py
Deploy: Push to GitHub → Connect to Streamlit Community Cloud
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="What's in a Name? | VizCon 2026",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    /* Dark theme overrides */
    .stApp { background-color: #0a0a1a; }
    
    /* Hero styling */
    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2, #06d6a0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    .hero-sub {
        text-align: center;
        font-size: 1.2rem;
        color: #8888aa;
        max-width: 700px;
        margin: 0 auto 1.5rem;
    }
    .thesis-box {
        text-align: center;
        font-size: 1.1rem;
        color: #667eea;
        background: rgba(102,126,234,0.08);
        border: 1px solid rgba(102,126,234,0.2);
        border-radius: 8px;
        padding: 14px 24px;
        max-width: 600px;
        margin: 1rem auto;
        font-style: italic;
    }
    
    /* Metric cards */
    .metric-row {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    .metric-card {
        text-align: center;
    }
    .metric-num {
        font-size: 2.2rem;
        font-weight: 700;
        color: #667eea;
    }
    .metric-lbl {
        font-size: 0.8rem;
        color: #8888aa;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Section styling */
    .section-num {
        font-size: 0.75rem;
        color: #667eea;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 4px;
    }
    .insight-box {
        background: linear-gradient(135deg, rgba(102,126,234,0.06), rgba(6,214,160,0.06));
        border: 1px solid rgba(102,126,234,0.15);
        border-radius: 10px;
        padding: 18px 24px;
        margin: 1rem 0;
    }
    .insight-text {
        font-size: 1.05rem;
        color: #d8d8f8;
        font-weight: 500;
    }
    .insight-detail {
        font-size: 0.88rem;
        color: #8888aa;
        margin-top: 6px;
    }
    
    /* Divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102,126,234,0.2), transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA LOADING (cached)
# ============================================================
@st.cache_data
def load_metrics():
    """Load pre-computed metrics file."""
    data_path = Path(__file__).parent.parent / "metrics-and-summary.csv"
    if not data_path.exists():
        data_path = Path("metrics-and-summary.csv")
    return pd.read_csv(data_path)

@st.cache_data
def compute_intro_data(df):
    """Compute all intro page metrics."""
    # Countryness over time
    year_countryness = df.groupby('year')['countryness'].mean().reset_index()
    year_countryness.columns = ['year', 'avg_countryness']
    
    # Life curves for example names
    life_curves = {}
    for name in ['Michael', 'Jennifer', 'Olivia', 'Nevaeh']:
        mask = df['name'] == name
        if mask.any():
            curve = df[mask].groupby('year')['total_num_babies_w_name'].sum().reset_index()
            curve.columns = ['year', 'babies']
            life_curves[name] = curve
    
    return year_countryness, life_curves

# Load data
df_metrics = load_metrics()
year_countryness, life_curves = compute_intro_data(df_metrics)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/baby.png", width=60)
    st.title("What's in a Name?")
    st.caption("VizCon 2026 Submission")
    st.markdown("---")
    st.markdown("**Navigate:**")
    st.markdown("""
    - 🌍 **Intro** (this page)
    - 🤝 Convergence
    - 🧱 Invisible Borders  
    - 🎉 Fun Facts
    - 📋 Methods
    """)
    st.markdown("---")
    st.markdown("**Dataset:**")
    st.markdown("1.55M records • 8 countries • 1935-2023")
    st.markdown("---")
    st.caption("Built with Streamlit + Plotly")
    st.caption("Theme: *How the world lives, thrives, and connects*")

# ============================================================
# HERO SECTION
# ============================================================
st.markdown('<div class="hero-title">What\'s in a Name?</div>', unsafe_allow_html=True)
st.markdown("""
<div class="hero-sub">
8 countries. 1 language. 114 years of baby names.<br>
Do they name babies the same way? The answer is more surprising than you think.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="thesis-box">"Same language. Same names? Let\'s find out."</div>', unsafe_allow_html=True)

# Metrics row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Name Records", "1.55M")
with col2:
    st.metric("Countries", "8")
with col3:
    st.metric("Unique Names", "18,000")
with col4:
    st.metric("Time Span", "1935–2023")

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================================
# SECTION: THE ANGLOSPHERE
# ============================================================
st.markdown('<div class="section-num">THE ANGLOSPHERE</div>', unsafe_allow_html=True)
st.header("Eight Countries United by One Language")

st.markdown("""
Connected through British colonization, migration, and shared media — but each carries 
its OWN cultural currents beneath the English surface.
""")

# Country cards
col1, col2, col3, col4 = st.columns(4)
countries_info = [
    ("🇺🇸 USA", "Hispanic influence, 3.6M births/yr"),
    ("🇬🇧 England & Wales", "Commonwealth diversity"),
    ("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland", "Scottish Gaelic heritage"),
    ("🇮🇪 Ireland", "Strong Gaelic naming tradition"),
    ("🇨🇦 Canada", "Francophone identity (Quebec)"),
    ("🇦🇺 Australia", "Indigenous cultures"),
    ("🇳🇿 New Zealand", "Māori naming tradition"),
    ("🏴 N. Ireland", "Post-Troubles Gaelic revival"),
]

for i, (country, desc) in enumerate(countries_info):
    with [col1, col2, col3, col4][i % 4]:
        st.markdown(f"**{country}**")
        st.caption(desc)

st.markdown("""
> The Anglosphere shares a language, legal traditions, and cultural exchange.  
> But does sharing a language mean sharing a **culture**?  
> Baby names — the most personal choice a family makes — give us the answer.
""")

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================================
# SECTION: THE CORE QUESTION
# ============================================================
st.markdown('<div class="section-num">THE CORE QUESTION</div>', unsafe_allow_html=True)
st.header("Language vs Culture — The Two Truths")

st.markdown("""
We measured cultural distinctness using a **"countryness" score**:
- **Low countryness (1-2)** = name used equally everywhere (e.g., Noah, Olivia)
- **High countryness (500+)** = name locked to one culture (e.g., Sadhbh, Raewyn)

*Countryness = how many times more prevalent a name is in its top country vs. any other.*
""")

st.markdown("**The result? Both things are true simultaneously:**")

col1, col2 = st.columns(2)
with col1:
    st.success("✅ **YES — Names ARE Converging**")
    st.metric("Countryness Decline", "−74%", delta="-74%", delta_color="normal")
    st.caption("Dropped from 42 (1980s) to 11 (2023). Countries are naming babies more similarly.")

with col2:
    st.error("❌ **BUT — Cultural Borders Persist**")
    st.metric("Names Still Locked", "39%", delta="+38% in N.Ireland", delta_color="inverse")
    st.caption("39% remain culturally distinct. N. Ireland is getting MORE distinct, not less.")

# ============================================================
# CHART: Countryness Over Time
# ============================================================
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.subheader("📉 Cultural Distinctness Score Over Time")
st.caption("Lower = countries naming babies more similarly")

fig_core = go.Figure()
fig_core.add_trace(go.Scatter(
    x=year_countryness['year'],
    y=year_countryness['avg_countryness'],
    mode='lines',
    fill='tozeroy',
    line=dict(color='#667eea', width=2.5),
    fillcolor='rgba(102,126,234,0.12)',
    hovertemplate='<b>%{x}</b><br>Avg Countryness: %{y:.1f}<extra></extra>'
))

# Annotations
fig_core.add_annotation(x=1980, y=42, text="1980s: 42<br>(names very distinct)",
    showarrow=True, arrowhead=2, font=dict(size=10, color='#667eea'),
    arrowcolor='#667eea')
fig_core.add_annotation(x=2023, y=11, text="2023: 11<br>(−74% decline)",
    showarrow=True, arrowhead=2, font=dict(size=10, color='#e63946'),
    arrowcolor='#e63946')

fig_core.update_layout(
    template='plotly_dark',
    height=400,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#b0b0d0'),
    yaxis=dict(title='Avg Countryness Score', gridcolor='rgba(255,255,255,0.05)'),
    xaxis=dict(title='Year', gridcolor='rgba(255,255,255,0.05)'),
    margin=dict(t=20, b=50, l=60, r=20),
    showlegend=False
)

st.plotly_chart(fig_core, use_container_width=True)

# Insight box
st.markdown("""
<div class="insight-box">
    <div class="insight-text">💡 This creates two opposite, coexisting truths — and that's the story.</div>
    <div class="insight-detail">Names are converging globally, but cultural resistance is real and measurable. 
    Explore both sides in the Convergence and Invisible Borders tabs.</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CHART: Name Life Curves
# ============================================================
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.subheader("📈 Name Archetypes: Different Life Curves")
st.markdown("Not all names live the same life. Some reign for decades, others flash and fade:")

colors_map = {
    'Michael': ('#4361ee', 'The 50-Year King'),
    'Jennifer': ('#e63946', 'The Sprinter'),
    'Olivia': ('#06d6a0', 'The Steady Climber'),
    'Nevaeh': ('#7209b7', 'The Viral Flash'),
}

fig_life = go.Figure()
for name, curve_df in life_curves.items():
    if name in colors_map:
        color, label = colors_map[name]
        fig_life.add_trace(go.Scatter(
            x=curve_df['year'],
            y=curve_df['babies'],
            mode='lines',
            name=f"{name} — {label}",
            line=dict(color=color, width=2.5),
            hovertemplate=f'<b>{name}</b><br>%{{x}}: %{{y:,.0f}} babies<extra></extra>'
        ))

fig_life.update_layout(
    template='plotly_dark',
    height=380,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#b0b0d0'),
    yaxis=dict(title='Babies Named Per Year', gridcolor='rgba(255,255,255,0.05)'),
    xaxis=dict(title='Year', gridcolor='rgba(255,255,255,0.05)'),
    margin=dict(t=20, b=50, l=60, r=20),
    legend=dict(orientation='h', y=-0.15, font=dict(size=11))
)

st.plotly_chart(fig_life, use_container_width=True)

st.markdown("""
**Michael** ruled for 50 years (1950-2000) — no name in recorded history had that kind of grip. 
**Jennifer** exploded in the 70s but crashed just as fast. 
**Olivia** shows the modern "steady climber" pattern. 
And **Nevaeh** (heaven backwards) is the prototype viral name: rockets up, already fading.

---

*Navigate to the other pages using the sidebar to explore Convergence, Invisible Borders, and Fun Facts.*
""")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#555; font-size:0.85rem;">
    <p><strong>VizCon 2026</strong> | "What's in a Name? Language vs Culture in the Anglosphere"</p>
    <p>Data: <a href="https://www.kaggle.com/datasets" style="color:#667eea;">Kaggle Anglosphere Baby Names</a> | 
    1.55M records, 8 countries, 1935–2023</p>
    <p><em>"Language connects us. Culture keeps us unique. Names show us both."</em></p>
</div>
""", unsafe_allow_html=True)
