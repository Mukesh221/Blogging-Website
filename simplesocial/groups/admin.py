from django.contrib import admin
from . import models


#this allows us to utilize the admin interface in our django website with the ability to edit models on the same page as the parent model
class GroupMemberInline(admin.TabularInline):
    model=models.GroupMember

admin.site.register(models.Group)


# Register your models here.
