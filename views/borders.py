import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import os
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
                💿 The Local Vinyl
            </h1>
            <p style="font-size: 1.2em; color: #4A5568; max-width: 650px; margin: 0 auto; line-height: 1.7;">
                Not every name makes it to the global playlist.<br>
                Some never leave the local record shop.
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
    # SECTION 1: QUIZ — Two columns (HTML card left, buttons right)
    # ══════════════════════════════════════════════════════════════

    # Pronunciation challenge data
    challenges = [
        {
            "name": "Sadhbh",
            "country": "🇮🇪 Ireland",
            "countryness": 8171,
            "actual": "SIVE (just one syllable!)",
            "hint": "Rhymes with a number between four and six.",
            "explain": "In Irish Gaelic, 'dh' and 'bh' are both silent between vowels. So Sa-dh-bh = just 'S' + 'ive'.",
            "audio_file": "sadhbh",
        },
        {
            "name": "Ngaire",
            "country": "🇳🇿 New Zealand",
            "countryness": 11270,
            "actual": "NY-ree",
            "hint": "The first two letters are actually one sound you already know.",
            "explain": "In Māori, 'Ng' is a single consonant — the same sound as the 'ng' in 'singing', but at the start.",
            "audio_file": "ngaire",
        },
        {
            "name": "Frédérique",
            "country": "🇨🇦 Canada",
            "countryness": 10588,
            "actual": "fray-day-REEK",
            "hint": "The accents aren't decorative — each one changes a vowel.",
            "explain": "In French, 'é' always sounds like 'ay'. Three é's = three 'ay' sounds: fray-day-reek.",
            "audio_file": "frederique",
        },
        {
            "name": "Caoimhín",
            "country": "🏴 N. Ireland",
            "countryness": 465,
            "actual": "KEE-veen",
            "hint": "You already know this name — just not in this spelling.",
            "explain": "It's literally 'Kevin' in Irish! 'Aoi' = 'ee', 'mh' = 'v', 'ín' = 'een'. Kevin → Kee-veen.",
            "audio_file": "caoimhin",
        },
        {
            "name": "Ffion",
            "country": "🏴󠁧󠁢󠁷󠁬󠁳󠁿 Wales",
            "countryness": 1761,
            "actual": "FEE-on",
            "hint": "In Welsh, one of these letters is lying to you.",
            "explain": "Welsh rule: 'ff' = English 'f' sound. A single 'f' in Welsh = English 'v' sound. So 'Ffion' = 'Fee-on'.",
            "audio_file": "ffion",
        },
    ]

    # Session state
    if "challenge_idx" not in st.session_state:
        st.session_state.challenge_idx = 0
    if "revealed" not in st.session_state:
        st.session_state.revealed = False
    if "show_hint" not in st.session_state:
        st.session_state.show_hint = False

    challenge = challenges[st.session_state.challenge_idx]
    c_name = challenge["name"]
    c_country = challenge["country"]
    c_idx = st.session_state.challenge_idx + 1
    c_total = len(challenges)

    # ─── Section heading ──────────────────────────────────────────
    st.markdown("### 🎤 Can You Say This?")
    st.markdown(
        "These names are **cultural passwords** — if you can't say them, "
        "they'll never leave their home country. Give it a try!"
    )

    # ─── Two columns: HTML card (vinyl+name) | Buttons ────────────
    col_card, col_buttons = st.columns([2, 0.8], vertical_alignment="center")

    with col_card:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #EEF2FF, #E8F4FD, #F0FFF4);
                    border-radius: 16px; padding: 28px 24px;
                    border: 1px solid #E2E8F0;
                    display: flex; align-items: center; justify-content: center; gap: 30px; flex-wrap: wrap;">
            <div style="flex-shrink: 0;">
                <svg width="150" height="150" viewBox="0 0 220 220">
                    <circle cx="110" cy="110" r="100" fill="#2D3748" stroke="#4A5568" stroke-width="1"/>
                    <circle cx="110" cy="110" r="90" fill="none" stroke="#3D4A5C" stroke-width="0.5"/>
                    <circle cx="110" cy="110" r="80" fill="none" stroke="#354258" stroke-width="0.5"/>
                    <circle cx="110" cy="110" r="70" fill="none" stroke="#3D4A5C" stroke-width="0.5"/>
                    <circle cx="110" cy="110" r="60" fill="none" stroke="#354258" stroke-width="0.5"/>
                    <circle cx="110" cy="110" r="50" fill="none" stroke="#3D4A5C" stroke-width="0.5"/>
                    <circle cx="110" cy="110" r="35" fill="#7C9FD6" opacity="0.9"/>
                    <circle cx="110" cy="110" r="28" fill="none" stroke="#5A82BE" stroke-width="0.8"/>
                    <circle cx="110" cy="110" r="18" fill="#2D3748"/>
                    <circle cx="110" cy="110" r="5" fill="#4A5568"/>
                    <circle cx="110" cy="110" r="3" fill="#2D3748"/>
                </svg>
            </div>
            <div style="text-align: center; min-width: 160px;">
                <div style="font-size: 0.7em; color: #718096; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 6px;">
                    SIDE {c_idx} OF {c_total}
                </div>
                <div style="font-size: 2.4em; font-weight: 800; color: #2D3748; font-family: Georgia, serif; margin: 4px 0;">
                    {c_name}
                </div>
                <div style="font-size: 1em; color: #4A5568; margin-top: 4px;">
                    {c_country}
                </div>
                <div style="background: rgba(124,159,214,0.12); border-radius: 8px; padding: 5px 14px; margin-top: 12px; display: inline-block; border: 1px solid rgba(124,159,214,0.25);">
                    <span style="font-size: 0.72em; color: #5A82BE; letter-spacing: 1px;">🎵 LOCAL VINYL RECORDS</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_buttons:
        if st.button("💡 Hint", use_container_width=True, key="btn_hint"):
            st.session_state.show_hint = True

        if st.button("🔊 Reveal", use_container_width=True, key="btn_reveal"):
            st.session_state.revealed = True

        if st.button("➡️ Next", use_container_width=True, key="btn_next"):
            st.session_state.challenge_idx = (st.session_state.challenge_idx + 1) % len(challenges)
            st.session_state.revealed = False
            st.session_state.show_hint = False
            st.rerun()

    # ─── Hint ─────────────────────────────────────────────────────
    if st.session_state.get("show_hint"):
        st.info(f'💡 {challenge["hint"]}')

    # ─── Progress dots ────────────────────────────────────────────
    dots = ""
    for i in range(len(challenges)):
        dots += "● " if i == st.session_state.challenge_idx else "○ "
    st.caption(dots)

    # ─── Reveal section ───────────────────────────────────────────
    if st.session_state.revealed:
        c_actual = challenge["actual"]
        c_explain = challenge["explain"]
        c_countryness = challenge["countryness"]

        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #F0FFF4, #E6FFF5); 
                        border: 2px solid #A8E6C8; border-radius: 12px;
                        padding: 18px; text-align: center; margin-top: 10px;">
                <div style="font-size: 0.75em; color: #059669; text-transform: uppercase; 
                            letter-spacing: 2px;">▶ Now Playing:</div>
                <div style="font-size: 1.8em; font-weight: 700; color: #059669; margin: 6px 0;">
                    "{c_actual}"
                </div>
                <div style="font-size: 0.85em; color: #4A5568; margin-top: 8px; 
                            background: rgba(6,214,160,0.08); border-radius: 6px; padding: 8px 12px;">
                    📖 {c_explain}
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
            with open(audio_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/wav", autoplay=True)
        else:
            st.caption("🔈 Audio clip coming soon!")

        # Countryness fact
        st.markdown(
            f"""
            <div style="background: #FFF5F5; border-radius: 8px; padding: 10px; 
                        margin-top: 10px; text-align: center; font-size: 0.9em;">
                <span style="color: #e63946; font-weight: 600;">
                    Countryness: {c_countryness:,}
                </span>
                <span style="color: #718096;"> — A name {c_countryness:,}x more popular in </span>
                <span style="font-weight: 600;">{c_country}</span>
                <span style="color: #718096;"> than anywhere else</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")


    # ══════════════════════════════════════════════════════════════
    # SECTION 2: WHAT STAYED IN THE SHOP
    # ══════════════════════════════════════════════════════════════

    st.markdown("### 🏪 What Stayed in the Shop?")
    st.markdown(
        "Could you read all of those? Probably not — and that's the point. "
        "But before we explore *why*, we need a way to **measure** how locked a name is."
    )

    # ─── Formula + Classification side by side ────────────────────
    st.markdown("""
    <style>
    .info-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:20px 0;}
    .info-card{background:linear-gradient(135deg,#EEF2FF,#E8F4FD);border:1px solid #E2E8F0;border-radius:12px;display:flex;flex-direction:column;padding:24px;box-sizing:border-box;}
    .small-title{text-transform:uppercase;letter-spacing:2px;font-size:0.72rem;color:#7C9FD6;text-align:center;margin-bottom:8px;}
    .main-title{text-align:center;font-size:1.45rem;font-weight:800;color:#2D3748;margin-bottom:4px;}
    .subtitle{text-align:center;color:#4A5568;font-size:.88rem;margin-bottom:18px;}
    .formula-box{background:white;border-radius:8px;border:1px solid #E2E8F0;padding:18px;}
    .formula-top{text-align:center;font-family:Courier New;color:#7C9FD6;font-weight:700;border-bottom:2px solid #2D3748;padding-bottom:8px;}
    .formula-bottom{text-align:center;font-family:Courier New;color:#718096;font-weight:700;padding-top:8px;}
    .note-box{margin-top:18px;padding:12px;background:rgba(124,159,214,.08);border-radius:8px;font-size:.8rem;line-height:1.6;color:#4A5568;}
    .info-card table{width:100%;border-collapse:collapse;font-size:.83rem;}
    .info-card th{text-align:left;padding:8px;border-bottom:2px solid #CBD5E0;color:#4A5568;}
    .info-card td{padding:8px;border-bottom:1px solid #E2E8F0;color:#4A5568;}
    .info-card tr:last-child td{border-bottom:none;}
    @media (max-width:900px){.info-grid{grid-template-columns:1fr;}}
    </style>

    <div class="info-grid">
      <div class="info-card">
        <div class="small-title">HOW WE MEASURED IT</div>
        <div class="main-title">The Countryness Score</div>
        <div class="subtitle">How many times more popular is this name at <strong>home</strong> vs <strong>abroad</strong>?</div>
        <div class="formula-box">
          <div class="formula-top">proportion in top country</div>
          <div class="formula-bottom">avg proportion in other countries</div>
        </div>
        <div class="note-box">
          <b style="color:#7C9FD6;">Proportion</b> = how many babies out of ALL babies born that year received the name.
          <br><br>
          Example: <b>2,450 Niamhs</b> out of <b>100,000 Irish babies</b> = <b>0.0245</b> (2.45%)
        </div>
      </div>

      <div class="info-card">
        <div class="small-title">HOW WE CLASSIFIED THEM</div>
        <div class="main-title">The Classification</div>
        <div class="subtitle">Not all locked names are locked equally.</div>
        <table>
          <thead>
            <tr><th>Label</th><th>Score</th><th>Meaning</th></tr>
          </thead>
          <tbody>
            <tr><td style="color:#059669;font-weight:600;">✅ Global</td><td><b>&lt;5</b></td><td><b>Shared — no single home</b></td></tr>
            <tr><td style="color:#B7791F;font-weight:600;">⚠️ Leaning</td><td><b>5–10</b></td><td><b>Concentrating in one place</b></td></tr>
            <tr><td style="color:#C53030;font-weight:600;">🔒 Locked</td><td><b>10–100</b></td><td><b>Clearly belongs to one country</b></td></tr>
            <tr><td style="color:#9B2C2C;font-weight:600;">🔐 Very Locked</td><td><b>100–1,000</b></td><td><b>Barely exists elsewhere</b></td></tr>
            <tr><td style="color:#742A2A;font-weight:600;">🚫 Extreme</td><td><b>1,000+</b></td><td><b>A cultural password</b></td></tr>
          </tbody>
        </table>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ─── Paragraph explanation (full width below) ─────────────────
    st.markdown(
        "A score below **5** means a name is genuinely shared — it's roughly equally popular "
        "across all countries. Think *Liam*, *Thomas*, *Emily*. No single country owns them. "
        "Once a name crosses **5**, something shifts. Over **62%** of all babies with that name "
        "are concentrated in a single country. It's no longer shared — it's *leaning*. "
        "By the time you hit **50–100**, nearly **88%** of the name's usage is in one place. "
        "These names — like *Siobhan* or *Conor* — are clearly Irish, clearly Scottish, clearly somewhere specific. "
        "And at **1,000+**? Over **97%** of all babies with that name live in one country. "
        "These are cultural passwords — names like *Narelle* (Australia) or *Sadhbh* (Ireland) "
        "that effectively don't exist anywhere else on Earth. "
        "We drew the line at **5** because that's the tipping point: "
        "below it, a name belongs to everyone. Above it, one country **owns** it."
    )

    # ─── Sample Local Collection: CD Cases (HTML) ─────────────────
    st.markdown("#### 🎵 Sample Local Collection")
    st.markdown(
        "Just like B-side tracks, these are names that are hardly listened to "
        "outside their home country."
    )

    tapes = [
        ("Northern Ireland", "65%", "#9FE6C8", [("Éireann", 1414), ("Roisé", 1373), ("Dáithí", 892), ("Ruadhán", 756), ("Cianán", 623)]),
        ("Ireland", "55%", "#A8E6C8", [("Naoise", 1086), ("Sadhbh", 905), ("Iarla", 743), ("Laoise", 612), ("Aoibhínn", 589)]),
        ("Scotland", "52%", "#C8A8E8", [("Innes", 1187), ("Ruairidh", 976), ("Munro", 654), ("Murdo", 521), ("Breagha", 489)]),
        ("USA", "44%", "#A8D8F0", [("Kaylani", 312), ("Anahi", 287), ("Tadeo", 245), ("Itzel", 198), ("Malani", 176)]),
        ("Canada", "36%", "#F5B7C5", [("Édouard", 1106), ("Éloi", 894), ("Ludovic", 756), ("Frédérique", 623), ("Noélie", 534)]),
        ("New Zealand", "36%", "#C8A8E8", [("Kauri", 867), ("Manaia", 745), ("Ardie", 612), ("Nikau", 534), ("Amarni", 423)]),
        ("England & Wales", "35%", "#F5D68A", [("Barney", 87), ("Isla-rose", 234), ("Delilah-rose", 198), ("Tommy-lee", 167), ("Ffion", 1761)]),
        ("Australia", "23%", "#F5C878", [("Narelle", 4738), ("Darcy", 56), ("Pippa", 43), ("Billie", 38), ("Matilda", 12)]),
    ]

    tape_html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; margin: 16px 0;">'

    for t_country, t_pct, t_color, t_names in tapes:
        tracks = ""
        for i, (n, score) in enumerate(t_names):
            tracks += (
                '<div style="display: flex; justify-content: space-between; align-items: center; padding: 3px 0;">'
                '<span style="font-size: 0.8em; color: #4A5568; font-weight: 600;">'
                + str(i + 1) + '. ' + n + '</span>'
                '<span style="font-size: 0.72em; font-weight: 700; color: #718096;">'
                + f'{score:,}' + '</span>'
                '</div>'
            )

        tape_html += (
            # Outer case
            '<div style="background: linear-gradient(145deg, ' + t_color + '35, ' + t_color + '20); border-radius: 6px;'
            ' padding: 0; overflow: hidden; border: 1px solid ' + t_color + '60;'
            ' box-shadow: 0 4px 12px rgba(0,0,0,0.12), inset 0 1px 0 rgba(255,255,255,0.05);'
            ' position: relative;">'
            # Spine
            '<div style="position: absolute; left: 0; top: 0; bottom: 0; width: 7px;'
            ' background: ' + t_color + ';'
            ' box-shadow: 1px 0 4px rgba(0,0,0,0.4);"></div>'
            # Top section
            '<div style="padding: 14px 14px 10px 22px; border-bottom: 1px solid ' + t_color + '40;'
            ' position: relative; min-height: 60px;">'
            # Cassette icon (top right)
            '<div style="position: absolute; top: 10px; right: 12px;">'
            '<svg width="52" height="36" viewBox="0 0 52 36">'
            '<rect x="1" y="1" width="50" height="34" rx="4" fill="#2D3748" stroke="#4A5568" stroke-width="1.5"/>'
            '<rect x="8" y="6" width="36" height="16" rx="2" fill="#1A202C" stroke="#4A5568" stroke-width="0.8"/>'
            '<circle cx="18" cy="14" r="5" fill="none" stroke="' + t_color + '" stroke-width="1.5"/>'
            '<circle cx="34" cy="14" r="5" fill="none" stroke="' + t_color + '" stroke-width="1.5"/>'
            '<circle cx="18" cy="14" r="1.5" fill="' + t_color + '"/>'
            '<circle cx="34" cy="14" r="1.5" fill="' + t_color + '"/>'
            '<line x1="23" y1="14" x2="29" y2="14" stroke="#4A5568" stroke-width="0.8"/>'
            '<rect x="12" y="25" width="28" height="6" rx="1" fill="#4A5568"/>'
            '</svg>'
            '</div>'
            # Country title
            '<div style="font-weight: 700; font-size: 0.9em; color: #2D3748;">'
            + t_country +
            "</div>"
            '<div style="font-size: 0.72em; color: #4A5568; margin-top: 3px; font-weight: 600;">'
            + t_pct + ' locked'
            "</div>"
            "</div>"
            # Track listing
            '<div style="padding: 10px 14px 12px 22px; background: ' + t_color + '15;">'
            '<div style="font-size: 0.6em; color: #718096; text-transform: uppercase;'
            ' letter-spacing: 1.5px; margin-bottom: 5px; font-weight: 600;">TRACKLIST</div>'
            + tracks +
            "</div>"
            "</div>"
        )

    tape_html += "</div>"
    st.markdown(tape_html, unsafe_allow_html=True)

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # SECTION 3: REASONS — Storyline Flow
    # ══════════════════════════════════════════════════════════════

    # ─── Intro ────────────────────────────────────────────────────
    st.markdown("### 🎧 What Keeps a Track Off the Global Playlist?")
    st.markdown(
        "Sometimes the lyrics are unreadable. Sometimes the cover exists in another language. "
        "Sometimes the artist chooses to stay underground. And sometimes — they press a record "
        "that was never meant to leave town."
    )

    st.markdown("---")

        # ══════════════════════════════════════════════════════════════
    # 🏷️ CAN'T READ THE LYRICS (Pronunciation Wall)
    # ══════════════════════════════════════════════════════════════

    st.markdown("### 🏷️ Can't Read the Lyrics")
    st.markdown(
        "The first wall is the simplest: if you can't read a name, you won't use it. "
        "**Same origin. Different fate.** Here's what that looks like:"
    )

    # ─── Part 1: Mini distribution sheets ─────────────────────────

    def mini_distribution_sheet(track, score, catalog, date, status, status_color, status_angle, shipped_count):
        html = (
            '<div style="background:linear-gradient(135deg,#F5F0E4,#EDE8D8,#F8F4EA);'
            'border:1px solid #C4AD82;border-radius:6px;padding:16px 18px;'
            'font-family:Courier New,monospace;box-shadow:0 4px 12px rgba(0,0,0,.08);'
            'position:relative;overflow:hidden;">'
            '<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) rotate('
            + str(status_angle) + 'deg);font-size:.85rem;font-weight:900;letter-spacing:3px;color:'
            + status_color + ';opacity:.10;white-space:nowrap;">' + status + '</div>'
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">'
            '<div>'
            '<div style="font-size:.5rem;letter-spacing:3px;color:#8D7555;font-weight:700;">POLARIS RECORDS</div>'
            '<div style="font-size:.45rem;color:#A89268;margin-top:1px;">DISTRIBUTION DEPT.</div>'
            '</div>'
            '<div style="text-align:right;">'
            '<div style="font-size:.5rem;color:#8D7555;font-weight:600;">' + catalog + '</div>'
            '<div style="font-size:.45rem;color:#A89268;margin-top:1px;">' + date + '</div>'
            '</div>'
            '</div>'
            '<div style="text-align:center;border-top:1px solid #CBB996;border-bottom:1px solid #CBB996;'
            'padding:10px 0;margin-bottom:10px;">'
            '<div style="display:inline-flex;align-items:center;gap:8px;">'
            '<svg width="18" height="18" viewBox="0 0 24 24">'
            '<circle cx="12" cy="12" r="11" fill="#2D3748"/>'
            '<circle cx="12" cy="12" r="4" fill="#7C9FD6" opacity=".8"/>'
            '<circle cx="12" cy="12" r="2" fill="#2D3748"/>'
            '</svg>'
            '<span style="font-size:1.4rem;font-weight:800;font-family:Georgia;color:#2D3748;">' + track + '</span>'
            '</div>'
            '<div style="font-size:.65rem;color:#7B6A54;margin-top:4px;">'
            'Origin: Ireland &nbsp;|&nbsp; Countryness: <b>' + score + '</b>'
            '</div></div>'
            '<div style="display:flex;justify-content:space-between;align-items:center;">'
            '<div style="font-size:.65rem;color:#8D7555;">'
            'Shipped to <b>' + shipped_count + '</b> of 8 territories'
            '</div>'
            '<span style="padding:4px 10px;border:1.5px solid ' + status_color + ';border-radius:3px;'
            'font-weight:800;letter-spacing:1.5px;font-size:.55rem;color:' + status_color + ';">'
            + status + '</span>'
            '</div>'
            '<div style="margin-top:10px;padding-top:8px;border-top:1px solid #CBB996;text-align:right;">'
            '<svg width="50" height="14" viewBox="0 0 50 14">'
            '<rect x="0" y="0" width="1.5" height="12" fill="#2D3748"/>'
            '<rect x="3" y="0" width="1" height="12" fill="#2D3748"/>'
            '<rect x="5.5" y="0" width="2" height="12" fill="#2D3748"/>'
            '<rect x="9" y="0" width="1" height="12" fill="#2D3748"/>'
            '<rect x="11.5" y="0" width="1.5" height="12" fill="#2D3748"/>'
            '<rect x="14.5" y="0" width="1" height="12" fill="#2D3748"/>'
            '<rect x="17" y="0" width="2" height="12" fill="#2D3748"/>'
            '<rect x="20.5" y="0" width="1" height="12" fill="#2D3748"/>'
            '<rect x="23" y="0" width="1.5" height="12" fill="#2D3748"/>'
            '<rect x="26" y="0" width="1" height="12" fill="#2D3748"/>'
            '<rect x="28.5" y="0" width="2" height="12" fill="#2D3748"/>'
            '<rect x="32" y="0" width="1" height="12" fill="#2D3748"/>'
            '<rect x="34.5" y="0" width="1.5" height="12" fill="#2D3748"/>'
            '</svg>'
            '</div>'
            '</div>'
        )
        return html

    declan = mini_distribution_sheet(
        track="Declan",
        score="2.5",
        catalog="CAT# IRL-1997-007",
        date="DIST. 1997–2023",
        status="WORLDWIDE",
        status_color="#059669",
        status_angle=-15,
        shipped_count="8",
    )

    niamh = mini_distribution_sheet(
        track="Niamh",
        score="28",
        catalog="CAT# IRL-1997-042",
        date="DIST. 1997–2023",
        status="LOCAL ONLY",
        status_color="#DC2626",
        status_angle=-12,
        shipped_count="3",
    )

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown(declan, unsafe_allow_html=True)
    with col_right:
        st.markdown(niamh, unsafe_allow_html=True)

    st.markdown("")
    st.markdown(
        "Both names are Irish. Both are common. But **Declan** is phonetically transparent — "
        "anyone can read it and say it. **Niamh** (pronounced *NEEV*) requires insider knowledge. "
        "Even the 3 countries it reached — England, Ireland, and Northern Ireland — all have "
        "significant Irish-speaking communities. Outside that circle, nobody picks it up because "
        "nobody knows how to say it. "
        "And this isn't unique to Ireland. Every country in the Anglosphere has its own "
        "phonetic code — a set of spelling rules that only locals can decode. "
        "Pick a country to hear the phonetics behind their names:"
    )

    # ─── Part 2: Music Sheet Phonetics (large SVG, varied notes) ──
    import streamlit.components.v1 as components
    
    # Station data — each rule has (pattern, sound, y_position, note_type)
    # note_type: "quarter" (consonant), "eighth" (vowel), "double" (diphthong), "rest" (silent)
    stations = {
        "Ireland": {
            "language": "Gaeilge",
            "subtitle": "Irish Gaelic",
            "color": "#4CAF78",
            "rules": [
                ("bh / mh", "'v'", 148, "quarter"),
                ("dh / gh", "silent", 190, "rest"),
                ("aoi", "'ee'", 128, "eighth"),
                ("fh", "silent", 170, "rest"),
            ]
        },
        "Scotland": {
            "language": "Gàidhlig",
            "subtitle": "Scottish Gaelic",
            "color": "#9B6FD4",
            "rules": [
                ("idh / aidh", "silent 'ee'", 180, "rest"),
                ("eo", "'aw'", 140, "eighth"),
                ("gh", "silent", 168, "rest"),
                ("mh", "'v'", 148, "quarter"),
            ]
        },
        "Canada": {
            "language": "Français",
            "subtitle": "Canadian French",
            "color": "#E07098",
            "rules": [
                ("é / è", "'ay'", 135, "eighth"),
                ("-ique", "'eek'", 155, "eighth"),
                ("oi", "'wa'", 175, "double"),
                ("ç", "'s'", 145, "quarter"),
            ]
        },
        "New Zealand": {
            "language": "Te Reo",
            "subtitle": "Māori",
            "color": "#D4940F",
            "rules": [
                ("ng-", "one sound", 160, "quarter"),
                ("wh", "'f'", 138, "quarter"),
                ("au", "'ow'", 180, "double"),
                ("vowels", "all said", 148, "eighth"),
            ]
        },
        "Wales": {
            "language": "Cymraeg",
            "subtitle": "Welsh",
            "color": "#C4920F",
            "rules": [
                ("ff", "'f'", 140, "quarter"),
                ("ll", "breathy 'l'", 168, "quarter"),
                ("dd", "'th'", 130, "quarter"),
                ("f", "'v'", 185, "quarter"),
            ]
        },
    }

    # Pills — country names
    country_names = list(stations.keys())
    selected_country = st.pills(
        "Each country's phonetic code",
        country_names,
        default=country_names[0],
        key="jukebox_dial",
        label_visibility="collapsed"
    )

    if selected_country:
        station = stations[selected_country]
        language = station["language"]
        subtitle = station["subtitle"]
        color = station["color"]
        rules = station["rules"]

        # SVG dimensions — wide and uses full space
        SVG_WIDTH = 1000
        SVG_HEIGHT = 420
        STAFF_LEFT = 80
        STAFF_RIGHT = 960
        STAFF_TOP = 80
        STAFF_GAP = 24

        num_notes = len(rules)
        # Notes spread evenly across staff
        note_start = 180
        note_end = STAFF_RIGHT - 60
        note_spacing = (note_end - note_start) / (num_notes - 1) if num_notes > 1 else 0

        # Build SVG
        svg = (
            '<svg width="880" height="380" viewBox="0 0 '
            + str(SVG_WIDTH) + ' ' + str(SVG_HEIGHT)
            + '" style="display:block; max-width:100%;">'
            '<style>'
            '.note { cursor:pointer; }'
            '.note:hover { opacity:0.7; }'
            '.staff-line { stroke:#B8C5D4; stroke-width:2; }'
            '.bar-line { stroke:' + color + '; stroke-width:2.5; opacity:0.25; }'
            '.rule-text { font-size:20px; font-weight:700; fill:#2D3748; font-family:monospace; }'
            '.sound-text { font-size:16px; fill:#718096; font-style:italic; }'
            '</style>'
        )

        # 5 staff lines
        for i in range(5):
            y = STAFF_TOP + i * STAFF_GAP
            svg += (
                '<line x1="' + str(STAFF_LEFT) + '" y1="' + str(y)
                + '" x2="' + str(STAFF_RIGHT) + '" y2="' + str(y)
                + '" class="staff-line"/>'
            )

        # Treble clef
        svg += (
            '<text x="20" y="' + str(STAFF_TOP + 72)
            + '" font-size="110" fill="#8092AF" font-family="serif"'
            ' style="user-select:none;">&#119070;</text>'
        )

        # Bar lines between notes
        for i in range(1, num_notes):
            bar_x = note_start + int(i * note_spacing) - int(note_spacing / 2)
            svg += (
                '<line x1="' + str(bar_x) + '" y1="' + str(STAFF_TOP - 12)
                + '" x2="' + str(bar_x) + '" y2="' + str(STAFF_TOP + 4 * STAFF_GAP + 12)
                + '" class="bar-line"/>'
            )

        # Draw different note shapes
        for i, (pattern, sound, note_y, ntype) in enumerate(rules):
            x = note_start + int(i * note_spacing)

            if ntype == "quarter":
                # Single filled note + stem
                svg += (
                    '<g class="note" data-idx="' + str(i) + '">'
                    '<rect x="' + str(x - 20) + '" y="' + str(note_y - 65)
                    + '" width="40" height="80" fill="transparent"/>'
                    '<ellipse cx="' + str(x) + '" cy="' + str(note_y)
                    + '" rx="14" ry="10" fill="' + color
                    + '" transform="rotate(-20 ' + str(x) + ' ' + str(note_y) + ')"/>'
                    '<line x1="' + str(x + 12) + '" y1="' + str(note_y)
                    + '" x2="' + str(x + 12) + '" y2="' + str(note_y - 60)
                    + '" stroke="' + color + '" stroke-width="3.5"/>'
                    '</g>'
                )

            elif ntype == "eighth":
                # Single note + stem + flag
                svg += (
                    '<g class="note" data-idx="' + str(i) + '">'
                    '<rect x="' + str(x - 20) + '" y="' + str(note_y - 65)
                    + '" width="40" height="80" fill="transparent"/>'
                    '<ellipse cx="' + str(x) + '" cy="' + str(note_y)
                    + '" rx="14" ry="10" fill="' + color
                    + '" transform="rotate(-20 ' + str(x) + ' ' + str(note_y) + ')"/>'
                    '<line x1="' + str(x + 12) + '" y1="' + str(note_y)
                    + '" x2="' + str(x + 12) + '" y2="' + str(note_y - 60)
                    + '" stroke="' + color + '" stroke-width="3.5"/>'
                    # Flag (curved line from top of stem)
                    '<path d="M' + str(x + 12) + ' ' + str(note_y - 60)
                    + ' q 12 15 4 35" fill="none" stroke="' + color + '" stroke-width="3"/>'
                    '</g>'
                )

            elif ntype == "double":
                # Two notes beamed together
                x1 = x - 14
                x2 = x + 14
                svg += (
                    '<g class="note" data-idx="' + str(i) + '">'
                    '<rect x="' + str(x1 - 15) + '" y="' + str(note_y - 60)
                    + '" width="' + str(x2 - x1 + 40) + '" height="80" fill="transparent"/>'
                    # Note 1
                    '<ellipse cx="' + str(x1) + '" cy="' + str(note_y)
                    + '" rx="12" ry="9" fill="' + color
                    + '" transform="rotate(-20 ' + str(x1) + ' ' + str(note_y) + ')"/>'
                    '<line x1="' + str(x1 + 10) + '" y1="' + str(note_y)
                    + '" x2="' + str(x1 + 10) + '" y2="' + str(note_y - 55)
                    + '" stroke="' + color + '" stroke-width="3.5"/>'
                    # Note 2
                    '<ellipse cx="' + str(x2) + '" cy="' + str(note_y)
                    + '" rx="12" ry="9" fill="' + color
                    + '" transform="rotate(-20 ' + str(x2) + ' ' + str(note_y) + ')"/>'
                    '<line x1="' + str(x2 + 10) + '" y1="' + str(note_y)
                    + '" x2="' + str(x2 + 10) + '" y2="' + str(note_y - 55)
                    + '" stroke="' + color + '" stroke-width="3.5"/>'
                    # Beam
                    '<rect x="' + str(x1 + 10) + '" y="' + str(note_y - 55)
                    + '" width="' + str(x2 - x1) + '" height="5" fill="' + color + '"/>'
                    # Double beam
                    '<rect x="' + str(x1 + 10) + '" y="' + str(note_y - 48)
                    + '" width="' + str(x2 - x1) + '" height="5" fill="' + color + '"/>'
                    '</g>'
                )

            elif ntype == "rest":
                # Quarter rest — zigzag shape
                svg += (
                    '<g class="note" data-idx="' + str(i) + '">'
                    '<rect x="' + str(x - 20) + '" y="' + str(note_y - 30)
                    + '" width="40" height="70" fill="transparent"/>'
                    '<path d="M' + str(x - 5) + ' ' + str(note_y - 25)
                    + ' l8 12 l-8 12 l8 12 l-8 12'
                    + '" fill="none" stroke="' + color + '" stroke-width="4" stroke-linecap="round"/>'
                    '</g>'
                )

            # Labels below staff
            label_y = STAFF_TOP + 5 * STAFF_GAP + 25
            sound_y = label_y + 24
            svg += (
                '<text x="' + str(x) + '" y="' + str(label_y)
                + '" text-anchor="middle" class="rule-text">' + pattern + '</text>'
            )
            svg += (
                '<text x="' + str(x) + '" y="' + str(sound_y)
                + '" text-anchor="middle" class="sound-text">' + sound + '</text>'
            )

        # Key items in a horizontal row, centered below staff
        key_y_base = STAFF_TOP + 5 * STAFF_GAP + 55
        key_items_width = 700
        key_start_x = (SVG_WIDTH - key_items_width) // 2
        item_gap = key_items_width // 4

        svg += (
            '<g>'
            # Subtle line separator
            '<line x1="' + str(key_start_x) + '" y1="' + str(key_y_base - 15)
            + '" x2="' + str(key_start_x + key_items_width) + '" y2="' + str(key_y_base - 15)
            + '" stroke="#E8DFC0" stroke-width="1"/>'

            # Item 1: Quarter note
            '<ellipse cx="' + str(key_start_x + 8) + '" cy="' + str(key_y_base + 5) + '" rx="6" ry="4" fill="' + color + '" transform="rotate(-20 ' + str(key_start_x + 8) + ' ' + str(key_y_base + 5) + ')"/>'
            '<line x1="' + str(key_start_x + 13) + '" y1="' + str(key_y_base + 5) + '" x2="' + str(key_start_x + 13) + '" y2="' + str(key_y_base - 10) + '" stroke="' + color + '" stroke-width="2"/>'
            '<text x="' + str(key_start_x + 22) + '" y="' + str(key_y_base + 9) + '" font-size="11" fill="#4A5568">A single clear beat</text>'

            # Item 2: Eighth note
            '<ellipse cx="' + str(key_start_x + item_gap + 8) + '" cy="' + str(key_y_base + 5) + '" rx="6" ry="4" fill="' + color + '" transform="rotate(-20 ' + str(key_start_x + item_gap + 8) + ' ' + str(key_y_base + 5) + ')"/>'
            '<line x1="' + str(key_start_x + item_gap + 13) + '" y1="' + str(key_y_base + 5) + '" x2="' + str(key_start_x + item_gap + 13) + '" y2="' + str(key_y_base - 10) + '" stroke="' + color + '" stroke-width="2"/>'
            '<path d="M' + str(key_start_x + item_gap + 13) + ' ' + str(key_y_base - 10) + ' q 5 5 2 12" fill="none" stroke="' + color + '" stroke-width="1.5"/>'
            '<text x="' + str(key_start_x + item_gap + 22) + '" y="' + str(key_y_base + 9) + '" font-size="11" fill="#4A5568">A lighter, shorter note</text>'

            # Item 3: Double beam
            '<ellipse cx="' + str(key_start_x + item_gap * 2 + 5) + '" cy="' + str(key_y_base + 5) + '" rx="5" ry="3.5" fill="' + color + '"/>'
            '<ellipse cx="' + str(key_start_x + item_gap * 2 + 15) + '" cy="' + str(key_y_base + 5) + '" rx="5" ry="3.5" fill="' + color + '"/>'
            '<line x1="' + str(key_start_x + item_gap * 2 + 9) + '" y1="' + str(key_y_base + 5) + '" x2="' + str(key_start_x + item_gap * 2 + 9) + '" y2="' + str(key_y_base - 8) + '" stroke="' + color + '" stroke-width="2"/>'
            '<line x1="' + str(key_start_x + item_gap * 2 + 19) + '" y1="' + str(key_y_base + 5) + '" x2="' + str(key_start_x + item_gap * 2 + 19) + '" y2="' + str(key_y_base - 8) + '" stroke="' + color + '" stroke-width="2"/>'
            '<rect x="' + str(key_start_x + item_gap * 2 + 9) + '" y="' + str(key_y_base - 8) + '" width="10" height="2.5" fill="' + color + '"/>'
            '<rect x="' + str(key_start_x + item_gap * 2 + 9) + '" y="' + str(key_y_base - 4) + '" width="10" height="2.5" fill="' + color + '"/>'
            '<text x="' + str(key_start_x + item_gap * 2 + 28) + '" y="' + str(key_y_base + 9) + '" font-size="11" fill="#4A5568">Two notes as one phrase</text>'

            # Item 4: Rest
            '<path d="M' + str(key_start_x + item_gap * 3 + 6) + ' ' + str(key_y_base - 6) + ' l3 5 l-3 5 l3 5" fill="none" stroke="' + color + '" stroke-width="2" stroke-linecap="round"/>'
            '<text x="' + str(key_start_x + item_gap * 3 + 22) + '" y="' + str(key_y_base + 9) + '" font-size="11" fill="#4A5568">Silence \u2014 nothing plays</text>'

            '</g>'
        )

        svg += '</svg>'

        js_code = ""

        # Title
        title_html = (
            '<div style="display:flex; align-items:baseline; gap:10px; margin-bottom:4px; padding:0 10px;">'
            '<span style="font-size:1.2rem; font-weight:700; color:#2D3748;">'
            + language + '</span>'
            '<span style="font-size:.85rem; color:#718096;">'
            + subtitle + '</span>'
            '</div>'
        )

        # Full HTML
        full_html = (
            '<!DOCTYPE html><html><body style="margin:0;padding:0;">'
            '<div style="background: linear-gradient(135deg, #FFFEF5, #FFF9E6, #FFFDF2);'
            'border-radius: 12px; padding: 16px 12px; border: 1px solid #E8DFC0;'
            'box-shadow: 0 4px 16px rgba(0,0,0,.06); font-family: Inter, -apple-system, sans-serif;">'
            + title_html + svg +
            '</div>'
            +
            '</body></html>'
        )

        components.html(full_html, height=440, scrolling=False)

    # ─── Part 3: The longer the name, the higher the wall ─────────
    st.markdown("")
    st.markdown(
        "There's a measurable pattern here too: **the longer the name, the higher the wall.** "
        "Visual length and spelling complexity work together as a pronunciation filter."
    )

    length_data = {
        "bracket": ["3–4 letters", "5–6 letters", "7–8 letters", "9–10 letters", "11+ letters"],
        "avg_countryness": [8, 14, 27, 89, 201],
    }

    fig = go.Figure(go.Bar(
        x=length_data["bracket"],
        y=length_data["avg_countryness"],
        marker_color=["#A8E6C8", "#7C9FD6", "#F5D68A", "#F5B7C5", "#E63946"],
        text=[str(v) for v in length_data["avg_countryness"]],
        textposition="outside",
        textfont=dict(size=14, color="#2D3748", family="Inter"),
    ))

    fig.update_layout(
        title="",
        xaxis_title="Name Length",
        yaxis_title="Avg Countryness Score",
        template="plotly_white",
        font=dict(family="Inter", size=12, color="#4A5568"),
        plot_bgcolor="white",
        height=350,
        margin=dict(t=20, b=60, l=60, r=20),
        xaxis=dict(gridcolor="#E2E8F0"),
        yaxis=dict(gridcolor="#E2E8F0"),
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "Names with **11+ letters** average a countryness of **201** — effectively cultural passwords. "
        "At 3–4 letters? Just **8** — practically global."
    )

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # 🎵 SAME SONG, DIFFERENT KEY (Patrick vs Pádraig)
    # ══════════════════════════════════════════════════════════════

    st.markdown("### 🎵 Same Song, Different Key")
    st.markdown(
        "Sometimes the song exists in both versions — an original and a remix. "
        "One gets global airplay. The other stays in the vault."
    )

    # ─── Saint Patrick watercolor illustration ────────────────────
    saint_img = "artifacts/image_063.png"
    col_spacer_l, col_img, col_spacer_r = st.columns([1, 2, 1])
    with col_img:
        st.image(saint_img, caption="St. Patrick — one saint, two spellings, two fates", use_container_width=True)

    # ─── Album cover cards: Original vs International Remix ───────
    col_original, col_remix = st.columns(2)

    with col_original:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #1A1A2E, #16213E);
                    border-radius: 8px; padding: 24px; text-align: center;
                    box-shadow: 0 8px 24px rgba(0,0,0,.3); position: relative; overflow: hidden;">
            <!-- Subtle texture -->
            <div style="position:absolute; inset:0; opacity:.04;
                        background:repeating-linear-gradient(45deg, #fff 0px, #fff 1px, transparent 1px, transparent 6px);"></div>
            <!-- Label -->
            <div style="font-size:.55rem; letter-spacing:4px; color:#E63946; font-weight:700; margin-bottom:12px;">
                ● ORIGINAL PRESSING
            </div>
            <!-- Album art area -->
            <div style="background: linear-gradient(135deg, #0F3443, #34e89e20);
                        border-radius: 6px; padding: 30px 20px; margin: 10px 0;">
                <div style="font-size: 2.4em; font-weight: 800; color: #F0FFF4; font-family: Georgia, serif;
                            text-shadow: 0 2px 8px rgba(0,0,0,.3);">
                    Pádraig
                </div>
                <div style="font-size: .75rem; color: #A8E6C8; margin-top: 8px; font-style: italic;">
                    /PAW-drig/
                </div>
            </div>
            <!-- Details -->
            <div style="margin-top: 14px; font-size: .7rem; color: #A0AEC0; font-family: 'Courier New', monospace;">
                Origin: Irish Gaelic<br>
                Countryness: <b style="color:#E63946;">343</b><br>
                Markets: Ireland, N. Ireland only
            </div>
            <!-- Status -->
            <div style="margin-top: 14px; padding: 6px 14px; border: 1.5px solid #E63946; border-radius: 3px;
                        display: inline-block; font-size: .6rem; font-weight: 800; letter-spacing: 2px; color: #E63946;">
                LIMITED RELEASE
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_remix:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #1A1A2E, #16213E);
                    border-radius: 8px; padding: 24px; text-align: center;
                    box-shadow: 0 8px 24px rgba(0,0,0,.3); position: relative; overflow: hidden;">
            <!-- Subtle texture -->
            <div style="position:absolute; inset:0; opacity:.04;
                        background:repeating-linear-gradient(45deg, #fff 0px, #fff 1px, transparent 1px, transparent 6px);"></div>
            <!-- Label -->
            <div style="font-size:.55rem; letter-spacing:4px; color:#059669; font-weight:700; margin-bottom:12px;">
                ● INTERNATIONAL REMIX
            </div>
            <!-- Album art area -->
            <div style="background: linear-gradient(135deg, #0F3443, #7C9FD620);
                        border-radius: 6px; padding: 30px 20px; margin: 10px 0;">
                <div style="font-size: 2.4em; font-weight: 800; color: #F0FFF4; font-family: Georgia, serif;
                            text-shadow: 0 2px 8px rgba(0,0,0,.3);">
                    Patrick
                </div>
                <div style="font-size: .75rem; color: #7C9FD6; margin-top: 8px; font-style: italic;">
                    /PAT-rik/
                </div>
            </div>
            <!-- Details -->
            <div style="margin-top: 14px; font-size: .7rem; color: #A0AEC0; font-family: 'Courier New', monospace;">
                Origin: English adaptation<br>
                Countryness: <b style="color:#059669;">2</b><br>
                Markets: All 8 countries
            </div>
            <!-- Status -->
            <div style="margin-top: 14px; padding: 6px 14px; border: 1.5px solid #059669; border-radius: 3px;
                        display: inline-block; font-size: .6rem; font-weight: 800; letter-spacing: 2px; color: #059669;">
                WORLDWIDE RELEASE
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown(
        "It's literally the same name — same saint, same meaning. But **Patrick** is the remix "
        "that stripped away the Gaelic spelling, making it readable for every English speaker on Earth. "
        "**Pádraig** kept its original form — and stayed home because of it."
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

    # ─── Reason 4: Active Cultural Revival ────────────────────────
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
