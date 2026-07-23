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
                <span style="-webkit-text-fill-color: initial;"> 📼</span> The Anglosphere Mixtape
            </h1>
            <p style="font-size:1.05em; color:#6b7280; max-width:700px; margin:0 auto;">
                Where names become hits—or hidden gems.
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
                Eight nations. One language. Centuries of shared history. Close allies. Shared intelligence. Shared defense.
                &nbsp;&nbsp;But do they share something as simple as… <strong style="color:#667eea;">a baby name?</strong>
            </p>
            <p style="font-size:1.2em; font-weight:700; color:#667eea; margin:12px 0 0; text-align:center;">
                This is THAT STORY.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ─── Anglosphere Context ──────────────────────────────────────
    st.markdown("")
    st.markdown(
        """
        <div style="padding:28px 32px; background:white; border-radius:14px;
            border:1px solid #e5e7eb; box-shadow: 0 4px 20px rgba(0,0,0,0.04);
            margin-bottom:1rem;">
            <h3 style="margin:0 0 14px; color:#1f2937; font-size:1.4rem;">
                🌍 The Anglosphere
            </h3>
            <p style="font-size:1.02rem; color:#374151; line-height:1.8; margin:0 0 12px;">
                The term "Anglosphere" was coined by sci-fi writer <strong>Neal Stephenson</strong>
                in his 1995 novel <em>The Diamond Age</em>. A fictional concept that became a geopolitical reality.
                Today it represents just <strong>6% of the world's population</strong> — but over <strong>30% of its economy</strong>.
                Every year, millions of babies receive a name across the English-speaking world—from
                New York to New Zealand, London to Lagos. Our dataset spans <strong>27 years, 8 countries, 117 million babies, and 17,575 unique names.</strong>
            </p>
            <p style="font-size:1.02rem; color:#374151; line-height:1.8; margin:0 0 12px;">
                We asked one simple question: <strong>Which names become global hits</strong>, crossing borders and
                topping the charts everywhere—and which remain <strong>timeless local favorites</strong>, never leaving home?
            </p>
            <p style="font-size:1.02rem; color:#374151; line-height:1.8; margin:0 0 16px;">
                So we turned every name into a track. Some earned a place on the
                <strong style="color:#7c9a8e;">Global Playlist</strong>. Others stayed on
                <strong style="color:#c99e85;">Local Vinyl</strong>.
            </p>
            <p style="font-size:1.15rem; font-weight:700; color:#667eea; margin:0; text-align:center;">
                🎶 Now Playing: The Name Playlist.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ─── Map Image (reduced height) ──────────────────────────────
    st.markdown(
        """
        <style>
            .map-container img {
                max-height: 70px;
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

    # ─── Visual Divider ───────────────────────────────────────────
    st.markdown(
        """
        <hr style="border:none; border-top:2px solid #e5e7eb; margin:1rem 0 2rem;">
        """,
        unsafe_allow_html=True,
    )

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
               👇 Click on a baby to explore their world
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
            width: 100%;
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
            height: 400px;
            transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            transform-style: preserve-3d;
        }}
        .flip-card.flipped .flip-card-inner {{
            transform: rotateY(180deg);
        }}
        .flip-card-front, .flip-card-back {{
            position: absolute;
            top: 0; left: 0;
            width: 100%;
            height: 100%;
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

    components.html(flip_html, height=450)


    # ─── Interactive Name Quiz ────────────────────────────────────
    st.markdown(
        """
        <hr style="border:none; border-top:2px solid #e5e7eb; margin:2rem 0 1.5rem;">
        """,
        unsafe_allow_html=True,
    )

    quiz_html = """
    <html>
    <head>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 5px 20px; }
        .quiz-container {
            text-align: center;
            max-width: 100%;
            margin: 0 auto;
        }
        .quiz-preheading {
            font-size: 1rem;
            font-weight: 600;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #667eea;
            margin-bottom: 18px;
        }
        .quiz-question {
            font-size: 1.6rem;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 8px;
        }
        .quiz-subtitle {
            font-size: 1.05rem;
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
        .quiz-btn span {
            display: block;
            font-size: 0.75rem;
            font-weight: 400;
            color: #9ca3af;
            margin-top: 4px;
        }
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
        .result-cta {
            font-size: 0.9rem;
            color: #6b7280;
            margin-top: 10px;
            font-weight: 500;
            font-style: italic;
        }
        .reset-btn {
            display: none;
            margin: 16px auto 0;
            padding: 8px 20px;
            font-size: 0.85rem;
            color: #667eea;
            background: none;
            border: 1px solid #667eea;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .reset-btn:hover {
            background: #667eea;
            color: white;
        }
    </style>
    </head>
    <body>
    <div class="quiz-container">
        <p class="quiz-preheading">🎵 Can You Read the Charts?</p>
        <p class="quiz-question">🔍 Two Names. One Playlist. Zero Clues.</p>
        <p class="quiz-subtitle">Which one made it to the Global Playlist?</p>

        <div class="quiz-options" id="options">
            <button class="quiz-btn nevaeh" onclick="showResult('global')">Nevaeh<span>"heaven" spelled backwards</span></button>
            <button class="quiz-btn trevor" onclick="showResult('local')">Trevor<span>classic Welsh origin</span></button>
        </div>

        <div class="quiz-result global" id="result-global">
            <p class="result-emoji">🎧</p>
            <p class="result-text">🎉 This name became a cross-country favorite.</p>
            <p class="result-cta">👆 Head to the 🎧 Global Playlist tab above to explore →</p>
        </div>

        <div class="quiz-result local" id="result-local">
            <p class="result-emoji">💿</p>
            <p class="result-text">🏠 This name remained a hometown classic.</p>
            <p class="result-cta">👆 Head to the 💿 Local Vinyl tab above to explore →</p>
        </div>

        <button class="reset-btn" id="reset-btn" onclick="resetQuiz()">↩ Reset</button>
    </div>

    <script>
        function showResult(type) {
            document.getElementById('options').style.display = 'none';
            if (type === 'global') {
                document.getElementById('result-global').style.display = 'block';
            } else {
                document.getElementById('result-local').style.display = 'block';
            }
            document.getElementById('reset-btn').style.display = 'block';
        }

        function resetQuiz() {
            document.getElementById('options').style.display = 'flex';
            document.getElementById('result-global').style.display = 'none';
            document.getElementById('result-local').style.display = 'none';
            document.getElementById('reset-btn').style.display = 'none';
        }
    </script>
    </body>
    </html>
    """

    components.html(quiz_html, height=320)
