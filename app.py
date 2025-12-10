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

# --- LE CERVEAU (CELUI DE VOTRE LISTE) ---
# On utilise le modèle 2.0 Lite Preview qui était dans votre diagnostic
try:
    model = genai.GenerativeModel('models/gemini-2.0-flash-lite-preview-02-05')
except:
    st.error("Erreur fatale de modèle.")

# --- INTERFACE ---
st.title("Assistant Virtuel")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Je suis connecté au modèle 2.0 Lite. Posez-moi une question sur votre page."}]

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
            if "429" in str(e):
                 message_placeholder.warning("⏳ Limite de vitesse atteinte. Attendez 30 secondes.")
            elif "404" in str(e):
                 message_placeholder.error(f"Modèle introuvable : {e}")
            else:
                 message_placeholder.error(f"Erreur : {e}")
