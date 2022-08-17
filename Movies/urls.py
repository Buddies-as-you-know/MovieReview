
from django.urls import path

from Movies import views

urlpatterns = [
     
    path("", views.index, name="index"),
    path("score_by/", views.score_by, name="score_by"),
    path("search/", views.search, name="search"),
    path("<str:type_movie_or_tv>/<int:id>/",
         views.view_tv_and_movie_detail,
         name="view_tv_and_movie_detail"),
    path("api/trendings/", views.view_trendings_results, name="trendings"),
]
