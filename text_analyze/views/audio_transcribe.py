from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import assemblyai as aai
from ..utils import generate_chat_completion

load_dotenv()

# Access the OpenAI API key
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
if not ASSEMBLYAI_API_KEY:
    raise ValueError("ASSEMBLYAI_API_KEY is not set in the environment variables.")

aai.settings.api_key = ASSEMBLYAI_API_KEY
transcriber = aai.Transcriber()

@csrf_exempt
def transcribe_audio_view(request):
    if request.method == "POST":
        try:
            # Default question
            default_system_command = "Break down the user content into numerical steps like in a list. The list will be used as instructions for a computer to follow."

            # Parse question and audio file from request
            request_data = request.POST.dict()
            system = request_data.get("system", default_system_command)
            audio_file = request.FILES.get('audio_file')
            
            if not audio_file:
                return JsonResponse({"error": "Audio file is required."}, status=400)

            # Transcribe audio
            user = transcriber.transcribe(audio_file)

            if user.status == aai.TranscriptStatus.error:
                return JsonResponse({"error": f"Transcription failed: {user.error}"}, status=500)

            # Use ChatGPT to create steps
            command_steps = generate_chat_completion(
                system,
                user.text
            )

            return JsonResponse({"steps": command_steps}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)