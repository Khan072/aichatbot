# =============================================================================
# AI Chatbot - app.py
# A beginner-friendly Streamlit chatbot powered by Google Gemini
# =============================================================================

import os                          # Access environment variables
import streamlit as st             # Build the web UI
from google import genai           # New official Google Gemini SDK
from google.genai import types     # For configuration objects
from dotenv import load_dotenv     # Load secrets from .env file

# -----------------------------------------------------------------------------
# 1. LOAD ENVIRONMENT VARIABLES
#    python-dotenv reads the .env file and loads GEMINI_API_KEY into the
#    process environment so we never hard-code the key in Python.
# -----------------------------------------------------------------------------
load_dotenv()


# -----------------------------------------------------------------------------
# 2. CONFIGURE THE PAGE
#    This must be the very first Streamlit call in the script.
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered",
)


# -----------------------------------------------------------------------------
# 3. HELPER FUNCTIONS
# -----------------------------------------------------------------------------

def get_gemini_client():
    """
    Create and return a Gemini client using the API key from the environment.
    Returns None if the key is missing, so we can show a friendly error.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None  # Key not found → will be handled in the UI layer

    return genai.Client(api_key=api_key)


def initialize_session_state():
    """
    Set up st.session_state on the very first run.

    st.session_state is Streamlit's way of keeping data alive between
    re-renders. Without it, every user action would wipe the chat history
    because Streamlit reruns the entire script on each interaction.
    """
    if "messages" not in st.session_state:
        # We store our system prompt separately
        st.session_state.system_prompt = (
            "You are a helpful, friendly, and knowledgeable AI assistant. "
            "Answer questions clearly and concisely. "
            "If you are unsure about something, say so honestly. "
            "Be encouraging and supportive to beginners learning new topics."
        )
        # Chat history — only user and assistant messages (no system here)
        st.session_state.messages = []


def clear_chat():
    """
    Reset the conversation by clearing the messages list.
    """
    st.session_state.messages = []


def get_ai_response(client, messages: list, system_prompt: str) -> str:
    """
    Send the full conversation history to Gemini and return the reply.

    Tries multiple models in order. If one is overloaded (503) or
    unavailable (404), it automatically falls back to the next one.
    """
    # Models tried in order — first available one wins
    MODELS = [
        "gemini-flash-latest",
        "gemini-flash-lite-latest",
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-pro-latest",
    ]

    # Convert previous messages (all except last) into Gemini history format
    # Gemini uses "user" and "model" roles (not "user" and "assistant")
    history = []
    for msg in messages[:-1]:   # all but the last message
        role = "user" if msg["role"] == "user" else "model"
        history.append(
            types.Content(
                role=role,
                parts=[types.Part(text=msg["content"])]
            )
        )

    last_error = None

    for model_name in MODELS:
        try:
            # Create a chat session with full prior history
            chat = client.chats.create(
                model=model_name,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.7,
                    max_output_tokens=1024,
                ),
                history=history,
            )

            # Send only the latest user message
            response = chat.send_message(messages[-1]["content"])

            # Gemini can return multi-part responses (thinking + text).
            # Iterate parts and return the last non-empty text part.
            if response.candidates:
                for candidate in response.candidates:
                    parts_text = [
                        part.text
                        for part in candidate.content.parts
                        if hasattr(part, "text") and part.text
                    ]
                    if parts_text:
                        return parts_text[-1]

            continue  # no text found, try next model

        except Exception as e:
            err_str = str(e)
            # 503 = overloaded, 404 = not found → silently try next model
            if any(code in err_str for code in ["503", "UNAVAILABLE", "404", "NOT_FOUND"]):
                last_error = e
                continue
            raise  # re-raise unexpected errors (bad key, network, etc.)

    # All models exhausted
    raise last_error or Exception("All Gemini models are currently unavailable. Please try again in a moment.")


def render_sidebar():
    """Draw the sidebar with app info and the Clear Chat button."""
    with st.sidebar:
        st.title("🤖 AI Chatbot")
        st.markdown("---")

        st.markdown("### About")
        st.info(
            "A beginner-friendly AI chatbot built with Streamlit and Google Gemini. "
            "Ask me anything — I'm here to help!"
        )

        st.markdown("### 🛠️ Tech Stack")
        st.markdown(
            """
            | Layer | Technology |
            |-------|-----------|
            | UI | Streamlit |
            | LLM | Gemini Flash (Latest) |
            | Language | Python 3.11+ |
            | Secrets | python-dotenv |
            | Memory | st.session_state |
            """
        )

        st.markdown("---")

        # Clear Chat button resets the conversation
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_chat()
            st.rerun()  # Force Streamlit to rerun so the empty chat appears

        st.markdown("---")
        st.caption("Built with ❤️ using Streamlit & Google Gemini")


def render_chat_history():
    """
    Replay every message in session_state onto the screen.
    Messages are stored as {"role": "user"/"assistant", "content": "..."}
    """
    for message in st.session_state.messages:
        role = message["role"]       # "user" or "assistant"
        content = message["content"]

        with st.chat_message(role):  # Renders with correct avatar
            st.markdown(content)


# -----------------------------------------------------------------------------
# 4. MAIN APPLICATION
# -----------------------------------------------------------------------------

def main():
    # -- Step A: Set up persistent state ----------------------------------------
    initialize_session_state()

    # -- Step B: Draw the sidebar ------------------------------------------------
    render_sidebar()

    # -- Step C: Page header -----------------------------------------------------
    st.title("💬 AI Chatbot")
    st.caption("Powered by Google Gemini Flash · Ask me anything!")

    # -- Step D: Validate the API key early -------------------------------------
    client = get_gemini_client()

    if client is None:
        st.error(
            "⚠️ **Gemini API key not found.**\n\n"
            "Please create a `.env` file in the project folder and add:\n"
            "```\nGEMINI_API_KEY=your-key-here\n```\n"
            "Get a free key at: https://aistudio.google.com/app/apikey\n\n"
            "Then restart the app with `streamlit run app.py`."
        )
        st.stop()  # Halt rendering — nothing else works without the key

    # -- Step E: Render existing conversation ------------------------------------
    render_chat_history()

    # -- Step F: Accept new user input ------------------------------------------
    #    st.chat_input() sticks to the bottom of the page automatically.
    user_input = st.chat_input("Type your message here…")

    if user_input:
        # Trim whitespace; ignore blank submissions
        user_input = user_input.strip()

        if not user_input:
            st.warning("Please type a message before sending.")
            st.stop()

        # -- Step G: Show the user's message immediately -----------------------
        with st.chat_message("user"):
            st.markdown(user_input)

        # -- Step H: Append user message to history ----------------------------
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        # -- Step I: Call Gemini and display the response ----------------------
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                try:
                    reply = get_ai_response(
                        client,
                        st.session_state.messages,
                        st.session_state.system_prompt,
                    )
                except Exception as e:
                    # Catch API errors (quota, invalid key, network, etc.)
                    st.error(f"❌ Gemini API error: {e}")
                    # Remove the user message so history stays clean
                    st.session_state.messages.pop()
                    st.stop()

            st.markdown(reply)

        # -- Step J: Save assistant reply to history ---------------------------
        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )


# -----------------------------------------------------------------------------
# 5. ENTRY POINT
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
