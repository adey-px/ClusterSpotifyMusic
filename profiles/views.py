from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from music.forms import AudioForm

from music.models import Audio

# Create your views here.


# View that displays profile for each user
def profile(request):
    """ Display current user's profile """

    # From UserProfile model, get profile (by username) for user,
    # then return it to designated page - profile.html
    user_pro = get_object_or_404(UserProfile, user=request.user)

    template = 'profiles/profile.html'

    context = {
        'username': user_pro,
    }

    return render(request, template, context)
