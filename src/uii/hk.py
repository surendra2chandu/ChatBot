import streamlit as st

def show_sticky_header(heading="Knowtion Chat"):
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
            margin-top: 80px;
        }
        </style>
        <div class="fixed-header" id="header-div"></div>
        <div class="spacer"></div>
    """, unsafe_allow_html=True)

    # Inject image and heading using Streamlit
    with st.container():
        st.markdown(f"<h2 style='text-align: center;'>{heading}</h2>", unsafe_allow_html=True)
