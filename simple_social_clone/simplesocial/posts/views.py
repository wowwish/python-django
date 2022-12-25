from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin # To ensure only logged in users can access certain views
from django.urls import reverse_lazy # To resolve names and url template tags to URL strings using lazy evaluation
from django.views import generic # For built-in generic class-based-views of Django
from django.http import Http404 # To return HTTP 404 responses errors
from django.contrib import messages # For the messaging framework of Django

# NOTE: USER 'pip install django-braces' TO INSTALL THE LIBRARY MIXIN CLASSES USED BELOW
# REFER: https://django-braces.readthedocs.io/en/latest/other.html#selectrelatedmixin
# REFER: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#select-related
from braces.views import SelectRelatedMixin 
from . import models
from groups.models import Group # Get the 'Group' model class declared in the 'groups' app
from . import forms
from django.contrib.auth import get_user_model # To get the current active 'User' model in this app (which is 
# usually the built-in 'User' model from 'django.contrib.auth')
User = get_user_model()

# Create your views here.
class PostList(generic.ListView, SelectRelatedMixin):
    # KEEP IN MIND THAT THE 'request' DATA FROM A TEMPLATE FORM IS ACCESSIBLE INSIDE THIS CLASS USING 'self.request'
    model = models.Post # connect the view to the 'Post' model
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#select-related
    selected_related = ('user', 'group') # tuple of fields of the 'Post' model that are related to other models
    # (the ForeignKeys of the 'Posts' model instance)
    posts = models.Post.objects.all() # get all the post instances from the Posts model
    def get_context_data(self, **kwargs): # Overriding the method that returns the context data to the template
        context =  super().get_context_data(**kwargs)
        # All group memberships associated with the user
        context['user_groups'] = Group.objects.filter(members__in = [self.request.user])
        # All 'Group' model instances
        context['all_groups'] = Group.objects.all()
        return context

class UserPosts(generic.ListView):
    # KEEP IN MIND THAT THE 'request' DATA FROM A TEMPLATE FORM IS ACCESSIBLE INSIDE THIS CLASS USING 'self.request'
    model = models.Post # connect the view to the 'Post' model
    template_name = 'posts/user_post_list.html' # Setup the template HTML for the list view when the default template naming convention is not used
    # Overriding Django's queryset manager method 'get_queryset' to return a query set of all objects of the 'Post' model with the properties that we require
    # REFER: https://docs.djangoproject.com/en/4.1/topics/db/queries/
    def get_queryset(self): # REFER: https://docs.djangoproject.com/en/4.1/topics/db/managers/#modifying-a-manager-s-initial-queryset
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
            # The 'User' model instances that belong to this particular 'Post' model instance are queried using
            # 'prefetch_related()' method of the users queryset (due to the many-to-many relationship of users with posts),
            # and the username of the users of this post instance are fetched using case-insensitive exact matching with 
            # the provided 'username' keyword argument.
            # REFER: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#prefetch-related
            # REFER: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#field-lookups
            # REFER: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#iexact
        except: # If the user with the specific username does not exist
            raise Http404
        else:
            return self.post_user.posts.all() # return all 'Post' model instance of the given username for the view.
            # Remember: This else block is run only when the try block succeeds.
    
    # REFER: https://docs.djangoproject.com/en/4.1/topics/class-based-views/generic-display/#adding-extra-context
    # REFER: https://docs.djangoproject.com/en/4.1/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_data
    # We override the 'get_context_data()' method here to provide our own additional content to the context 
    # dictionary like 'post_user'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # get the context dictionary from the parent ListView class
        context['post_user'] = self.post_user # adding additional content to the context dictionary of the view
        return context


