import streamlit as st
import requests
import random
import string
import google.generativeai as genai
import re
import math

# 🔐 Configure Google Gemini AI API Key (Replace with a valid API key)
GENAI_API_KEY = "AIzaSyBBTNFznyQOKaD56pYb-dXxwbp8bGYOXAI"  # Replace with your real API key

# ✅ Set Streamlit Theme and Page Config
st.set_page_config(page_title="🔐 AI Password Strength Checker", page_icon="🔑", layout="centered")

# 🎨 Custom CSS for a Sleeker Design
custom_css = """
<style>
<style>
body, .stApp {
    background: linear-gradient(135deg, #0D47A1, #1976D2);  /* Soft Blue Gradient */
    color: #E0E0E0;
    font-family: 'Poppins', sans-serif;
}

h1, h2, h3 {
    color: #FFD700;  /* Gold Text for a Premium Feel */
    text-align: center;
    font-weight: 600;
}

.stButton button {
    background: linear-gradient(135deg, #FFD700, #FFA500) !important;
    color: #fff !important;
    border-radius: 8px;
    transition: all 0.3s ease-in-out;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.stButton button:hover {
    background: linear-gradient(135deg, #FFA500, #FFD700) !important;
    transform: scale(1.05);
}

.stTextInput input {
    border: 1px solid #FFD700;
    border-radius: 8px;
    background-color: rgba(13, 71, 161, 0.6);  /* Adjusted for new background */
    color: #E0E0E0;
    padding: 8px;
}

[data-testid="stSidebar"] {
    background-color: #1565C0;
    border-right: 1px solid #FFD700;
}

.stAlert {
    border-left: 5px solid #FFD700;
    background-color: rgba(13, 71, 161, 0.7);
    color: #E0E0E0;
}

.stMarkdown {
    background-color: rgba(13, 71, 161, 0.7);
    padding: 10px;
    border-radius: 8px;
}

.stSpinner {
    color: #FFD700 !important;
}

.card {
    background: rgba(13, 71, 161, 0.6);
    border-radius: 10px;
    padding: 20px;
    margin-bot

</style>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Initialize Google Gemini AI API
genai.configure(api_key=GENAI_API_KEY)
MODEL_NAME = "gemini-1.5-flash"

def generate_password(strength):
    chars = {
        "Weak": string.ascii_lowercase,
        "Medium": string.ascii_letters + string.digits,
        "Strong": string.ascii_letters + string.digits + "!@#$%^&*()-_=+<>?",
        "Very Strong": string.ascii_letters + string.digits + "!@#$%^&*()-_=+<>?"
    }.get(strength, "")
    length = {
        "Weak": random.randint(6, 8),
        "Medium": random.randint(8, 10),
        "Strong": random.randint(12, 16),
        "Very Strong": random.randint(18, 24)
    }.get(strength, 0)
    return "".join(random.choice(chars) for _ in range(length))

def classify_password(password):
    if len(password) < 8:
        return "❌ Weak - Too short!"
    if not (re.search(r"[A-Z]", password) and re.search(r"\d", password) and re.search(r"[!@#$%^&*()]", password)):
        return "⚠️ Medium - Needs uppercase, numbers, and special characters!"
    if len(password) >= 12:
        return "✅ Strong - Secure password!"
    return "✅ Very Strong - Highly secure password!"

def calculate_entropy(password):
    char_sets = [
        (string.ascii_lowercase, 26),
        (string.ascii_uppercase, 26),
        (string.digits, 10),
        ("!@#$%^&*()-_=+<>?", 15)
    ]
    pool_size = sum(size for charset, size in char_sets if any(c in charset for c in password))
    entropy = math.log2(pool_size) * len(password) if pool_size > 0 else 0
    return round(entropy, 2)

def improve_password_with_ai(password):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"Improve this password to make it stronger and more secure: {password}"
        response = model.generate_content(prompt)
        return response.text.strip() if response and hasattr(response, "text") else "⚠️ AI error!"
    except Exception as e:
        return f"⚠️ AI error: {e}"

def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip() if response and hasattr(response, "text") else "⚠️ AI error!"
    except Exception as e:
        return f"❌ Error: {e}"

# 🎨 Streamlit UI
st.title("🔐 AI-Powered Password Strength Checker & Chatbot")

# 📋 Sidebar Configuration
with st.sidebar:
    st.subheader("🔑 Password Generator")
    strength_level = st.selectbox("Select Strength:", ["Weak", "Medium", "Strong", "Very Strong"])
    if st.button("Generate Password"):
        generated_password = generate_password(strength_level)
        st.success(f"✅ {strength_level} Password: `{generated_password}`")

    st.subheader("🤖 Ask AI (Gemini)")
    user_prompt = st.text_input("Ask a question:")
    if st.button("Ask Gemini 🤖"):
        if user_prompt.strip():
            with st.spinner("Generating response..."):
                gemini_response = ask_gemini(user_prompt)
            st.write(gemini_response)
        else:
            st.warning("⚠️ Enter a question!")

# 📝 Password Strength Checker
st.subheader("📝 Password Strength Checker")
password_input = st.text_input("Enter your password:", type="password")
if password_input:
    strength = classify_password(password_input)
    entropy = calculate_entropy(password_input)
    st.markdown(f"**Password Strength:** {strength}")
    st.markdown(f"🔢 **Entropy Score:** `{entropy} bits`")
    with st.spinner("🔄 Improving password..."):
        improved_password = improve_password_with_ai(password_input)
    st.markdown(f"**🔒 AI Improved Password:** `{improved_password}`")
