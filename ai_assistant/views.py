from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .services.mistral import ask_mistral
from .services.gemini import ask_gemini

from rest_framework.decorators import api_view
@csrf_exempt
@require_http_methods(["POST"])
def gemini_api_view(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        prompt = data.get("prompt", "")
        if not prompt:
            return JsonResponse({"error": "Le champ 'prompt' est requis"}, status=400)

        response = ask_gemini(prompt)
        return JsonResponse({"response": response})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['POST'])
def chat(request):
    data = request.data
    message = data.get("message", "")

    if not message:
        return JsonResponse({"reply": "Aucun message reçu."}, status=400)

    try:
        reply = ask_mistral(message)
        return JsonResponse({"reply": reply})
    except Exception as e:
        return JsonResponse({"reply": "Erreur lors de la génération de la réponse."}, status=500)
