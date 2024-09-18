import streamlit as st
import openai
import logging

# Access the OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Chatbot Assistant")
st.write("Hello! I'm your Chatbot Assistant. How can I help you today?")

# Initialize the session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Initialize input field state if not already
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Display the chat history
for chat in st.session_state.history:
    st.markdown(f"**{chat['role'].capitalize()}:** {chat['content']}")

# User input for chat
user_input = st.text_input("You:", key="user_input")


# Function to get response from OpenAI API
def get_openai_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return "Error: Unable to generate a response."


# Handle user input submission
if st.button("Send") and st.session_state.user_input:
    # Add user input to chat history
    st.session_state.history.append({"role": "user", "content": st.session_state.user_input})

    # Show spinner while processing
    with st.spinner("Generating response..."):
        # Generate chatbot response
        chatbot_response = get_openai_response(st.session_state.user_input)

    # Add chatbot response to chat history
    st.session_state.history.append({"role": "assistant", "content": chatbot_response})

    # Clear user input
    st.session_state.user_input = ""
