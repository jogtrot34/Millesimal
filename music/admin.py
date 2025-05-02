from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.contrib.filters.admin import RangeDateFilter
from unfold.forms import *

from .models import *


admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin,ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Audio)
class AudioAdmin(ModelAdmin):
    pass

@admin.register(Video)
class VideoAdmin(ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    pass

@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    pass

@admin.register(Message)
class MessageAdmin(ModelAdmin):
    pass

@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    pass

@admin.register(Genre)
class GenreAdmin(ModelAdmin):
    pass

@admin.register(Ft)
class FtAdmin(ModelAdmin):
    pass

@admin.register(Like)
class LikeAdmin(ModelAdmin):
    pass

@admin.register(Platform)
class PlatformAdmin(ModelAdmin):
    pass

@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(ModelAdmin):
    pass