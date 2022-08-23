import requests
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect
from Tmdb_api_key import TMDB_API_KEY

from Movies.forms import CommentCreateForm
from Movies.models import Comment, TVAndMovie


class TvAndMovieDetail:
    def __init__(self, request, obj_tv_comment_or_movie: object) -> None:
        self.request = request
        self.obj_tv_comment_or_movie: object = obj_tv_comment_or_movie

    def get_object_tv_or_movie_data(self) -> dict:
        tv_or_movie_url: str = (
            "https://api.themoviedb.org/3/"
            + self.obj_tv_comment_or_movie.judge_tv_or_movie
            + "/"
            + str(self.obj_tv_comment_or_movie.tmdb_id)
            + "?api_key="
            + TMDB_API_KEY
            + "&language=en-US"
        )
        return (requests.get(tv_or_movie_url)).json()

    def get_recommendations_tmdb_data(self) -> dict:
        recommendations_url: str = (
            "https://api.themoviedb.org/3/"
            + self.obj_tv_comment_or_movie.judge_tv_or_movie
            + "/"
            + str(self.obj_tv_comment_or_movie.tmdb_id)
            + "/recommendations?api_key="
            + TMDB_API_KEY
            + "&language=en-US"
        )
        return (requests.get(recommendations_url)).json()


class GetObjComment:
    def __init__(self, data_obj_tv_or_movie: TvAndMovieDetail) -> None:
        self.data_obj_tv_or_movie: object = data_obj_tv_or_movie

    def get_comment_for_tv_or_movie(self) -> object:
        if self.data_obj_tv_or_movie.request.user.id is not None:
            return (
                Comment.objects.filter(
                    tv_or_movie=self.data_obj_tv_or_movie.obj_tv_comment_or_movie.id
                )
                .exclude(user=self.data_obj_tv_or_movie.request.user)
                .order_by("-updated_at")
            )
        else:
            return Comment.objects.filter(
                tv_or_movie=self.data_obj_tv_or_movie.obj_tv_comment_or_movie.id
            ).order_by("-updated_at")

    def get_user_post_comment_for_tv_or_movie(self) -> object:
        if self.data_obj_tv_or_movie.request.user.id is not None:
            try:
                return Comment.objects.get(
                    user=self.data_obj_tv_or_movie.request.user,
                    tv_or_movie=self.data_obj_tv_or_movie.obj_tv_comment_or_movie,
                )
            except Comment.DoesNotExist:
                return None
        else:
            return None


class CommentPostTask:
    def __init__(self, data_obj_tv_or_movie: TvAndMovieDetail) -> None:
        self.data_obj_tv_or_movie = data_obj_tv_or_movie
        self.get_obj_comment = GetObjComment(data_obj_tv_or_movie)

    def post_comment_action(self) -> redirect:
        mycomment_obj = self.get_obj_comment.get_user_post_comment_for_tv_or_movie()
        if self.data_obj_tv_or_movie.request.POST.get("action") == "delete":
            mycomment_obj.delete()
        else:
            form = CommentCreateForm(
                self.data_obj_tv_or_movie.request.POST, instance=mycomment_obj
            )
            if form.is_valid() and self.data_obj_tv_or_movie.request.POST.get(
                "action"
            ) == ("update"):
                form.save()
            elif form.is_valid() and self.data_obj_tv_or_movie.request.POST.get(
                "action"
            ) == ("create"):
                Comment(
                    comment=form.cleaned_data["comment"],
                    user=self.data_obj_tv_or_movie.request.user,
                    stars=form.cleaned_data["stars"],
                    tv_or_movie=self.data_obj_tv_or_movie.obj_tv_comment_or_movie,
                ).save()
        return redirect(
            "view_tv_and_movie_detail",
            type_movie_or_tv=(
                self.data_obj_tv_or_movie.obj_tv_comment_or_movie.judge_tv_or_movie
            ),
            id=self.data_obj_tv_or_movie.obj_tv_comment_or_movie.tmdb_id,
        )


class GetFormNotPost:
    def __init__(self, get_obj_comment: TvAndMovieDetail) -> None:
        self.get_obj_comment: GetObjComment = GetObjComment(get_obj_comment)

    def not_post_form_send(self):
        mycomment_obj = self.get_obj_comment.get_user_post_comment_for_tv_or_movie()
        form = CommentCreateForm(instance=mycomment_obj)
        return form


