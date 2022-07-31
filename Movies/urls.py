
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
     path('score_by/', views.Score_by, name='score_by'),
    path("search/", views.search, name="search"),
    path("tv/<int:tv_id>/", views.view_tv_detail, name="view_tv_detail"),
    path("movie/<int:movie_id>/", views.view_movie_detail , name='view_movie_detail'),
    path("api/trendings/", views.view_trendings_results, name="trendings"),
]
