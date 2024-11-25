from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ..utils import generate_chat_completion

@csrf_exempt
def ask_chatgpt_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            system = data.get("system")
            user = data.get("user")

            if not system or not user:
                return JsonResponse({"error": "Content and question are required."}, status=400)

            response = generate_chat_completion(system, user)

            return JsonResponse({"response": response}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)