from django.db import models
from django.contrib.auth.models import User
from django.core.validators import *
import uuid
from django.utils.timezone import now, timedelta

# Create your models here.
class Profile(models.Model):
    AUDIENCE = 'Audience'
    CREATOR =   'Creator'
    types = {
        (AUDIENCE, 'Audience'),
        (CREATOR, 'Creator'),
    }
    profile_photo       = models.ImageField(default='profiles/blank.png', upload_to='profiles')
    monthly_listeners   = models.IntegerField(default=0)
    user                = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio                 = models.TextField(blank=True,null=True)
    birth_date          = models.DateField(blank=False, null=True)
    type                = models.CharField(max_length=20, default='Audience', choices=types)
    fb                = models.CharField(max_length=20000, default='#')
    ig                = models.CharField(max_length=20000, default='#')
    tk                = models.CharField(max_length=20000, default='#')


    def __str__(self):
        return f"{self.user.username}'s profile"

class Genre(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name

class Audio(models.Model):

    SONG        = 'song'
    POEM        = 'poem'
    PODCAST     = 'podcast'
    TYPES       =   [
        (SONG, 'song'),
        (POEM, 'poem'),
        (PODCAST, 'podcast')
    ]
    title       = models.CharField(max_length=100)
    description = models.TextField()
    type        = models.CharField(max_length=10, choices=TYPES, default=SONG)
    lyrics      = models.TextField(default='N/A')
    artwork     = models.ImageField(default='artworks/default.jpg', upload_to='artworks')
    likes       = models.IntegerField(default=0)
    views       = models.IntegerField(default=0)
    audio       = models.FileField(null=False, blank=False)
    genre       = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    date        = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    album       = models.CharField(max_length=100, default='Unknown')

    def __str__(self):
        return f'{self.title}'

class Video(models.Model):

    SONG        = 'song'
    POEM        = 'poem'
    PODCAST     = 'podcast'
    TYPES       =   [
        (SONG, 'song'),
        (POEM, 'poem'),
        (PODCAST, 'podcast')
    ]
    title       = models.CharField(max_length=100)
    description = models.TextField()
    type        = models.CharField(max_length=10, choices=TYPES, default=SONG)
    thumbnail   = models.ImageField(null=True, blank=True,upload_to='artworks')
    likes       = models.IntegerField(default=0)
    views       = models.IntegerField(default=0)
    video       = models.FileField(null=False, blank=False)
    genre       = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    date        = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    album       = models.CharField(max_length=100, default='Unknown')

    def __str__(self):
        return f'{self.title}'

class Message(models.Model):
    sender  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} to {self.receiver} - {self.message}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} - {self.message}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100, unique=True)
    valid = models.BooleanField(default=True)

    def __str__(self):
        return f"Payment {self.transaction_id} for {self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        message = f"Your payment of {self.amount} has been confirmed! Expect your account to be activated soon."
        Notification.objects.create(user=self.user, message=message)

    def mark_invalid(self):
        self.valid = False
        self.save()

class Like(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    video= models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True,related_name='vid_likes')
    audio= models.ForeignKey(Audio, on_delete=models.CASCADE, null=True, blank=True, related_name='aud_likes')
    def __str__(self):
        return f'{self.user.username}: like {self.id}'

class Ft(models.Model):
    names = models.CharField(max_length=6000)
    video= models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True,related_name='vid_fts')
    audio= models.ForeignKey(Audio, on_delete=models.CASCADE, null=True, blank=True, related_name='aud_fts')
    def __str__(self):
        return f' ft {self.names}'


class Platform(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    domain = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="password_reset_tokens")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        # Check if the token is valid (e.g., valid for 1 hour)
        return not self.is_used and self.created_at >= now() - timedelta(hours=1)

    def __str__(self):
        return f"Token for {self.user.username} {self.token}"