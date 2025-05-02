from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .tokens import *
from django.http import FileResponse, Http404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models import *
from .search import search_audio
from django.contrib.auth.decorators import login_required
from datetime import timedelta, timezone
from django.core.paginator import Paginator
from django.db.models import Q
from .functions import *
# Create your views here.

#Normal functions


# Authentication views
def signup_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            user = User.objects.get(username=username)
            Profile.objects.create(user=user)
            return redirect('login')
        else:
            messages.error(request, f'Your passwords do not match or are too weak')
    else:
        form = UserRegisterForm()
    return render(request, 'pages-register.html', {'form': form})



def forgot_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Create a reset token
            reset_token = PasswordResetToken.objects.create(user=user)
            plat = Platform.objects.get(name='Millesimal Arts and Entertainment')
            # Send reset email
            reset_link = f"{plat.domain}/reset-password/{reset_token.token}/"
            send_reset_email(reset_link, user)
            messages.success(request, 'Check your email for a reset link!')  # A page to inform the user to check their email
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return render(request, 'forgot.html')

    return render(request, 'forgot.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page or desired location
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = LoginForm()
    return render(request, 'pages-login.html', {'form': form})


def reemail_view(request):

    if request.method == 'POST':
        form = EmailForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            code = form.cleaned_data.get('code')
            user = User.objects.get(username=username)
            if code.lower() == user.profile.v_token.lower():
                user.profile.is_email_verified = True
                messages.success(request,f'Email successfully verified!')
                return redirect('dashboard')

            else:
                messages.error(request,'Codes do not match!')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = EmailForm()
    return render(request, 'email.html', {'form': form})


def reset_password(request, token):
    reset_token = get_object_or_404(PasswordResetToken, token=token)

    if not reset_token.is_valid():
        messages.error(request, 'Your token is invalid!') # Inform the user that the token is invalid or expired

    if request.method == 'POST':
        new_password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if new_password != confirm_password:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match.'})

        # Set the new password and mark the token as used
        user = reset_token.user
        user.password = make_password(new_password)
        user.save()
        reset_token.is_used = True
        reset_token.save()

        return redirect('login')  # Redirect to a success page

    return render(request, 'reset_password.html')

def email_view(request):
    if request.method == 'POST':
        form = EmailForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            code = form.cleaned_data.get('code')
            user = User.objects.get(username=username)
            if code.lower() == user.profile.v_token.lower():
                user.profile.is_email_verified = True
                user.profile.save()
                messages.success(request,f'Email successfully verified!')
                return redirect('dashboard')

            else:
                messages.error(request,'Codes do not match!')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = EmailForm()
    return render(request, 'email.html', {'form': form})

#Others
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'create_profile.html', {'form': form})
#Player end code
def index_view(request,*args, **kwargs):
    audios = Audio.objects.all()
    videos = Video.objects.all()

    if request.user.is_authenticated:
        return redirect('home')

    context = {
        'audios': audios,
        'videos': videos
    }
    return render(request, 'home1.html', context)

@login_required
def home_view(request,*args, **kwargs):
    audios = Audio.objects.all()
    videos = Video.objects.all()

    context = {
        'audios': audios,
        'videos': videos
    }
    return render(request, 'home.html', context)

@login_required
def user_content_view(request,user_id):
    artist = User.objects.get(id=user_id)
    audios = Audio.objects.filter(user=artist)
    videos = Video.objects.filter(user=artist)

    context = {
        'audios': audios,
        'videos': videos,
        'artist': artist,
    }
    return render(request, 'user_content.html', context)

@login_required
def trending_view(request,*args, **kwargs):
    audios = Audio.objects.all().order_by('-likes')[:20]
    videos = Video.objects.all().order_by('-likes')[:20]

    context = {
        'audios': audios,
        'videos': videos
    }
    return render(request, 'home.html', context)
@login_required
def music_view(request,*args, **kwargs):
    audios = Audio.objects.filter(type='song')
    videos = Video.objects.filter(type='song')

    context = {
        'audios': audios,
        'videos': videos
    }
    return render(request, 'home.html', context)
