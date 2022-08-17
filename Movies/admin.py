from django.contrib import admin

from Movies.models import Comment, TVAndMovie

# Register your models here.
admin.site.register(Comment)
admin.site.register(TVAndMovie)
