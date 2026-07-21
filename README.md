# What's in a Name? 👶

**VizCon 2026 Submission** — "Language vs Culture in the Anglosphere"

## 🚀 Run Locally

```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Structure

```
streamlit_app/
├── app.py                    # Main page (Intro)
├── pages/
│   ├── 1_🤝_Convergence.py  # POV1: Coming Together
│   ├── 2_🧱_Borders.py      # POV2: Invisible Borders
│   ├── 3_🎉_Fun_Facts.py    # Discoveries
│   └── 4_📋_Methods.py      # Methodology
├── requirements.txt          # Dependencies
├── .streamlit/config.toml    # Theme config
└── README.md                 # This file
```

## 🌐 Deploy to Streamlit Cloud

1. Push this folder to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file path: `streamlit_app/app.py`
5. Deploy!

## 📊 Data Files Needed

Place these CSV files in the parent directory (or same directory):
- `all-names-long.csv` (1.55M rows)
- `metrics-and-summary.csv` (268K rows)
- `summary-1997-2023.csv` (19K rows)

## 🏆 Theme

"How the world lives, thrives, and connects" — Analyticon VizCon 2026
