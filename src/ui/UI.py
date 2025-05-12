# Import necessary libraries
import streamlit as st
import sys
sys.path.append(r'C:\PycharmProjects\ChatBot')

from src.api.ChatBot import ChatBot
from src.api.TextSummarizer import TextSummarizer
from src.database_utilities.Semantic_Table import SemanticTable


# Container for the title
container = st.container(height=120, border=True)
container.title("What assistance do you require?")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "operation" not in st.session_state:
    st.session_state.operation = None
if "doc_id" not in st.session_state:
    st.session_state.doc_id = None

# Sidebar for selecting document and operation
with st.sidebar:
    contain = st.container(height=210, border=True)
    contain.title("**Documents**")
    st.session_state.doc_id = contain.selectbox("Select the document", SemanticTable().get_all_document_ids())
    contain.title("**Operation**")
    st.session_state.operation = contain.radio("Select the operation", ["Q&A", "Summarize"])

    con = st.container(height=210, border=True)
    con.title("**Operation**")
    st.session_state.operation = con.radio("Select the operation", ["Q&A", "Summarize"])

    if st.button("🔄 Refresh"):
        st.session_state.messages = []
        st.session_state.operation = None

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input for Q&A
if st.session_state.operation == "Q&A":
    if prompt := st.chat_input("Enter your query..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(f"***Question:*** {prompt}")

        # Process Q&A query
        try:
            response = ChatBot().get_response(prompt, st.session_state.doc_id)
        except Exception as e:
            response = f"There was an error while processing your request: {e}"

        # Display assistant's response
        with st.chat_message("assistant"):
            st.markdown(f"***Answer:*** {response}")

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# Process Summarization separately (without user input)
elif st.session_state.operation == "Summarize":
    try:
        if st.session_state.doc_id:
            response = TextSummarizer().summarize(st.session_state.doc_id)

            # Display assistant's response
            with st.chat_message("assistant"):
                st.markdown(f"***Summary:*** {response}")

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(f"There was an error while processing the summarization: {e}")

# Custom CSS for buttons
st.markdown(
    """
    <style>
        .stButton>button { 
            width: 200px;   /* Set button width */
            height: 45px;   /* Set button height */
            font-size: 14px; /* Set button font size */
        }
    </style>
    """,
    unsafe_allow_html=True,
)
