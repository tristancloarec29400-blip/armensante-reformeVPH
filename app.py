import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Mon Assistant", page_icon="🤖", layout="centered")

# CSS pour le style
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    h1 {color: #0066cc; text-align: center;}
    </style>
""", unsafe_allow_html=True)

# Connexion
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.warning("⚠️ Clé API manquante.")
    st.stop()

# Chargement contexte
@st.cache_data
def load_context():
    if os.path.exists('contexte.txt'):
        with open('contexte.txt', 'r', encoding='utf-8') as f:
            return f.read()
    return ""

contexte = load_context()
model = genai.GenerativeModel('gemini-1.5-flash')

# Chat
st.title("Assistant Virtuel")
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Comment puis-je vous aider ?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Votre question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        full_prompt = f"Réponds uniquement selon ce contexte : {contexte}. Question : {prompt}"
        response = model.generate_content(full_prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
    except:
        st.error("Erreur de connexion.")
