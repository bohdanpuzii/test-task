from django.contrib import admin

from .models import User, Post, PostLikes

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(PostLikes)
