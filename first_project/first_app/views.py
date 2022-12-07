from django.shortcuts import render
from django.http import HttpResponse
from first_app.models import Topic,Webpage,AccessRecord

# Create your views here.

# Django uses request and response objects to pass state through the system.
# When a page is requested, Django creates an HttpRequest object that contains metadata about the request. 
# Then Django loads the appropriate view, passing the HttpRequest as the first argument to the view function. 
# Each view is responsible for returning an HttpResponse object.

# REFER: https://docs.djangoproject.com/en/4.1/topics/http/views/
# REFER: https://docs.djangoproject.com/en/4.1/ref/request-response/


def index(request):
    webpages_list = AccessRecord.objects.order_by('date') # Order the query results by the 'date' field/column
    date_dict = {'access_records': webpages_list}
    my_dict = {'insert_me': 'Now I am coming from first_app/index.html'}
    # return render(request, 'first_app/index.html', context=my_dict)
    return render(request, 'first_app/index2.html', context=date_dict)



# Models-Templates-Views (MTV) Paradigm
# SERVING DYNAMIC CONTENT TO THE USER BASED OFF THE CONNECTION OF MODELS, VIEWS AND TEMPLATES
# Import any Models to use in this 'views.py' file
# Use the view to query the Model for any data that we will need for constructing the Web content
# Pass results from the Model to the appropriate Template. Make sure the Template is ready to accept and display
# data from the Model.
# Finally, Map a URL to the view.