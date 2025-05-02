from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import Profile
from .models import Audio, Video


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_photo', 'bio', 'birth_date', 'type']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', "class":"form-control"}),
            'bio': forms.Textarea(attrs={'placeholder': 'Tell us about yourself'}),
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email address',
            "class": "form-control"
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Choose a username',
            "class": "form-control"
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create a password',
            "class": "form-control"
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            "class": "form-control"
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-control'
        })
    )



class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = ['title', 'description', 'type', 'lyrics', 'artwork', 'audio', 'genre', 'album']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe the audio', 'class': 'form-control'}),
            'lyrics': forms.Textarea(attrs={'placeholder': 'Add lyrics (optional)', 'class': 'form-control'}),
            'album': forms.TextInput(attrs={'placeholder': 'Album name (if any)', 'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'type', 'thumbnail', 'video', 'genre', 'album']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe the video', 'class': 'form-control'}),
            'album': forms.TextInput(attrs={'placeholder': 'Album name (if any)', 'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    fields= ['old_password', 'new_password1', 'new_password2']

class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model= Profile
        fields = ['profile_photo']

class UserdetailsForm(forms.ModelForm):
    class Meta:
        model= User
        fields = ['first_name', 'last_name', 'username', 'email']