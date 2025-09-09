from django.contrib import admin

from .models import Accounts, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'post_type',
        'image',
    ]


@admin.register(Accounts)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = [
        'tgid',
        'userlogin',
        'username',
        'rateclass',
        'lastdate',
        'regdate',
    ]
    readonly_fields = (
        'tgid',
        'userlogin',
        'username',
                       )