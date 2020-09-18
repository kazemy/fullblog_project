from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    #using existing blog/home.html template instead of django convetion for this one
    template_name = 'blog/home.html'
    #adding an extra attribute to identify post object instead of django convention for this one
    context_object_name = 'posts'
    #using class based view method on a date_posted field to change display ordering of posts objects
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    #override the form valid mehtod to add author
    def form_valid(self, form):
        #get the current form instance author and set it to
        #the current logged in user
        form.instance.author = self.request.user
        #now can validate the form using the parent class
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']

    #override the form valid mehtod to add author
    def form_valid(self, form):
        #get the current form instance author and set it to
        #the current logged in user
        form.instance.author = self.request.user
        #now can validate the form using the parent class
        return super().form_valid(form)
    
    #method to use by UserPassesTestMixin to make sure only author of posts
    #can update their own posts
    def test_func(self):
        # get current post object
        post = self.get_object()
        #check if the current logged in user is the post object author atribute
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post

    #add attribute success_url to forward to blog home after suceessfull deletion
    success_url = '/'

    #method to use by UserPassesTestMixin to make sure only author of posts
    #can update their own posts
    def test_func(self):
        # get current post object
        post = self.get_object()
        #check if the current logged in user is the post object author atribute
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
