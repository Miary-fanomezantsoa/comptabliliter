# ai_assistant/services/mistral.py
from text_generation import Client

MODEL_PATH = "../../../Mistral-7B-Instruct-v0.3-Q6_K.gguf"  # remplace par le chemin exact
client = Client(MODEL_PATH)

def ask_mistral(prompt: str, max_length: int = 200) -> str:
    """Génère une réponse à partir d'un prompt local GGUF"""
    response = client.generate(prompt, max_new_tokens=max_length)
    return response.generations[0].text
