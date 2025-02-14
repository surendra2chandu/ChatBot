import streamlit as st
import requests

class ChatBotUtilities:

    @staticmethod
    def show_chat_history(self):
        """
        This method displays the chat history.
        :return:
        """

        # Display chat history section
        if st.checkbox("Show Chat History"):
            st.write("### Chat History")

            # Display chat history if available
            if st.session_state.history:
                chat_history = ""
                for user_input, bot_response in st.session_state.history:
                    chat_history += f"**You**: {user_input}\n"
                    chat_history += f"**Bot**: {bot_response}\n\n"
                # Display the entire chat history in the text area
                st.text_area("Chat History", value=chat_history, height=300)
            else:
                # Display message if no chat history is available
                st.write("No chat history yet.")

    @staticmethod
    def handle_query(self, query, documents):
        """
        This method processes the query and returns the response.
        :param self: The object of the class
        :param query: The query entered by the user
        :param documents: The list of documents to compare the query with
        :return: The response to the query
        """

        # Process query and return response
        url = "http://127.0.0.1:8002/tf-idf/"

        response = requests.post(url, json={"corpus": documents, "query": query})
        if response.status_code == 200:
            res = response.json().get("response", "")
        else:
            res = "Error occurred when processing the request to url " + url

        # Append query and response to chat history
        st.session_state.history.append((query, res))

        # Display response in the text area as well
        if 'history' in st.session_state:
            chat_history = ""
            for user_input, bot_response in st.session_state.history:
                chat_history += f"**You**: {user_input}\n"
                chat_history += f"**Bot**: {bot_response}\n\n"
            # Update the chat history in the text area
            st.text_area("Chat History", value=chat_history, height=300)

    def retrive_chunks(self, query):
        """
        This method retrieves the chunks from the database.
        :param query: The query to retrieve the chunks.
        :return: The chunks and similarity scores.
        """

        url = "http://127.0.0.1:8002/retrieve_text/"

        response = requests.post(url, params={"query": query})

        if response.status_code == 200:
            res = response.json()
        else:
            res = "Error occurred when processing the request to url " + url

        # Append query and response to chat history
        st.session_state.history.append((query, res))

        # Display response in the text area as well
        if 'history' in st.session_state:
            chat_history = ""
            for user_input, bot_response in st.session_state.history:
                chat_history += f"**You**: {user_input}\n"
                chat_history += f"**Bot**: {bot_response}\n\n"
            # Update the chat history in the text area
            st.text_area("Chat History", value=chat_history, height=300)



    @staticmethod
    def clear_chat_history(self):
        """
        This method clears the chat history.
        """

        # Button to clear chat history
        if st.button("Refresh"):
            st.session_state.history = []

    # Create a button color
    @staticmethod
    def button_color(self):
        st.markdown(
            """
            <style>
            div.stButton > button:first-child {background-color: black;color: white;font-size: 16px; border-radius: 5px;border: 2px solid black;}
            div.stButton > button:first-child:hover {background-color: black;color: white;}
            </style>
            """,
            unsafe_allow_html=True,
        )