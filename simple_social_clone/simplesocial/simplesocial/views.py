# This views.py is for the 'simplesocial' app
from django.views.generic import TemplateView

# Create the login redirect view using the generic class-based 'TemplateView' that comes built-in with Django
class TestPage(TemplateView):
    template_name = 'test.html' # name of html file to be used as template (must be relative path from 
    # TEMPLATE_DIR or other directory set up in DIRS under TEMPLATES)

# Create the logout redirect view using the generic class-based 'TemplateView' that comes built-in with Django
class ThanksPage(TemplateView):
    template_name = 'thanks.html' # name of html file to be used as template (must be relative path from 
    # TEMPLATE_DIR or other directory set up in DIRS under TEMPLATES)

# Create a basic homepage view using the generic class-based view 'TemplateView' that comes built-in with Django
class HomePage(TemplateView):
    template_name = 'index.html' # name of html file to be used as template (must be relative path from 
    # TEMPLATE_DIR or other directory set up in DIRS under TEMPLATES)
    