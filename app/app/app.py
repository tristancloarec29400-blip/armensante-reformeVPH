import streamlit as st
import google.generativeai as genai
import os

# 1. Configuration de la page (Titre et Icône)
st.set_page_config(page_title="Mon Assistant Expert", page_icon="🤖")

# 2. Masquer le branding Streamlit (Pour faire "Pro")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Connexion à Google (Récupère la clé secrète)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Erreur : La clé API n'est pas configurée.")
    st.stop()

# 4. Charger votre contexte (Mémoire)
def load_context():
    try:
        with open('contexte.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Pas de contexte trouvé."

contexte = load_context()

# 5. Configuration du modèle IA
model = genai.GenerativeModel('gemini-1.5-flash')

# 6. Interface de Chat
st.title("Bonjour, comment puis-je vous aider ?")

# Initialiser l'historique si vide
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher les anciens messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie utilisateur
if prompt := st.chat_input("Posez votre question ici..."):
    # Afficher la question de l'utilisateur
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Préparer la réponse
    try:
        # On dit à l'IA : "Voici ce que tu sais (contexte), réponds à la question."
        full_prompt = f"Tu es un assistant expert. Utilise UNIQUEMENT les informations suivantes pour répondre. Si la réponse n'est pas dans le texte, dis que tu ne sais pas.\n\nINFORMATIONS :\n{contexte}\n\nQUESTION : {prompt}"
        
        response = model.generate_content(full_prompt)
        text_response = response.text
        
        # Afficher la réponse
        with st.chat_message("assistant"):
            st.markdown(text_response)
        st.session_state.messages.append({"role": "assistant", "content": text_response})
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")
