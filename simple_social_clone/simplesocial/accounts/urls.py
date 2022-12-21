from django.urls import path
from django.contrib.auth import views as auth_views # For using built-in LoginView and LogoutView
from . import views # Custom user-made views from 'views.py'

app_name = 'accounts' # For accessing the urls of this app using its <app_name>:<view_name> in url template tags

urlpatterns = [
    # You can set the template_name attribute of LoginView class here itself
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup')
]