class PageGetCommentAndMovieTV:
    def __init__(self, request, data_comment) -> None:
        self.comment_list_or_obj = data_comment
        self.request = request

    def get_page(self, page_num):
        paginator = Paginator(self.comment_list_or_obj, page_num)
        page = self.request.GET.get("page", 1)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(1)
        return pages


class SenddetailMovieAndTVData:
    def __init__(self, request, obj_tv_or_movie: object, page_num: int) -> None:
        self.request = request
        self.obj_tv_or_movie = obj_tv_or_movie
        self.page_num = page_num

    def detail_movie_or_tv_set(self):
        self.data_obj = TvAndMovieDetail(self.request, self.obj_tv_or_movie)
        self.comment_data = GetObjComment(self.data_obj)
        self.form_get_obj = GetFormNotPost(self.data_obj)
        self.page_and_comment_get_obj = PageGetCommentAndMovieTV(
            self.request, self.comment_data.get_comment_for_tv_or_movie()
        )

    def send_contexts_detail(self) -> dict:
        self.detail_movie_or_tv_set()
        data_for_tv_or_movie = self.data_obj.get_object_tv_or_movie_data()
        recommendations_data = self.data_obj.get_recommendations_tmdb_data()
        movie_or_tv = self.obj_tv_or_movie.judge_tv_or_movie
        mycomment_obj = self.comment_data.get_user_post_comment_for_tv_or_movie()
        average = self.obj_tv_or_movie.average_stars()
        form = self.form_get_obj.not_post_form_send()
        pages = self.page_and_comment_get_obj.get_page(3)
        context = {
            "data": data_for_tv_or_movie,
            "recommendations": recommendations_data,
            "type": movie_or_tv,
            "mycomment": mycomment_obj,
            "average": average,
            "form": form,
            "pages": pages,  # NOTE add the comment to context
        }
        return context


class ScoreRankinghelper:
    def __init__(self, request) -> None:
        self.request = request

    def rank_movie_objs(self):
        return TVAndMovie.objects.filter(judge_tv_or_movie="movie").order_by("-stars")

    def rank_tv_objs(self):
        return TVAndMovie.objects.filter(judge_tv_or_movie="tv").order_by("-stars")

    def filter_score_query(self):
        self.min_score_query: float = (
            self.request.GET.get("min") if self.request.GET.get("min") else 0
        )
        self.max_score_query: float = (
            self.request.GET.get("max") if self.request.GET.get("max") else 10
        )

    def score_by_data_list_send(self, objs_detail_movie_or_tv) -> list:
        detail_rank_list: list = []
        if objs_detail_movie_or_tv.exists():
            for tmp_obj in objs_detail_movie_or_tv:
                average_score: float = tmp_obj.stars
                if (self.min_score_query <= average_score) and (
                    self.max_score_query >= average_score
                ):
                    data: dict = TvAndMovieDetail(
                        self.request, tmp_obj
                    ).get_object_tv_or_movie_data()
                    data["score"] = average_score
                    detail_rank_list.append(data)
        return detail_rank_list

    def get_rank_tv_and_movie(self) -> dict:
        self.filter_score_query()
        movie_rank_page = PageGetCommentAndMovieTV(
            self.request, self.score_by_data_list_send(self.rank_movie_objs())
        ).get_page(3)
        tv_rank_page = PageGetCommentAndMovieTV(
            self.request, self.score_by_data_list_send(self.rank_tv_objs())
        ).get_page(3)
        contexts = {"movie": movie_rank_page, "tv": tv_rank_page}
        return contexts


class SearchMovieAndTV:
    def __init__(self, request, query) -> None:
        self._request = request
        self._query = query

    def search_data(self) -> dict:
        url_search: str = (
            "https://api.themoviedb.org/3/search/"
            "{self._request.GET.get('type')}?"
            + "api_key={TMDB_API_KEY}&language=en-US&page=1&"
            + "include_adult=false&query={self._query}"
        )
        data_search: dict = (requests.get(url_search)).json()
        search_context = {
            "search_data": data_search,
            "type": self._request.GET.get("type"),
        }

        return search_context
