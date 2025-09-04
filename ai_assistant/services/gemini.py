import os
import google.generativeai as genai

# Config API
def ask_gemini(user, prompt: str, notif_type="info") -> str:
    try:
        response = model.generate_content(prompt)

        suggestion = ""
        if response and hasattr(response, "text"):
            suggestion = response.text.strip()
        elif response and response.candidates:
            # concatène les réponses candidates si disponibles
            suggestion = " ".join([c.text for c in response.candidates if hasattr(c, "text")])
        else:
            suggestion = "Desolé nous avons pas de suggestion pour ce type de probleme"

        # Crée une notification pour l'utilisateur
        Notification.objects.create(
            user=user,
            message=f"💡 Suggestion IA : {suggestion}",
            type=notif_type
        )

        return suggestion

    except Exception as e:
        err_msg = f"Erreur IA : {e}"
        Notification.objects.create(
            user=user,
            message=err_msg,
            type='error'
        )
        return err_msg

