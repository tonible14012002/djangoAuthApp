from importlib.resources import path
from posixpath import basename
from unicodedata import name
from django.urls import path, reverse_lazy
from. import views
from django.contrib.auth import views as auth_views
app_name = 'accounts'

urlpatterns = [
    path('home', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/api', views.loginUser, name='login-api'),
    path('logout/', auth_views.LogoutView\
        .as_view(next_page = reverse_lazy('accounts:login')), name='logout'),
    path('password_change', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/api', views.password_change_api, name='password_change_api'),
    
    path('password_reset/', views. password_reset, name='password_reset'),
    path('password_reset/api', views.password_reset_api, name='password_reset_api'),
    path('password_reset/confirm/<uidb64>/<token>', views.password_reset_confirm, name='password_reset_confirm'),
    path('password_reset/confirm/api/<uidb64>/<token>', views.password_reset_confirm_api, name='password_reset_confirm_api')

]