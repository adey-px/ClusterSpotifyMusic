from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Audio


# This context name is added to settings.py to make its variables
# accessible across all templates of the project
def project_context(request):

    # Get audio_id put in session in music/now_playing view
    audio = request.session.get("audio_id")

    # Pass the audio_id into context and use the var in sidenav btn
    context = {
        'audio_play': audio,
    }

    return context
