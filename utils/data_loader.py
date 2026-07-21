import streamlit as st
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


@st.cache_data
def load_metrics():
    """Year-level summary with countryness (268K rows)."""
    df = pd.read_csv(os.path.join(DATA_DIR, "metrics-and-summary.csv"))
    df = df[df["year"] >= 1997]
    return df


@st.cache_data
def load_summary():
    """Aggregated 1997-2023 summary (19K rows)."""
    return pd.read_csv(os.path.join(DATA_DIR, "summary-1997-2023.csv"))


@st.cache_data
def load_all_names():
    """Full granular data — compressed .gz, pandas reads it natively."""
    df = pd.read_csv(os.path.join(DATA_DIR, "all-names-long.csv.gz"), compression="gzip")
    df = df[df["year"] >= 1997]
    return df
