import streamlit as st
import google.generativeai as genai
import os

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Mon Assistant", page_icon="🤖", layout="centered")

# --- 2. STYLE (Cacher les menus Streamlit) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    h1 {color: #0066cc; text-align: center;}
    .stChatInput {border-color: #0066cc;}
    </style>
""", unsafe_allow_html=True)

# --- 3. CONNEXION ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Erreur de clé API : {e}")
    st.stop()

# --- 4. CHARGEMENT DU CONTEXTE (Vos PDF) ---
@st.cache_data
def load_context():
    if os.path.exists('contexte.txt'):
        with open('contexte.txt', 'r', encoding='utf-8') as f:
            return f.read()
    return ""

contexte = load_context()

# --- 5. LE CERVEAU (Mise à jour avec VOTRE modèle disponible) ---
try:
    # On utilise le modèle que nous avons trouvé dans votre liste
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error(f"Erreur de chargement du modèle : {e}")

# --- 6. INTERFACE DE CHAT ---
st.title("Assistant Virtuel")

# Message d'accueil
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Je connais vos documents par cœur. Posez-moi une question."}]

# Afficher l'historique
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- 7. TRAITEMENT DE LA QUESTION ---
if prompt := st.chat_input("Posez votre question ici..."):
    # Afficher la question utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Générer la réponse
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            full_prompt = f"""
            Tu es un assistant expert et pédagogique.
            Utilise UNIQUEMENT le contexte ci-dessous pour répondre.
            Si la réponse n'est pas dans le texte, dis poliment que tu ne sais pas.
            
            CONTEXTE :
            {contexte}
            
            QUESTION : 
            {prompt}
            """
            
            # Envoi à Gemini 2.0
            response = model.generate_content(full_prompt)
            
            # Affichage
            message_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            message_placeholder.error(f"Une erreur est survenue : {e}")
