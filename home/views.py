from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from music.models import Audio
from profiles.models import UserProfile

# Create your views here.


# Home page view that renders all audio from db
def index(request):
    """ A view that renders home page with all audio songs """

    songs = Audio.objects.all()
    query = None

    # Search audio by title or artist in search bar
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']

            queries = Q(title__icontains=query) | Q(artist__icontains=query)
            songs = songs.filter(queries)

            # If user submit empty or blank form
            if not query:
                messages.error(request,
                               ("You didn't enter any search criteria!"))
                return redirect(reverse('home'))

    context = {
        "songs": songs,
        "search_term": query,
    }

    return render(request, 'home/index.html', context)
