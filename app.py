import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Mon Assistant", page_icon="🤖")

# --- CONNEXION ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Erreur de clé : {e}")
    st.stop()

# --- CHARGEMENT CONTEXTE ---
@st.cache_data
def load_context():
    if os.path.exists('contexte.txt'):
        with open('contexte.txt', 'r', encoding='utf-8') as f:
            return f.read()
    return ""

contexte = load_context()

# --- MODÈLE (Le Standard 1.5 Flash) ---
# C'est le meilleur pour le mode gratuit
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    # Roue de secours si le premier échoue
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- INTERFACE ---
st.title("Assistant Virtuel")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Je suis prêt."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Votre question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            full_prompt = f"Contexte: {contexte}. Question: {prompt}"
            response = model.generate_content(full_prompt)
            message_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            message_placeholder.error(f"Erreur : {e}")
