"""
Methods — The story behind the data and tools.
Part of "Now Playing: The Name Playlist" data storytelling project.
"""

import streamlit as st


def render():
    # ─── Header ───────────────────────────────────────────────────
    st.markdown("""
    <div style="background: linear-gradient(135deg, #EEF2FF, #E8F4FD, #F0FFF4); 
                border-radius: 16px; padding: 40px 30px; text-align: center; 
                margin-bottom: 20px; border: 1px solid #E2E8F0;">
        <h1 style="font-size: 2.4em; font-weight: 800; color: #2D3748; margin: 0 0 12px 0;">
            📋 Methods
        </h1>
        <p style="font-size: 1.2em; color: #4A5568; max-width: 650px; margin: 0 auto; line-height: 1.7;">
            How we built this — the data, the tools, and the process.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ─── Section 1: The Dataset ───────────────────────────────────
    st.markdown("""
    <h2 style="margin: 2rem 0 0.5rem; color: #1f2937;">📊 The Dataset</h2>
    <p style="font-size: 0.95rem; color: #4a5568; margin-bottom: 1.5rem;">
        Three core datasets power this story — all sourced from official government baby name registries.
    </p>
    """, unsafe_allow_html=True)

    # Dataset cards
    st.markdown("""
    <div style="display:grid; gap:1rem; margin-bottom:2rem;">
        <!-- Dataset 1 -->
        <div style="background:white; border-radius:14px; padding:1.5rem; border:1px solid #e5e7eb; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
            <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.8rem;">
                <span style="font-size:1.5rem;">💾</span>
                <h3 style="margin:0; color:#2d3436; font-size:1.1rem;">all-names-long.csv.gz</h3>
                <span style="background:#e8f5e9; color:#2e7d32; padding:2px 8px; border-radius:6px; 
                             font-size:0.72rem; font-weight:600;">PRIMARY</span>
            </div>
            <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:1rem; margin-bottom:0.8rem;">
                <div style="text-align:center;">
                    <div style="font-size:1.3rem; font-weight:800; color:#667eea;">970K</div>
                    <div style="font-size:0.7rem; color:#999;">Records</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:1.3rem; font-weight:800; color:#667eea;">61K</div>
                    <div style="font-size:0.7rem; color:#999;">Unique Names</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:1.3rem; font-weight:800; color:#667eea;">8</div>
                    <div style="font-size:0.7rem; color:#999;">Countries</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:1.3rem; font-weight:800; color:#667eea;">27yr</div>
                    <div style="font-size:0.7rem; color:#999;">1997–2023</div>
                </div>
            </div>
            <p style="font-size:0.82rem; color:#636e72; margin:0; line-height:1.5;">
                Full per-country yearly breakdown. Each row = one name × one country × one year.
                Minimum threshold: 3+ babies per country per year. Used for flow analysis, sparklines, and country-level trends.
            </p>
        </div>

        <!-- Dataset 2 -->
        <div style="background:white; border-radius:14px; padding:1.5rem; border:1px solid #e5e7eb;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
            <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.8rem;">
                <span style="font-size:1.5rem;">📈</span>
                <h3 style="margin:0; color:#2d3436; font-size:1.1rem;">summary-1997-2023.csv</h3>
                <span style="background:#e3f2fd; color:#1565c0; padding:2px 8px; border-radius:6px; 
                             font-size:0.72rem; font-weight:600;">AGGREGATED</span>
            </div>
            <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:1rem; margin-bottom:0.8rem;">
                <div style="text-align:center;">
                    <div style="font-size:1.3rem; font-weight:800; color:#7c9a8e;">18,968</div>
                    <div style="font-size:0.7rem; color:#999;">Rows</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:1.3rem; font-weight:800; color:#7c9a8e;">17,575</div>
                    <div style="font-size:0.7rem; color:#999;">Unique Names</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:1.3rem; font-weight:800; color:#7c9a8e;">117M</div>
                    <div style="font-size:0.7rem; color:#999;">Total Babies</div>
                </div>
            </div>
            <p style="font-size:0.82rem; color:#636e72; margin:0; line-height:1.5;">
                Pre-computed from full government records (no minimum threshold). Includes countryness scores, max_country,
                total babies, and country counts. Used for Track Lookup and classification.
            </p>
        </div>

        <!-- Dataset 3 -->
        <div style="background:white; border-radius:14px; padding:1.5rem; border:1px solid #e5e7eb;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
            <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.8rem;">
                <span style="font-size:1.5rem;">📉</span>
                <h3 style="margin:0; color:#2d3436; font-size:1.1rem;">metrics-and-summary.csv</h3>
                <span style="background:#fff3e0; color:#e65100; padding:2px 8px; border-radius:6px; 
                             font-size:0.72rem; font-weight:600;">YEARLY</span>
            </div>
            <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:1rem; margin-bottom:0.8rem;">
                <div style="text-align:center;">
                    <div style="font-size:1.3rem; font-weight:800; color:#c99e85;">196,626</div>
                    <div style="font-size:0.7rem; color:#999;">Rows</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:1.3rem; font-weight:800; color:#c99e85;">Per-Year</div>
                    <div style="font-size:0.7rem; color:#999;">Breakdowns</div>
                </div>
            </div>
            <p style="font-size:0.82rem; color:#636e72; margin:0; line-height:1.5;">
                Year-level countryness metrics. Requires 2+ countries in the same year. Used for convergence timelines,
                media era analysis, and trend visualizations.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Countries covered
    st.markdown("""
    <div style="background:linear-gradient(135deg, #f8f9ff, #eef1ff); border-radius:12px; 
                padding:1.2rem 1.5rem; border:1px solid rgba(102,126,234,0.15); margin-bottom:2rem;">
        <p style="font-size:0.85rem; font-weight:600; color:#667eea; margin:0 0 0.5rem; 
                  text-transform:uppercase; letter-spacing:1px;">🌍 Countries Covered</p>
        <div style="display:flex; flex-wrap:wrap; gap:0.5rem;">
            <span style="background:white; padding:4px 12px; border-radius:8px; font-size:0.82rem; border:1px solid #e5e7eb;">🇺🇸 USA</span>
            <span style="background:white; padding:4px 12px; border-radius:8px; font-size:0.82rem; border:1px solid #e5e7eb;">🏴󠁧󠁢󠁥󠁮󠁧󠁿 England & Wales</span>
            <span style="background:white; padding:4px 12px; border-radius:8px; font-size:0.82rem; border:1px solid #e5e7eb;">🇨🇦 Canada</span>
            <span style="background:white; padding:4px 12px; border-radius:8px; font-size:0.82rem; border:1px solid #e5e7eb;">🇦🇺 Australia</span>
            <span style="background:white; padding:4px 12px; border-radius:8px; font-size:0.82rem; border:1px solid #e5e7eb;">🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland</span>
            <span style="background:white; padding:4px 12px; border-radius:8px; font-size:0.82rem; border:1px solid #e5e7eb;">🇮🇪 Ireland</span>
            <span style="background:white; padding:4px 12px; border-radius:8px; font-size:0.82rem; border:1px solid #e5e7eb;">🇳🇿 New Zealand</span>
            <span style="background:white; padding:4px 12px; border-radius:8px; font-size:0.82rem; border:1px solid #e5e7eb;">Northern Ireland</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # The Countryness Formula
    st.markdown("""
    <div style="background:white; border-radius:14px; padding:1.5rem; border:1px solid #e5e7eb;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04); margin-bottom:2rem;">
        <h3 style="margin:0 0 0.8rem; color:#1f2937;">🧮 The Countryness Score</h3>
        <div style="background:#f8f9ff; border-radius:10px; padding:1rem; text-align:center; margin-bottom:1rem;
                    border:1px solid rgba(102,126,234,0.1);">
            <p style="font-size:1.1rem; font-weight:700; color:#1f2937; margin:0; font-family:'Courier New', monospace;">
                Countryness = Proportion in Top Country ÷ Avg Proportion in Other Countries
            </p>
        </div>
        <p style="font-size:0.85rem; color:#4a5568; line-height:1.6; margin:0;">
            A score of <strong>1.0</strong> means perfectly equal usage across all nations — a true global hit.
            The higher the score, the more "local" the name. A score of 168,731 (Raewyn) means it exists 
            almost exclusively in one country. We use the <strong>mean</strong> (not sum) when aggregating 
            across years since it's a ratio.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ─── Section 2: Tools Used ────────────────────────────────────
    st.markdown("""
    <h2 style="margin: 2rem 0 0.5rem; color: #1f2937;">🛠️ Tools Used</h2>
    <p style="font-size: 0.95rem; color: #4a5568; margin-bottom: 1.5rem;">
        This project was built entirely with AI-assisted development — no manual coding from scratch.
    </p>
    """, unsafe_allow_html=True)

    # Tool cards
    st.markdown("""
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem; margin-bottom:2rem;">
        <!-- Amazon Quick -->
        <div style="background:white; border-radius:14px; padding:1.5rem; border:1px solid #e5e7eb;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.04); border-top:4px solid #667eea;">
            <div style="font-size:1.8rem; margin-bottom:0.5rem;">🤖</div>
            <h3 style="margin:0 0 0.4rem; color:#2d3436; font-size:1.05rem;">Amazon Quick</h3>
            <p style="font-size:0.8rem; color:#636e72; line-height:1.5; margin:0;">
                AI work companion for data analysis, code generation, visualization design,
                and iterative development. Used for all Python/Streamlit code, chart design,
                data exploration, and audio processing.
            </p>
        </div>

        <!-- Kiro -->
        <div style="background:white; border-radius:14px; padding:1.5rem; border:1px solid #e5e7eb;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.04); border-top:4px solid #2ecc71;">
            <div style="font-size:1.8rem; margin-bottom:0.5rem;">💻</div>
            <h3 style="margin:0 0 0.4rem; color:#2d3436; font-size:1.05rem;">Kiro</h3>
            <p style="font-size:0.8rem; color:#636e72; line-height:1.5; margin:0;">
                AI-powered IDE for code editing, debugging, and deployment workflows.
                Used for refining Streamlit components, handling edge cases, 
                and managing the GitHub repository.
            </p>
        </div>

        <!-- Agent Spaces -->
        <div style="background:white; border-radius:14px; padding:1.5rem; border:1px solid #e5e7eb;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.04); border-top:4px solid #9b59b6;">
            <div style="font-size:1.8rem; margin-bottom:0.5rem;">🧠</div>
            <h3 style="margin:0 0 0.4rem; color:#2d3436; font-size:1.05rem;">Agent Spaces</h3>
            <p style="font-size:0.8rem; color:#636e72; line-height:1.5; margin:0;">
                Knowledge management for storing datasets, reference documents, and 
                project context. Enabled persistent memory across development sessions
                and structured data retrieval.
            </p>
        </div>

        <!-- Streamlit -->
        <div style="background:white; border-radius:14px; padding:1.5rem; border:1px solid #e5e7eb;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.04); border-top:4px solid #e74c3c;">
            <div style="font-size:1.8rem; margin-bottom:0.5rem;">🚀</div>
            <h3 style="margin:0 0 0.4rem; color:#2d3436; font-size:1.05rem;">Streamlit</h3>
            <p style="font-size:0.8rem; color:#636e72; line-height:1.5; margin:0;">
                Open-source Python framework for building interactive data apps. 
                Deployed on Streamlit Cloud. Used with Plotly for charts, 
                components.html() for custom interactivity, and CSS animations.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tech stack summary
    st.markdown("""
    <div style="background:linear-gradient(135deg, #0d1117, #1a1a2e); border-radius:14px;
                padding:1.5rem 2rem; color:white; margin-bottom:2rem;">
        <p style="font-size:0.75rem; color:rgba(255,255,255,0.5); text-transform:uppercase; 
                  letter-spacing:1.5px; margin:0 0 0.8rem;">Tech Stack</p>
        <div style="display:flex; flex-wrap:wrap; gap:0.6rem;">
            <span style="background:rgba(255,255,255,0.1); padding:5px 12px; border-radius:8px; font-size:0.8rem;">Python</span>
            <span style="background:rgba(255,255,255,0.1); padding:5px 12px; border-radius:8px; font-size:0.8rem;">Streamlit 1.60</span>
            <span style="background:rgba(255,255,255,0.1); padding:5px 12px; border-radius:8px; font-size:0.8rem;">Plotly</span>
            <span style="background:rgba(255,255,255,0.1); padding:5px 12px; border-radius:8px; font-size:0.8rem;">Pandas</span>
            <span style="background:rgba(255,255,255,0.1); padding:5px 12px; border-radius:8px; font-size:0.8rem;">NumPy</span>
            <span style="background:rgba(255,255,255,0.1); padding:5px 12px; border-radius:8px; font-size:0.8rem;">CSS3 Animations</span>
            <span style="background:rgba(255,255,255,0.1); padding:5px 12px; border-radius:8px; font-size:0.8rem;">JavaScript (Canvas API)</span>
            <span style="background:rgba(255,255,255,0.1); padding:5px 12px; border-radius:8px; font-size:0.8rem;">SVG</span>
            <span style="background:rgba(255,255,255,0.1); padding:5px 12px; border-radius:8px; font-size:0.8rem;">HTML5 Audio</span>
            <span style="background:rgba(255,255,255,0.1); padding:5px 12px; border-radius:8px; font-size:0.8rem;">GitHub</span>
            <span style="background:rgba(255,255,255,0.1); padding:5px 12px; border-radius:8px; font-size:0.8rem;">Streamlit Cloud</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Data sources
    st.markdown("""
    <div style="background:white; border-radius:14px; padding:1.5rem; border:1px solid #e5e7eb;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
        <h3 style="margin:0 0 0.8rem; color:#1f2937;">📚 Data Sources</h3>
        <p style="font-size:0.85rem; color:#4a5568; line-height:1.8; margin:0;">
            All data sourced from official government registries:
        </p>
        <ul style="font-size:0.82rem; color:#4a5568; line-height:2; margin:0.5rem 0 0; padding-left:1.2rem;">
            <li><strong>USA</strong> — Social Security Administration (SSA)</li>
            <li><strong>England & Wales</strong> — Office for National Statistics (ONS)</li>
            <li><strong>Canada</strong> — Provincial vital statistics agencies</li>
            <li><strong>Australia</strong> — State & territory registries</li>
            <li><strong>Scotland</strong> — National Records of Scotland (NRS)</li>
            <li><strong>Ireland</strong> — Central Statistics Office (CSO)</li>
            <li><strong>New Zealand</strong> — Department of Internal Affairs (DIA)</li>
            <li><strong>Northern Ireland</strong> — NISRA</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
