# Declating custom Template Filter Functions
# REFER: https://docs.djangoproject.com/en/4.1/howto/custom-template-tags/#writing-custom-template-filters

from django import template

# Import registering method from django to register custom functions as Template Filters
register = template.Library()

# Custom function (using decorators to register it during declaration itself as Template FIlter)
@register.filter(name='cutit')
def cut(value, arg):
    """
    This cuts out all values of "arg" from the string!
    """
    return value.replace(arg, '')

# Registering the custom function as a Template Filter after declaration
# register.filter('cutit', cut)