"""simplesocial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views # Import the custom views from the 'views.py' that we have created here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePage.as_view(), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')), # connect the URLs from the 'accounts' app to the project
    # We also give an application/instance namespace for the URLs being included here as 'accounts'
    path('accounts/', include('django.contrib.auth.urls')), # also include the in-built authorization URLs from Django in 'accounts/' path
    path('test/', views.TestPage.as_view(), name='test'), 
    path('thanks/', views.ThanksPage.as_view(), name='thanks'),
    # connect the URLs from the 'postss' app to the project
    # We also give an application/instance namespace for the URLs being included here as 'posts'
    # This will make the 'posts' app urls to be accessible as 'posts:create', 'posts:delete' etc.
    path('posts/', include('posts.urls', namespace='posts')),
    # connect the URLs from the 'groups' app to the project
    # We also give an application/instance namespace for the URLs being included here as 'groups'
    # This will make the 'groups' app urls to be accessible as 'groups:join', 'groups:leave' etc.
    path('groups/', include('groups.urls', namespace='groups')),
]
