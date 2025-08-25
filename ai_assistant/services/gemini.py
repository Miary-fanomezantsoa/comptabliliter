import os
import google.generativeai as genai

# Config API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Utilise un modèle valide
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(prompt: str) -> str:
    """Envoie une requête à Gemini et retourne la réponse"""
    try:
        response = model.generate_content(prompt)

        # Retourne directement le texte simplifié
        if response and hasattr(response, "text"):
            return response.text.strip()

        # Sinon, parcours les candidates manuellement
        if response and response.candidates:
            return response.candidates[0].content.parts[0].text.strip()

        return "aucune correspondance trouvée."

    except Exception as e:
        return f"Erreur: {e}"

