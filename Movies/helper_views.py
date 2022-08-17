import requests
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect
from Tmdb_api_key import TMDB_API_KEY

from Movies.forms import CommentCreateForm
from Movies.models import Comment


class TvAndMovieDetail:
    def __init__(self,
                 request,
                 obj_tv_or_movie: object) -> None:
        self.request = request
        self.obj_tv_or_movie: object = obj_tv_or_movie
        
     
class GetObjComment:
    def __init__(self, data_obj_tv_or_movie: TvAndMovieDetail) -> None:
        self.data_obj_tv_or_movie: object = data_obj_tv_or_movie
        
    def get_comment_for_tv_or_movie(self) -> object:
        if self.data_obj_tv_or_movie.request.user.id is not None:
            return (
                Comment.objects.filter(tv_or_movie=self.data_obj_tv_or_movie.obj_tv_or_movie.id)
                .exclude(user=self.data_obj_tv_or_movie.request.user)
                .order_by("-updated_at")
            )
        else:
            return Comment.objects.filter(tv_or_movie=self.data_obj_tv_or_movie.obj_tv_or_movie.id).order_by(
                "-updated_at"
            )

    def get_user_post_comment_for_tv_or_movie(self) -> object:
        if self.data_obj_tv_or_movie.request.user.id is not None:
            try:
                return Comment.objects.get(
                    user=self.data_obj_tv_or_movie.request.user, tv_or_movie=self.data_obj_tv_or_movie.obj_tv_or_movie
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
            form = CommentCreateForm(self.data_obj_tv_or_movie.request.POST, instance=mycomment_obj)
            if form.is_valid() and self.data_obj_tv_or_movie.request.POST.get("action") == "update":
                form.save()
            elif form.is_valid() and self.data_obj_tv_or_movie.request.POST.get("action") == "create":
                Comment(
                    comment=form.cleaned_data["comment"],
                    user=self.data_obj_tv_or_movie.request.user,
                    stars=form.cleaned_data["stars"],
                    tv_or_movie=self.data_obj_tv_or_movie.obj_tv_or_movie,
                ).save()
        return redirect("view_tv_and_movie_detail",
                        type_movie_or_tv=self.data_obj_tv_or_movie.obj_tv_or_movie.judge_tv_or_movie,
                        id=self.data_obj_tv_or_movie.obj_tv_or_movie.tmdb_id,
                        )
                
                
class GetFormNotPost:
    def __init__(self, get_obj_comment: object) -> None:
        self.get_obj_comment: GetObjComment = GetObjComment(get_obj_comment)
          
    def not_post_form_send(self):
        mycomment_obj = self.get_obj_comment.get_user_post_comment_for_tv_or_movie()
        form = CommentCreateForm(instance=mycomment_obj)
        return form
    
    
class PageGetComment(GetObjComment):
    def __init__(self, data_obj_tv_or_movie: object, page_num: int) -> None:
        super().__init__(data_obj_tv_or_movie)
        self.page_num: int = page_num
    
    def get_page_comment(self):
        other_comments = self.get_comment_for_tv_or_movie()
        paginator = Paginator(other_comments, self.page_num)
        page = self.data_obj_tv_or_movie.request.GET.get("page", 1)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(1)
        return pages


class SenddetailMovieAndTVData:
    def __init__(self, data_obj_tv_or_movie: TvAndMovieDetail, page_num: int) -> None:
        self.data_obj_tv_or_movie = data_obj_tv_or_movie
        self.form_get_obj = GetFormNotPost(data_obj_tv_or_movie)
        self.page_and_comment_get_obj = PageGetComment(data_obj_tv_or_movie, page_num)
        
    def get_object_tv_or_movie_data(self) -> dict:
        tv_or_movie_url: str = (
            "https://api.themoviedb.org/3/" +
            self.data_obj_tv_or_movie.obj_tv_or_movie.judge_tv_or_movie +
            "/" +
            str(self.data_obj_tv_or_movie.obj_tv_or_movie.tmdb_id) +
            "?api_key=" +
            TMDB_API_KEY +
            "&language=en-US"
        )
        return (requests.get(tv_or_movie_url)).json()

    def get_recommendations_tmdb_data(self) -> dict:
        recommendations_url: str = (
            "https://api.themoviedb.org/3/" +
            self.data_obj_tv_or_movie.obj_tv_or_movie.judge_tv_or_movie +
            "/" +
            str(self.data_obj_tv_or_movie.obj_tv_or_movie.tmdb_id) +
            "/recommendations?api_key=" +
            TMDB_API_KEY +
            "&language=en-US"
        )
        return (requests.get(recommendations_url)).json()

    def send_contexts_detail(self) -> dict:
        data_for_tv_or_movie = self.get_object_tv_or_movie_data()
        recommendations_data = self.get_recommendations_tmdb_data()
        for_movie_or_tv = self.data_obj_tv_or_movie.obj_tv_or_movie.judge_tv_or_movie
        mycomment_obj = self.page_and_comment_get_obj.get_user_post_comment_for_tv_or_movie()
        average = self.data_obj_tv_or_movie.obj_tv_or_movie.average_stars()
        form = self.form_get_obj.not_post_form_send()
        pages = self.page_and_comment_get_obj.get_page_comment()
        context = {
            "data": data_for_tv_or_movie,
            "recommendations": recommendations_data,
            "type": for_movie_or_tv,
            "mycomment": mycomment_obj,
            "average": average,
            "form": form,
            "pages": pages,  # NOTE add the comment to context
        }
        return context
    
"""
class TmbdMovieTV:
    def __init__(
        self,
        tv_or_movie_judge: str,
        tv_or_movie_object: object = None,
        inputs_request=None,
        tmdb_api_key: str = TMDB_API_KEY,
    ) -> None:
        self.judge_tv_or_movie = tv_or_movie_judge
        self.object_tv_or_movie = tv_or_movie_object
        self.inputs_request = inputs_request
        self.tmdb_api_key = tmdb_api_key

    
    def recommendations_tmdb_data(self, id) -> requests:
        recommendations_url: str = (
            "https://api.themoviedb.org/3/" +
            self.judge_tv_or_movie +
            "/" +
            str(id) +
            "/recommendations?api_key=" +
            self.tmdb_api_key +
            "&language=en-US"
        )
        recommendations = requests.get(recommendations_url)
        print(recommendations_url)
        return recommendations
    
    def score_by_data_format_save(self) -> None:
        min_score_query: float = 0
        max_score_query: float = 10
        if self.inputs_request.GET.get("min") and self.inputs_request.GET.get("max"):
            min_score_query = self.inputs_request.request.GET.get("min")
            max_score_query = self.inputs_request.request.GET.get("max")
        tv_or_movie_list: list = []
        if self.object_tv_or_movie.exists():
            for tmp_obj in self.object_tv_or_movie:
                if (min_score_query <= tmp_obj.average_stars()) and (
                    max_score_query >= tmp_obj.average_stars()
                ):
                    tv_or_movie_url: str = (
                        "https://api.themoviedb.org/3/" +
                        self.judge_tv_or_movie +
                        "/" +
                        tmp_obj.id +
                        "?api_key=" +
                        self.tmdb_api_key +
                        "&language=en-US"
                    )
                    data: dict = (requests.get(tv_or_movie_url)).json()
                    data["score"] = tmp_obj.average_stars()
                    tv_or_movie_list.append(data)
        return tv_or_movie_list
    
    def search_data(self, query) -> dict:
        url_search: str = (
            "https://api.themoviedb.org/3/search/" +
            "{self.__request.GET.get('type')}?" +
            "api_key={self.__tmdb_api_key}&language=en-US&page=1&" +
            "include_adult=false&query={query}"
        )
        data_search: dict = (requests.get(url_search)).json()

        search_context = {
            "search_data": data_search,
            "type": self.inputs_request.GET.get("type"),
        }

        return search_context

    def pagitor_deliver(self, tv_or_movie_list, page_number, html_page_tag="page") -> Paginator:
        paginator: Paginator = Paginator(tv_or_movie_list, page_number)
        page = self.inputs_request.GET.get(html_page_tag, 1)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(1)
        return pages
    
    def detail_tv_show(self, id):
        if TV.objects.filter(id=id).exists() is False:
            TV(id=id).save()
        tv = get_object_or_404(TV, id=id)
        if self.inputs_request.user.id is not None:
            try:
                comment_tv = Comment_tv.objects.get(user=self.inputs_request.user, tv=tv)
            except Comment_tv.DoesNotExist:
                comment_tv = None
        else:
            comment_tv = None
        if self.inputs_request.method == "POST":
            if self.inputs_request.POST.get("action") == "delete":
                comment_tv.delete()
                return redirect("view_tv_detail", tv_id=id)
            else:
                form = Comment_tv_CreateForm(self.inputs_request.POST, instance=comment_tv)
                if form.is_valid() and self.inputs_request.POST.get("action") == "update":
                    form.save()
                    return redirect("view_tv_detail", tv_id=id)
                elif form.is_valid() and self.inputs_request.POST.get("action") == "create":
                    Comment_tv(
                        comment=form.cleaned_data["comment"],
                        user=self.inputs_request.user,
                        stars=form.cleaned_data["stars"],
                        tv=tv,
                    ).save()
                    return redirect("view_tv_detail", tv_id=id)
        else:
            form = Comment_tv_CreateForm(instance=comment_tv)
        if self.inputs_request.user.id is not None:
            comments = Comment_tv.objects.filter(tv_id=id).exclude(user=self.inputs_request.user).order_by("-id")
            mycomment = reversed(Comment_tv.objects.filter(tv_id=id, user=self.inputs_request.user))
        else:
            comments = Comment_tv.objects.filter(tv_id=id).order_by("-id")
            mycomment = reversed(Comment_tv.objects.none())
        return comments, mycomment, tv, form
"""
