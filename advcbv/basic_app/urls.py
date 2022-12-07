from django.urls import path
from basic_app import views

app_name = 'basic_app' # To allow using {% url 'basic_app:<url_name>' %} in the templates
urlpatterns = [
    path('', views.SchoolListView.as_view(), name='list'), # ListView from CBV
    path('<int:pk>/', views.SchoolDetailView.as_view(), name='detail'), # 'pk' stands for Primary Key
    # 'int:' in '<int:pk>' indicates that the primary key is of type Integer. This path matches any route that
    # corresponds to a 'localhost:8000/basic_app/<school_primary_key_number>/'.
    # This Primary Key number is sent as a URL Keyword Argument to the 'views.SchoolUpdateView' view under the
    # variable name 'pk'
    path('create/', views.SchoolCreateView.as_view(), name='create'),
    path('update/<int:pk>', views.SchoolUpdateView.as_view(), name='update'), # 'pk' stands for Primary Key
    # 'int:' in '<int:pk>' indicates that the primary key is of type Integer. This path matches any route that
    # corresponds to a 'localhost:8000/basic_app/update/<school_primary_key_number>/'.
    # This Primary Key number is sent as a URL Keyword Argument to the 'views.SchoolUpdateView' view under the
    # variable name 'pk'
    path('delete/<int:pk>', views.SchoolDeleteView.as_view(), name='delete'), # 'pk' stands for Primary Key
    # 'int:' in '<int:pk>' indicates that the primary key is of type Integer. This path matches any route that
    # corresponds to a 'localhost:8000/basic_app/delete/<school_primary_key_number>/'.
    # This Primary Key number is sent as a URL Keyword Argument to the 'views.SchoolDeleteView' view under the
    # variable name 'pk'
]