# App speciic URLs
from django.urls import path
from AppTwo import views

urlpatterns = [
    path('', views.help, name='help'),
    path('users/', views.table, name='User Table'),
    path('newuser/', views.new, name="New User")
]
