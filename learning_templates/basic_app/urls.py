from django import urls
from basic_app import views
from django.urls import path

# TEMPLATE TAGGING. REFER : https://docs.djangoproject.com/en/4.1/topics/http/urls/#naming-url-patterns
# Setting up the app namespace:
app_name = 'basic_app'
urlpatterns = [
    path('relative/', views.relative, name='relative'),
    path('other/', views.other, name='other'),
]