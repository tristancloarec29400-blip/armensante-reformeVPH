import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Mon Assistant", page_icon="🤖", layout="centered")

# --- STYLE ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    h1 {color: #0066cc; text-align: center;}
    </style>
""", unsafe_allow_html=True)

# --- CONNEXION ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Erreur de clé API : {e}")
    st.stop()

# --- CHARGEMENT CONTEXTE ---
@st.cache_data
def load_context():
    if os.path.exists('contexte.txt'):
        with open('contexte.txt', 'r', encoding='utf-8') as f:
            return f.read()
    return ""

contexte = load_context()

# --- C'EST ICI LE CHANGEMENT (Modèle standard) ---
try:
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("Le modèle n'est pas disponible.")

# --- INTERFACE ---
st.title("Assistant Virtuel")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Je suis prêt à répondre à vos questions."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- TRAITEMENT QUESTION ---
if prompt := st.chat_input("Votre question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            full_prompt = f"""
            Tu es un expert. Réponds uniquement selon ce contexte.
            Si la réponse n'est pas dedans, dis que tu ne sais pas.
            
            CONTEXTE: {contexte}
            
            QUESTION: {prompt}
            """
            
            response = model.generate_content(full_prompt)
            message_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            message_placeholder.error(f"ERREUR : {e}")
