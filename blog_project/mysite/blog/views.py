from django.shortcuts import render,get_object_or_404,redirect
# REFER: https://docs.djangoproject.com/en/4.1/topics/http/shortcuts/#get-object-or-404
from django.utils import timezone
from django.urls import reverse_lazy
from django.utils import timezone # For time and date utilities
from blog.forms import PostForm,CommentForm # import forms of the App
from blog.models import Post,Comment # Import models of the app
from blog.forms import PostForm,CommentForm # import forms of the app
from django.contrib.auth.decorators import login_required # For making login mandatory in function-based views
from django.contrib.auth.mixins import LoginRequiredMixin # Mixin similar to '@login_required' decorator to restrict view to logged-in users
from django.views.generic import (TemplateView,ListView,DetailView,CreateView, UpdateView, DeleteView) # Import genetic class-based views

# Create your views here.
# CLASS BASED VIEWS
class AboutView(TemplateView):
    template_name = 'about.html' # Connect the template HTML to the view

class PostListView(ListView):
    model = Post
    # A Manager is the interface through which database query operations are provided to Django models. 
    # At least one Manager exists for every model in a Django application.
    # You can override a Manager’s base QuerySet by overriding the Manager.get_queryset() method. 'get_queryset()' 
    # should return a QuerySet with the properties you require.
    # REFER: https://docs.djangoproject.com/en/4.1/topics/db/managers/
    def get_queryset(self): # Performs a SQL-like query on the Model - grab all the objects from the 'Post' model,
        # Filter by the 'published_date' attribute and keep only the objects with less than current Date and Time
        # (using the '__lte' field lookup condition) and order them by DESCENDING ORDER (LATEST DATE FIRST) (indicated
        # by the '-' sign that 'order_by()' should order the records by descending order of 'published_date' field)
        # REFER: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#field-lookups
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post # Connect the model


# REFER: https://docs.djangoproject.com/en/4.1/topics/class-based-views/mixins/
# REFER: https://docs.djangoproject.com/en/4.1/topics/auth/default/#limiting-access-to-logged-in-users
class CreatePostView(LoginRequiredMixin, CreateView):
    # mixins are just like decorators (such as @login_required for function-based views) 
    # Here, we inherit the 'LoginRequiredMixin' mixin class to make this view available only to logged-in Users.
    login_url = '/login/' # attribute specific to the 'LoginRequiredMixin' to redirect unauthorized users to a log-in page
    redirect_field_name = 'blog/post_details.html' # Redirection of User after they Log-in to Post instance detail page
    model = Post # Connect the model
    form_class = PostForm # The form to use in the CreateView
    model = Post


# REFER: https://docs.djangoproject.com/en/4.1/topics/class-based-views/mixins/
# REFER: https://docs.djangoproject.com/en/4.1/topics/auth/default/#limiting-access-to-logged-in-users
class PostUpdateView(LoginRequiredMixin, UpdateView):
    # mixins are just like decorators (such as @login_required for function-based views) 
    # Here, we inherit the 'LoginRequiredMixin' mixin class to make this view available only to logged-in Users.
    login_url = '/login/' # attribute specific to the 'LoginRequiredMixin' to redirect unauthorized users to a log-in page
    redirect_field_name = 'blog/post_details.html' # Redirection of User after they Log-in to Post instance detail page
    model = Post # Connect the model
    form_class = PostForm # The form to use in the CreateView
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    # REFER: https://docs.djangoproject.com/en/4.1/ref/urlresolvers/
    # Use 'reverse_lazy()' to redirect the User upon successful deletion of a Post instance to a page
    # 'reverse_lazy()' is a lazy URLresolver that evaluates only upon success of an event.
    success_url = reverse_lazy('post_list') # Redirect user upon successful deletion of a Post instance to the
    # URL named 'post_list'


# View showing list of unapproved/unpublished Post instances (Draft Posts)
class DraftListView(LoginRequiredMixin, ListView):
    # mixins are just like decorators (such as @login_required for function-based views) 
    # Here, we inherit the 'LoginRequiredMixin' mixin class to make this view available only to logged-in Users.
    login_url = '/login/' # attribute specific to the 'LoginRequiredMixin' to redirect unauthorized users to a log-in page
    redirect_field_name = 'blog/post_list.html' # Redirection of User after they Log-in to Post instance detail page
    model = Post
    # A Manager is the interface through which database query operations are provided to Django models. 
    # At least one Manager exists for every model in a Django application.
    # You can override a Manager’s base QuerySet by overriding the Manager.get_queryset() method. 'get_queryset()' 
    # should return a QuerySet with the properties you require.
    # REFER: https://docs.djangoproject.com/en/4.1/topics/db/managers/
    def get_queryset(self):
        # get the un-published post objects, order by the Date of creation of the 'Post' model instance
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


####################################################################################
# Function-based Views for handling Comments
####################################################################################

# Method to add a Comment to a Post
@login_required
def add_comment_to_post(request, pk):
    # 'get_object_or_404()' Calls get() on a given model manager, but it raises Http404 instead of the model’s DoesNotExist exception.
    # We supply the primary key to the get() call here to get a unique record out using SQL-like field lookup.
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#field-lookups
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#django.db.models.query.QuerySet.get
    post = get_object_or_404(Post, pk=pk) 
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid(): # If all fields are valid in the Form
            # Every ModelForm also has a 'save()' method. This method creates and saves a database object from the data 
            # bound to the form. A subclass of ModelForm can accept an existing model instance as the keyword argument 
            # instance; if this is supplied, 'save()' will update that instance. If it’s not supplied, 'save()' will create 
            # a new instance of the specified model. 
            # Note that if the form hasn’t been validated, calling save() will do so by checking form.errors. 
            # A ValueError will be raised if the data in the form doesn’t validate – i.e., if form.errors evaluates to True.
            # If an optional field doesn’t appear in the form’s data, the resulting model instance uses the model 
            # field default, if there is one, for that field.
            # This save() method accepts an optional commit keyword argument, which accepts either True or False. 
            # If you call save() with commit=False, then it will return an object that hasn’t yet been saved to the 
            # database. In this case, it’s up to you to call save() on the resulting model instance. This is useful if 
            # you want to do custom processing on the object before saving it, or if you want to use one of the specialized 
            # model saving options. commit is True by default.
            # REFER: https://docs.djangoproject.com/en/4.1/topics/forms/modelforms/#the-save-method
            comment = form.save(commit=False)
            comment.post = post # The CommentForm does not have the 'post' field. Hence, we need to connect it to the Post instance
            comment.save()
            return redirect('post_detail', pk=post.pk) # Redirects user to the resolved URL upon creating the Model instance from the form data.
    else:
        form = CommentForm()
        return render(request, 'blog/comment_form.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk) # Get the Comment instance using primary key
    comment.approve() # Call the approve() method implemented in the Model to approve the comment
    return redirect('post_detail', pk=comment.post.pk) # Redirect the user to the Post detail page after approving a comment
    # The redirection is done using the primary key of the post taken from the comment instance (The post that the comment is linked to.)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk) # Get the Comment instance using primary key
    post_pk = comment.post.pk # Get the primary key of the post that the comment is linked to
    comment.delete() # Delete the comment instance
    return redirect('post_detail', pk=post_pk) # Redirect the user to the Post instance detail page (the post linked to the deleted comment)


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk) # Get the post instance using its primary key
    post.publish() # Publish the post instance using the publish() method described in the 'Post' model
    return redirect('post_detail', pk=post.pk) # Redirect after successful publishing of post to the detail page of the newly created Post
