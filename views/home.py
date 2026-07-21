    # --- At the very end of render() ---
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <p style="font-size:0.8rem; color:#667eea; text-transform:uppercase; letter-spacing:3px;">
            THE TWO WORLDS OF NAMING
        </p>
        <h2 style="color:#fff; font-size:1.8rem; margin:0;">
            Same Language. Different Cultures. One Choice.
        </h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.image("assets/baby_popculture.png", use_container_width=True)
        st.markdown("""
        <div style="text-align:center; padding:12px; background:rgba(6,214,160,0.08); 
            border:1px solid rgba(6,214,160,0.2); border-radius:10px; margin-top:10px;">
            <p style="font-size:1.3rem; margin:0; color:#06d6a0;">🤝 "Maverick"</p>
            <p style="font-size:0.85rem; color:#8888aa; margin:4px 0 0;">
                Pop culture baby — trending in ALL 8 countries.<br>
                <strong style="color:#06d6a0;">Countryness: 1.2</strong> (global)
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.image("assets/baby_traditional.png", use_container_width=True)
        st.markdown("""
        <div style="text-align:center; padding:12px; background:rgba(230,57,70,0.08);
            border:1px solid rgba(230,57,70,0.2); border-radius:10px; margin-top:10px;">
            <p style="font-size:1.3rem; margin:0; color:#e63946;">🧱 "Sadhbh"</p>
            <p style="font-size:0.85rem; color:#8888aa; margin:4px 0 0;">
                Gaelic name — locked to Ireland. Unpronounceable elsewhere.<br>
                <strong style="color:#e63946;">Countryness: 8,171</strong> (fortress)
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-top:1.5rem; padding:20px;
        background:rgba(102,126,234,0.05); border-radius:10px;">
        <p style="font-size:1.1rem; color:#c0c0e0; font-style:italic; margin:0;">
            "One baby named for the world. One named for home.<br>
            Both are real. Both are happening right now. That's the story."
        </p>
    </div>
    """, unsafe_allow_html=True)
