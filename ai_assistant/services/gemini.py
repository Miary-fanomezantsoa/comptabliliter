import os
import google.generativeai as genai
from comptabiliter.settings import GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)
model=genai.GenerativeModel('gemini-1.5-flash-latest')
def ask_gemini(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)

        suggestion = getattr(response, "text", None)
        if suggestion:
            suggestion = suggestion.strip()
        else:
            suggestion = "Désolé, nous n'avons pas de suggestion pour ce type de problème."

        return suggestion

    except Exception as e:
        return f"Erreur IA : {e}"
