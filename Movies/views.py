import requests
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from Movies.forms import Comment_movie_CreateForm, Comment_tv_CreateForm
from Movies.models import TV, Comment_movie, Comment_tv, Movie
from Movies.wrapper import CreateSearchAndReturnTVOrMovie
from Tmdb_api_key import TMDB_API_KEY


# Create your views here.
def search(request):
    # Get the query from the search box
    search_query = request.GET.get("q")
    search_data_odject = CreateSearchAndReturnTVOrMovie("search", request=request)
    # If the query is not empty
    if search_query is None:
        return render(request, "Movie/not_search.html")
    context_data = search_data_odject.search_data(search_query)
    return render(
        request,
        "Movie/results.html",
        context_data,
    )


def score_by(request):
    movies = Movie.objects.order_by("-stars")
    movie_score_data = CreateSearchAndReturnTVOrMovie("movie", movies, inputs_request=request)
    movie_score_data.score_by_data_format_save()
    pages_movie = movie_score_data.pagitor_deliver(3)
    tvs = TV.objects.order_by("-stars")
    tv_score_data = CreateSearchAndReturnTVOrMovie("tv", tvs, inputs_request=request)
    tv_score_data.score_by_data_format_save()
    pages_tv = tv_score_data.pagitor_deliver(3)
    context = {"movie": pages_movie, "tv": pages_tv}
    return render(request, "Movie/score_by.html", context)


def index(request):
    return render(request, "Movie/index.html")


def view_tv_detail(request, tv_id):
    if TV.objects.filter(id=tv_id).exists() is None:
        TV(id=tv_id).save()
    tv = get_object_or_404(TV, id=tv_id)

    if request.user.id is not None:
        try:
            comment_tv = Comment_tv.objects.get(user=request.user, tv=tv)
        except Comment_tv.DoesNotExist:
            comment_tv = None
    else:
        comment_tv = None

    if request.method == "POST":
        if request.POST.get("action") == "delete":
            comment_tv.delete()
            return redirect("view_tv_detail", tv_id=tv_id)
        else:
            form = Comment_tv_CreateForm(request.POST, instance=comment_tv)
            if form.is_valid() and request.POST.get("action") == "update":
                form.save()
                return redirect("view_tv_detail", tv_id=tv_id)
            elif form.is_valid() and request.POST.get("action") == "create":
                Comment_tv(
                    comment=form.cleaned_data["comment"],
                    user=request.user,
                    stars=form.cleaned_data["stars"],
                    tv=tv,
                ).save()
                return redirect("view_tv_detail", tv_id=tv_id)
    else:
        form = Comment_tv_CreateForm(instance=comment_tv)

    data = requests.get(
        f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={TMDB_API_KEY}&language=en-US"
    )
    recommendations = requests.get(
        f"https://api.themoviedb.org/3/tv/{tv_id}/recommendations?api_key={TMDB_API_KEY}&language=en-US"
    )
    if request.user.id is not None:
        comments = Comment_tv.objects.filter(tv_id=tv_id).exclude(user=request.user)
        mycomment = reversed(Comment_tv.objects.filter(tv_id=tv_id, user=request.user))
    else:
        comments = Comment_tv.objects.filter(tv_id=tv_id)
        mycomment = reversed(Comment_tv.objects.none())
    paginator = Paginator(comments, 3)
    page = request.GET.get("page", 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)
    average = tv.average_stars()
    context = {
        "data": data.json(),
        "recommendations": recommendations.json(),
        "type": "tv",
        "pages": pages,
        "mycomment": mycomment,
        "average": average,
        "form": form,
        "comment_tv": comment_tv,
    }
    return render(request, "Movie/tv_detail.html", context)


def view_movie_detail(request, movie_id):
    if Movie.objects.filter(id=movie_id).exists() is None:
        Movie(id=movie_id).save()
    movie = get_object_or_404(Movie, id=movie_id)

    if request.user.id is not None:
        try:
            comment_movie = Comment_movie.objects.get(user=request.user, movie=movie)
        except Comment_movie.DoesNotExist:
            comment_movie = None
    else:
        comment_movie = None

    if request.method == "POST":
        if request.POST.get("action") == "delete":
            comment_movie.delete()
            return redirect("view_movie_detail", movie_id=movie_id)
        else:
            form = Comment_movie_CreateForm(request.POST, instance=comment_movie)
            if form.is_valid() and request.POST.get("action") == "update":
                form.save()
                return redirect("view_movie_detail", movie_id=movie_id)
            elif form.is_valid() and request.POST.get("action") == "create":
                Comment_movie(
                    comment=form.cleaned_data["comment"],
                    user=request.user,
                    stars=form.cleaned_data["stars"],
                    movie=movie,
                ).save()
                return redirect("view_movie_detail", movie_id=movie_id)
    else:
        form = Comment_movie_CreateForm(instance=comment_movie)

    # Put your view logic outside of the conditional expression.
    # Otherwise your code breaks when the form validates to False
    data = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    )
    recommendations = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}&language=en-US"
    )
    if request.user.id is not None:
        comments = (
            Comment_movie.objects.filter(movie_id=movie_id)
            .exclude(user=request.user)
            .order_by("-id")
        )
        mycomment = reversed(
            Comment_movie.objects.filter(movie_id=movie_id, user=request.user)
        )
    else:
        comments = Comment_movie.objects.filter(movie_id=movie_id).order_by("-id")
        mycomment = reversed(Comment_movie.objects.none())
    paginator = Paginator(comments, 3)
    page = request.GET.get("page", 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)

    average = movie.average_stars()
    context = {
        "data": data.json(),
        "recommendations": recommendations.json(),
        "type": "movie",
        "mycomment": mycomment,
        "average": average,
        "form": form,
        "pages": pages,
        "comment_movie": comment_movie,  # NOTE add the comment to context
    }
    return render(request, "Movie/movie_detail.html", context)


def view_trendings_results(request) -> JsonResponse:

    types: str = request.GET.get("media_type")
    time_window: str = request.GET.get("time_window")

    trendings: dict = (
        requests.get(
            f"https://api.themoviedb.org/3/trending/{types}/{time_window}?api_key={TMDB_API_KEY}&language=en-US"
        )
    ).json()
    return JsonResponse(trendings)
