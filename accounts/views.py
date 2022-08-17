
import requests  # 追加
from django.contrib.auth.mixins import LoginRequiredMixin  # 追加
from django.contrib.auth.views import (PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from Tmdb_api_key import TMDB_API_KEY

from accounts.forms import (MyPasswordChangeForm, MyPasswordResetForm,
                            MySetPasswordForm, ProfileForm)
from accounts.models import CustomUser


# userのhome
class HomeView(TemplateView):
    template_name = "account/home.html"
    model = CustomUser


# userのプロフィール変更
class ProfileEditView(LoginRequiredMixin, UpdateView):  # 追加
    template_name = "account/edit_profile.html"
    model = CustomUser
    form_class = ProfileForm
    success_url = "/accounts/edit_profile/"

    def get_object(self):
        return self.request.user


def Comment_List_Movie(request, user_id):
    comment_movie = Comment_movie.objects.filter(user=user_id)  # ４０４は表示せずuserが何も持っていないことを示す。
    context = {}
    context["user"] = CustomUser.objects.filter(id=user_id)
    if comment_movie.exists():
        movie_list = []
        for obj in comment_movie:
            data = requests.get(
                f"https://api.themoviedb.org/3/movie/{obj.movie.id}?api_key={TMDB_API_KEY}&language=en-US"
            )
            data_movie = data.json()
            data_movie["comment"] = obj.comment
            data_movie["stars"] = obj.stars
            movie_list.append(data_movie)
        paginator_movie = Paginator(movie_list, 5)
        page_movie = request.GET.get("page", 1)
        try:
            pages_movie = paginator_movie.page(page_movie)
        except PageNotAnInteger:
            pages_movie = paginator_movie.page(1)
        except EmptyPage:
            pages_movie = paginator_movie.page(1)
        context["pages"] = pages_movie
    return render(request, "account/user_comment_list_movie.html", context)


def Comment_List_TV(request, user_id):
    comment_tv = Comment_tv.objects.filter(user=user_id)  # ４０４は表示せずuserが何も持っていないことを示す。
    context = {}
    context["user"] = CustomUser.objects.filter(id=user_id)
    if comment_tv.exists():
        tv_list = []
        for obj in comment_tv:
            data = requests.get(
                f"https://api.themoviedb.org/3/tv/{obj.tv.id}?api_key={TMDB_API_KEY}&language=en-US"
            )
            data_tv = data.json()
            data_tv["comment"] = obj.comment
            data_tv["stars"] = obj.stars
            tv_list.append(data_tv)
        paginator_tv = Paginator(tv_list, 5)
        page_tv = request.GET.get("page", 1)
        try:
            pages_tv = paginator_tv.page(page_tv)
        except PageNotAnInteger:
            pages_tv = paginator_tv.page(1)
        except EmptyPage:
            pages_tv = paginator_tv.page(1)
        context["pages"] = pages_tv
    return render(request, "account/user_comment_list_tv.html", context)


class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""

    form_class = MyPasswordChangeForm
    success_url = reverse_lazy("accounts:password_change_done")
    template_name = "account/password_change.html"


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""

    template_name = "account/password_change_done.html"


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""

    subject_template_name = "account/mail_template/password_reset/subject.txt"
    email_template_name = "account/mail_template/password_reset/message.txt"
    template_name = "account/password_reset_form.html"
    form_class = MyPasswordResetForm
    success_url = reverse_lazy("accounts:password_reset_done")


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""

    template_name = "account/password_reset_done.html"


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""

    form_class = MySetPasswordForm
    success_url = reverse_lazy("accounts:password_reset_complete")
    template_name = "account/password_reset_confirm.html"


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""

    template_name = "account/password_reset_complete.html"
