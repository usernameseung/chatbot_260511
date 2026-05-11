import streamlit as st
from openai import OpenAI
import base64

# --- Page Configuration ---
st.set_page_config(
    page_title="귀여운 챗봇 친구", 
    page_icon="💖", 
    layout="wide",
)

# --- Custom Cute UI/UX with CSS ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# (Optional: Add a base64 background image, for simplicity, I'll use a color and shapes)
# background_image_base64 = get_base64_of_bin_file("cute_background.png") # Put a cute png in the same folder

st.markdown("""
<style>
    /* Main Background and Container */
    .stApp {
        background-color: #ffeef2; /* Light pastel pink/cream */
        background-image: 
            radial-gradient(#ffcad4 10%, transparent 10%),
            radial-gradient(#b3e5fc 5%, transparent 5%);
        background-size: 80px 80px, 40px 40px;
        background-position: 0 0, 40px 40px;
    }
    .main .block-container {
        padding: 2rem 5rem;
        background-color: rgba(255, 255, 255, 0.7); /* Translucent white inner container */
        border-radius: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }

    /* Typography */
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap');
    html, body, [class*="st-"] {
        font-family: 'Quicksand', sans-serif;
    }
    h1 {
        font-weight: 700 !important;
        color: #ff6b81 !important; /* Hearty Pink */
        text-shadow: 2px 2px 0px rgba(255, 107, 129, 0.2);
    }
    h2, h3, h4, h5, h6, .stSubheader {
        font-weight: 600 !important;
        color: #a29bfe !important; /* Soft Purple */
    }

    /* Inputs (API Key, Chat Input) */
    .stTextInput > div > div > input, 
    .stChatInput > div > div > div > textarea {
        border-radius: 20px !important;
        border: 2px solid #ffcad4 !important;
        background-color: #fffaf0 !important;
        padding: 10px 15px !important;
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus,
    .stChatInput > div > div > div > textarea:focus {
        border-color: #ff6b81 !important;
        box-shadow: 0 0 10px rgba(255, 107, 129, 0.3) !important;
    }
    .stChatInput > div {
        bottom: 10px !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 20px !important;
        padding: 5px !important;
    }

    /* Chat Messages */
    .stChatMessage {
        border-radius: 25px !important;
        padding: 15px 20px !important;
        margin-bottom: 15px !important;
        max-width: 80%;
    }
    .stChatMessage.user {
        background-color: #d1f2ff !important; /* Soft blue for user */
        float: right !important;
        border-bottom-right-radius: 5px !important;
    }
    .stChatMessage.assistant {
        background-color: #fce4ec !important; /* Soft pink for assistant */
        float: left !important;
        border-top-left-radius: 5px !important;
    }
    .stChatMessage div.avatar {
        width: 35px !important;
        height: 35px !important;
        font-size: 20px !important;
        line-height: 35px !important;
        border-radius: 50% !important;
    }
    .stChatMessage .avatar p {
        margin: 0 !important;
    }

    /* Link and Buttons */
    a {
        color: #ff6b81 !important;
        text-decoration: underline !important;
    }
    button.st-af {
        border-radius: 20px !important;
        background-color: #ff6b81 !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 8px 20px !important;
    }
    button.st-af:hover {
        background-color: #ff8e9b !important;
    }

    /* Info Box */
    .stAlert {
        border-radius: 20px !important;
        background-color: #ffe082 !important;
        color: #795548 !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- App Title and Description ---
# Custom header structure
st.markdown("""
<div style='text-align: center; margin-bottom: 30px;'>
    <div style='font-size: 70px;'>💖</div>
    <h1>귀여운 챗봇 친구</h1>
    <p style='color: #888; font-size: 1.1em;'>
        안녕! 저는 OpenAI의 GPT-3.5 모델을 사용하는 친구예요.<br>
        나랑 신나게 이야기하고 싶다면, 너의 특별한 API 키를 보여줘!<br>
        <a href="https://platform.openai.com/account/api-keys" target="_blank">키는 여기서 얻을 수 있어</a> (비밀이야!🤫)<br>
        혹시 챗봇 만드는 법이 궁금하면, <a href="https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps" target="_blank">우리 튜토리얼을 따라해봐!</a>
    </p>
</div>
""", unsafe_allow_html=True)


# --- API Key Input ---
# Place it inside a container to manage its appearance better
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # A more inviting label
        openai_api_key = st.text_input("✨ 당신의 OpenAI API 키는?", type="password", help="키를 입력하고 엔터를 눌러주세요!")
    
if not openai_api_key:
    # A friendlier info message
    st.info("비밀 키를 아직 입력하지 않았네요! 키를 보여줘야 친구가 될 수 있어요.", icon="🔑")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    # Target elements in the CSS using user and assistant classes
    for message in st.session_state.messages:
        # Custom avatars
        avatar_emoji = "👤" if message["role"] == "user" else "💖"
        with st.chat_message(message["role"], avatar=avatar_emoji):
            st.markdown(message["content"])

    # --- Chat Input field ---
    if prompt := st.chat_input("오늘 기분이 어때? 무슨 이야기든 환영이야!"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response and store it.
        with st.chat_message("assistant", avatar="💖"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
