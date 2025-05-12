import streamlit as st

# Sticky header style
st.markdown("""
    <style>
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background-color: white;
        z-index: 9999;
        padding: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .spacer {
        margin-top: 80px; /* Push content down to avoid overlap */
    }
    </style>
    <div class="fixed-header">
        <img src="your_logo.png" width="150">
        <h2>💬 Knowtion Chat</h2>
    </div>
    <div class="spacer"></div>
""", unsafe_allow_html=True)
