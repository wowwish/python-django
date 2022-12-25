from django.urls import path
from . import views

app_name = 'groups' # To reference these 'groups' app URLs later in templates

urlpatterns = [
    path('', views.ListGroups.as_view(), name='all'),
    path('new/', views.CreateGroup.as_view(), name='create'),
    # REFER: https://docs.djangoproject.com/en/4.1/topics/http/urls/#path-converters
    path('posts/in/<slug:slug>/', views.SingleGroup.as_view(), name='single'),
    # Although we use only the slugified group name as unique identified for the 'group' model instance in the URL,
    # most modern web apps use both the primary key and the slugified name as the unique identifier in the URL string.
    path('join/<str:slug>/', views.JoinGroup.as_view(), name='join'),
    path('leave/<str:slug>/', views.LeaveGroup.as_view(), name='leave'),
]