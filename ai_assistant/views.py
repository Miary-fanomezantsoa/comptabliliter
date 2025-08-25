from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .services.gemini import ask_gemini

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
