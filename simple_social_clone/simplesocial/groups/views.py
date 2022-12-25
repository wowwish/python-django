from django.shortcuts import render
# Import built-in user authentication classes
from django.contrib.auth.mixins import (LoginRequiredMixin, 
                                                PermissionRequiredMixin)
from django.urls import reverse # used for resolving URLs
from django.views import generic # contains all the built-in generic class-based views of Django 
# like ListView, CreateView, DeleteView, DetailView etc
from groups.models import Group, GroupMembers
from django.shortcuts import get_object_or_404
from django.contrib import messages # for sending message through templates to the user
from django.db import IntegrityError # Database transaction error class

# Create your views here.
class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description') # included/editable fields of the CreateView form
    model = Group # The model for which an instance will be created with the given form data

class SingleGroup(generic.DetailView): # View showing details of a single 'Group' model instance
    model = Group

class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    # KEEP IN MIND THAT THE 'request' DATA FROM A TEMPLATE FORM IS ACCESSIBLE INSIDE THIS CLASS USING 'self.request'
    # When a user opts to join a group, we should process the request in backend and redirect the user upon successful joining to a page
    # Hence, we use the RedirectView class-based generic view here.
    # REFER: https://docs.djangoproject.com/en/4.1/ref/class-based-views/base/#redirectview
    def get_redirect_url(self, *args, **kwargs): # Set the Redirect view URL to redirect the user to once they land on this view
        # Use URL resolver 'reverse()' to build the redirection URL and redirect user to a specific group Detail view
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#methods-that-do-not-return-querysets
    # Overriding the 'get()' method which returns an object matching the given lookup parameters from a Model, 
    # Manager or QuerySet. The lookup parameters should follow certain rules: 
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#methods-that-do-not-return-querysets
    def get(self, request, *args, **kwargs):
        # REFER: https://docs.djangoproject.com/en/4.1/topics/http/shortcuts/#get-object-or-404
        # 'get_object_or_404()' is a shortcut function that calls the 'get()' method of the given model manager
        # and raises a Http404 error when no object/model instance is found for the given lookup parameters (**kwargs).
        group = get_object_or_404(Group, slug=self.kwargs.get('slug')) 
        # get the slug of the group to which the user wants to join, from the keyword arguments 
        try:
            # Try creating a GroupMembers instance to keep a record of a user's membership to a specific group
            GroupMembers.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            messages.warning(self.request,'Warning already a member!')
        else:
            messages.success(self.request, 'You are now a member!')
        return super().get(request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    # KEEP IN MIND THAT THE 'request' DATA FROM A TEMPLATE FORM IS ACCESSIBLE INSIDE THIS CLASS USING 'self.request'
    # When a user opts to leave a group, we should process the request in backend and redirect the user upon successfully leaving a group, to a page
    # Hence, we use the RedirectView class-based generic view here.
    # REFER: https://docs.djangoproject.com/en/4.1/ref/class-based-views/base/#redirectview
    def get_redirect_url(self, *args, **kwargs): # Set the Redirect view URL to redirect the user to, once they land on this view
        # Use URL resolver 'reverse()' to build the redirection URL and redirect user to a specific group Detail view
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})
    def get(self, request, *args, **kwargs):
        try:
            # Filter the 'GroupMembers' model instances for the specific user and the specific group that they want to leave
            # using 'group.slug' for the group of the 'GroupMembers' objects/instance (group__slug) equal to the slug of the 
            # request
            membership = GroupMembers.objects.filter(
                user = self.request.user,
                group__slug = self.kwargs.get('slug')
            ).get()
        except GroupMembers.DoesNotExist: # error of not being able to get a filtered instance of 'GroupMembers'
            # for this particular user and group
            messages.warning(self.request, 'Sorry you are not in this group!')
        else: 
            # If the try block executed without errors
            membership.delete() # Delete the 'GroupMembers' model instance connecting the particular user to the particular group
            messages.success(self.request, 'You have left the group!')
        return super().get(request, *args, **kwargs) # For running the standard stuff to process a get request 
        # for a Django RedirectView