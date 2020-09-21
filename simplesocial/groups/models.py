from django.db import models
from django.utils.text import slugify
import misaka 
from django.urls import reverse
from django.contrib.auth import get_user_model

User=get_user_model() #we get current user from here, who is playing around with the website right now
from django import template
register = template.Library() #this is how we can use custom template tags in the future, later on we will have, "in group members check template tag" while dealing with group html files

class Group(models.Model):
    name=models.CharField(max_length=255,unique=True) #name of the group, here "unique=true" means groups will have unique names
    slug=models.SlugField(allow_unicode=True,unique=True)#group names should not overlap after slugify
    description=models.TextField(blank=True,default='')#description of the group
    description_html=models.TextField(editable=False,default='',blank=True)
    members=models.ManyToManyField(User,through='GroupMember')

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name) #whatever the group name is(having spaces while filling out the form), it essentially just replace and lowercase things 
        self.description_html=misaka.html(self.description)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})
    
    class Meta:
        ordering=['name']

class GroupMember(models.Model):
    group = models.ForeignKey(Group,related_name='memberships',on_delete=models.CASCADE,) #groupmember is related to the member class through this foreign key which we called memberships, which makes sense because a group member will have a membership to the group
    user=models.ForeignKey(User,related_name='user_groups',on_delete=models.CASCADE,) #we have user who will belong to some groups or who will be the member of some groups, we want to link this groupmember class to both the user and the groups that this user could belong to

    def __str__(self):
        return self.user.username
    
    class Meta:
        unique_together=('group','user')

# Create your models here.
