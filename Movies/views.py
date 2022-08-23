import requests
from django.http import JsonResponse
from django.shortcuts import render
from Tmdb_api_key import TMDB_API_KEY

from Movies.helper_views import (
    CommentPostTask,
    ScoreRankinghelper,
    SearchMovieAndTV,
    SenddetailMovieAndTVData,
    TvAndMovieDetail,
)
from Movies.models import TVAndMovie

# Create your views here.


def search(request):
    # Get the query from the search box
    search_query = request.GET.get("q")
    if search_query is None:
        return render(request, "Movie/not_search.html")
    # If the query is not empty
    search_data_odject = SearchMovieAndTV(request, search_query)
    context_data = search_data_odject.search_data()
    return render(
        request,
        "Movie/results.html",
        context_data,
    )


def score_by(request) -> render:
    contents = ScoreRankinghelper(request).get_rank_tv_and_movie()
    return render(request, "Movie/score_by.html", contents)


def index(request) -> render:
    return render(request, "Movie/index.html")


def view_tv_and_movie_detail(request, type_movie_or_tv, id) -> render:
    tv_or_movie_object, _ = TVAndMovie.objects.get_or_create(
        tmdb_id=id, judge_tv_or_movie=type_movie_or_tv
    )
    if request.method == "POST":
        detail_tv_or_movie = TvAndMovieDetail(request, tv_or_movie_object)
        CommentPostTask(detail_tv_or_movie).post_comment_action()
    context_obj = SenddetailMovieAndTVData(request, tv_or_movie_object, 3)
    contents = context_obj.send_contexts_detail()
    template_place = (
        "Movie/movie_detail.html"
        if type_movie_or_tv == "movie"
        else "Movie/tv_detail.html"
    )
    return render(request, template_place, contents)


def view_trendings_results(request) -> JsonResponse:
    types: str = request.GET.get("media_type")
    time_window: str = request.GET.get("time_window")

    trendings: dict = (
        requests.get(
            f"https://api.themoviedb.org/3/trending/{types}/{time_window}?api_key={TMDB_API_KEY}&language=en-US"
        )
    ).json()
    return JsonResponse(trendings)
