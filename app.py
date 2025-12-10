import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Diagnostic", page_icon="🔧")
st.title("🔧 Diagnostic Google Gemini")

# 1. Vérification de la Clé
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    st.success("✅ ÉTAPE 1 : Clé API détectée.")
except Exception as e:
    st.error(f"❌ ÉTAPE 1 : Problème de clé. {e}")
    st.stop()

# 2. Liste des modèles disponibles
st.write("---")
st.write("⏳ Je demande à Google la liste des modèles disponibles pour votre compte...")

try:
    modeles_trouves = []
    # On demande la liste
    for m in genai.list_models():
        # On garde ceux qui savent générer du texte
        if 'generateContent' in m.supported_generation_methods:
            st.code(m.name) # On affiche le nom technique exact
            modeles_trouves.append(m.name)
            
    if len(modeles_trouves) > 0:
        st.success(f"✅ J'ai trouvé {len(modeles_trouves)} modèles utilisables !")
        st.info("Copiez le nom d'un modèle ci-dessus et donnez-le moi.")
    else:
        st.error("❌ Aucun modèle trouvé. Votre clé API semble valide mais n'a accès à aucun service.")
        st.warning("Conseil : Vérifiez que vous avez activé la facturation (Billing) sur Google Cloud si vous utilisez un projet payant, ou recréez une clé gratuite.")

except Exception as e:
    st.error(f"❌ Erreur lors de la récupération de la liste : {e}")