class PostDetail(SelectRelatedMixin, generic.DeleteView):
    # KEEP IN MIND THAT THE 'request' DATA FROM A TEMPLATE FORM IS ACCESSIBLE INSIDE THIS CLASS USING 'self.request'
    model = models.Post
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#select-related
    select_related = ('user', 'group') # tuple of fields of the 'Post' model that are related to other models
    # (the ForeignKeys of the 'Posts' model instance)

    # Overriding Django's queryset manager method 'get_queryset' to return a query set of all objects of the 'Post' model with the properties that we require
    # REFER: https://docs.djangoproject.com/en/4.1/topics/db/queries/
    def get_queryset(self): # REFER: https://docs.djangoproject.com/en/4.1/topics/db/managers/#modifying-a-manager-s-initial-queryset
        queryset = super().get_queryset()
        # The queryset from the parent View class is queried by filtering for case-insensitive exact matches
        # of the instances of 'Posts' model in the queryset with the 'username' keyword argument provided to the
        # view. Here, 'user__username' is synonymous to 'user.username'
        # REFER: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#prefetch-related
        # REFER: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#field-lookups
        # REFER: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#iexact
        return queryset.filter(user__username__iexact = self.kwargs.get('username'))


# Only logged-in users can create posts
class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # KEEP IN MIND THAT THE 'request' DATA FROM A TEMPLATE FORM IS ACCESSIBLE INSIDE THIS CLASS USING 'self.request'
    fields = ('message', 'group') # editable fields of the post creation form
    model = models.Post
    # REFER: https://docs.djangoproject.com/en/4.1/topics/class-based-views/generic-editing/#form-handling-with-class-based-views
    # REFER: https://docs.djangoproject.com/en/4.1/ref/class-based-views/mixins-editing/#django.views.generic.edit.ModelFormMixin.form_valid
    def form_valid(self, form): # Overriding Form data validation Method
        self.object = form.save(commit=False) # Get the form data without saving the data as an instance of the 'Post' model
        self.object.user = self.request.user # Add the user property for the 'Post' model instance form data
        self.object.save() # Create a new 'Post' model instance with the modified form content
        return super().form_valid(form) # check if the form data is valid using the parent CreateView class's 'form_valid()' method


class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    # KEEP IN MIND THAT THE 'request' DATA FROM A TEMPLATE FORM IS ACCESSIBLE INSIDE THIS CLASS USING 'self.request'
    model = models.Post
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#select-related
    select_related = ('user', 'group') # tuple of fields of the 'Post' model that are related to other models
    # (the ForeignKeys of the 'Posts' model instance)
    success_url = reverse_lazy('posts:all') # (only) Upon successful deletion of a Post instance, return user to the all posts ListView
    
    # Overriding Django's queryset manager method 'get_queryset' to return a query set of all objects of the 'Post' model with the properties that we require
    # REFER: https://docs.djangoproject.com/en/4.1/topics/db/queries/
    def get_queryset(self): # REFER: https://docs.djangoproject.com/en/4.1/topics/db/managers/#modifying-a-manager-s-initial-queryset
        queryset = super().get_queryset() # invoking the parent DeleteView class's 'get_queryset()' method to obtain the model instances for DeleteView
        return queryset.filter(user_id = self.request.user.id) # Return query instances that have the same 'user_id' 
        # property as seen in the DeleteView request data
    
    # REFER: https://docs.djangoproject.com/en/4.1/topics/db/models/#overriding-predefined-model-methods
    # REFER: https://docs.djangoproject.com/en/4.1/topics/db/queries/#deleting-objects
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/instances/#django.db.models.Model.delete
    def delete(self, *args, **kwargs): # Method overriding to delete a Post instance and display success message and redirect the user
        # REFER: https://docs.djangoproject.com/en/4.1/ref/contrib/messages/#module-django.contrib.messages
        # REFER: https://docs.djangoproject.com/en/4.1/ref/contrib/messages/#module-django.contrib.messages
        # Show a success message when a post is deleted - this message is passed as a string in the context and
        # must be handled in the view with appropriate UI.
        messages.succes(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs) # Calling the delete() method of 'DeleteView' class