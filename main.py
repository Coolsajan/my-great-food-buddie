import streamlit as st
from app.recommender import retrive_generate, check_dB_data
import time
from streamlit_lottie import st_lottie
import requests
import json

# Set page configuration
st.set_page_config(
    page_title="Food Buddy Chatbot",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling and animations
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stApp {
        max-width: 1000px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        display: flex;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .chat-message.user {
        background-color: #2b313e;
        color: #fff;
        border-top-right-radius: 0;
    }
    .chat-message.bot {
        background-color: #ffffff;
        border-top-left-radius: 0;
    }
    .chat-message .avatar {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1rem;
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
        padding: 15px 20px;
        font-size: 16px;
        border: 1px solid #ddd;
        background-color: white;
    }
    .stButton>button {
        border-radius: 20px;
        padding: 10px 24px;
        font-weight: 500;
        background-color: #FF5349;
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #E73F3F;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    .bounce {
        animation: bounce 1s ease infinite;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    .stTitle {
        font-size: 2.5rem !important;
        font-weight: 300 !important;
        margin-bottom: 2rem !important;
        color: #2b313e;
        text-align: center;
    }
    .step-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    div[data-testid="stVerticalBlock"] > div:has(div.step-indicator) {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .step-indicator {
        font-weight: bold;
        color: #FF5349;
        margin-bottom: 10px;
    }
    .loading-dots:after {
        content: '.';
        animation: dots 1.5s steps(5, end) infinite;
    }
    @keyframes dots {
        0%, 20% { content: '.'; }
        40% { content: '..'; }
        60% { content: '...'; }
        80%, 100% { content: ''; }
    }
</style>
""", unsafe_allow_html=True)

# Function to load and display Lottie animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.place = ""
    st.session_state.location = ""
    st.session_state.question = ""
    st.session_state.first_load = True

# Load animations
food_lottie = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_UBiAAmbBRN.json")
search_lottie = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_bdsthrsj.json")
chat_lottie = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_4fewfamh.json")

# Header with animation
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🍽️Great Food Buddie",)
    if food_lottie:
        st_lottie(food_lottie, height=150, key="food_animation")

# Simulated typing effect function
def simulate_typing(message, message_placeholder):
    full_message = ""
    for char in message:
        full_message += char
        message_placeholder.markdown(full_message + "▌")
        time.sleep(0.01)
    message_placeholder.markdown(full_message)
    return full_message

# Function to display chat messages
def display_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
            st.write(message["content"])

# Process user input based on current step
def process_user_input(user_input):
    if not user_input:
        return
        
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Process based on current step
    if st.session_state.step == 1:
        st.session_state.place = user_input
        st.session_state.step = 2
        
        # Add bot response
        response = f"Great! '{user_input}' sounds delicious. Where is it located?"
        st.session_state.messages.append({"role": "assistant", "content": response})
        
    elif st.session_state.step == 2:
        st.session_state.location = user_input
        st.session_state.step = 3
        
        # Extract reviews into ChromeaDB
        foodPlace = st.session_state.place + "_" + st.session_state.location
        
        # Display loading message with animation
        with st.spinner("Looking up information about this place..."):
            time.sleep(1)
            st.session_state.retriver = check_dB_data(foodPlace=foodPlace)
        
        response = f"I've found information about {st.session_state.place} in {user_input}. What would you like to know about it?"
        st.session_state.messages.append({"role": "assistant", "content": response})
        
    elif st.session_state.step == 3:
        st.session_state.question = user_input
        
        # Get response using the retriever
        with st.spinner("Finding answers for you..."):
            _, answer = retrive_generate(
                retriever=st.session_state.retriver,
                question=st.session_state.question
            )
        
        response = answer
        st.session_state.messages.append({"role": "assistant", "content": response})

# Initial welcome message
if st.session_state.first_load:
    welcome_message = "👋 Hello! I'm your Food Buddy AI assistant. I can help you find information about restaurants or food places. What restaurant would you like to know about?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})
    st.session_state.first_load = False

# Display chat history
display_messages()

# Chat input
user_input = st.chat_input("Type your message here...")
if user_input:
    process_user_input(user_input)
    # Force a rerun to update the chat
    st.rerun()

# Add a sidebar with options
with st.sidebar:
    st.header("Options")
    
    if st.button("Start New Conversation"):
        # Reset all states
        st.session_state.messages = []
        st.session_state.step = 1
        st.session_state.place = ""
        st.session_state.location = ""
        st.session_state.question = ""
        st.session_state.first_load = True
        st.rerun()
    
    # Show current status
    st.subheader("Current Status")
    if st.session_state.place:
        st.info(f"Restaurant: {st.session_state.place}")
    if st.session_state.location:
        st.info(f"Location: {st.session_state.location}")
    
    # Display the Lottie animation in the sidebar
    if chat_lottie:
        st_lottie(chat_lottie, height=200, key="chat_animation")
    
    st.markdown("---")
    st.caption("Great Food Buddie - Your personal restaurant information assistant")