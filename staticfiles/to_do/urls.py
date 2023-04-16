from django.urls import path
from . import views
from .views import UpdateProfile, TaskDeleteView, NewTask, UpdateTask, TaskDetail, PasswordsChangeView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup-user', views.signup, name='signup'),
    path('signin-user', views.signin, name='signin'),
    path('sign-out', views.signout, name='signout'),
    path('new-task', NewTask.as_view(), name='new-task'),
    path('account-settings/<str:pk>',
         views.account_settings, name='account-settings'),
    path('update-my-#@@$@!@profile/<str:pk>/',
         UpdateProfile.as_view(), name='update-profile'),
     path('update-my-#@@$@!@task12/<str:pk>/',
         UpdateTask.as_view(), name='update-task'),
    path('confirmed_deletion>', views.success_onDelete, name='confirm_deletion'),
     path('task/<str:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
     path('task/<str:pk>/inDetail/', TaskDetail.as_view(), name='task_detail'),
    path('allmytasks', views.alltasks, name='all-tasks'),
    path('go_back/', views.go_back, name='go_back'),
    #change password
    path('change-password/', PasswordsChangeView.as_view(template_name='passcode_reset/change-password.html'), name='change-password'),
    #forgot password / resetting security key
    #1
    path('reset_password/', 
    auth_views.PasswordResetView.as_view(template_name='passcode_reset/email_input_reset_password.html'), 
    name='reset_password'),
    #2
    path('password_reset_sent/', 
    auth_views.PasswordResetDoneView.as_view(template_name='passcode_reset/password_reset_sent.html'), 
    name='password_reset_done'),
    #3
    path('reset/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(template_name='passcode_reset/password_reset_confirm.html'), 
    name='password_reset_confirm'),
    #4
    path('reset_password_complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name='passcode_reset/password_reset_complete.html'), 
    name='password_reset_complete'),

]
