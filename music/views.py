from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When
from django.core.paginator import Paginator

from profiles.models import UserProfile
from .models import Audio

from .forms import AudioForm

# Create your views here.


# View for uploading or adding audio into db. Note attached user profile
@login_required
def add_audio(request):
    """ A view that uploads audio songs into db """

    # Note capture of .files to get in the images of the audio uploaded.
    # Based on django message levels in base.html, message.success, .error etc
    # .....will select template to use from includes/toasts directory

    # First check if current user is registered and properly logged in
    # to prevent any user with add_audio url from gaining access to add audio
    if request.user.is_authenticated:
        if request.method == 'POST':

            # Get UserProfile model, imported above, from profiles app
            user_profile = UserProfile.objects.get(user=request.user)

            # Check if form is submitted, then attach its data to current user
            form = AudioForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(user_profile)
                messages.success(request, 'New audio added successfully')
                return redirect('add_audio')
            else:
                messages.error(request, 'Failed to add audio. Please try again.')
                return redirect('add_audio')
        else:
            form = AudioForm()
    else:
        return redirect(reverse('account_signup'))

    template = 'music/add_audio.html'
    context = {
        'form': form
    }

    return render(request, template, context)


# View for displaying blank page when user has not played audio
def not_playing(request):
    """ A view that displays blank page """

    return render(request, 'music/not_playing.html')


# View for playing audio songs existing in db
# This view performs 2 functions - logic to play audio and 
# code to render now_playing template, wc can be separated
def now_playing(request, audio_id):
    """ A view that plays/pauses audio songs from db """

    # Get each audio to play by id from the db
    audio_playing = get_object_or_404(Audio, pk=audio_id)

    # Pass the audio_id of audio playing into current session
    # Ref to context.py where this session audio_id is used
    if audio_playing:
        request.session['audio_id'] = audio_id

    # Get all audios from db, making audio_playing always show 1st
    # using Conditional expressions - Case & When
    audios = Audio.objects.all().order_by(
        Case(When(pk=audio_playing.pk, then=0), default=1)
    )

    # Pass audios variable above into paginator - one audio per page
    interface = Paginator(audios, 1)
    paging = request.GET.get('page')
    pagination = interface.get_page(paging)

    # For right sidebar, get all audios from db to display them
    songs = Audio.objects.all()

    context = {
        "pagination": pagination,
        "active_audio": audio_playing,
        "songs": songs
    }

    return render(request, 'music/now_playing.html', context)


# View for displaying audio added/uploaded by user in their accounts
# Note - Another way is by saving audio (in add_audio view above) in
# user_profile.my_audio where my_audio is a field inside the Profile model
# This avoids published_by in Audio model. Ref to save_audio view below.
@login_required
def my_audio(request):
    """ A view that displays user audio. Get user profile and use it
    to filter all audio objects in the Audio model """

    # Get audios from db and filter them by current user profile
    user_profile = UserProfile.objects.get(user=request.user)
    audio = Audio.objects.filter(published_by=user_profile)

    context = {
        'user_audio': audio
    }

    return render(request, 'music/my_audio.html', context)


# View for editing uploaded audio by inidividual user
@login_required
def edit_audio(request, audio_id):
    """ A view that edits audio """

    # Get userprofile & the selected audio by id from db to be edited
    user_profile = UserProfile.objects.get(user=request.user)
    audio = get_object_or_404(Audio, pk=audio_id)

    # Check if audio is published_by the current user, else throw error
    if user_profile == audio.published_by:
        # Get form data with instance of the audio selected by its id
        if request.method == 'POST':
            form = AudioForm(request.POST, request.FILES, instance=audio)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your audio was edited successfully')
                return redirect('my_audio')
            else:
                messages.error(request, 'Failed task. Please try again.')
                return redirect('edit_audio')
        else:
            form = AudioForm(instance=audio)

    # If not, check if user has admin/superuser previledges
    elif request.user.is_superuser:
        if request.method == 'POST':
            form = AudioForm(request.POST, request.FILES, instance=audio)
            if form.is_valid():
                form.save()
                messages.success(request, 'Selected audio was edited successfully')
                return redirect('manage_product')
            else:
                messages.error(request, 'Failed task. Please try again.')
                return redirect('edit_audio')
        else:
            form = AudioForm(instance=audio)

    # If at least one in the above conditions is not met, throw error
    else:
        messages.error(request, 'You are not authorized to edit audio.')
        return redirect(reverse('home'))

    template = 'music/edit_audio.html'
    context = {
        'form': form,
        'audio': audio,
    }

    return render(request, template, context)


# View for deleting uploaded audio in individual user account
@login_required
def delete_audio(request, audio_id):
    """ A view that edits audio uploaded in user account """

    # Get userprofile & the selected audio by id from db to be deleted
    user_profile = UserProfile.objects.get(user=request.user)
    audio = get_object_or_404(Audio, pk=audio_id)

    # First check if current user is registered and properly logged in
    if request.user.is_authenticated:

        # Check if audio is published_by the current user
        if user_profile == audio.published_by:
            audio.delete()
            messages.success(request, 'Your audio has been deleted')
            return redirect(reverse('my_audio'))
        
        # Verify if current user has admin/superuser previledges
        elif request.user.is_superuser:
            audio.delete()
            messages.success(request, 'Unwanted audio has been deleted.')
            return redirect(reverse('manage_product'))

        # If at least one in the above conditions is not met, throw error
        else:
            messages.error(request, 'You are not authorized to delete audio.')
            return redirect(reverse('home'))


# View for saving favourite audio to fav_audio field in userprofile
# Note - this view is only logic code that carries out a functionality
# Since it doesn't return any template, it doesn't require context.
@login_required
def save_audio(request, audio_id):
    """ A view that saves favourite audio """

    # Get audio from db and userprofile from Profile model
    audio = get_object_or_404(Audio, pk=audio_id)
    user_profile = UserProfile.objects.get(user=request.user)

    # First check if current user is registered and properly logged in
    if request.user.is_authenticated:

        # Add/Save the audio inside fav_audio field in userprofile
        user_profile.fav_audio.add(audio)
        messages.success(request, 'Your favourite audio has been saved')
    else:
        return redirect(reverse('account_signup'))

    # After adding/saving audio, redirect to home page
    return redirect(reverse('home'))


# View for displaying saved favourite audio in user account
# Note - this view can be combined with save_audio after return redirect
# Refer to add_audio view above for sample logic
@login_required
def view_saved_audio(request):

    # Get current userprofile & all audio in their fav_audio field
    user_profile = UserProfile.objects.get(user=request.user)
    favourite = user_profile.fav_audio.all()

    # Pass it to context and render it in template
    context = {
        'favourite': favourite,
    }

    return render(request, 'music/saved_audio.html', context)


# View for displaying play history to user account
@login_required
def history(request):
    """ A view that gets play history """

    return render(request, 'music/history.html')


# View for sharing audio to social media platforms
@login_required
def share_audio(request):
    """ A view that shares audio to social media """

    return render(request, 'music/share_audio.html')


# View for managing product on the site
@login_required
def manage_product(request):
    """ A view that diplays all audios from db to be managed """

    # Get all audios from db for product management
    songs = Audio.objects.all()

    context = {
        'audios': songs,
    }

    return render(request, 'music/manage_product.html', context)
