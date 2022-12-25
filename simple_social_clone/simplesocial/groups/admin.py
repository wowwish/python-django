from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Group)
# Since our 'GroupMember' model basically inherits from our 'Group' model, we can use the 'TabularInline' built-in
# class from Django to allow editing the Parent 'Group' model fields as well in the Admin-privileges site 
# (/admin/) from any of the 'GroupMember' class instance Detail Page.
class GroupMemberInline(admin.TabularInline):
    model = models.GroupMembers # The 'GroupMember' model becomes and does not require any registering when
    # declated as an child class of 'TabularInline' class of Django.