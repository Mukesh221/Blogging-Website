from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin #by this we knew someone is logged in or not so that he can create a post and form a group
from django.urls import reverse_lazy #if someone deletes a post

from django.http import Http404 #by this, 404 page could be returned
from django.views import generic #for generic class based views
from django.contrib import messages
from braces.views import SelectRelatedMixin

from . import models
from . import forms
from django.contrib.auth import get_user_model
User = get_user_model()

class PostList(SelectRelatedMixin,generic.ListView): #for list of posts belonging to a group
    model=models.Post 
    select_related=('user','group') # "template_name" is a mixin that allows us to provide a tupple of related models, basically the foreign keys for this post

class UserPosts(generic.ListView): #for list of posts belonging to a user
    model=models.Post
    template_name='posts/user_post_list.html' 

    def get_queryset(self): #"get_queryset" is a method, when this class(UserPosts) is called, this is what it will actually do
        try:
            #line 26 is ORM(object relational model) of django.      
            self.post_user=User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
            #it will try to set the user, that belongs to a particular posts, equal to the user, that user objects.... the username is exactly the equal to the username of whatever user if logged in
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_contex_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['post_user']=self.post_user
        return context

class PostDetail(SelectRelatedMixin,generic.DetailView):
    model=models.Post
    select_related=('user','group')

    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    fields=('message','group')
    model=models.Post

    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.objects.user=self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DetailView):
    model=models.Post
    select_related=('user','group')
    success_url=reverse_lazy('posts:all') #after deleting, it will take the user to all posts

    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)

# Create your views here.
