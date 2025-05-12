import streamlit as st

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Function to switch pages and rerun the app
def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ---------- Main Home Page ----------
if st.session_state.page == "home":
    st.title("🌟 Welcome to My App")
    st.subheader("Choose a Page")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➡️ Page 1"):
            go_to("page1")
        if st.button("➡️ Page 3"):
            go_to("page3")

    with col2:
        if st.button("➡️ Page 2"):
            go_to("page2")
        if st.button("➡️ Page 4"):
            go_to("page4")

# ---------- Page 1 ----------
elif st.session_state.page == "page1":
    st.title("📄 Page 1")
    st.write("This is the content of Page 1.")
    if st.button("⬅️ Go Back"):
        go_to("home")

# ---------- Page 2 ----------
elif st.session_state.page == "page2":
    st.title("📄 Page 2")
    st.write("This is the content of Page 2.")
    if st.button("⬅️ Go Back"):
        go_to("home")

# ---------- Page 3 ----------
elif st.session_state.page == "page3":
    st.title("📄 Page 3")
    st.write("This is the content of Page 3.")
    if st.button("⬅️ Go Back"):
        go_to("home")

# ---------- Page 4 ----------
elif st.session_state.page == "page4":
    st.title("📄 Page 4")
    st.write("This is the content of Page 4.")
    if st.button("⬅️ Go Back"):
        go_to("home")
