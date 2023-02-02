from django.conf.urls import url
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('', views.note_list, name="note_list"),
    path('loginpage/', views.loginpage, name="loginpage"),
    path('mainpage/', views.mainpage, name="mainpage"),
    path('register/', views.register, name="register"),
    path('change_password/', views.change_password, name="change_password"),
    path('change_username/', views.change_username, name="change_username"),
    path('change_email/', views.change_email, name="change_email"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="home/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="home/password_reset_sent.html"),
         name="password_reset_done"),
    path('reser/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="home/password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="home/password_reset_done.html"),
         name="password_reset_complete"),
    path('logout/', LogoutView.as_view(next_page='loginpage'), name="logout"),
    path('ShareNote/', views.ShareNote, name="ShareNote"),
    path('createnote-success/', views.createnotesuccess, name="createnote-success"),
    path('note_list/', views.note_list, name="note_list"),
    path('note_details/<int:id>', views.note_details, name="note_details"),
    path('my_notes', views.my_notes, name="my_notes"),
    path('delete_note/<int:id>', views.delete_note, name="delete_note"),
    path('favourite_note/<int:id>', views.favourite_note, name="favourite_note"),
    path('note_favourite_list', views.note_favourite_list, name="note_favourite_list"),
    path('delete_fav_note/<int:id>', views.delete_fav_note, name="delete_fav_note"),
    path('Cancelled_note/<int:id>', views.Cancelled_note, name="Cancelled_note"),
    path('Approved_note/<int:id>', views.Approved_note, name="Approved_note"),
    path('admin_pending_notes', views.admin_pending_notes, name="admin_pending_notes"),
    path('admin_pending_comments/<int:id>', views.admin_pending_comments, name="admin_pending_comments"),
    path('delete_comment/<int:id>', views.delete_comment, name="delete_comment"),
    path('publish_comment/<int:id>', views.publish_comment, name="publish_comment"),
    path('chatbot', views.chatbot, name="chatbot"),
]