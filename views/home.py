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
                <span style="-webkit-text-fill-color: initial;">🎶</span> Now Playing: The Name Playlist
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
                👇 The Anglosphere Mixtape
            </h3>
            <p style="font-size:1.02rem; color:#374151; line-height:1.8; margin:0 0 12px;">
                The term "Anglosphere" was coined by sci-fi writer <strong>Neal Stephenson</strong>
                in his 1995 novel <em>The Diamond Age</em>. A fictional concept that became a geopolitical reality.
                Today it represents just <strong>6% of the world's population</strong> — but over <strong>30% of its economy</strong>.
            </p>
            <p style="font-size:1.02rem; color:#374151; line-height:1.8; margin:0 0 12px;">
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
    # ─── Map Image with animated travel lines ─────────────────────
    st.image("assets/world_map.png", use_container_width=True)
    
    from streamlit.components.v1 import html as st_html_map
    
    # Overlay animated travel lines (positioned to overlap the map above)
    travel_lines_html = """
    <html>
    <head>
    <style>
        body { margin: 0; padding: 0; }
        .lines-container {
            width: 100%;
            height: 100%;
            margin-top: -10px;
        }
        svg { width: 100%; height: 100%; }
        
        .travel-path {
            fill: none;
            stroke-width: 2;
            stroke-dasharray: 8 5;
            opacity: 0.6;
            animation: dashMove 2s linear infinite;
        }
        @keyframes dashMove {
            to { stroke-dashoffset: -26; }
        }
        
        .travel-dot {
            animation: dotPulse 2s ease-in-out infinite;
        }
        @keyframes dotPulse {
            0%, 100% { opacity: 0.6; }
            50% { opacity: 1; }
        }
    </style>
    </head>
    <body>
        <div class="lines-container">
            <svg viewBox="0 0 1000 60" preserveAspectRatio="none">
                <!-- Animated connecting lines (horizontal, representing travel) -->
                <path class="travel-path" d="M 50 30 Q 200 10 400 30 Q 600 50 800 25 Q 900 15 950 30" stroke="#667eea" style="animation-delay: 0s;"/>
                <path class="travel-path" d="M 80 40 Q 250 55 450 35 Q 650 15 850 40" stroke="#3498db" style="animation-delay: 0.5s;"/>
                <path class="travel-path" d="M 100 20 Q 300 45 500 25 Q 700 40 900 20" stroke="#9b59b6" style="animation-delay: 1s;"/>
                <path class="travel-path" d="M 150 45 Q 350 20 550 45 Q 750 25 920 35" stroke="#e74c3c" style="animation-delay: 1.5s;"/>
                
                <!-- Dots representing countries -->
                <circle class="travel-dot" cx="100" cy="30" r="4" fill="#3498db" style="animation-delay: 0s;"/>
                <circle class="travel-dot" cx="300" cy="30" r="4" fill="#9b59b6" style="animation-delay: 0.3s;"/>
                <circle class="travel-dot" cx="500" cy="30" r="4" fill="#f39c12" style="animation-delay: 0.6s;"/>
                <circle class="travel-dot" cx="680" cy="30" r="4" fill="#e74c3c" style="animation-delay: 0.9s;"/>
                <circle class="travel-dot" cx="780" cy="30" r="4" fill="#1abc9c" style="animation-delay: 1.2s;"/>
                <circle class="travel-dot" cx="900" cy="30" r="4" fill="#2ecc71" style="animation-delay: 1.5s;"/>
                <circle class="travel-dot" cx="950" cy="30" r="4" fill="#e91e63" style="animation-delay: 1.8s;"/>
            </svg>
        </div>
    </body>
    </html>
    """
    
    st_html_map(travel_lines_html, height=50)

    # ─── How We Measured It ───────────────────────────────────────
    st.markdown(
        """
        <div style="margin: 2rem 0 1.5rem;">
            <h3 style="margin:0 0 8px; color:#1f2937; font-size:1.3rem; text-align:center;">
                📐 How We Measured It
            </h3>
            <p style="font-size:0.92rem; color:#6b7280; text-align:center; margin:0 0 1.2rem; max-width:700px; margin-left:auto; margin-right:auto;">
                We created the <strong>Countryness Score</strong> — a single number that tells you whether a name is a global hit or a local gem.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Formula card
    st.markdown(
        """
        <div style="padding:20px 28px; background:linear-gradient(135deg, #f8f9ff, #eef1ff); 
                    border-radius:12px; border:1px solid rgba(102,126,234,0.15);
                    margin-bottom:1.2rem; text-align:center;">
            <p style="font-size:0.8rem; color:#667eea; font-weight:600; letter-spacing:1px; 
                      text-transform:uppercase; margin:0 0 8px;">The Formula</p>
            <p style="font-size:1.2rem; font-weight:700; color:#1f2937; margin:0 0 10px; font-family: 'Courier New', monospace;">
                Countryness = Proportion in Top Country ÷ Avg Proportion in Other Countries
            </p>
            <p style="font-size:0.85rem; color:#6b7280; margin:0; line-height:1.6;">
                A score of <strong>1.0</strong> = perfectly equal usage across all nations.<br>
                The higher the score, the more "local" the name — it lives in just one country.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Classification table
    st.markdown(
        """
        <div style="padding:20px 24px; background:white; border-radius:12px;
                    border:1px solid #e5e7eb; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
            <table style="width:100%; border-collapse:collapse; font-size:0.88rem;">
                <thead>
                    <tr style="border-bottom:2px solid #e5e7eb;">
                        <th style="text-align:left; padding:8px 12px; color:#374151;">Score</th>
                        <th style="text-align:left; padding:8px 12px; color:#374151;">Classification</th>
                        <th style="text-align:left; padding:8px 12px; color:#374151;">Meaning</th>
                        <th style="text-align:right; padding:8px 12px; color:#374151;">Example</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom:1px solid #f3f4f6;">
                        <td style="padding:10px 12px; font-weight:600; color:#7c9a8e;">< 5</td>
                        <td style="padding:10px 12px;"><span style="background:#e8f5e9; color:#2e7d32; padding:2px 8px; border-radius:6px; font-weight:600; font-size:0.8rem;">🎧 Global Hit</span></td>
                        <td style="padding:10px 12px; color:#6b7280;">Charts in every country equally</td>
                        <td style="padding:10px 12px; text-align:right; font-weight:600;">Isabella (1.06)</td>
                    </tr>
                    <tr style="border-bottom:1px solid #f3f4f6;">
                        <td style="padding:10px 12px; font-weight:600; color:#667eea;">5 – 10</td>
                        <td style="padding:10px 12px;"><span style="background:#e8eaf6; color:#3949ab; padding:2px 8px; border-radius:6px; font-weight:600; font-size:0.8rem;">🌍 Leaning Global</span></td>
                        <td style="padding:10px 12px; color:#6b7280;">Popular in most, peaks in one</td>
                        <td style="padding:10px 12px; text-align:right; font-weight:600;">Nevaeh (7.2)</td>
                    </tr>
                    <tr style="border-bottom:1px solid #f3f4f6;">
                        <td style="padding:10px 12px; font-weight:600; color:#f39c12;">10 – 100</td>
                        <td style="padding:10px 12px;"><span style="background:#fff3e0; color:#e65100; padding:2px 8px; border-radius:6px; font-weight:600; font-size:0.8rem;">📻 Regional</span></td>
                        <td style="padding:10px 12px; color:#6b7280;">Strong in a few, absent elsewhere</td>
                        <td style="padding:10px 12px; text-align:right; font-weight:600;">Callum (42)</td>
                    </tr>
                    <tr style="border-bottom:1px solid #f3f4f6;">
                        <td style="padding:10px 12px; font-weight:600; color:#c99e85;">100 – 1000</td>
                        <td style="padding:10px 12px;"><span style="background:#fce4ec; color:#c62828; padding:2px 8px; border-radius:6px; font-weight:600; font-size:0.8rem;">💿 Local Classic</span></td>
                        <td style="padding:10px 12px; color:#6b7280;">Dominates one country only</td>
                        <td style="padding:10px 12px; text-align:right; font-weight:600;">Siobhan (350)</td>
                    </tr>
                    <tr>
                        <td style="padding:10px 12px; font-weight:600; color:#e63946;">1000+</td>
                        <td style="padding:10px 12px;"><span style="background:#ffebee; color:#b71c1c; padding:2px 8px; border-radius:6px; font-weight:600; font-size:0.8rem;">🚫 Cultural Exclusive</span></td>
                        <td style="padding:10px 12px; color:#6b7280;">Exists in one country, zero elsewhere</td>
                        <td style="padding:10px 12px; text-align:right; font-weight:600;">Raewyn (168,731)</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
            <p class="result-cta">👇 Scroll down to explore the Global Playlist</p>
        </div>

        <div class="quiz-result local" id="result-local">
            <p class="result-emoji">💿</p>
            <p class="result-text">🏠 This name remained a hometown classic.</p>
            <p class="result-cta">👇 Scroll down to explore the Local Vinyl</p>
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
