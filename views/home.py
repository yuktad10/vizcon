import streamlit as st
import base64
import streamlit.components.v1 as components
from utils.data_loader import load_metrics
from utils.charts import countryness_over_time, COLORS


def render():
    from utils.data_loader import load_metrics

    df = load_metrics()

    # Compute actual stats from data
    unique_names = df["name"].nunique()
    num_countries = df["max_country"].nunique()
    year_min = df["year"].min()
    year_max = df["year"].max()
    total_records = len(df)

    # ─── Hero Section ─────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center; padding: 20px 0 10px;">
            <h1 style="font-size:2.4em; font-weight:800; 
                       background: linear-gradient(135deg, #667eea, #764ba2);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       margin-bottom: 5px;">
                Passport for a Name
            </h1>
            <p style="font-size:1.05em; color:#6b7280; max-width:700px; margin:0 auto;">
                Some names travel the world. Others never leave home.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ─── Story Hook ───────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center; width:100%; margin:1rem auto; padding:18px 30px;
            background: linear-gradient(135deg, #f8f9ff 0%, #eef1ff 100%);
            border: 1px solid rgba(102,126,234,0.2);
            border-radius:10px;
            box-shadow: 0 4px 20px rgba(102,126,234,0.1);">
            <p style="font-size:1.05em; color:#374151; line-height:1.6; margin:0;">
                Eight nations. One language. The tightest alliance in modern history. They share armies. Intelligence. Borders.
                &nbsp;&nbsp;But do they share something as simple as... <strong style="color:#667eea;">a baby name?</strong>
                &nbsp;&nbsp;<span style="font-size:1.1em; font-weight:700; color:#667eea;">This is THAT STORY.</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ─── Anglosphere Context ──────────────────────────────────────
    st.markdown("")
    st.markdown("### 🌍 The Anglosphere")
    st.markdown(
        'The term "Anglosphere" was coined by sci-fi writer **Neal Stephenson** '
        "in his 1995 novel *The Diamond Age*. A fictional concept that became a geopolitical reality. "
        "Today it represents just **6% of the world's population** — but over **30% of its economy**."
    )

    # ─── Map Image (reduced height) ──────────────────────────────
    st.markdown(
        """
        <style>
            .map-container img {
                max-height: 160px;
                object-fit: cover;
                object-position: center;
                border-radius: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    st.image("assets/world_map.png", width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── The Two Worlds (integrated baby section) ─────────────────
    st.markdown("")

    # ─── Section Header: Two Worlds of Naming ─────────────────────
    st.markdown(
        """
        <div style="text-align:center; padding: 30px 0 10px;">
            <p style="font-size:1.05rem; font-weight:600; letter-spacing:3px;
                      text-transform:uppercase; color:#667eea; margin-bottom:10px;">
                THE TWO WORLDS OF NAMING
            </p>
            <h2 style="font-size:2rem; font-weight:800; color:#1f2937; margin:0 0 12px;">
                Same Language. Different Cultures. One Choice.
            </h2>
            <p style="font-size:0.95rem; color:#9ca3af; margin:0;">
                👆 Click on a baby to explore their world
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ─── Helper: encode image to base64 data URI ──────────────────
    def img_to_base64(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{data}"

    def audio_to_base64(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:audio/wav;base64,{data}"

    img_pop = img_to_base64("assets/baby_popculture.png")
    img_trad = img_to_base64("assets/baby_traditional.png")
    aud_pop = audio_to_base64("assets/audio_pop.wav")
    aud_trad = audio_to_base64("assets/audio_trad.wav")

    # ─── Baby Images with flip-on-click + audio (using components.html) ───
    flip_html = f"""
    <html>
    <head>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }}
        .flip-container {{
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            padding: 10px;
        }}
        .flip-card {{
            perspective: 1000px;
            width: 48%;
            min-width: 280px;
            cursor: pointer;
        }}
        .flip-card-inner {{
            position: relative;
            width: 100%;
            padding-bottom: 75%;
            transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            transform-style: preserve-3d;
        }}
        .flip-card.flipped .flip-card-inner {{
            transform: rotateY(180deg);
        }}
        .flip-card-front, .flip-card-back {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            backface-visibility: hidden;
            border-radius: 12px;
            overflow: hidden;
        }}
        .flip-card-front img {{
            width: 100%; height: 100%;
            object-fit: cover;
            border-radius: 12px;
        }}
        .flip-card-back {{
            transform: rotateY(180deg);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
            border-radius: 12px;
        }}
        .flip-card-back.pop-back {{
            background: #f0fdf4;
            border: 2px solid #06d6a0;
        }}
        .flip-card-back.trad-back {{
            background: #fef2f2;
            border: 2px solid #e63946;
        }}
        .flip-hint {{
            text-align: center;
            font-size: 0.85rem;
            color: #9ca3af;
            margin-top: 8px;
        }}
    </style>
    </head>
    <body>
    <div class="flip-container">
        <!-- Pop Culture Card -->
        <div class="flip-card" id="card-pop">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <img src="{img_pop}" alt="Pop culture babies">
                </div>
                <div class="flip-card-back pop-back">
                    <div style="text-align:center;">
                        <p style="font-size:1.6rem; margin:0;">🎧</p>
                        <p style="font-size:1rem; color:#374151; margin:6px 0 0; line-height:1.6;">
                            Some names hit <strong>#1 in all 8 countries</strong> —<br>
                            like a global chart-topper that plays everywhere.
                        </p>
                    </div>
                </div>
            </div>
            <p class="flip-hint">🎧 Click to flip the record</p>
        </div>

        <!-- Traditional Card -->
        <div class="flip-card" id="card-trad">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <img src="{img_trad}" alt="Traditional babies">
                </div>
                <div class="flip-card-back trad-back">
                    <div style="text-align:center;">
                        <p style="font-size:1.6rem; margin:0;">💿</p>
                        <p style="font-size:1rem; color:#374151; margin:6px 0 0; line-height:1.6;">
                            Some never leave their homeland —<br>
                            like a vinyl that only plays in <strong>one shop</strong>.
                        </p>
                    </div>
                </div>
            </div>
            <p class="flip-hint">💿 Click to flip the vinyl</p>
        </div>
    </div>

    <!-- Audio elements -->
    <audio id="audio-pop" src="{aud_pop}" preload="auto"></audio>
    <audio id="audio-trad" src="{aud_trad}" preload="auto"></audio>

    <script>
        document.getElementById('card-pop').addEventListener('click', function() {{
            this.classList.toggle('flipped');
            document.getElementById('audio-pop').currentTime = 0;
            document.getElementById('audio-pop').play();
        }});
        document.getElementById('card-trad').addEventListener('click', function() {{
            this.classList.toggle('flipped');
            document.getElementById('audio-trad').currentTime = 0;
            document.getElementById('audio-trad').play();
        }});
    </script>
    </body>
    </html>
    """

    components.html(flip_html, height=550)


    # ─── Interactive Name Quiz ────────────────────────────────────
    quiz_html = """
    <html>
    <head>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 5px 20px; }
        .quiz-container {
            text-align: center;
            max-width: 600px;
            margin: 0 auto;
        }
        .quiz-question {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 8px;
        }
        .quiz-subtitle {
            font-size: 0.95rem;
            color: #6b7280;
            margin-bottom: 24px;
        }
        .quiz-options {
            display: flex;
            gap: 16px;
            justify-content: center;
        }
        .quiz-btn {
            padding: 14px 36px;
            font-size: 1.1rem;
            font-weight: 600;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            background: white;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .quiz-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .quiz-btn.nevaeh:hover { border-color: #06d6a0; color: #06d6a0; }
        .quiz-btn.trevor:hover { border-color: #e63946; color: #e63946; }
        .quiz-result {
            display: none;
            margin-top: 24px;
            padding: 20px 28px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .quiz-result:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.12);
        }
        .quiz-result.global {
            background: #f0fdf4;
            border: 2px solid #06d6a0;
        }
        .quiz-result.local {
            background: #fef2f2;
            border: 2px solid #e63946;
        }
        .result-emoji { font-size: 2rem; margin-bottom: 8px; }
        .result-text { font-size: 1.05rem; color: #374151; font-weight: 600; }
        .result-cta { font-size: 0.85rem; color: #6b7280; margin-top: 8px; }
    </style>
    </head>
    <body>
    <div class="quiz-container">
        <p class="quiz-question">🔍 Two Names. One Passport. Zero Clues.</p>
        <p class="quiz-subtitle">Which one do you think got the passport?</p>

        <div class="quiz-options" id="options">
            <button class="quiz-btn nevaeh" onclick="showResult('global')">Nevaeh</button>
            <button class="quiz-btn trevor" onclick="showResult('local')">Trevor</button>
        </div>

        <div class="quiz-result global" id="result-global" onclick="switchTab(1)">
            <p class="result-emoji">🎧</p>
            <p class="result-text">✈️ Passport APPROVED — welcome to The Global Playlist</p>
            <p class="result-cta">👆 Step inside →</p>
        </div>

        <div class="quiz-result local" id="result-local" onclick="switchTab(2)">
            <p class="result-emoji">💿</p>
            <p class="result-text">🚫 Passport DENIED — you're on The Local Vinyl</p>
            <p class="result-cta">👆 Step inside →</p>
        </div>
    </div>

    <script>
        function showResult(type) {
            document.getElementById('options').style.display = 'none';
            if (type === 'global') {
                document.getElementById('result-global').style.display = 'block';
            } else {
                document.getElementById('result-local').style.display = 'block';
            }
        }

        function switchTab(tabIndex) {
            // Access the parent Streamlit page and click the tab
            const tabs = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
            if (tabs && tabs[tabIndex]) {
                tabs[tabIndex].click();
            }
        }
    </script>
    </body>
    </html>
    """

    components.html(quiz_html, height=250)

    # ─── Closing Quote ────────────────────────────────────────────
    st.markdown("")
    st.markdown(
        """
        <div style="text-align:center; margin:1.5rem 0; padding:20px;
            background:#f5f5fa; border-radius:10px; border:1px solid #e5e7eb;">
            <p style="font-size:1.05rem; color:#4b5563; font-style:italic; margin:0;">
                "One baby named for the world. One named for home.<br>
                Both are real. Both are happening right now. That's the story."
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
