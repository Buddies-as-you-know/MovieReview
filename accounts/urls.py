from django.urls import path

from .views import (Comment_List_Movie, Comment_List_TV, HomeView,
                    PasswordChange, PasswordChangeDone, PasswordReset,
                    PasswordResetComplete, PasswordResetConfirm,
                    PasswordResetDone, ProfileEditView)

app_name = 'accounts'
urlpatterns = [
   path('home/', HomeView.as_view(), name='home'),
   path('edit_profile/', ProfileEditView.as_view(), name='edit_profile'),  # 追加
   path('commnet_list_movie/<int:user_id>/', Comment_List_Movie, name =  'comment_list_movie'),
   path('commnet_list_tv/<int:user_id>/', Comment_List_TV, name =  'comment_list_tv'),
   path('password_change/', PasswordChange.as_view(), name='password_change'),
   path('password_change/done/', PasswordChangeDone.as_view(), name='password_change_done'),
   path('password_reset/', PasswordReset.as_view(), name='password_reset'),
   path('password_reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
   path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
   path('password_reset/complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),
  
]
