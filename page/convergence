"""
Page 2: POV1 — Convergence
"The Anglosphere is becoming one naming culture"
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import collections

st.set_page_config(page_title="Convergence | VizCon 2026", page_icon="🤝", layout="wide")

# ============================================================
# DATA
# ============================================================
@st.cache_data
def load_data():
    p = Path(__file__).parent.parent.parent / "metrics-and-summary.csv"
    if not p.exists(): p = Path(__file__).parent.parent / "metrics-and-summary.csv"
    if not p.exists(): p = Path("metrics-and-summary.csv")
    return pd.read_csv(p)

df = load_data()

# ============================================================
# HEADER
# ============================================================
st.markdown("##### POINT OF VIEW 1")
st.title("🤝 Convergence — Coming Together")
st.markdown("""
> *Shared screens create shared names. Each new media era accelerated the collapse 
> of cultural naming boundaries.*
""")

st.markdown("---")

# ============================================================
# CHART 1: Media Era
# ============================================================
st.subheader("📺 Cultural Distinctness by Media Era")
st.markdown("Each media revolution pushed naming cultures closer together:")

era_bins = {'Pre-TV (1935-55)': (1935,1955), 'TV Era (1956-85)': (1956,1985),
            'Cable (1986-99)': (1986,1999), 'Internet (2000-10)': (2000,2010),
            'Streaming (2011-23)': (2011,2023)}

era_avgs = []
for label, (lo, hi) in era_bins.items():
    vals = df[(df['year']>=lo) & (df['year']<=hi)]['countryness']
    era_avgs.append({'era': label, 'avg': vals.mean()})
era_df = pd.DataFrame(era_avgs)

fig_era = go.Figure(go.Bar(
    x=era_df['era'], y=era_df['avg'],
    marker_color=['#2a9d8f','#4361ee','#7209b7','#e63946','#fb8500'],
    text=[f"{v:.1f}" for v in era_df['avg']], textposition='outside',
    textfont=dict(color='#c0c0e0'),
    hovertemplate='<b>%{x}</b><br>Avg Countryness: %{y:.1f}<extra></extra>'
))
fig_era.update_layout(template='plotly_dark', height=380,
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#b0b0d0'),
    yaxis=dict(title='Avg Cultural Distinctness', gridcolor='rgba(255,255,255,0.05)'),
    margin=dict(t=20,b=50,l=60,r=20), showlegend=False)

st.plotly_chart(fig_era, use_container_width=True)
st.info("💡 The streaming era (2011+) has the lowest cultural distinctness ever — a **50% drop** from pre-TV levels.")

st.markdown("---")

# ============================================================
# TABLE: Pop Culture Lifespans
# ============================================================
st.subheader("📡 Pop Culture Creates Disposable Names")
st.markdown("Pop culture accelerates convergence — but creates names that burn bright and die fast:")

pop_data = pd.DataFrame({
    'Name': ['James', 'Jennifer', 'Britney', 'Khaleesi'],
    'Source': ['Classic English', 'Love Story (1970)', 'Pop star (1999)', 'Game of Thrones'],
    'Rise': ['12 yrs', '16 yrs', '9 yrs', '6 yrs'],
    'Fall': ['76+ yrs', '33 yrs', '9 yrs', '5+ yrs'],
    'Total Lifespan': ['88+ (alive!)', '49 years', '18 years', '11 years']
})
st.dataframe(pop_data, use_container_width=True, hide_index=True)

st.markdown("---")

# ============================================================
# CHART 2: Sankey - Import/Export
# ============================================================
st.subheader("🌐 The Import/Export Economy of Names")
st.markdown("We tracked which countries **export** names and which **absorb** them:")

# Build influence from first-appearance data
@st.cache_data
def compute_influence():
    p = Path(__file__).parent.parent.parent / "all-names-long.csv"
    if not p.exists(): p = Path(__file__).parent.parent / "all-names-long.csv"
    if not p.exists(): p = Path("all-names-long.csv")
    
    import csv
    name_first = collections.defaultdict(dict)
    with open(p, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            freq = int(row['frequency'])
            if freq >= 10:
                key = (row['name'], row['sex'])
                c = row['country']
                yr = int(row['year'])
                if c not in name_first[key] or yr < name_first[key][c]:
                    name_first[key][c] = yr
    
    ALL = ['USA','England and Wales','Australia','Canada','Ireland','Scotland','New Zealand','Northern Ireland']
    influence = collections.defaultdict(lambda: collections.defaultdict(int))
    for key, countries in name_first.items():
        if len(countries) >= 5:
            path = sorted(countries.items(), key=lambda x: x[1])
            for i in range(len(path)-1):
                influence[path[i][0]][path[i+1][0]] += 1
    return influence, ALL

influence, ALL = compute_influence()

COLORS = {'USA':'#4361ee','England and Wales':'#e63946','Australia':'#2a9d8f',
           'Canada':'#7209b7','Ireland':'#fb8500','Scotland':'#06d6a0',
           'New Zealand':'#ef476f','Northern Ireland':'#118ab2'}
SHORT_MAP = {'England and Wales':'England','Northern Ireland':'N.Ireland','New Zealand':'NZ'}

flows = [(s,d,influence[s][d]) for s in ALL for d in ALL if s!=d and influence[s][d]>50]
flows.sort(key=lambda x:-x[2])
top_flows = flows[:16]

src_n = list(set(f[0] for f in top_flows))
tgt_n = list(set(f[1] for f in top_flows))
all_n = src_n + [f"{n} " for n in tgt_n]
node_c = [COLORS.get(n.strip(),'#888') for n in all_n]
sk_s, sk_t, sk_v, sk_c = [],[],[],[]
for s,d,v in top_flows:
    sk_s.append(all_n.index(s)); sk_t.append(all_n.index(f"{d} ")); sk_v.append(v)
    c = COLORS.get(s,'#888')
    r,g,b = int(c[1:3],16),int(c[3:5],16),int(c[5:7],16)
    sk_c.append(f'rgba({r},{g},{b},0.3)')

fig_sk = go.Figure(go.Sankey(
    node=dict(pad=15, thickness=20, line=dict(color='rgba(255,255,255,0.1)',width=1),
              label=[SHORT_MAP.get(n.strip(), n.strip()) for n in all_n], color=node_c),
    link=dict(source=sk_s, target=sk_t, value=sk_v, color=sk_c)
))
fig_sk.update_layout(template='plotly_dark', height=420,
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#b0b0d0',size=11), margin=dict(t=20,b=20,l=20,r=20))

st.plotly_chart(fig_sk, use_container_width=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🇨🇦 Canada", "−572 net", help="Exports 962, imports 390")
    st.caption("Biggest exporter")
with col2:
    st.metric("🇺🇸 USA", "+506 net", help="Imports 1,043 names")
    st.caption("Biggest importer")
with col3:
    st.metric("🇮🇪 Liam", "85 → 1.5", help="Irish → USA #1 name")
    st.caption("Name gentrification")

st.markdown("---")

# ============================================================
# CHART 3: Similarity over time
# ============================================================
st.subheader("📈 Country Similarity Over Time")

@st.cache_data
def compute_similarity():
    ALL_C = ['USA','England and Wales','Australia','Canada','Ireland','Scotland','New Zealand','Northern Ireland']
    sim = {}
    for year in range(1997, 2024):
        top50 = {}
        for c in ALL_C:
            sub = df[(df['year']==year) & (df['max_country']==c)]
            # Use all names where this country is max for that year
        # Alternative: use country_year approach from metrics
        names_yr = df[df['year']==year]
        for c in ALL_C:
            c_names = names_yr[names_yr['max_country']==c].nlargest(50, 'total_num_babies_w_name')['name'].tolist()
            if c_names:
                top50[c] = set(c_names)
        
        if len(top50) >= 6:
            ov, pairs = 0, 0
            for i, c1 in enumerate(ALL_C):
                for c2 in ALL_C[i+1:]:
                    if c1 in top50 and c2 in top50:
                        ov += len(top50[c1] & top50[c2]); pairs += 1
            if pairs: sim[year] = ov / pairs
    return sim

sim_time = compute_similarity()
if sim_time:
    yrs_s = sorted(sim_time.keys())
    fig_sim = go.Figure(go.Scatter(
        x=yrs_s, y=[sim_time[y] for y in yrs_s],
        mode='lines+markers', line=dict(color='#06d6a0', width=2.5),
        marker=dict(size=5), fill='tozeroy', fillcolor='rgba(6,214,160,0.08)',
        hovertemplate='%{x}: %{y:.1f} shared names<extra></extra>'
    ))
    fig_sim.update_layout(template='plotly_dark', height=320,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#b0b0d0'),
        yaxis=dict(title='Avg Names Shared (of top 50)', gridcolor='rgba(255,255,255,0.05)'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        margin=dict(t=20,b=50,l=60,r=20), showlegend=False)
    st.plotly_chart(fig_sim, use_container_width=True)

st.success("**Key takeaway:** Convergence is real, measurable, and accelerating — driven by shared media, migration, and the internet. But it's not the whole story...")
