from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from groups.models import Group,GroupMember
from . import models
from django.shortcuts import get_object_or_404
class CreateGroup(LoginRequiredMixin,generic.CreateView): #if someone is logged into the group and wants to create a group, this will be the view for that
    fields=('name','description') #this user can edit only name and description of the group, which are directly connected to the Group class in models.py file
    model=Group #connect it to group model
    
class SingleGroup(generic.DetailView):#details of the group,like the posts inside that group
    model= Group

class ListGroups(generic.ListView): #when someone goes to listgroups page, the user should see list of all groups
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    def get(self,request,*args,**kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,'warning already a member!!')
        else:
            messages.success(self.request,'You are now a member!!')
        return super().get(request,*args,**kwargs)


class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):

        try:
            membership=models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,'Sorry you are not in this group!!')
        else:
            membership.delete()
            messages.success(self.request,'you have left the group!!')
        return super().get(request,*args,**kwargs)


 
