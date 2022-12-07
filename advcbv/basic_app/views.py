from django.shortcuts import render
# Imports for Generic Class-based views
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView 
from django.http import HttpResponse # For returning content over HTTP
from basic_app import models # Import models of the App
from django.urls import reverse_lazy # A variant of the 'reverse' function that converts page views to URL strings.
# This variant of the reverse() function is evaluated only when it is actually called. It is used here to make sure
# that the user is sent to 'success_url' only after the Model instance is successfully deleted and not before it.

# Class-based views (CBV) are implemented as Classes that provided many additional functionality and flexibility to
# function-based views.
# The Class-based views will be invoked in the 'urls.py' file using the '.as_view()' method of the CBV
# Create your views here.

# def index(request):
#     return render(request, 'basic_app/index.html')

# A basic Class-based View
# class CBView():
#     def get(self, request):
#         return HttpResponse('CLASS BASED VIEWS ARE COOL!')

# Another more easier way to create Class-based Views
# BoilerPlate Code
class IndexView(TemplateView):
    # Set the template HTML to be rendered
    template_name = 'index.html'
    # Method to obtain the context dictionary and read it using the TemplateView.get_context_data() method
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inject_me'] = 'BASIC INJECTION!' # Set the keys and values of the Context Dictionary and return it
        return context

# Often, when we have Models, we want to show all the records of the Model or a single record from the Model
# Database. Django has some very generic view classes that you can inherit to very quickly display information
# from your model using Class-based Views (ListView and DetailView).

# Also, it is very common to have the 'templates' directory underneath the App (basic_app) directory
#  instead of having it at the Project dir 


# REFER: https://docs.djangoproject.com/en/4.1/topics/class-based-views/generic-display/
# Generic Model Views - ListView
class SchoolListView(ListView):
    # Keep in mind, the ListView automatically creates a 'school_list' key-value pair in the Context Dictionary
    # It sets the key name as '<model_name(lowercase of 'School' in this case)>_list' and the value is all the
    # records of the Model. You can loop through these records and access each record's field using the '.' operator
    # For example: sc.name for sc in school_list
    # You can change this default context object name by using the attribute 'context_object_name' 
    context_object_name = 'schools' # This sets the default 'school_list' key to 'schools' instead as specified for the context dictionary
    model = models.School
    # This ListView class will be default look for a template named '<app_name>/<model_name_in_lowercase>_detail.html'
    # since no 'template_name' attribute is specified here.

# Generic Model Views - DetailView
# Similar to ListViews, DetailViews also create and pass a context dictionary object to the rendered template
# with the lowercase name of the Model (Default). The value for this key in the context dictionary created by
# the DetalView will be all fields of a single record from the Model (which record is chosen can be customized
# by overriding the get_object(self) method implementation. By default, it looks for a 'pk_url_kwarg' argument in
# the arguments to the view; if this argument is found, this method performs a primary-key based lookup using that value)
# The name of the URLConf keyword argument that contains the primary key. By default, pk_url_kwarg is 'pk'
# We can override this naming in the same way as in ListView using the 'context_object_name' attribute
class SchoolDetailView(DetailView):
    context_object_name = 'school_detail'
    model = models.School
    template_name = 'basic_app/school_detail.html' # This is also the default template name that will be searched
    # for when no 'template_name' is specified in this DetailView. (<app_name>/<model_name_in_lowercase>_detail.html)


# CRUD (Create, Read, Update, Delete) OPERATIONS WITH MODELS USING GENERIC CLASS-BASED VIEWS


# Generic Model View - CreateViews
# CreateViews are used to create new records of a Model ('School' in this case.)
# We have to specify which fields are prohibited from creation and which fileds are allowed in creation of a record
# of our Model. Without this specified, the Model record creation view will error out 
# (Using ModelFormMixin (base class of SchoolCreateView) without the 'fields' attribute is prohibited.)
# If no 'template_name' attribute is provided, this view will look for a template like 'basic_app/school_form.html'
class SchoolCreateView(CreateView):
    # The CreateView by default 
    fields = ('name', 'principal', 'location') # allow all the fields for creation of a record
    model = models.School
    # If you don't define a get_absolute_url(self) method in your Model definition (definition of School model),
    # You will encounter the following error when submitting the instance creation form for the Model:
    # No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model.

# Generic Model View - UpdateView
class SchoolUpdateView(UpdateView):
    fields = ('name', 'principal') # What fields of an instance of the 'School' model do you allow the user to update ?
    # We donot allow the user to update the 'location' field of the 'School' model instance in this case.
    model = models.School


# Generic Model View - DeleteView
class SchoolDeleteView(DeleteView):
    model = models.School
    success_url = reverse_lazy('basic_app:list') # The URL to redirect the user to upon successful deletion
    # of a Model instance (an instance/record of School)
    # The default HTML template file expected by DeleteView is 'basic_app/school_confirm_delete.html'
    # (<app_name>/<model_name_in_lowercase>_confirm_delete.html)

