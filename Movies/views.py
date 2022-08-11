import requests
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from Movies.forms import Comment_movie_CreateForm, Comment_tv_CreateForm
from Movies.models import TV, Comment_movie, Comment_tv, Movie

# Create your views here.

TMDB_API_KEY = "XXXXX"


def search(request):
    # Get the query from the search box
    query = request.GET.get("q")
    # If the query is not empty
    if query:
        data = requests.get(
            f"https://api.themoviedb.org/3/search/{request.GET.get('type')}?api_key={TMDB_API_KEY}&language=en-US&page=1&include_adult=false&query={query}"
        )
    else:
        return render(request, "Movie/not_search.html")

    # Render the template
    return render(
        request,
        "Movie/results.html",
        {"data": data.json(), "type": request.GET.get("type")},
    )


def Score_by(request):
    query_min = 0
    query_max = 10
    if request.GET.get("min") and request.GET.get("max"):
        query_min = request.GET.get("min")
        query_max = request.GET.get("max")
    movies = Movie.objects.order_by("-stars")
    if movies.exists():
        movie_list = []

        for obj in movies:
            if (float(query_min) <= float(obj.average_stars())) and (
                float(query_max) >= float(obj.average_stars())
            ):
                data = requests.get(
                    f"https://api.themoviedb.org/3/movie/{obj.id}?api_key={TMDB_API_KEY}&language=en-US"
                )
                data_movie = data.json()
                data_movie["score"] = obj.average_stars()
                movie_list.append(data_movie)

        paginator_movie = Paginator(movie_list, 3)
        page_movie = request.GET.get("page", 1)
        try:
            pages_movie = paginator_movie.page(page_movie)
        except PageNotAnInteger:
            pages_movie = paginator_movie.page(1)

        except EmptyPage:
            pages_movie = paginator_movie.page(1)
    tv = TV.objects.order_by("-stars")
    tv_list = []
    if tv.exists():
        for obj in tv:
            if (float(query_min) <= float(obj.average_stars())) and (
                float(query_max) >= float(obj.average_stars())
            ):
                data = requests.get(
                    f"https://api.themoviedb.org/3/tv/{obj.id}?api_key={TMDB_API_KEY}&language=en-US"
                )
                data_tv = data.json()
                data_tv["score"] = obj.stars
                tv_list.append(data_tv)
        paginator_tv = Paginator(tv_list, 3)
        page_tv = request.GET.get("page", 1)
        try:
            pages_tv = paginator_tv.page(page_tv)
        except PageNotAnInteger:
            pages_tv = paginator_tv.page(1)
        except EmptyPage:
            pages_tv = paginator_tv.page(1)
    context = {"movie": pages_movie, "tv": pages_tv}
    return render(request, "Movie/score_by.html", context)


def index(request):
    return render(request, "Movie/index.html")


def view_tv_detail(request, tv_id):
    if not (TV.objects.filter(id=tv_id)):
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

    if not (Movie.objects.filter(id=movie_id)):
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


def view_trendings_results(request):
    type = request.GET.get("media_type")
    time_window = request.GET.get("time_window")

    trendings = requests.get(
        f"https://api.themoviedb.org/3/trending/{type}/{time_window}?api_key={TMDB_API_KEY}&language=en-US"
    )
    return JsonResponse(trendings.json())
