from django.contrib import admin

from .models import TV, Comment_movie, Comment_tv, Movie

# Register your models here.
admin.site.register(Comment_movie)
admin.site.register(Comment_tv)
admin.site.register(Movie)
admin.site.register(TV)
