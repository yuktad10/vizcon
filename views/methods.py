
import streamlit as st


def render():
    st.markdown("## 📋 Methods & Sources")
    st.markdown("---")

    st.markdown("### Dataset")
    st.markdown(
        """
        - **Source:** Anglosphere Baby Names — Kaggle
        - **Records:** 1,549,669 individual name records
        - **Countries:** USA, England & Wales, Scotland, Northern Ireland, 
          Ireland, Canada, Australia, New Zealand
        - **Time span:** 1997–2023 (all 8 countries covered)
        - **Fields:** year, sex, country, name, frequency, proportion
        """
    )

    st.markdown("### Key Metrics")
    st.markdown(
        """
        - **Countryness Score:** Ratio of a name's proportion in its dominant 
          country vs. average usage elsewhere. Higher = more culturally specific.
        - **Global (countryness < 5):** Name used roughly equally across all countries.
        - **Locked (countryness > 100):** Name strongly associated with one culture.
        """
    )

    st.markdown("### Tools")
    st.markdown(
        """
        - Python 3.13, Streamlit, Plotly
        - Data processing: pandas, numpy
        - GenAI: Used for data exploration, hypothesis generation, 
          code generation, narrative drafting, and QA
        """
    )
