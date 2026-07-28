"""
Discoveries Tab — Full Page
"🎉 I Never Knew That"
"""
import streamlit as st
import plotly.graph_objects as go
from utils.charts import CHART_LAYOUT, COLORS, COUNTRY_COLORS


def render():
    # ─── Header ───────────────────────────────────────────────────
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #EEF2FF, #E8F4FD, #F0FFF4); 
                    border-radius: 16px; padding: 50px 30px; text-align: center; 
                    margin-bottom: 20px; border: 1px solid #E2E8F0;">
            <h1 style="font-size: 2.8em; font-weight: 800; color: #2D3748; margin: 0 0 12px 0;">
                🎉 I Never Knew That
            </h1>
            <p style="font-size: 1.2em; color: #4A5568; max-width: 650px; margin: 0 auto; line-height: 1.7;">
                Surprising stories hiding in 27 years of baby name data.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ══════════════════════════════════════════════════════════════
    # 🤖 CORPORATE ERASURE
    # ══════════════════════════════════════════════════════════════

    st.markdown("### 🤖 Corporate Erasure")
    st.markdown(
        "What happens when a tech giant names a product after a human name? "
        "The humans stop using it."
    )

    # ─── Alexa & Siri line charts ─────────────────────────────────
    alexa_data = {
        "year": [1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023],
        "frequency": [3398,3927,3926,3927,4197,4750,4938,4798,5039,6649,6348,5878,6063,5807,5288,5011,4785,4880,6702,5450,4535,3394,2128,1334,718,605,511]
    }

    siri_data = {
        "year": [1997,1998,1999,2000,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2017,2021,2023],
        "frequency": [8,7,9,5,6,25,33,65,68,66,83,94,69,66,10,11,8,3,3,7]
    }

    col_alexa, col_siri = st.columns(2)

    with col_alexa:
        fig_alexa = go.Figure()
        fig_alexa.add_trace(go.Scatter(
            x=alexa_data["year"],
            y=alexa_data["frequency"],
            mode="lines+markers",
            line=dict(color="#7C9FD6", width=3),
            marker=dict(size=5),
            fill="tozeroy",
            fillcolor="rgba(124,159,214,0.1)",
        ))
        fig_alexa.add_vline(x=2014, line_dash="dash", line_color="#E63946", opacity=0.7)
        fig_alexa.add_annotation(
            x=2014, y=6702,
            text="Amazon Echo<br>launches",
            showarrow=True, arrowhead=2,
            font=dict(size=10, color="#E63946"),
            ax=40, ay=-30
        )
        fig_alexa.update_layout(
            **CHART_LAYOUT,
            title="Alexa",
            xaxis_title="",
            yaxis_title="Babies per year",
            height=350,
        )
        st.plotly_chart(fig_alexa, use_container_width=True)

    with col_siri:
        fig_siri = go.Figure()
        fig_siri.add_trace(go.Scatter(
            x=siri_data["year"],
            y=siri_data["frequency"],
            mode="lines+markers",
            line=dict(color="#C8A8E8", width=3),
            marker=dict(size=5),
            fill="tozeroy",
            fillcolor="rgba(200,168,232,0.1)",
        ))
        fig_siri.add_vline(x=2011, line_dash="dash", line_color="#E63946", opacity=0.7)
        fig_siri.add_annotation(
            x=2011, y=94,
            text="Apple launches<br>Siri",
            showarrow=True, arrowhead=2,
            font=dict(size=10, color="#E63946"),
            ax=40, ay=-30
        )
        fig_siri.update_layout(
            **CHART_LAYOUT,
            title="Siri",
            xaxis_title="",
            yaxis_title="Babies per year",
            height=350,
        )
        st.plotly_chart(fig_siri, use_container_width=True)

    # ─── Before/After stat cards ──────────────────────────────────
    col_a1, col_a2, col_a3 = st.columns(3)

    with col_a1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #EEF2FF, #E8F4FD);
                    border-radius: 12px; padding: 20px; text-align: center;
                    border: 1px solid #E2E8F0;">
            <div style="font-size: 0.75em; color: #718096; text-transform: uppercase; letter-spacing: 1px;">
                Alexa — Peak (2015)
            </div>
            <div style="font-size: 2.2em; font-weight: 800; color: #7C9FD6;">
                6,702
            </div>
            <div style="font-size: 0.8em; color: #4A5568;">babies/year</div>
        </div>
        """, unsafe_allow_html=True)

    with col_a2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFF5F5, #FEE2E2);
                    border-radius: 12px; padding: 20px; text-align: center;
                    border: 1px solid #FECACA;">
            <div style="font-size: 0.75em; color: #718096; text-transform: uppercase; letter-spacing: 1px;">
                Alexa — Now (2023)
            </div>
            <div style="font-size: 2.2em; font-weight: 800; color: #E63946;">
                511
            </div>
            <div style="font-size: 0.8em; color: #4A5568;">−92% erased</div>
        </div>
        """, unsafe_allow_html=True)

    with col_a3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #F5F0FF, #EDE9FE);
                    border-radius: 12px; padding: 20px; text-align: center;
                    border: 1px solid #E2D9F3;">
            <div style="font-size: 0.75em; color: #718096; text-transform: uppercase; letter-spacing: 1px;">
                Siri — Peak → Now
            </div>
            <div style="font-size: 2.2em; font-weight: 800; color: #9B6FD4;">
                94 → 7
            </div>
            <div style="font-size: 0.8em; color: #4A5568;">−93% erased</div>
        </div>
        """, unsafe_allow_html=True)

    # ─── Insight text ─────────────────────────────────────────────
    st.markdown("")
    st.markdown(
        "**Alexa** was a top-100 name with nearly 7,000 babies a year. Amazon named their voice assistant after it in 2014 "
        "— and initially, the name *rose* (curiosity effect?). But by 2017, reports of children being bullied "
        "(*'Alexa, do my homework'*) began spreading. The collapse was swift: −92% in 6 years."
    )
    st.markdown(
        "**Siri** was a rising Scandinavian name — growing steadily from 8 babies (1997) to 94 (2010). "
        "Then Apple launched their voice assistant in October 2011. By 2013, just 10 babies were named Siri. "
        "A name that was *on its way up* was killed overnight by a product launch."
    )

    st.info(
        "💡 **The asymmetry:** Alexa had a bigger victim pool (6,702 babies/year) but Siri was the crueller kill "
        "— it was actively *growing* when Apple took it. Alexa was already past peak."
    )

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # ⚠️ BANNED FROM THE AIRWAVES (Controversial Names)
    # ══════════════════════════════════════════════════════════════

    st.markdown("### ⚠️ Banned from the Airwaves")
    st.markdown(
        "Some tracks don't fade naturally — they get **pulled from rotation**. "
        "A name can carry a thousand years of history, then lose it all in a single news cycle."
    )

    st.markdown("")

    # --- ISIS & OSAMA: "BROADCAST BAN" notices ---
    st.markdown("#### 📵 Emergency Broadcast Bans")
    st.markdown(
        "These names weren't declining. They were healthy, growing, beloved — "
        "until a global event made them radioactive overnight."
    )

    col_isis, col_osama = st.columns(2)

    with col_isis:
        isis_html = (
            '<div style="'
            'background: linear-gradient(135deg, #FFF5F5, #FED7D7, #FFF5F5);'
            'border: 2px solid #FC8181;'
            'border-radius: 16px;'
            'padding: 28px 24px;'
            'position: relative;'
            'overflow: hidden;'
            '">'
            '<div style="'
            'position: absolute;'
            'top: 50%;'
            'left: 50%;'
            'transform: translate(-50%, -50%) rotate(-25deg);'
            'font-size: 64px;'
            'font-weight: 900;'
            'color: rgba(229, 62, 62, 0.08);'
            'letter-spacing: 12px;'
            'white-space: nowrap;'
            'pointer-events: none;'
            '">BANNED</div>'
            '<div style="'
            'display: flex;'
            'align-items: center;'
            'gap: 12px;'
            'margin-bottom: 16px;'
            '">'
            '<div style="'
            'background: #E53E3E;'
            'color: white;'
            'padding: 4px 10px;'
            'border-radius: 4px;'
            'font-size: 11px;'
            'font-weight: 700;'
            'letter-spacing: 1px;'
            '">BROADCAST BAN</div>'
            '<span style="color: #A0AEC0; font-size: 12px;">June 2014</span>'
            '</div>'
            '<div style="'
            'font-size: 42px;'
            'font-weight: 800;'
            'color: #2D3748;'
            'margin-bottom: 4px;'
            'text-decoration: line-through;'
            'text-decoration-color: #E53E3E;'
            'text-decoration-thickness: 3px;'
            '">Isis</div>'
            '<div style="'
            'font-size: 13px;'
            'color: #718096;'
            'margin-bottom: 20px;'
            '">Egyptian goddess of magic &amp; motherhood</div>'
            '<div style="'
            'display: grid;'
            'grid-template-columns: 1fr 1fr;'
            'gap: 12px;'
            'margin-bottom: 16px;'
            '">'
            '<div style="background: white; border-radius: 8px; padding: 12px; text-align: center;">'
            '<div style="font-size: 11px; color: #A0AEC0; text-transform: uppercase; letter-spacing: 0.5px;">Before</div>'
            '<div style="font-size: 24px; font-weight: 700; color: #2D3748;">576</div>'
            '<div style="font-size: 11px; color: #718096;">babies/year (2007)</div>'
            '</div>'
            '<div style="background: white; border-radius: 8px; padding: 12px; text-align: center;">'
            '<div style="font-size: 11px; color: #A0AEC0; text-transform: uppercase; letter-spacing: 0.5px;">After</div>'
            '<div style="font-size: 24px; font-weight: 700; color: #E53E3E;">8</div>'
            '<div style="font-size: 11px; color: #718096;">babies/year (2018)</div>'
            '</div>'
            '</div>'
            '<div style="'
            'background: #E53E3E;'
            'color: white;'
            'border-radius: 8px;'
            'padding: 10px 16px;'
            'text-align: center;'
            'font-weight: 700;'
            'font-size: 18px;'
            'margin-bottom: 12px;'
            '">&minus;98.4%</div>'
            '<div style="'
            'background: rgba(72, 187, 120, 0.1);'
            'border-left: 3px solid #48BB78;'
            'padding: 8px 12px;'
            'border-radius: 0 8px 8px 0;'
            'font-size: 12px;'
            'color: #2F855A;'
            '">&#128225; Signal returning: 159 babies in 2023 — parents reclaiming the goddess</div>'
            '</div>'
        )
        st.markdown(isis_html, unsafe_allow_html=True)

    with col_osama:
        osama_html = (
            '<div style="'
            'background: linear-gradient(135deg, #FFF5F5, #FED7D7, #FFF5F5);'
            'border: 2px solid #FC8181;'
            'border-radius: 16px;'
            'padding: 28px 24px;'
            'position: relative;'
            'overflow: hidden;'
            '">'
            '<div style="'
            'position: absolute;'
            'top: 50%;'
            'left: 50%;'
            'transform: translate(-50%, -50%) rotate(-25deg);'
            'font-size: 64px;'
            'font-weight: 900;'
            'color: rgba(229, 62, 62, 0.08);'
            'letter-spacing: 12px;'
            'white-space: nowrap;'
            'pointer-events: none;'
            '">BANNED</div>'
            '<div style="'
            'display: flex;'
            'align-items: center;'
            'gap: 12px;'
            'margin-bottom: 16px;'
            '">'
            '<div style="'
            'background: #E53E3E;'
            'color: white;'
            'padding: 4px 10px;'
            'border-radius: 4px;'
            'font-size: 11px;'
            'font-weight: 700;'
            'letter-spacing: 1px;'
            '">BROADCAST BAN</div>'
            '<span style="color: #A0AEC0; font-size: 12px;">September 2001</span>'
            '</div>'
            '<div style="'
            'font-size: 42px;'
            'font-weight: 800;'
            'color: #2D3748;'
            'margin-bottom: 4px;'
            'text-decoration: line-through;'
            'text-decoration-color: #E53E3E;'
            'text-decoration-thickness: 3px;'
            '">Osama</div>'
            '<div style="'
            'font-size: 13px;'
            'color: #718096;'
            'margin-bottom: 20px;'
            '">Arabic: &quot;lion&quot; — a common name for centuries</div>'
            '<div style="'
            'display: grid;'
            'grid-template-columns: 1fr 1fr;'
            'gap: 12px;'
            'margin-bottom: 16px;'
            '">'
            '<div style="background: white; border-radius: 8px; padding: 12px; text-align: center;">'
            '<div style="font-size: 11px; color: #A0AEC0; text-transform: uppercase; letter-spacing: 0.5px;">Before</div>'
            '<div style="font-size: 24px; font-weight: 700; color: #2D3748;">71</div>'
            '<div style="font-size: 11px; color: #718096;">babies/year (1999)</div>'
            '</div>'
            '<div style="background: white; border-radius: 8px; padding: 12px; text-align: center;">'
            '<div style="font-size: 11px; color: #A0AEC0; text-transform: uppercase; letter-spacing: 0.5px;">After</div>'
            '<div style="font-size: 24px; font-weight: 700; color: #E53E3E;">3</div>'
            '<div style="font-size: 11px; color: #718096;">babies/year (2009)</div>'
            '</div>'
            '</div>'
            '<div style="'
            'background: #E53E3E;'
            'color: white;'
            'border-radius: 8px;'
            'padding: 10px 16px;'
            'text-align: center;'
            'font-weight: 700;'
            'font-size: 18px;'
            'margin-bottom: 12px;'
            '">&minus;96%</div>'
            '<div style="'
            'background: rgba(113, 128, 150, 0.1);'
            'border-left: 3px solid #718096;'
            'padding: 8px 12px;'
            'border-radius: 0 8px 8px 0;'
            'font-size: 12px;'
            'color: #4A5568;'
            '">USA dropped to 0 instantly. England held on 3 more years.</div>'
            '</div>'
        )
        st.markdown(osama_html, unsafe_allow_html=True)

    st.markdown("")
    st.markdown(
        "Two names. Two histories stretching back millennia. "
        "Both destroyed in under 24 months by a single association. "
        "Isis — the Egyptian goddess who reassembled Osiris and birthed Horus — "
        "became unsayable in a maternity ward. "
        "Osama — meaning 'lion' in Arabic, used for centuries across the Muslim world — "
        "vanished from American birth certificates within a year of September 11."
    )

    st.markdown("")

    # --- KAREN: "Death by Meme" ---
    st.markdown("#### 📉 Death by Meme")
    st.markdown(
        "Not every name dies from a single blow. Some are already fading — "
        "and then the internet decides to make them a punchline."
    )

    karen_html = (
        '<div style="'
        'background: linear-gradient(135deg, #EEF2FF, #E8F4FD, #F0FFF4);'
        'border: 2px solid #E2E8F0;'
        'border-radius: 16px;'
        'padding: 28px 32px;'
        'max-width: 700px;'
        '">'
        '<div style="'
        'display: flex;'
        'justify-content: space-between;'
        'align-items: center;'
        'margin-bottom: 20px;'
        '">'
        '<div>'
        '<div style="font-size: 36px; font-weight: 800; color: #2D3748;">Karen</div>'
        '<div style="font-size: 13px; color: #718096;">Peak popularity: 1960s (outside our dataset)</div>'
        '</div>'
        '<div style="'
        'background: #ECC94B;'
        'color: #744210;'
        'padding: 4px 10px;'
        'border-radius: 4px;'
        'font-size: 11px;'
        'font-weight: 700;'
        'letter-spacing: 1px;'
        '">FADING + MEME</div>'
        '</div>'
        '<div style="'
        'display: flex;'
        'align-items: center;'
        'gap: 0;'
        'margin-bottom: 20px;'
        '">'
        '<div style="text-align: center; flex: 1;">'
        '<div style="font-size: 20px; font-weight: 700; color: #2D3748;">2,588</div>'
        '<div style="font-size: 10px; color: #A0AEC0;">1997</div>'
        '</div>'
        '<div style="flex: 0.5; text-align: center; color: #CBD5E0; font-size: 20px;">&rarr;</div>'
        '<div style="text-align: center; flex: 1;">'
        '<div style="font-size: 20px; font-weight: 700; color: #718096;">563</div>'
        '<div style="font-size: 10px; color: #A0AEC0;">2017 (pre-meme)</div>'
        '</div>'
        '<div style="flex: 0.5; text-align: center;">'
        '<div style="font-size: 16px;">&#128128;</div>'
        '<div style="font-size: 9px; color: #E53E3E; font-weight: 600;">meme</div>'
        '</div>'
        '<div style="text-align: center; flex: 1;">'
        '<div style="font-size: 20px; font-weight: 700; color: #E53E3E;">204</div>'
        '<div style="font-size: 10px; color: #A0AEC0;">2021 (bottom)</div>'
        '</div>'
        '<div style="flex: 0.5; text-align: center; color: #CBD5E0; font-size: 20px;">&rarr;</div>'
        '<div style="text-align: center; flex: 1;">'
        '<div style="font-size: 20px; font-weight: 700; color: #48BB78;">238</div>'
        '<div style="font-size: 10px; color: #A0AEC0;">2023</div>'
        '</div>'
        '</div>'
        '<div style="'
        'background: rgba(236, 201, 75, 0.1);'
        'border-left: 3px solid #ECC94B;'
        'padding: 12px 16px;'
        'border-radius: 0 8px 8px 0;'
        'font-size: 13px;'
        'color: #744210;'
        'line-height: 1.5;'
        '">'
        '<strong>The difference:</strong> Karen was already on a 40-year decline. '
        "The &quot;Karen&quot; meme (2019-2020) didn't kill it — it accelerated an existing death. "
        'From 2017 to 2021, it dropped 64%. Without the meme, the generational curve suggests '
        'it would have fallen ~40% anyway. The meme added roughly 24 percentage points of extra damage.'
        '</div>'
        '</div>'
    )
    st.markdown(karen_html, unsafe_allow_html=True)

    st.markdown("")

    # --- Comparison / Insight ---
    st.markdown(
        "**The pattern:** Real-world violence creates **instant, total** bans "
        "(Isis: −98%, Osama: −96%). Internet culture creates **accelerated fades** "
        "(Karen: −64% in 4 years vs. an expected −40%). "
        "One is a cliff. The other is a steeper slope."
    )

    # Recovery comparison cards
    recovery_html = (
        '<div style="'
        'display: grid;'
        'grid-template-columns: 1fr 1fr 1fr;'
        'gap: 16px;'
        'margin-top: 16px;'
        '">'
        '<div style="'
        'background: linear-gradient(135deg, #F0FFF4, #C6F6D5);'
        'border: 1px solid #9AE6B4;'
        'border-radius: 12px;'
        'padding: 16px;'
        'text-align: center;'
        '">'
        '<div style="font-size: 13px; color: #276749; font-weight: 600;">Isis</div>'
        '<div style="font-size: 24px; font-weight: 800; color: #22543D; margin: 4px 0;">&uarr; recovering</div>'
        '<div style="font-size: 11px; color: #48BB78;">8 &rarr; 159 since 2018</div>'
        '</div>'
        '<div style="'
        'background: linear-gradient(135deg, #FFFFF0, #FEFCBF);'
        'border: 1px solid #ECC94B;'
        'border-radius: 12px;'
        'padding: 16px;'
        'text-align: center;'
        '">'
        '<div style="font-size: 13px; color: #744210; font-weight: 600;">Osama</div>'
        '<div style="font-size: 24px; font-weight: 800; color: #975A16; margin: 4px 0;">&#8599; slow return</div>'
        '<div style="font-size: 11px; color: #B7791F;">3 &rarr; 32 over 14 years</div>'
        '</div>'
        '<div style="'
        'background: linear-gradient(135deg, #FFF5F5, #FED7D7);'
        'border: 1px solid #FC8181;'
        'border-radius: 12px;'
        'padding: 16px;'
        'text-align: center;'
        '">'
        '<div style="font-size: 13px; color: #9B2C2C; font-weight: 600;">Karen</div>'
        '<div style="font-size: 24px; font-weight: 800; color: #C53030; margin: 4px 0;">&darr; still falling</div>'
        '<div style="font-size: 11px; color: #E53E3E;">generational decline continues</div>'
        '</div>'
        '</div>'
    )
    st.markdown(recovery_html, unsafe_allow_html=True)

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # 🧟 ZOMBIE NAMES
    # ══════════════════════════════════════════════════════════════

    st.markdown("### 🧟 Back from the Dead")
    st.markdown(
        "Some names flatline completely — years of silence, single digits, near-zero. "
        "Then something happens. A TV show. A cultural shift. A vibe change. "
        "And the name claws its way back."
    )

    st.markdown("")

    # ─── Top 5 Zombie Cards ───────────────────────────────────────
    zombies = [
        {"name": "Wren", "trough": 3, "trough_year": 1999, "peak": "2,596", "peak_year": 2022, "ratio": "865x", "trigger": "Nature names + cottagecore + gender-neutral trend", "color": "#48BB78"},
        {"name": "Salem", "trough": 9, "trough_year": 2000, "peak": "1,246", "peak_year": 2023, "ratio": "138x", "trigger": "WitchTok + Chilling Adventures of Sabrina (2018)", "color": "#9B6FD4"},
        {"name": "Tru", "trough": 6, "trough_year": 2011, "peak": "720", "peak_year": 2022, "ratio": "120x", "trigger": "Authenticity culture — true to yourself", "color": "#ECC94B"},
        {"name": "Octavia", "trough": 43, "trough_year": 2011, "peak": "1,577", "peak_year": 2021, "ratio": "37x", "trigger": "The 100 (CW, 2014-2020) — Octavia Blake", "color": "#F56565"},
        {"name": "Xena", "trough": 10, "trough_year": 2004, "peak": "278", "peak_year": 2022, "ratio": "28x", "trigger": "Streaming brought Warrior Princess to a new generation", "color": "#7C9FD6"},
    ]

    for z in zombies:
        name = z["name"]
        color = z["color"]
        ratio = z["ratio"]
        trigger = z["trigger"]
        trough = str(z["trough"])
        trough_year = str(z["trough_year"])
        peak = z["peak"]
        peak_year = str(z["peak_year"])

        card_html = (
            '<div style="'
            'background: linear-gradient(135deg, #EEF2FF, #E8F4FD, #F0FFF4);'
            'border: 1px solid #E2E8F0;'
            'border-radius: 16px;'
            'padding: 24px 28px;'
            'margin-bottom: 16px;'
            'display: grid;'
            'grid-template-columns: 1fr auto 1fr auto;'
            'align-items: center;'
            'gap: 24px;'
            '">'
            '<div>'
            '<div style="font-size: 28px; font-weight: 800; color: #2D3748;">'
            + name +
            '</div>'
            '<div style="font-size: 12px; color: #718096; margin-top: 4px;">'
            + trigger +
            '</div>'
            '</div>'
            '<div style="text-align: center;">'
            '<div style="font-size: 11px; color: #A0AEC0; text-transform: uppercase; letter-spacing: 0.5px;">Flatlined</div>'
            '<div style="font-size: 22px; font-weight: 700; color: #E53E3E;">'
            + trough +
            '</div>'
            '<div style="font-size: 10px; color: #718096;">'
            + trough_year +
            '</div>'
            '</div>'
            '<div style="font-size: 24px; color: ' + color + ';">&rarr;</div>'
            '<div style="text-align: center;">'
            '<div style="font-size: 11px; color: #A0AEC0; text-transform: uppercase; letter-spacing: 0.5px;">Comeback</div>'
            '<div style="font-size: 22px; font-weight: 700; color: ' + color + ';">'
            + peak +
            '</div>'
            '<div style="font-size: 10px; color: #718096;">'
            + peak_year + ' (' + ratio + ')'
            '</div>'
            '</div>'
            '</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("")

    # ─── Combined comeback chart ──────────────────────────────────
    st.markdown("#### The Comeback Curves")

    fig_zombie = go.Figure()

    chart_data = {
        "Wren": {"years": [1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023], "freqs": [3,6,5,14,11,17,24,54,41,86,107,159,203,288,419,504,569,855,1012,1053,1159,1325,1988,2596,2535], "color": "#48BB78"},
        "Salem": {"years": [1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023], "freqs": [34,18,40,9,44,43,40,43,55,46,54,56,70,77,57,84,88,150,220,263,305,327,564,711,951,1152,1246], "color": "#9B6FD4"},
        "Tru": {"years": [2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023], "freqs": [72,55,42,14,39,29,37,6,10,30,31,36,21,52,138,261,338,538,720,670], "color": "#ECC94B"},
        "Octavia": {"years": [1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023], "freqs": [220,233,202,177,156,176,128,74,143,84,67,91,79,47,43,63,53,66,279,391,682,943,1066,1152,1577,1509,1441], "color": "#F56565"},
        "Xena": {"years": [1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023], "freqs": [246,156,86,74,37,31,18,10,13,13,14,12,13,18,14,34,38,38,58,70,109,126,162,169,162,278,261], "color": "#7C9FD6"},
    }

    for name, data in chart_data.items():
        fig_zombie.add_trace(go.Scatter(
            x=data["years"],
            y=data["freqs"],
            mode="lines",
            name=name,
            line=dict(color=data["color"], width=2.5),
        ))

    fig_zombie.update_layout(
        **CHART_LAYOUT,
        title="",
        xaxis_title="",
        yaxis_title="Babies per year",
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
        ),
    )
    st.plotly_chart(fig_zombie, use_container_width=True)

    st.markdown(
        "**What brings a name back?** Streaming services resurrecting old shows (Xena). "
        "A breakout character on a new series (Octavia). Aesthetic movements that go viral "
        "(Salem, Wren). Or simply: culture circles back. The names that return aren't random — "
        "they carry a *vibe* that suddenly fits again."
    )

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # 4. 🌊 NATURAL DISASTER
    # ══════════════════════════════════════════════════════════════

    st.markdown("### 🌊 The Hurricane Effect")
    st.markdown("Hurricane Katrina hit in August 2005. The name never recovered.")

    katrina_years = [1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023]
    katrina_freq = [1964,1792,1734,1782,1655,1480,1442,1473,1612,1123,664,585,445,402,304,341,304,274,272,217,212,166,144,128,137,142,139]

    fig_katrina = go.Figure()
    fig_katrina.add_trace(go.Scatter(x=katrina_years, y=katrina_freq, mode="lines+markers",
        line=dict(color="#7C9FD6", width=3), marker=dict(size=5),
        fill="tozeroy", fillcolor="rgba(124,159,214,0.1)"))
    fig_katrina.add_vline(x=2005, line_dash="dash", line_color="#E63946", opacity=0.7)
    fig_katrina.add_annotation(x=2005, y=1612, text="Hurricane Katrina<br>Aug 2005",
        showarrow=True, arrowhead=2, font=dict(size=10, color="#E63946"), ax=50, ay=-20)
    fig_katrina.update_layout(**CHART_LAYOUT, title="Katrina", xaxis_title="", yaxis_title="Babies per year", height=350)
    st.plotly_chart(fig_katrina, use_container_width=True)

    col_k1, col_k2, col_k3 = st.columns(3)
    col_k1.metric("Before (2005)", "1,612")
    col_k2.metric("Year 2 (2007)", "664", "-59%")
    col_k3.metric("Now (2023)", "139", "-91%")

    st.markdown(
        "Unlike controversial names that sometimes recover (Isis is climbing back), "
        "natural disaster names seem permanently stained. 18 years later, Katrina is still at rock bottom."
    )

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # 5. 🕉️ SANSKRIT / INDIAN DIASPORA
    # ══════════════════════════════════════════════════════════════

    st.markdown("### 🕉️ Immigration Written in Names")
    st.markdown(
        "The Indian diaspora is large enough to register simultaneously in all 8 countries. "
        "Sanskrit names grew **+1,902%** in 27 years."
    )

    indian_years = list(range(1997, 2024))
    indian_totals_data = [924,1012,1150,1280,1450,1620,1890,2300,2850,3400,4100,4900,5600,6500,7400,8200,9100,10200,11500,12800,14200,15500,16800,17500,18000,18200,18503]

    fig_indian = go.Figure()
    fig_indian.add_trace(go.Scatter(x=indian_years, y=indian_totals_data, mode="lines+markers",
        line=dict(color="#F6AD55", width=3), marker=dict(size=4),
        fill="tozeroy", fillcolor="rgba(246,173,85,0.1)"))
    fig_indian.update_layout(**CHART_LAYOUT, title="Sanskrit/Indian Names — Total Across Anglosphere", xaxis_title="", yaxis_title="Babies per year", height=350)
    st.plotly_chart(fig_indian, use_container_width=True)

    st.markdown("**Top risers:**")
    col_i1, col_i2, col_i3, col_i4, col_i5 = st.columns(5)
    col_i1.metric("Aria", "8,819", "+9,384%")
    col_i2.metric("Zara", "2,840", "+593%")
    col_i3.metric("Ayaan", "1,163", "+29,075%")
    col_i4.metric("Aarav", "718", "+4,124%")
    col_i5.metric("Kiaan", "579", "+19,200%")

    st.markdown(
        "These names have LOW countryness (2-4) — they're shared equally across diaspora countries. "
        "Indian families name children the same way regardless of which country they're in."
    )

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # 6. ⚧️ GENDER-NEUTRAL NAMES
    # ══════════════════════════════════════════════════════════════

    st.markdown("### ⚧️ The Gender-Neutral Wave")
    st.markdown("Names that belong equally to boys and girls grew **84%** in 27 years.")

    neutral_years = list(range(1997, 2022))
    neutral_counts = [74,77,75,80,80,77,78,83,90,90,93,94,98,94,99,96,98,95,93,106,112,118,131,130,136]

    fig_neutral = go.Figure()
    fig_neutral.add_trace(go.Bar(x=neutral_years, y=neutral_counts,
        marker_color="#C8A8E8", opacity=0.8))
    fig_neutral.update_layout(**CHART_LAYOUT, title="Number of Gender-Neutral Names Per Year (>100 babies, >30% each sex)",
        xaxis_title="", yaxis_title="Count of names", height=350)
    st.plotly_chart(fig_neutral, use_container_width=True)

    st.markdown("**Most balanced names** (nearly 50/50 boy/girl):")
    st.markdown(
        "Riley (89% balanced), Casey (87%), Skyler (83%), Harley (82%), "
        "Jamie (53% M), Quinn (63% F), River (52% M), Phoenix (54% M)"
    )

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # 7. ✂️ NAMES GETTING SHORTER
    # ══════════════════════════════════════════════════════════════

    st.markdown("### ✂️ Names Are Shrinking")
    st.markdown("The average baby name lost a third of a letter in 27 years.")

    length_years = list(range(1997, 2024))
    avg_lengths = [6.06,6.04,6.02,6.00,5.97,5.95,5.91,5.89,5.88,5.88,5.87,5.86,5.85,5.84,5.83,5.82,5.82,5.82,5.81,5.81,5.79,5.77,5.76,5.75,5.72,5.74,5.73]

    fig_length = go.Figure()
    fig_length.add_trace(go.Scatter(x=length_years, y=avg_lengths, mode="lines+markers",
        line=dict(color="#4A5568", width=3), marker=dict(size=5)))
    fig_length.update_layout(**CHART_LAYOUT, title="Average Name Length (weighted by frequency)",
        xaxis_title="", yaxis_title="Letters", height=300, yaxis_range=[5.6, 6.15])
    st.plotly_chart(fig_length, use_container_width=True)

    col_l1, col_l2 = st.columns(2)
    col_l1.metric("Avg Length 1997", "6.06 letters")
    col_l2.metric("Avg Length 2023", "5.73 letters", "-0.33")

    st.markdown(
        "Short names (4 letters or fewer) grew from **13.7%** to **20.3%** of all babies. "
        "The winners: Mia, Leo, Ivy, Kai, Ava, Lux, Wren, Finn, Zoe, Max."
    )

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # 8. 😈 TABOO BREAKERS
    # ══════════════════════════════════════════════════════════════

    st.markdown("### 😈 Taboo Breakers")
    st.markdown("Some names should be impossible. But culture finds a way.")

    col_lucifer, col_adolf = st.columns(2)

    with col_lucifer:
        lucifer_years = [2016,2017,2018,2019,2020,2021,2022,2023]
        lucifer_freq = [10,13,11,20,29,37,77,57]
        fig_luc = go.Figure()
        fig_luc.add_trace(go.Bar(x=lucifer_years, y=lucifer_freq, marker_color="#9B6FD4"))
        fig_luc.update_layout(**CHART_LAYOUT, title="Lucifer — the taboo that broke", xaxis_title="", yaxis_title="Babies", height=300)
        st.plotly_chart(fig_luc, use_container_width=True)
        st.markdown(
            "**Zero** babies named Lucifer until 2016. Then Netflix's *Lucifer* (2016-2021) "
            "rebranded the devil as a charming protagonist. By 2022: **77 babies.**"
        )

    with col_adolf:
        st.markdown(
            '<div style="background: linear-gradient(135deg, #2D3748, #1A202C);'
            'border-radius: 16px; padding: 40px 24px; text-align: center;'
            'color: white; height: 280px; display: flex; flex-direction: column;'
            'justify-content: center;">'
            '<div style="font-size: 64px; margin-bottom: 12px;">0</div>'
            '<div style="font-size: 18px; font-weight: 700;">Adolf</div>'
            '<div style="font-size: 13px; color: #A0AEC0; margin-top: 8px;">'
            'Zero babies. 8 countries. 27 years.<br>The ultimate name death.'
            '</div>'
            '<div style="font-size: 11px; color: #718096; margin-top: 16px;">'
            '80+ years of erasure and counting'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # 9. 🎯 DIVERSITY EXPLOSION
    # ══════════════════════════════════════════════════════════════

    st.markdown("### 🎯 The Diversity Explosion")
    st.markdown("Parents are choosing more unique names than ever. The era of 'everyone is called John' is over.")

    col_unique, col_top10 = st.columns(2)

    with col_unique:
        unique_years = [1997,2000,2003,2006,2009,2012,2015,2018,2021,2023]
        unique_counts = [13889,14500,15200,17800,20100,22500,25000,28200,31500,33902]
        fig_uniq = go.Figure()
        fig_uniq.add_trace(go.Bar(x=unique_years, y=unique_counts, marker_color="#48BB78", opacity=0.8))
        fig_uniq.update_layout(**CHART_LAYOUT, title="Unique Names Per Year", xaxis_title="", yaxis_title="Count", height=300)
        st.plotly_chart(fig_uniq, use_container_width=True)

    with col_top10:
        top10_years = [1997,2005,2010,2015,2020,2023]
        top10_pct = [8.8,6.7,6.0,5.7,5.5,4.5]
        fig_top10 = go.Figure()
        fig_top10.add_trace(go.Scatter(x=top10_years, y=top10_pct, mode="lines+markers",
            line=dict(color="#E53E3E", width=3), marker=dict(size=8)))
        fig_top10.update_layout(**CHART_LAYOUT, title="Top-10 Names as % of All Babies", xaxis_title="", yaxis_title="%", height=300, yaxis_range=[3, 10])
        st.plotly_chart(fig_top10, use_container_width=True)

    col_d1, col_d2, col_d3 = st.columns(3)
    col_d1.metric("Unique Names", "33,902", "+144% since 1997")
    col_d2.metric("Top-10 Share", "4.5%", "was 8.8% in 1997")
    col_d3.metric("Name Pool", "2.4x bigger", "in 27 years")

    st.markdown(
        "In 1997, the top 10 names accounted for nearly 1 in 11 babies. "
        "By 2023, it's 1 in 22. The long tail of naming is getting longer every year."
    )

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # 10. 🌏 AU/NZ TWINS
    # ══════════════════════════════════════════════════════════════

    st.markdown("### 🌏 The Antipodean Twins")
    st.markdown(
        "Australia and New Zealand share a hemisphere, an accent, and a rivalry. "
        "But their names tell different stories."
    )

    col_au, col_nz = st.columns(2)

    with col_au:
        st.markdown(
            '<div style="background: linear-gradient(135deg, #FFFFF0, #FEFCBF);'
            'border-radius: 12px; padding: 20px; text-align: center;'
            'border: 1px solid #ECC94B;">'
            '<div style="font-size: 0.8em; color: #744210; text-transform: uppercase;">Australia</div>'
            '<div style="font-size: 2.5em; font-weight: 800; color: #975A16;">46</div>'
            '<div style="font-size: 0.85em; color: #744210;">locked names</div>'
            '<div style="font-size: 0.75em; color: #A0AEC0; margin-top: 8px;">'
            'Narelle, Peta, Kym, Pippa, Darcy'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    with col_nz:
        st.markdown(
            '<div style="background: linear-gradient(135deg, #F0FFF4, #C6F6D5);'
            'border-radius: 12px; padding: 20px; text-align: center;'
            'border: 1px solid #9AE6B4;">'
            '<div style="font-size: 0.8em; color: #276749; text-transform: uppercase;">New Zealand</div>'
            '<div style="font-size: 2.5em; font-weight: 800; color: #22543D;">176</div>'
            '<div style="font-size: 0.85em; color: #276749;">locked names</div>'
            '<div style="font-size: 0.75em; color: #A0AEC0; margin-top: 8px;">'
            'Ngaire, Aroha, Sione, Raewyn, Kauri'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown(
        "**New Zealand has 4x more locked names** than Australia — thanks to Te Reo Maori "
        "and Polynesian heritage. Australia's locked names are mostly Anglo slang "
        "(Narelle, Kym) while NZ's carry deep cultural meaning (Aroha = love, Kauri = native tree)."
    )
