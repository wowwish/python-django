from django import forms
from blog.models import Post,Comment # importing models

# REFER: https://docs.djangoproject.com/en/4.1/ref/forms/widgets/

class PostForm(forms.ModelForm): # A ModelForm for Model instance creation via HTML Forms
    class Meta(): # Class that provides information on the model connected to the form
        model = Post
        fields = ('author', 'title', 'text') # Allowed editable fields of the Form/Model
        # Connect 'widgets' to the Form fields to format the Form Fields
        # A widget is Django's representation of an HTML input element. The widget handles 
        # the rendering of the HTML, and the extraction of data from a GET/POST dictionary that corresponds to the widget. 
        widgets = {
            # You can also set HTML element attributes such as CSS 'classes' for the HTML tag of the form fields
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editor ck-editor-textarea postcontent', 'id': 'editor'}) # Add the class name 'editor' to the text area
        }

class CommentForm(forms.ModelForm):
    class Meta(): # Class that connects a model to the form
        model = Comment
        fields = ('author', 'text') # Editable fields of the Model/Form
        # Connect 'widgets' to the Form fields to format them
        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editor ck-editor-textarea', 'id': 'editor'})
        }

