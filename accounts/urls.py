from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    path('', views.Dashboard.as_view(), name='dashboard'), # dashboard url

    path('register/', views.Register.as_view(), name='register'), # register new user
    path('edit/', views.EditProfile.as_view(), name='edit'), # edit Profile

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), # login urls from drf
    path('obtain-auth-token/', views.CustomAuthToken.as_view() ), # obtain custom auth token 
]