@login_required
def poetry_view(request,*args, **kwargs):
    audios = Audio.objects.filter(type='poem')
    videos = Video.objects.filter(type='poem')

    context = {
        'audios': audios,
        'videos': videos
    }
    return render(request, 'home.html', context)

@login_required
def podcast_view(request,*args, **kwargs):
    audios = Audio.objects.filter(type='podcast')
    videos = Video.objects.filter(type='podcast')

    context = {
        'audios': audios,
        'videos': videos
    }
    return render(request, 'home.html', context)

@login_required
def video_view(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    audios = Audio.objects.filter(genre=video.genre, type=video.type)
    videos = Video.objects.filter(genre=video.genre, type=video.type)

    context = {
        'video': video,
        'audios': audios,
        'videos': videos
    }
    return render(request, 'video-player.html', context)

@login_required
def audio_view(request, audio_id):
    audio = get_object_or_404(Audio, pk=audio_id)
    artist_songs = Audio.objects.filter(genre=audio.genre, type=audio.type)
    other_songs = Audio.objects.filter(genre=audio.genre, type=audio.type)
    audios = artist_songs | other_songs
    videos = Video.objects.filter(genre=audio.genre, type=audio.type)
    paginator = Paginator(audios, 1)
    page_number = request.GET.get('page')

    context = {
        'audio': audio,
        'audios': audios,
        'videos': videos,
        'paginator': paginator,
    }
    return render(request, 'audio-player.html', context)

@login_required
def download_audio(request, audio_id):
    audio = get_object_or_404(Audio, id=audio_id)
    audio_path = audio.audio.path
    cover_path = audio.artwork.path  # assuming you have `audio.artwork` as ImageField

    # Embed the cover art into the audio file
    embed_cover_art(audio_path, cover_path)

    # Serve the updated file
    file_name = f"{audio.title}.mp3"
    response = FileResponse(open(audio_path, 'rb'), as_attachment=True, filename=file_name)

    # Optional: track downloads
    audio.views += 1
    audio.save()

    return response
@login_required
def search_view(request,*args, **kwargs):
    videos = Video.objects.filter(type='podcast')
    query = request.GET.get('q','')
    if query:
        audios = search_audio(query)
    else:
        audios = Audio.objects.none()
    context = {
        'audios': audios,
        'videos': videos,
        'query': query
    }
    return render(request, 'home.html', context)

#Admin end  code starts here

# login required pages
@login_required
def upload_audio(request):
    notifs = Notification.objects.filter(user=request.user)
    messages = Message.objects.filter(receiver=request.user)
    genres = Genre.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        descp = request.POST.get('description')
        type  = request.POST.get('type')
        lyrics = request.POST.get('lyrics')
        art = request.FILES.get('artwork')
        audio = request.FILES.get('audio')
        genre = request.POST.get('genres')
        album = request.POST.get('album')
        aud = Audio.objects.create(
            title=title,
            description =descp,
            type=type,
            lyrics=lyrics,
            artwork=art,
            audio =audio,
            genre=Genre.objects.get(name=str(genre)),
            album=album,
            user=request.user,
        )
        ft  = request.POST.get('ft')

        if str(ft) != '':
            Ft.objects.create(
                audio = aud,
                names=ft,
            )

        return redirect('my-uploads')  # Replace 'home' with the desired redirect URL

    context = {
    'genres': genres,
    'notes': notifs,
    'messages': messages,
    }
    return render(request, 'audio_upload.html', context)

@login_required
def upload_video(request):
    notifs = Notification.objects.filter(user=request.user)
    messages = Message.objects.filter(receiver=request.user)
    genres = Genre.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        descp = request.POST.get('description')
        type  = request.POST.get('type')
        art = request.FILES.get('artwork')
        video = request.FILES.get('video')
        genre = request.POST.get('genres')
        album = request.POST.get('album')
        vid = Video.objects.create(
            title=title,
            description =descp,
            type=type,
            thumbnail=art,
            video =video,
            genre=Genre.objects.get(name=str(genre)),
            album=album,
            user=request.user,
        )
        ft = request.POST.get('ft')

        if str(ft) != '':
            Ft.objects.create(
                video=vid,
                names=ft,
            )

    return redirect('my-uploads')  # Replace 'home' with the desired redirect URL

    context = {
    'genres': genres,
    'notes': notifs,
    'messages': messages,
    }
    return render(request, 'video_upload.html', context)
@login_required
def profile_view(request):
    notifs = Notification.objects.filter(user=request.user)
    messages = Message.objects.filter(receiver=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        passform = PasswordChangeForm(request.POST, user=request.user)
        if passform.is_valid():
            passform.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        passform = PasswordChangeForm(user=request.user)
    return render(request, 'user-profile.html', {'form': form})

@login_required
def my_uploads(request):
    notifs = Notification.objects.filter(user=request.user)
    messages = Message.objects.filter(receiver=request.user)
    videos = Video.objects.filter(user=request.user)
    audios = Audio.objects.filter(user=request.user)
    context = {
        'notes': notifs,
        'messages': messages,
        'audios': audios,
        'videos': videos,
    }
    return render(request, 'forms-editors.html', context)

@login_required
def delete_audio(request, audio_id):
    # Get the media object by ID
    media = get_object_or_404(Audio, id=audio_id)

    # Delete the file from the database and the file system
    try:
        media.delete()
        messages.success(request, 'Media deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting media: {e}')

    return redirect('settings')


@login_required
def delete_video(request, video_id):
    # Get the media object by ID
    media = get_object_or_404(Video, id=video_id)

    # Delete the file from the database and the file system
    try:
        media.delete()
        messages.success(request, 'Media deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting media: {e}')

    return redirect('settings')


@login_required
def settings_view(request, *args, **kwargs):
    notifs = Notification.objects.filter(user=request.user)
    messages = Message.objects.filter(receiver=request.user)
    audios = Audio.objects.filter(user=request.user)
    videos = Video.objects.filter(user=request.user)
    user = request.user
    password_changed = False  # Flag to check if the password was changed
    if request.method == 'POST':
        pic = request.FILES.get('pic')
        first = request.POST.get('first')
        last = request.POST.get('last')
        username = request.POST.get('username')
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        fb = request.POST.get('fb')
        ig = request.POST.get('ig')
        tk = request.POST.get('tik')
        profile = Profile.objects.get(user=user)

        if pic:
            profile.profile_photo = pic
            profile.save()
        if first:
            user.first_name = first
            user.save()

        if last:
            user.last_name = last
            user.save()

        if email:
            user.email = email
            user.save()

        if username:
            user.username = username
            user.save()

        if bio:
            profile.bio = bio
            profile.save()

        if fb:
            profile.fb = fb
            profile.save()

        if ig:
            profile.ig = ig
            profile.save()

        if tk:
            profile.tk = tk
            profile.save()






    context = {
        'audios': audios,
        'videos': videos,
        'notes': notifs,
        'messages': messages,
    }
    return render(request, 'users-profile.html', context)

@login_required
def search(request):
    query = request.POST .get('q')  # Get the search query from the URL parameter 'q'
    results = []

    if query:
        # Search in Audio model
        audios = Audio.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

        # Search in Video model
        videos = Video.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

        # Combine results
        results = list(audios) + list(videos)

    return render(request, 'search_results.html', {'results': results, 'query': query, 'audios': audios, 'videos': videos})

from django.contrib.auth import get_user_model

def create_superuser(request, username, password):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username=username,
            password=password,
        )
        print("Superuser created successfully.")
    else:
        print("Superuser already exists.")

def like(request, media_id, media_type):
    if media_type == 'AUD':
        aud = get_object_or_404(Audio, id=media_id)
        Like.objects.create(
            user=request.user,
            audio=aud
        )
        aud.likes += 1
        aud.save()
        return redirect('audio', audio_id=media_id)
    if media_type == 'VID':
        vid = get_object_or_404(Video, id=media_id)
        Like.objects.create(
            user=request.user,
            video=vid
        )
        vid.likes += 1
        vid.save()
        return redirect('video', video_id=media_id)