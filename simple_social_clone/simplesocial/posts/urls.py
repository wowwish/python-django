# URLs for the 'posts' app
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostList.as_view(), name='all'),
    path('post/new', views.CreatePost.as_view(), name='create'),
    # REFER: https://docs.djangoproject.com/en/4.1/topics/http/urls/#path-converters
    path('by/<str:username>/', views.UserPosts.as_view(), name='for_user'),
    path('by/<str:username>/<int:pk>/', views.PostDetail.as_view(), name='single'),
    path('delete/<int:pk>/', views.DeletePost.as_view(), name='delete')
]
