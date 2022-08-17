import requests
from django.http import JsonResponse
from django.shortcuts import render
from Tmdb_api_key import TMDB_API_KEY

from Movies.helper_views import (CommentPostTask, SenddetailMovieAndTVData,
                                 TvAndMovieDetail)
from Movies.models import TVAndMovie

# Create your views here.


def search(request):
    # Get the query from the search box
    pass
    """
    search_query = request.GET.get("q")
    search_data_odject = TmbdMovieTV("search", request=request)
    # If the query is not empty
    if search_query is None:
        return render(request, "Movie/not_search.html")
    context_data = search_data_odject.search_data(search_query)
    return render(
        request,
        "Movie/results.html",
        context_data,
    )
"""


def score_by(request):
    pass
    """
    movies = Movie.objects.order_by("-stars")
    movie_score_data = TmbdMovieTV("movie", movies, inputs_request=request)
    movie_score_list = movie_score_data.score_by_data_format_save()
    pages_movie = movie_score_data.pagitor_deliver(movie_score_list, 3)
    tvs = TV.objects.order_by("-stars")
    tv_score_data = TmbdMovieTV("tv", tvs, inputs_request=request)
    tv_score_list = tv_score_data.score_by_data_format_save()
    pages_tv = tv_score_data.pagitor_deliver(tv_score_list, 3)
    context = {"movie": pages_movie, "tv": pages_tv}
    return render(request, "Movie/score_by.html", context)
    """


def index(request):
    return render(request, "Movie/index.html")


def view_tv_and_movie_detail(request, type_movie_or_tv, id):
    tv_or_movie_object, _ = TVAndMovie.objects.get_or_create(
        tmdb_id=id, judge_tv_or_movie=type_movie_or_tv
    )
    detail_tv_or_movie = TvAndMovieDetail(request, tv_or_movie_object)
    if request.method == "POST":
        comment_post = CommentPostTask(detail_tv_or_movie)
        comment_post.post_comment_action()
    context_obj = SenddetailMovieAndTVData(detail_tv_or_movie,3)
    contents = context_obj.send_contexts_detail()
    template_place = "Movie/movie_detail.html" if type_movie_or_tv == "movie" else "Movie/tv_detail.html"
    return render(request, template_place, contents)


def view_trendings_results(request):
    types: str = request.GET.get("media_type")
    time_window: str = request.GET.get("time_window")

    trendings: dict = (
        requests.get(
            f"https://api.themoviedb.org/3/trending/{types}/{time_window}?api_key={TMDB_API_KEY}&language=en-US"
        )
    ).json()
    return JsonResponse(trendings)
