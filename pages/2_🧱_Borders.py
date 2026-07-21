"""
Page 3: POV2 — Invisible Borders
"The Names That Refuse to Cross"
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Invisible Borders | VizCon 2026", page_icon="🧱", layout="wide")

@st.cache_data
def load_data():
    p = Path(__file__).parent.parent / "Data" / "metrics-and-summary.csv"
    if not p.exists(): p = Path(__file__).parent.parent / "metrics-and-summary.csv"
    if not p.exists(): p = Path("Data") / "metrics-and-summary.csv"
    return pd.read_csv(p)

df = load_data()
ALL_COUNTRIES = ['USA','England and Wales','Australia','Canada','Ireland','Scotland','New Zealand','Northern Ireland']
SHORT = ['USA','England','Australia','Canada','Ireland','Scotland','NZ','N.Ireland']
COLORS = {'USA':'#4361ee','England and Wales':'#e63946','Australia':'#2a9d8f',
           'Canada':'#7209b7','Ireland':'#fb8500','Scotland':'#06d6a0',
           'New Zealand':'#ef476f','Northern Ireland':'#118ab2'}

st.markdown("##### POINT OF VIEW 2")
st.title("🧱 Invisible Borders — The Names That Refuse to Cross")
st.markdown("> *Despite sharing a language, cultural walls persist. 39% of names remain locked.*")
st.markdown("---")

# ============================================================
# THE PRONUNCIATION WALL
# ============================================================
st.subheader("🔤 The Pronunciation Wall")
st.markdown("**The only names that stay truly 'yours' are the ones no one else can pronounce.**")

col1, col2 = st.columns(2)
with col1:
    st.success("**Declan** — You CAN say it → It left Ireland")
    st.metric("Countryness", "2,071 → 2.5", delta="-99.9%")
with col2:
    st.error("**Niamh** (\"Neev\") — You CAN'T say it → It stayed")
    st.metric("Countryness", "3,417 → 28", delta="-99.2% but still locked")

st.markdown("")
st.warning("""
**7.4x more culturally locked** — Names WITH Gaelic orthography (bh, dh, gh, aoi) are 7.4x more 
likely to stay in Ireland/NI than names without it.

Of names that escaped Ireland: only **3.2%** had Gaelic spelling.  
Of names that stayed: **30.2%**. That's a 10x difference.
""")

st.markdown("---")

# ============================================================
# N. IRELAND DIVERGENCE
# ============================================================
st.subheader("🏴 Northern Ireland Goes Against the Tide")

st.markdown("""
While the rest of the world **converges**, Northern Ireland is going the **opposite direction** — 
actively creating MORE culturally distinct names.
""")

# NI vs Ireland trend
ni_data = df[df['max_country']=='Northern Ireland'].groupby('year')['countryness'].mean()
ie_data = df[df['max_country']=='Ireland'].groupby('year')['countryness'].mean()

fig_ni = go.Figure()
fig_ni.add_trace(go.Scatter(x=ie_data.index, y=ie_data.values, mode='lines',
    name='Ireland (converging ↓)', line=dict(color='#fb8500', width=2.5)))
fig_ni.add_trace(go.Scatter(x=ni_data.index, y=ni_data.values, mode='lines',
    name='N. Ireland (diverging ↑)', line=dict(color='#118ab2', width=2.5)))
fig_ni.update_layout(template='plotly_dark', height=350,
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#b0b0d0'),
    yaxis=dict(title='Avg Countryness', gridcolor='rgba(255,255,255,0.05)'),
    legend=dict(orientation='h', y=-0.15), margin=dict(t=20,b=50,l=60,r=20))
st.plotly_chart(fig_ni, use_container_width=True)

st.info("**Same Gaelic heritage. Opposite response.** The Gaelic naming revival in NI is tied to post-Troubles political identity. Naming is a political act.")

# New names table
st.markdown("**85 brand-new locked names created since 2010:**")
new_names = pd.DataFrame({
    'Name': ['Sadhbh','Caoilfhionn','Iarla','Cadain','Frédérique','Siún','Aibhlinn'],
    'Country': ['Ireland','Ireland','Ireland','N. Ireland','Canada','Ireland','N. Ireland'],
    'Countryness': [8171, 2974, 815, 702, 10588, 713, 465],
    'Pronounced': ['"Sive"','"Kee-lin"','"Ear-la"','"Cah-dan"','French','"Shoon"','"Av-leen"'],
    'Why Locked': ['Zero phonetic clues','11 letters, 5 sounds','NEW (2015)','NEW (2017)','Accent = wall','NEW (2013)','NEW (2018)']
})
st.dataframe(new_names, use_container_width=True, hide_index=True)

st.markdown("---")
